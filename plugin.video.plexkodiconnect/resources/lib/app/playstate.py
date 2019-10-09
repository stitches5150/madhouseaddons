#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals


class PlayState(object):
    # "empty" dict for the PLAYER_STATES above. Use copy.deepcopy to duplicate!
    template = {
        'type': None,
        'time': {
            'hours': 0,
            'minutes': 0,
            'seconds': 0,
            'milliseconds': 0},
        'totaltime': {
            'hours': 0,
            'minutes': 0,
            'seconds': 0,
            'milliseconds': 0},
        'speed': 0,
        'shuffled': False,
        'repeat': 'off',
        'position': None,
        'playlistid': None,
        'currentvideostream': -1,
        'currentaudiostream': -1,
        'subtitleenabled': False,
        'currentsubtitle': -1,
        'file': None,
        'kodi_id': None,
        'kodi_type': None,
        'plex_id': None,
        'plex_type': None,
        'container_key': None,
        'volume': 100,
        'muted': False,
        'playmethod': None,
        'playcount': None
    }

    def __init__(self):
        # Kodi player states - here, initial values are set
        self.player_states = {
            0: {},
            1: {},
            2: {}
        }
        # The LAST playstate once playback is finished
        self.old_player_states = {
            0: {},
            1: {},
            2: {}
        }
        self.played_info = {}

        # Set by SpecialMonitor - did user choose to resume playback or start from the
        # beginning?
        # Set to None if resume dialog has not been shown
        # True if dialog has been shown and user selected to resume
        # False if dialog has been shown and user chose to start from beginning
        self.resume_playback = None
        # Was the playback initiated by the user using the Kodi context menu?
        self.context_menu_play = False
        # Set by context menu - shall we force-transcode the next playing item?
        self.force_transcode = False
        # Which Kodi player is/has been active? (either int 1, 2 or 3)
        self.active_players = set()
