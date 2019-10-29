#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Collection of functions associated with Kodi and Plex playlists and playqueues
"""
from __future__ import absolute_import, division, unicode_literals
from logging import getLogger

from .plex_api import API
from .mchm_db import PlexDB
from . import plex_functions as PF
from .kodi_db import kodiid_from_filename
from .downloadutils import DownloadUtils as DU
from . import utils
from . import json_rpc as js
from . import variables as v
from . import app

###############################################################################

LOG = getLogger('PLEX.playlist_func')

###############################################################################


class PlaylistError(Exception):
    """
    Exception for our playlist constructs
    """
    pass


class Playqueue_Object(object):
    """
    MHC object to represent PMS playQueues and Kodi playlist for queueing

    playlistid = None     [int] Kodi playlist id (0, 1, 2)
    type = None           [str] Kodi type: 'audio', 'video', 'picture'
    kodi_pl = None        Kodi xbmc.PlayList object
    items = []            [list] of Playlist_Items
    id = None             [str] Plex playQueueID, unique Plex identifier
    version = None        [int] Plex version of the playQueue
    selectedItemID = None
                          [str] Plex selectedItemID, playing element in queue
    selectedItemOffset = None
                          [str] Offset of the playing element in queue
    shuffled = 0          [int] 0: not shuffled, 1: ??? 2: ???
    repeat = 0            [int] 0: not repeated, 1: ??? 2: ???

    If Companion playback is initiated by another user:
    plex_transient_token = None
    """
    kind = 'playQueue'

    def __init__(self):
        self.id = None
        self.type = None
        self.playlistid = None
        self.kodi_pl = None
        self.items = []
        self.version = None
        self.selectedItemID = None
        self.selectedItemOffset = None
        self.shuffled = 0
        self.repeat = 0
        self.plex_transient_token = None
        # Need a hack for detecting swaps of elements
        self.old_kodi_pl = []
        # Did MHC itself just change the playqueue so the MHC playqueue monitor
        # should not pick up any changes?
        self.pkc_edit = False
        # Workaround to avoid endless loops of detecting PL clears
        self._clear_list = []
        # To keep track if Kodi playback was initiated from a Kodi playlist
        # There are a couple of pitfalls, unfortunately...
        self.kodi_playlist_playback = False

    def __repr__(self):
        answ = ("{{"
                "'playlistid': {self.playlistid}, "
                "'id': {self.id}, "
                "'version': {self.version}, "
                "'type': '{self.type}', "
                "'selectedItemID': {self.selectedItemID}, "
                "'selectedItemOffset': {self.selectedItemOffset}, "
                "'shuffled': {self.shuffled}, "
                "'repeat': {self.repeat}, "
                "'kodi_playlist_playback': {self.kodi_playlist_playback}, "
                "'pkc_edit': {self.pkc_edit}, ".format(self=self))
        answ = answ.encode('utf-8')
        # Since list.__repr__ will return string, not unicode
        return answ + b"'items': {self.items}}}".format(self=self)

    def __str__(self):
        return self.__repr__()

    def is_pkc_clear(self):
        """
        Returns True if MHC has cleared the Kodi playqueue just recently.
        Then this clear will be ignored from now on
        """
        try:
            self._clear_list.pop()
        except IndexError:
            return False
        else:
            return True

    def clear(self, kodi=True):
        """
        Resets the playlist object to an empty playlist.

        Pass kodi=False in order to NOT clear the Kodi playqueue
        """
        # kodi monitor's on_clear method will only be called if there were some
        # items to begin with
        if kodi and self.kodi_pl.size() != 0:
            self._clear_list.append(None)
            self.kodi_pl.clear()  # Clear Kodi playlist object
        self.items = []
        self.id = None
        self.version = None
        self.selectedItemID = None
        self.selectedItemOffset = None
        self.shuffled = 0
        self.repeat = 0
        self.plex_transient_token = None
        self.old_kodi_pl = []
        self.kodi_playlist_playback = False
        LOG.debug('Playlist cleared: %s', self)

    def position_from_plex_id(self, plex_id):
        """
        Returns the position [int] for the very first item with plex_id [int]
        (Plex seems uncapable of adding the same element multiple times to a
        playqueue or playlist)

        Raises KeyError if not found
        """
        for position, item in enumerate(self.items):
            if item.plex_id == plex_id:
                break
        else:
            raise KeyError('Did not find plex_id %s in %s', plex_id, self)
        return position


class PlaylistItem(object):
    """
    Object to fill our playqueues and playlists with.

    id = None          [int] Plex playlist/playqueue id, e.g. playQueueItemID
    plex_id = None     [int] Plex unique item id, "ratingKey"
    plex_type = None   [str] Plex type, e.g. 'movie', 'clip'
    kodi_id = None     [int] Kodi unique kodi id (unique only within type!)
    kodi_type = None   [str] Kodi type: 'movie'
    file = None        [str] Path to the item's file. STRING!!
    uri = None         [str] PMS path to item; will be auto-set with plex_id
    guid = None        [str] Weird Plex guid
    xml = None         [etree] XML from PMS, 1 lvl below <MediaContainer>
    playmethod = None  [str] either 'DirectPath', 'DirectStream', 'Transcode'
    playcount = None   [int] how many times the item has already been played
    offset = None      [int] the item's view offset UPON START in Plex time
    part = 0           [int] part number if Plex video consists of mult. parts
    force_transcode    [bool] defaults to False
    """
    def __init__(self):
        self.id = None
        self._plex_id = None
        self.plex_type = None
        self.kodi_id = None
        self.kodi_type = None
        self.file = None
        self._uri = None
        self.guid = None
        self.xml = None
        self.playmethod = None
        self.playcount = None
        self.offset = None
        # Transcoding quality, if needed
        self.quality = None
        # If Plex video consists of several parts; part number
        self.part = 0
        self.force_transcode = False
        # Shall we ask user to resume this item?
        #   None: ask user to resume
        #   False: do NOT resume, don't ask user
        #   True: do resume, don't ask user
        self.resume = None

    @property
    def plex_id(self):
        return self._plex_id

    @plex_id.setter
    def plex_id(self, value):
        self._plex_id = value
        self._uri = ('server://%s/com.plexapp.plugins.library/library/metadata/%s' %
                     (app.CONN.machine_identifier, value))

    @property
    def uri(self):
        return self._uri

    def __unicode__(self):
        return ("{{"
                "'id': {self.id}, "
                "'plex_id': {self.plex_id}, "
                "'plex_type': '{self.plex_type}', "
                "'kodi_id': {self.kodi_id}, "
                "'kodi_type': '{self.kodi_type}', "
                "'file': '{self.file}', "
                "'guid': '{self.guid}', "
                "'playmethod': '{self.playmethod}', "
                "'playcount': {self.playcount}, "
                "'offset': {self.offset}, "
                "'force_transcode': {self.force_transcode}, "
                "'part': {self.part}".format(self=self))

    def __repr__(self):
        return self.__unicode__().encode('utf-8')

    def plex_stream_index(self, kodi_stream_index, stream_type):
        """
        Pass in the kodi_stream_index [int] in order to receive the Plex stream
        index.

            stream_type:    'video', 'audio', 'subtitle'

        Returns None if unsuccessful
        """
        stream_type = v.PLEX_STREAM_TYPE_FROM_STREAM_TYPE[stream_type]
        count = 0
        if kodi_stream_index == -1:
            # Kodi telling us "it's the last one"
            iterator = list(reversed(self.xml[0][self.part]))
            kodi_stream_index = 0
        else:
            iterator = self.xml[0][self.part]
        # Kodi indexes differently than Plex
        for stream in iterator:
            if (stream.attrib['streamType'] == stream_type and
                    'key' in stream.attrib):
                if count == kodi_stream_index:
                    return stream.attrib['id']
                count += 1
        for stream in iterator:
            if (stream.attrib['streamType'] == stream_type and
                    'key' not in stream.attrib):
                if count == kodi_stream_index:
                    return stream.attrib['id']
                count += 1

    def kodi_stream_index(self, plex_stream_index, stream_type):
        """
        Pass in the kodi_stream_index [int] in order to receive the Plex stream
        index.

            stream_type:    'video', 'audio', 'subtitle'

        Returns None if unsuccessful
        """
        stream_type = v.PLEX_STREAM_TYPE_FROM_STREAM_TYPE[stream_type]
        count = 0
        for stream in self.xml[0][self.part]:
            if (stream.attrib['streamType'] == stream_type and
                    'key' in stream.attrib):
                if stream.attrib['id'] == plex_stream_index:
                    return count
                count += 1
        for stream in self.xml[0][self.part]:
            if (stream.attrib['streamType'] == stream_type and
                    'key' not in stream.attrib):
                if stream.attrib['id'] == plex_stream_index:
                    return count
                count += 1


def playlist_item_from_kodi(kodi_item):
    """
    Turns the JSON answer from Kodi into a playlist element

    Supply with data['item'] as returned from Kodi JSON-RPC interface.
    kodi_item dict contains keys 'id', 'type', 'file' (if applicable)
    """
    item = PlaylistItem()
    item.kodi_id = kodi_item.get('id')
    item.kodi_type = kodi_item.get('type')
    if item.kodi_id:
        with PlexDB(lock=False) as mchmdb:
            db_item = mchmdb.item_by_kodi_id(kodi_item['id'], kodi_item['type'])
        if db_item:
            item.plex_id = db_item['plex_id']
            item.plex_type = db_item['plex_type']
    item.file = kodi_item.get('file')
    if item.plex_id is None and item.file is not None:
        try:
            query = item.file.split('?', 1)[1]
        except IndexError:
            query = ''
        query = dict(utils.parse_qsl(query))
        item.plex_id = utils.cast(int, query.get('plex_id'))
        item.plex_type = query.get('itemType')
    LOG.debug('Made playlist item from Kodi: %s', item)
    return item


def verify_kodi_item(plex_id, kodi_item):
    """
    Tries to lookup kodi_id and kodi_type for kodi_item (with kodi_item['file']
    supplied) - if and only if plex_id is None.

    Returns the kodi_item with kodi_item['id'] and kodi_item['type'] possibly
    set to None if unsuccessful.

    Will raise a PlaylistError if plex_id is None and kodi_item['file'] starts
    with either 'plugin' or 'http'.
    Will raise KeyError if neither plex_id nor kodi_id are found
    """
    if plex_id is not None or kodi_item.get('id') is not None:
        # Got all the info we need
        return kodi_item
    # Special case playlist startup - got type but no id
    if (not app.SYNC.direct_paths and app.SYNC.enable_music and
            kodi_item.get('type') == v.KODI_TYPE_SONG and
            kodi_item['file'].startswith('http')):
        kodi_item['id'], _ = kodiid_from_filename(kodi_item['file'],
                                                  v.KODI_TYPE_SONG)
        LOG.debug('Detected song. Research results: %s', kodi_item)
        return kodi_item
    # Need more info since we don't have kodi_id nor type. Use file path.
    if ((kodi_item['file'].startswith('plugin') and
         not kodi_item['file'].startswith('plugin://%s' % v.ADDON_ID)) or
            kodi_item['file'].startswith('http')):
        LOG.debug('kodi_item cannot be used for Plex playback: %s', kodi_item)
        raise PlaylistError('kodi_item cannot be used for Plex playback')
    LOG.debug('Starting research for Kodi id since we didnt get one: %s',
              kodi_item)
    # Try the VIDEO DB first - will find both movies and episodes
    kodi_id, kodi_type = kodiid_from_filename(kodi_item['file'],
                                              db_type='video')
    if not kodi_id:
        # No movie or episode found - try MUSIC DB now for songs
        kodi_id, kodi_type = kodiid_from_filename(kodi_item['file'],
                                                  db_type='music')
    kodi_item['id'] = kodi_id
    kodi_item['type'] = None if kodi_id is None else kodi_type
    if plex_id is None and kodi_id is None:
        raise KeyError('Neither Plex nor Kodi id found for %s' % kodi_item)
    LOG.debug('Research results for kodi_item: %s', kodi_item)
    return kodi_item


def playlist_item_from_plex(plex_id):
    """
    Returns a playlist element providing the plex_id ("ratingKey")

    Returns a Playlist_Item
    """
    item = PlaylistItem()
    item.plex_id = plex_id
    with PlexDB(lock=False) as mchmdb:
        db_item = mchmdb.item_by_id(plex_id)
    if db_item:
        item.plex_type = db_item['plex_type']
        item.kodi_id = db_item['kodi_id']
        item.kodi_type = db_item['kodi_type']
    else:
        raise KeyError('Could not find plex_id %s in database' % plex_id)
    LOG.debug('Made playlist item from plex: %s', item)
    return item


def playlist_item_from_xml(xml_video_element, kodi_id=None, kodi_type=None):
    """
    Returns a playlist element for the playqueue using the Plex xml

    xml_video_element: etree xml piece 1 level underneath <MediaContainer>
    """
    item = PlaylistItem()
    api = API(xml_video_element)
    item.plex_id = api.plex_id
    item.plex_type = api.plex_type
    # item.id will only be set if you passed in an xml_video_element from e.g.
    # a playQueue
    item.id = api.item_id()
    if kodi_id is not None:
        item.kodi_id = kodi_id
        item.kodi_type = kodi_type
    elif item.plex_type != v.PLEX_TYPE_CLIP:
        with PlexDB(lock=False) as mchmdb:
            db_element = mchmdb.item_by_id(item.plex_id,
                                           plex_type=item.plex_type)
        if db_element:
            item.kodi_id = db_element['kodi_id']
            item.kodi_type = db_element['kodi_type']
    item.guid = api.guid_html_escaped()
    item.playcount = api.viewcount()
    item.offset = api.resume_point()
    item.xml = xml_video_element
    LOG.debug('Created new playlist item from xml: %s', item)
    return item


def _get_playListVersion_from_xml(playlist, xml):
    """
    Takes a PMS xml as input to overwrite the playlist version (e.g. Plex
    playQueueVersion).

    Raises PlaylistError if unsuccessful
    """
    playlist.version = utils.cast(int,
                                  xml.get('%sVersion' % playlist.kind))
    if playlist.version is None:
        raise PlaylistError('Could not get new playlist Version for playlist '
                            '%s' % playlist)


def get_playlist_details_from_xml(playlist, xml):
    """
    Takes a PMS xml as input and overwrites all the playlist's details, e.g.
    playlist.id with the XML's playQueueID

    Raises PlaylistError if something went wrong.
    """
    playlist.id = utils.cast(int,
                             xml.get('%sID' % playlist.kind))
    playlist.version = utils.cast(int,
                                  xml.get('%sVersion' % playlist.kind))
    playlist.shuffled = utils.cast(int,
                                   xml.get('%sShuffled' % playlist.kind))
    playlist.selectedItemID = utils.cast(int,
                                         xml.get('%sSelectedItemID'
                                                 % playlist.kind))
    playlist.selectedItemOffset = utils.cast(int,
                                             xml.get('%sSelectedItemOffset'
                                                     % playlist.kind))
    LOG.debug('Updated playlist from xml: %s', playlist)


def update_playlist_from_PMS(playlist, playlist_id=None, xml=None):
    """
    Updates Kodi playlist using a new PMS playlist. Pass in playlist_id if we
    need to fetch a new playqueue

    If an xml is passed in, the playlist will be overwritten with its info

    Raises PlaylistError if something went wront
    """
    if xml is None:
        xml = get_PMS_playlist(playlist, playlist_id)
    # Clear our existing playlist and the associated Kodi playlist
    playlist.clear()
    # Set new values
    get_playlist_details_from_xml(playlist, xml)
    for plex_item in xml:
        playlist_item = add_to_Kodi_playlist(playlist, plex_item)
        if playlist_item is not None:
            playlist.items.append(playlist_item)


def init_plex_playqueue(playlist, plex_id=None, kodi_item=None):
    """
    Initializes the Plex side without changing the Kodi playlists
    WILL ALSO UPDATE OUR PLAYLISTS.

    Returns the first MHC playlist item or raises PlaylistError
    """
    LOG.debug('Initializing the playqueue on the Plex side: %s', playlist)
    verify_kodi_item(plex_id, kodi_item)
    playlist.clear(kodi=False)
    try:
        if plex_id:
            item = playlist_item_from_plex(plex_id)
        else:
            item = playlist_item_from_kodi(kodi_item)
        params = {
            'next': 0,
            'type': playlist.type,
            'uri': item.uri
        }
        xml = DU().downloadUrl(url="{server}/%ss" % playlist.kind,
                               action_type="POST",
                               parameters=params)
        if xml in (None, 401):
            raise PlaylistError('Did not receive a valid xml from the PMS')
        get_playlist_details_from_xml(playlist, xml)
        # Need to get the details for the playlist item
        item = playlist_item_from_xml(xml[0])
    except (KeyError, IndexError, TypeError):
        LOG.error('Could not init Plex playlist: plex_id %s, kodi_item %s',
                  plex_id, kodi_item)
        raise PlaylistError
    playlist.items.append(item)
    LOG.debug('Initialized the playqueue on the Plex side: %s', playlist)
    return item


def add_listitem_to_playlist(playlist, pos, listitem, kodi_id=None,
                             kodi_type=None, plex_id=None, file=None):
    """
    Adds a listitem to both the Kodi and Plex playlist at position pos [int].

    If file is not None, file will overrule kodi_id!

    file: str!!
    """
    LOG.debug('add_listitem_to_playlist at position %s. Playlist before add: '
              '%s', pos, playlist)
    kodi_item = {'id': kodi_id, 'type': kodi_type, 'file': file}
    if playlist.id is None:
        init_plex_playqueue(playlist, plex_id, kodi_item)
    else:
        add_item_to_plex_playqueue(playlist, pos, plex_id, kodi_item)
    if kodi_id is None and playlist.items[pos].kodi_id:
        kodi_id = playlist.items[pos].kodi_id
        kodi_type = playlist.items[pos].kodi_type
    if file is None:
        file = playlist.items[pos].file
    # Otherwise we double the item!
    del playlist.items[pos]
    kodi_item = {'id': kodi_id, 'type': kodi_type, 'file': file}
    add_listitem_to_Kodi_playlist(playlist,
                                  pos,
                                  listitem,
                                  file,
                                  kodi_item=kodi_item)


def add_item_to_playlist(playlist, pos, kodi_id=None, kodi_type=None,
                         plex_id=None, file=None):
    """
    Adds an item to BOTH the Kodi and Plex playlist at position pos [int]
        file: str!

    Raises PlaylistError if something went wrong
    """
    LOG.debug('add_item_to_playlist. Playlist before adding: %s', playlist)
    kodi_item = {'id': kodi_id, 'type': kodi_type, 'file': file}
    if playlist.id is None:
        item = init_plex_playqueue(playlist, plex_id, kodi_item)
    else:
        item = add_item_to_plex_playqueue(playlist, pos, plex_id, kodi_item)
    params = {
        'playlistid': playlist.playlistid,
        'position': pos
    }
    if item.kodi_id is not None:
        params['item'] = {'%sid' % item.kodi_type: int(item.kodi_id)}
    else:
        params['item'] = {'file': item.file}
    reply = js.playlist_insert(params)
    if reply.get('error') is not None:
        raise PlaylistError('Could not add item to playlist. Kodi reply. %s'
                            % reply)
    return item


def add_item_to_plex_playqueue(playlist, pos, plex_id=None, kodi_item=None):
    """
    Adds a new item to the playlist at position pos [int] only on the Plex
    side of things (e.g. because the user changed the Kodi side)
    WILL ALSO UPDATE OUR PLAYLISTS

    Returns the MHC PlayList item or raises PlaylistError
    """
    verify_kodi_item(plex_id, kodi_item)
    if plex_id:
        item = playlist_item_from_plex(plex_id)
    else:
        item = playlist_item_from_kodi(kodi_item)
    url = "{server}/%ss/%s?uri=%s" % (playlist.kind, playlist.id, item.uri)
    # Will always put the new item at the end of the Plex playlist
    xml = DU().downloadUrl(url, action_type="PUT")
    try:
        xml[-1].attrib
    except (TypeError, AttributeError, KeyError, IndexError):
        raise PlaylistError('Could not add item %s to playlist %s'
                            % (kodi_item, playlist))
    api = API(xml[-1])
    item.xml = xml[-1]
    item.id = api.item_id()
    item.guid = api.guid_html_escaped()
    item.offset = api.resume_point()
    item.playcount = api.viewcount()
    playlist.items.append(item)
    if pos == len(playlist.items) - 1:
        # Item was added at the end
        _get_playListVersion_from_xml(playlist, xml)
    else:
        # Move the new item to the correct position
        move_playlist_item(playlist,
                           len(playlist.items) - 1,
                           pos)
    LOG.debug('Successfully added item on the Plex side: %s', playlist)
    return item


def add_item_to_kodi_playlist(playlist, pos, kodi_id=None, kodi_type=None,
                              file=None, xml_video_element=None):
    """
    Adds an item to the KODI playlist only. WILL ALSO UPDATE OUR PLAYLISTS

    Returns the playlist item that was just added or raises PlaylistError

    file: str!
    """
    LOG.debug('Adding new item kodi_id: %s, kodi_type: %s, file: %s to Kodi '
              'only at position %s for %s',
              kodi_id, kodi_type, file, pos, playlist)
    params = {
        'playlistid': playlist.playlistid,
        'position': pos
    }
    if kodi_id is not None:
        params['item'] = {'%sid' % kodi_type: int(kodi_id)}
    else:
        params['item'] = {'file': file}
    reply = js.playlist_insert(params)
    if reply.get('error') is not None:
        raise PlaylistError('Could not add item to playlist. Kodi reply. %s',
                            reply)
    if xml_video_element is not None:
        item = playlist_item_from_xml(xml_video_element)
        item.kodi_id = kodi_id
        item.kodi_type = kodi_type
        item.file = file
    elif kodi_id is not None:
        item = playlist_item_from_kodi(
            {'id': kodi_id, 'type': kodi_type, 'file': file})
        if item.plex_id is not None:
            xml = PF.GetPlexMetadata(item.plex_id)
            item.xml = xml[-1]
    playlist.items.insert(pos, item)
    return item


def move_playlist_item(playlist, before_pos, after_pos):
    """
    Moves playlist item from before_pos [int] to after_pos [int] for Plex only.

    WILL ALSO CHANGE OUR PLAYLISTS.
    """
    LOG.debug('Moving item from %s to %s on the Plex side for %s',
              before_pos, after_pos, playlist)
    if after_pos == 0:
        url = "{server}/%ss/%s/items/%s/move?after=0" % \
              (playlist.kind,
               playlist.id,
               playlist.items[before_pos].id)
    else:
        url = "{server}/%ss/%s/items/%s/move?after=%s" % \
              (playlist.kind,
               playlist.id,
               playlist.items[before_pos].id,
               playlist.items[after_pos - 1].id)
    # We need to increment the playlistVersion
    _get_playListVersion_from_xml(
        playlist, DU().downloadUrl(url, action_type="PUT"))
    # Move our item's position in our internal playlist
    playlist.items.insert(after_pos, playlist.items.pop(before_pos))
    LOG.debug('Done moving for %s', playlist)


def get_PMS_playlist(playlist, playlist_id=None):
    """
    Fetches the PMS playlist/playqueue as an XML. Pass in playlist_id if we
    need to fetch a new playlist

    Raises PlaylistError if something went wrong
    """
    playlist_id = playlist_id if playlist_id else playlist.id
    if playlist.kind == 'playList':
        xml = DU().downloadUrl("{server}/playlists/%s/items" % playlist_id)
    else:
        xml = DU().downloadUrl("{server}/playQueues/%s" % playlist_id)
    try:
        xml.attrib
    except AttributeError:
        raise PlaylistError('Did not get a valid xml')
    return xml


def refresh_playlist_from_PMS(playlist):
    """
    Only updates the selected item from the PMS side (e.g.
    playQueueSelectedItemID). Will NOT check whether items still make sense.
    """
    get_playlist_details_from_xml(playlist, get_PMS_playlist(playlist))


def delete_playlist_item_from_PMS(playlist, pos):
    """
    Delete the item at position pos [int] on the Plex side and our playlists
    """
    LOG.debug('Deleting position %s for %s on the Plex side', pos, playlist)
    xml = DU().downloadUrl("{server}/%ss/%s/items/%s?repeat=%s" %
                           (playlist.kind,
                            playlist.id,
                            playlist.items[pos].id,
                            playlist.repeat),
                           action_type="DELETE")
    _get_playListVersion_from_xml(playlist, xml)
    del playlist.items[pos]


# Functions operating on the Kodi playlist objects ##########

def add_to_Kodi_playlist(playlist, xml_video_element):
    """
    Adds a new item to the Kodi playlist via JSON (at the end of the playlist).
    Pass in the PMS xml's video element (one level underneath MediaContainer).

    Returns a Playlist_Item or raises PlaylistError
    """
    item = playlist_item_from_xml(xml_video_element)
    if item.kodi_id:
        json_item = {'%sid' % item.kodi_type: item.kodi_id}
    else:
        json_item = {'file': item.file}
    reply = js.playlist_add(playlist.playlistid, json_item)
    if reply.get('error') is not None:
        raise PlaylistError('Could not add item %s to Kodi playlist. Error: '
                            '%s', xml_video_element, reply)
    return item


def add_listitem_to_Kodi_playlist(playlist, pos, listitem, file,
                                  xml_video_element=None, kodi_item=None):
    """
    Adds an xbmc listitem to the Kodi playlist.xml_video_element

    WILL NOT UPDATE THE PLEX SIDE, BUT WILL UPDATE OUR PLAYLISTS

    file: string!
    """
    LOG.debug('Insert listitem at position %s for Kodi only for %s',
              pos, playlist)
    # Add the item into Kodi playlist
    playlist.kodi_pl.add(url=file, listitem=listitem, index=pos)
    # We need to add this to our internal queue as well
    if xml_video_element is not None:
        item = playlist_item_from_xml(xml_video_element)
    else:
        item = playlist_item_from_kodi(kodi_item)
    if file is not None:
        item.file = file
    playlist.items.insert(pos, item)
    LOG.debug('Done inserting for %s', playlist)
    return item


def remove_from_kodi_playlist(playlist, pos):
    """
    Removes the item at position pos from the Kodi playlist using JSON.

    WILL NOT UPDATE THE PLEX SIDE, BUT WILL UPDATE OUR PLAYLISTS
    """
    LOG.debug('Removing position %s from Kodi only from %s', pos, playlist)
    reply = js.playlist_remove(playlist.playlistid, pos)
    if reply.get('error') is not None:
        LOG.error('Could not delete the item from the playlist. Error: %s',
                  reply)
        return
    try:
        del playlist.items[pos]
    except IndexError:
        LOG.error('Cannot delete position %s for %s', pos, playlist)


def get_pms_playqueue(playqueue_id):
    """
    Returns the Plex playqueue as an etree XML or None if unsuccessful
    """
    xml = DU().downloadUrl(
        "{server}/playQueues/%s" % playqueue_id,
        headerOptions={'Accept': 'application/xml'})
    try:
        xml.attrib
    except AttributeError:
        LOG.error('Could not download Plex playqueue %s', playqueue_id)
        xml = None
    return xml


def get_plextype_from_xml(xml):
    """
    Needed if PMS returns an empty playqueue. Will get the Plex type from the
    empty playlist playQueueSourceURI. Feed with (empty) etree xml

    returns None if unsuccessful
    """
    try:
        plex_id = utils.REGEX_PLEX_ID_FROM_URL.findall(
            xml.attrib['playQueueSourceURI'])[0]
    except IndexError:
        LOG.error('Could not get plex_id from xml: %s', xml.attrib)
        return
    new_xml = PF.GetPlexMetadata(plex_id)
    try:
        new_xml[0].attrib
    except (TypeError, IndexError, AttributeError):
        LOG.error('Could not get plex metadata for plex id %s', plex_id)
        return
    return new_xml[0].attrib.get('type').decode('utf-8')
