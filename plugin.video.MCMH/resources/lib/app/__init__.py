#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Used to save MHC's application state and share between modules. Be careful
if you invoke another MHC Python instance (!!) when e.g. MHC.movies is called
"""
from __future__ import absolute_import, division, unicode_literals
from .account import Account
from .application import App
from .connection import Connection
from .libsync import Sync
from .playstate import PlayState

ACCOUNT = None
APP = None
CONN = None
SYNC = None
PLAYSTATE = None


def init(entrypoint=False):
    """
    entrypoint=True initiates only the bare minimum - for other MHC python
    instances
    """
    global ACCOUNT, APP, CONN, SYNC, PLAYSTATE
    APP = App(entrypoint)
    CONN = Connection(entrypoint)
    ACCOUNT = Account(entrypoint)
    SYNC = Sync(entrypoint)
    if not entrypoint:
        PLAYSTATE = PlayState()
