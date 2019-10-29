#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals
from logging import getLogger
import Queue
from threading import Lock, RLock

import xbmc

from .. import utils

LOG = getLogger('PLEX.app')


class App(object):
    """
    This class is used to store variables across MHC modules
    """
    def __init__(self, entrypoint=False):
        self.fetch_pms_item_number = None
        self.force_reload_skin = None
        if entrypoint:
            self.load_entrypoint()
        else:
            self.load()
            # Quit MHC?
            self.stop_pkc = False
            # This will suspend the main thread also
            self.suspend = False
            # Update Kodi widgets
            self.update_widgets = False
            # Need to lock all methods and functions messing with Plex Companion subscribers
            self.lock_subscriber = RLock()
            # Need to lock everything messing with Kodi/MHC playqueues
            self.lock_playqueues = RLock()
            # Necessary to temporarily hold back librarysync/websocket listener when doing
            # a full sync
            self.lock_playlists = Lock()

            # Plex Companion Queue()
            self.companion_queue = Queue.Queue(maxsize=100)
            # Websocket_client queue to communicate with librarysync
            self.websocket_queue = Queue.Queue()
            # xbmc.Monitor() instance from kodimonitor.py
            self.monitor = None
            # xbmc.Player() instance
            self.player = None
            # All thread instances
            self.threads = []
            # Instance of FanartThread()
            self.fanart_thread = None
            # Instance of ImageCachingThread()
            self.caching_thread = None

    @property
    def is_playing(self):
        return self.player.isPlaying()

    @property
    def is_playing_video(self):
        return self.player.isPlayingVideo()

    def register_fanart_thread(self, thread):
        self.fanart_thread = thread
        self.threads.append(thread)

    def deregister_fanart_thread(self, thread):
        self.fanart_thread = None
        self.threads.remove(thread)

    def suspend_fanart_thread(self, block=True):
        try:
            self.fanart_thread.suspend(block=block)
        except AttributeError:
            pass

    def resume_fanart_thread(self):
        try:
            self.fanart_thread.resume()
        except AttributeError:
            pass

    def register_caching_thread(self, thread):
        self.caching_thread = thread
        self.threads.append(thread)

    def deregister_caching_thread(self, thread):
        self.caching_thread = None
        self.threads.remove(thread)

    def suspend_caching_thread(self, block=True):
        try:
            self.caching_thread.suspend(block=block)
        except AttributeError:
            pass

    def resume_caching_thread(self):
        try:
            self.caching_thread.resume()
        except AttributeError:
            pass

    def register_thread(self, thread):
        """
        Hit with thread [backgroundthread.Killablethread instance] to register
        any and all threads
        """
        self.threads.append(thread)

    def deregister_thread(self, thread):
        """
        Sync thread has done it's work and is e.g. about to die
        """
        self.threads.remove(thread)

    def suspend_threads(self, block=True):
        """
        Suspend all threads' activity with or without blocking.
        Returns True only if MHC shutdown requested
        """
        LOG.debug('Suspending threads: %s', self.threads)
        for thread in self.threads:
            thread.suspend()
        if block:
            while True:
                for thread in self.threads:
                    if not thread.suspend_reached:
                        LOG.debug('Waiting for thread to suspend: %s', thread)
                        # Send suspend signal again in case self.threads
                        # changed
                        thread.suspend()
                        if self.monitor.waitForAbort(0.1):
                            return True
                        break
                else:
                    break
        return xbmc.abortRequested

    def resume_threads(self, block=True):
        """
        Resume all thread activity with or without blocking.
        Returns True only if MHC shutdown requested
        """
        LOG.debug('Resuming threads: %s', self.threads)
        for thread in self.threads:
            thread.resume()
        if block:
            while True:
                for thread in self.threads:
                    if thread.suspend_reached:
                        LOG.debug('Waiting for thread to resume: %s', thread)
                        if self.monitor.waitForAbort(0.1):
                            return True
                        break
                else:
                    break
        return xbmc.abortRequested

    def stop_threads(self, block=True):
        """
        Stop all threads. Will block until all threads are stopped
        Will NOT quit if MHC should exit!
        """
        LOG.debug('Killing threads: %s', self.threads)
        for thread in self.threads:
            thread.abort()
        if block:
            while self.threads:
                LOG.debug('Waiting for threads to exit: %s', self.threads)
                if xbmc.sleep(100):
                    return True

    def load(self):
        # Number of items to fetch and display in widgets
        self.fetch_pms_item_number = int(utils.settings('fetch_pms_item_number'))
        # Hack to force Kodi widget for "in progress" to show up if it was empty
        # before
        self.force_reload_skin = utils.settings('forceReloadSkinOnPlaybackStop') == 'true'

    def load_entrypoint(self):
        self.fetch_pms_item_number = int(utils.settings('fetch_pms_item_number'))
