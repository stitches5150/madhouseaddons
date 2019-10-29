#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
plex_api interfaces with all Plex Media Server (and plex.tv) xml responses
"""
from __future__ import absolute_import, division, unicode_literals

from .base import Base
from .artwork import Artwork
from .file import File
from .media import Media
from .user import User
from .playback import Playback

from ..mchm_db import PlexDB


class API(Base, Artwork, File, Media, User, Playback):
    pass


def mass_api(xml):
    """
    Pass in an entire XML PMS response with e.g. several movies or episodes
    Will Look-up Kodi ids in the Plex.db for every element (thus speeding up
    this process for several PMS items!)
    """
    apis = [API(x) for x in xml]
    with PlexDB(lock=False) as mchmdb:
        for api in apis:
            api.check_db(mchmdb=mchmdb)
    return apis
