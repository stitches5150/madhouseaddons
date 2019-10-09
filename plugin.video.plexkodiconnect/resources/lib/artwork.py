#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals
from logging import getLogger
import requests

from .kodi_db import KodiVideoDB, KodiMusicDB, KodiTextureDB
from . import app, backgroundthread, utils

LOG = getLogger('PLEX.artwork')

# Disable annoying requests warnings
requests.packages.urllib3.disable_warnings()

# Potentially issues with limited number of threads Hence let Kodi wait till
# download is successful
TIMEOUT = (35.1, 35.1)
BATCH_SIZE = 500


def double_urlencode(text):
    return utils.quote_plus(utils.quote_plus(text))


def double_urldecode(text):
    return utils.unquote(utils.unquote(text))


class ImageCachingThread(backgroundthread.KillableThread):
    def __init__(self):
        super(ImageCachingThread, self).__init__()
        self.suspend_points = [(self, '_suspended')]
        if not utils.settings('imageSyncDuringPlayback') == 'true':
            self.suspend_points.append((app.APP, 'is_playing_video'))

    def isSuspended(self):
        return any(getattr(obj, txt) for obj, txt in self.suspend_points)

    @staticmethod
    def _url_generator(kind, kodi_type):
        """
        Main goal is to close DB connection between calls
        """
        offset = 0
        i = 0
        while True:
            batch = []
            with kind(texture_db=True) as kodidb:
                texture_db = KodiTextureDB(kodiconn=kodidb.kodiconn,
                                           artconn=kodidb.artconn,
                                           lock=False)
                for i, url in enumerate(kodidb.artwork_generator(kodi_type,
                                                                 BATCH_SIZE,
                                                                 offset)):
                    if texture_db.url_not_yet_cached(url):
                        batch.append(url)
                        if len(batch) == BATCH_SIZE:
                            break
            offset += i
            for url in batch:
                yield url
            if i + 1 < BATCH_SIZE:
                break

    def run(self):
        LOG.info("---===### Starting ImageCachingThread ###===---")
        app.APP.register_caching_thread(self)
        try:
            self._run()
        except Exception:
            utils.ERROR()
        finally:
            app.APP.deregister_caching_thread(self)
            LOG.info("---===### Stopped ImageCachingThread ###===---")

    def _run(self):
        kinds = [KodiVideoDB]
        if app.SYNC.enable_music:
            kinds.append(KodiMusicDB)
        for kind in kinds:
            for kodi_type in ('poster', 'fanart'):
                for url in self._url_generator(kind, kodi_type):
                    if self.wait_while_suspended():
                        return
                    cache_url(url)
        # Toggles Image caching completed to Yes
        utils.settings('plex_status_image_caching', value=utils.lang(107))


def cache_url(url):
    url = double_urlencode(url)
    sleeptime = 0
    while True:
        try:
            requests.head(
                url="http://%s:%s/image/image://%s"
                    % (app.CONN.webserver_host,
                       app.CONN.webserver_port,
                       url),
                auth=(app.CONN.webserver_username,
                      app.CONN.webserver_password),
                timeout=TIMEOUT)
        except requests.Timeout:
            # We don't need the result, only trigger Kodi to start the
            # download. All is well
            break
        except requests.ConnectionError:
            if app.APP.stop_pkc:
                # Kodi terminated
                break
            # Server thinks its a DOS attack, ('error 10053')
            # Wait before trying again
            if sleeptime > 5:
                LOG.error('Repeatedly got ConnectionError for url %s',
                          double_urldecode(url))
                break
            LOG.debug('Were trying too hard to download art, server '
                      'over-loaded. Sleep %s seconds before trying '
                      'again to download %s',
                      2**sleeptime, double_urldecode(url))
            app.APP.monitor.waitForAbort((2**sleeptime))
            sleeptime += 1
            continue
        except Exception as err:
            LOG.error('Unknown exception for url %s: %s'.
                      double_urldecode(url), err)
            import traceback
            LOG.error("Traceback:\n%s", traceback.format_exc())
            break
        # We did not even get a timeout
        break
