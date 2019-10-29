#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Synced playlists are stored in our mchm.db. Interact with it through this
module
"""
from __future__ import absolute_import, division, unicode_literals
from logging import getLogger

from .common import Playlist, PlaylistError
from ..mchm_db import PlexDB
from ..kodi_db import kodiid_from_filename
from .. import path_ops, utils, variables as v
###############################################################################
LOG = getLogger('PLEX.playlists.db')

###############################################################################


def plex_playlist_ids():
    """
    Returns a list of all Plex ids of the playlists already in our DB
    """
    with PlexDB() as mchmdb:
        return list(mchmdb.playlist_ids())


def kodi_playlist_paths():
    """
    Returns a list of all Kodi playlist paths of the playlists already synced
    """
    with PlexDB() as mchmdb:
        return list(mchmdb.kodi_playlist_paths())


def update_playlist(playlist, delete=False):
    """
    Assumes that all sync operations are over. Takes playlist [Playlist]
    and creates/updates the corresponding Plex playlists table entry

    Pass delete=True to delete the playlist entry
    """
    with PlexDB() as mchmdb:
        if delete:
            mchmdb.delete_playlist(playlist)
        else:
            mchmdb.add_playlist(playlist)


def get_playlist(path=None, plex_id=None):
    """
    Returns the playlist as a Playlist for either the plex_id or path
    """
    playlist = Playlist()
    with PlexDB() as mchmdb:
        playlist = mchmdb.playlist(playlist, plex_id, path)
    return playlist


def _m3u_iterator(text):
    """
    Yields e.g. plugin://plugin.video.MCMH.movies/?plex_id=xxx
    """
    lines = iter(text.split('\n'))
    for line in lines:
        if line.startswith('#EXTINF:'):
            yield next(lines).strip()


def m3u_to_plex_ids(playlist):
    """
    Adapter to process *.m3u playlist files. Encoding is not uniform!
    """
    plex_ids = list()
    with open(path_ops.encode_path(playlist.kodi_path), 'rb') as f:
        text = f.read()
    try:
        text = text.decode(v.M3U_ENCODING)
    except UnicodeDecodeError:
        LOG.warning('Fallback to ISO-8859-1 decoding for %s', playlist)
        text = text.decode('ISO-8859-1')
    for entry in _m3u_iterator(text):
        plex_id = utils.REGEX_PLEX_ID.search(entry)
        if plex_id:
            plex_id = plex_id.group(1)
            plex_ids.append(plex_id)
        else:
            # Add-on paths not working, try direct
            kodi_id, kodi_type = kodiid_from_filename(entry,
                                                      db_type=playlist.kodi_type)
            if not kodi_id:
                continue
            with PlexDB() as mchmdb:
                item = mchmdb.item_by_kodi_id(kodi_id, kodi_type)
            if item:
                plex_ids.append(item['plex_id'])
    return plex_ids


def playlist_file_to_plex_ids(playlist):
    """
    Takes the playlist file located at path [unicode] and parses it.
    Returns a list of plex_ids (str) or raises PL.PlaylistError if a single
    item cannot be parsed from Kodi to Plex.
    """
    if playlist.kodi_extension == 'm3u':
        plex_ids = m3u_to_plex_ids(playlist)
    else:
        LOG.error('Unsupported playlist extension: %s',
                  playlist.kodi_extension)
        raise PlaylistError
    return plex_ids
