#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Used to kick off Kodi playback
"""
from __future__ import absolute_import, division, unicode_literals
from logging import getLogger
from threading import Thread
import datetime

import xbmc

from .plex_api import API
from .plex_db import PlexDB
from . import plex_functions as PF
from . import utils
from .kodi_db import KodiVideoDB
from . import playlist_func as PL
from . import playqueue as PQ
from . import json_rpc as js
from . import transfer
from .playback_decision import set_playurl
from . import variables as v
from . import app

###############################################################################
LOG = getLogger('PLEX.playback')
# Do we need to return ultimately with a setResolvedUrl?
RESOLVE = True
###############################################################################


def playback_triage(plex_id=None, plex_type=None, path=None, resolve=True):
    """
    Hit this function for addon path playback, Plex trailers, etc.
    Will setup playback first, then on second call complete playback.

    Will set Playback_Successful() with potentially a PKCListItem() attached
    (to be consumed by setResolvedURL in default.py)

    If trailers or additional (movie-)parts are added, default.py is released
    and a completely new player instance is called with a new playlist. This
    circumvents most issues with Kodi & playqueues

    Set resolve to False if you do not want setResolvedUrl to be called on
    the first pass - e.g. if you're calling this function from the original
    service.py Python instance
    """
    try:
        _playback_triage(plex_id, plex_type, path, resolve)
    finally:
        # Reset some playback variables the user potentially set to init
        # playback
        app.PLAYSTATE.context_menu_play = False
        app.PLAYSTATE.force_transcode = False
        app.PLAYSTATE.resume_playback = None


def _playback_triage(plex_id, plex_type, path, resolve):
    plex_id = utils.cast(int, plex_id)
    LOG.info('playback_triage called with plex_id %s, plex_type %s, path %s, '
             'resolve %s', plex_id, plex_type, path, resolve)
    global RESOLVE
    # If started via Kodi context menu, we never resolve
    RESOLVE = resolve if not app.PLAYSTATE.context_menu_play else False
    if not app.CONN.online or not app.ACCOUNT.authenticated:
        if not app.CONN.online:
            LOG.error('PMS not online for playback')
            # "{0} offline"
            utils.dialog('notification',
                         utils.lang(29999),
                         utils.lang(39213).format(app.CONN.server_name),
                         icon='{plex}')
        else:
            LOG.error('Not yet authenticated for PMS, abort starting playback')
            # "Unauthorized for PMS"
            utils.dialog('notification', utils.lang(29999), utils.lang(30017))
        _ensure_resolve(abort=True)
        return
    with app.APP.lock_playqueues:
        playqueue = PQ.get_playqueue_from_type(
            v.KODI_PLAYLIST_TYPE_FROM_PLEX_TYPE[plex_type])
        try:
            pos = js.get_position(playqueue.playlistid)
        except KeyError:
            # Kodi bug - Playlist plays (not Playqueue) will ALWAYS be audio for
            # add-on paths
            LOG.info('No position returned from player! Assuming playlist')
            playqueue = PQ.get_playqueue_from_type(v.KODI_PLAYLIST_TYPE_AUDIO)
            try:
                pos = js.get_position(playqueue.playlistid)
            except KeyError:
                LOG.info('Assuming video instead of audio playlist playback')
                playqueue = PQ.get_playqueue_from_type(v.KODI_PLAYLIST_TYPE_VIDEO)
                try:
                    pos = js.get_position(playqueue.playlistid)
                except KeyError:
                    LOG.error('Still no position - abort')
                    # "Play error"
                    utils.dialog('notification',
                                 utils.lang(29999),
                                 utils.lang(30128),
                                 icon='{error}')
                    _ensure_resolve(abort=True)
                    return
        # HACK to detect playback of playlists for add-on paths
        items = js.playlist_get_items(playqueue.playlistid)
        try:
            item = items[pos]
        except IndexError:
            LOG.info('Could not apply playlist hack! Probably Widget playback')
        else:
            if ('id' not in item and
                    item.get('type') == 'unknown' and item.get('title') == ''):
                LOG.info('Kodi playlist play detected')
                _playlist_playback(plex_id, plex_type)
                return

        # Can return -1 (as in "no playlist")
        pos = pos if pos != -1 else 0
        LOG.debug('playQueue position %s for %s', pos, playqueue)
        # Have we already initiated playback?
        try:
            item = playqueue.items[pos]
        except IndexError:
            LOG.debug('PKC playqueue yet empty, need to initialize playback')
            initiate = True
        else:
            if item.plex_id != plex_id:
                LOG.debug('Received new plex_id %s, expected %s',
                          plex_id, item.plex_id)
                initiate = True
            else:
                initiate = False
        if not initiate and app.PLAYSTATE.resume_playback is not None:
            LOG.debug('Detected re-playing of the same item')
            initiate = True
        if initiate:
            _playback_init(plex_id, plex_type, playqueue, pos)
        else:
            # kick off playback on second pass
            _conclude_playback(playqueue, pos)


def _playlist_playback(plex_id, plex_type):
    """
    Really annoying Kodi behavior: Kodi will throw the ENTIRE playlist some-
    where, causing Playlist.onAdd to fire for each item like this:
    Playlist.OnAdd Data: {u'item': {u'type': u'episode', u'id': 164},
                          u'playlistid': 0,
                          u'position': 2}
    This does NOT work for Addon paths, type and id will be unknown:
        {u'item': {u'type': u'unknown'},
         u'playlistid': 0,
         u'position': 7}
    At the end, only the element being played actually shows up in the Kodi
    playqueue.
    Hence: if we fail the first addon paths call, Kodi will start playback
    for the next item in line :-)
    (by the way: trying to get active Kodi player id will return [])
    """
    xml = PF.GetPlexMetadata(plex_id, reraise=True)
    if xml in (None, 401):
        _ensure_resolve(abort=True)
        return
    # Kodi bug: playqueue will ALWAYS be audio playqueue UNTIL playback
    # has actually started. Need to tell Kodimonitor
    playqueue = PQ.get_playqueue_from_type(v.KODI_PLAYLIST_TYPE_AUDIO)
    playqueue.clear(kodi=False)
    # Set the flag for the potentially WRONG audio playlist so Kodimonitor
    # can pick up on it
    playqueue.kodi_playlist_playback = True
    playlist_item = PL.playlist_item_from_xml(xml[0])
    playqueue.items.append(playlist_item)
    _conclude_playback(playqueue, pos=0)


def _playback_init(plex_id, plex_type, playqueue, pos):
    """
    Playback setup if Kodi starts playing an item for the first time.
    """
    LOG.info('Initializing PKC playback')
    # Stop playback so we don't get an error message that the last item of the
    # queue failed to play
    app.APP.player.stop()
    xml = PF.GetPlexMetadata(plex_id, reraise=True)
    if xml in (None, 401):
        LOG.error('Could not get a PMS xml for plex id %s', plex_id)
        _ensure_resolve(abort=True)
        return
    if (xbmc.getCondVisibility('Window.IsVisible(Home.xml)') and
            plex_type in v.PLEX_VIDEOTYPES and
            playqueue.kodi_pl.size() > 1):
        # playqueue.kodi_pl.size() could return more than one - since playback
        # was initiated from the audio queue!
        LOG.debug('Detected widget playback for videos')
    elif playqueue.kodi_pl.size() > 1:
        # Special case - we already got a filled Kodi playqueue
        try:
            _init_existing_kodi_playlist(playqueue, pos)
        except PL.PlaylistError:
            LOG.error('Playback_init for existing Kodi playlist failed')
            _ensure_resolve(abort=True)
            return
        # Now we need to use setResolvedUrl for the item at position ZERO
        # playqueue.py will pick up the missing items
        _conclude_playback(playqueue, 0)
        return
    # "Usual" case - consider trailers and parts and build both Kodi and Plex
    # playqueues
    # Release default.py
    _ensure_resolve()
    api = API(xml[0])
    if api.resume_point() and (app.SYNC.direct_paths or
                               app.PLAYSTATE.context_menu_play):
        # Since Kodi won't ask if user wants to resume playback -
        # we need to ask ourselves
        resume = resume_dialog(int(api.resume_point()))
        if resume is None:
            LOG.info('User cancelled resume dialog')
            return
    elif app.SYNC.direct_paths:
        resume = False
    else:
        resume = app.PLAYSTATE.resume_playback or False
    trailers = False
    if (not resume and plex_type == v.PLEX_TYPE_MOVIE and
            utils.settings('enableCinema') == "true"):
        if utils.settings('askCinema') == "true":
            # "Play trailers?"
            trailers = utils.yesno_dialog(utils.lang(29999), utils.lang(33016))
        else:
            trailers = True
    LOG.debug('Resuming: %s. Playing trailers: %s', resume, trailers)
    playqueue.clear()
    if plex_type != v.PLEX_TYPE_CLIP:
        # Post to the PMS to create a playqueue - in any case due to Companion
        xml = PF.init_plex_playqueue(plex_id,
                                     plex_type,
                                     xml.get('librarySectionUUID'),
                                     trailers=trailers)
        if xml is None:
            LOG.error('Could not get a playqueue xml for plex id %s', plex_id)
            # "Play error"
            utils.dialog('notification',
                         utils.lang(29999),
                         utils.lang(30128),
                         icon='{error}')
            # Do NOT use _ensure_resolve() because we resolved above already
            return
        PL.get_playlist_details_from_xml(playqueue, xml)
    stack = _prep_playlist_stack(xml, resume)
    _process_stack(playqueue, stack)
    # New thread to release this one sooner (e.g. harddisk spinning up)
    thread = Thread(target=threaded_playback,
                    args=(playqueue.kodi_pl, pos, None))
    thread.setDaemon(True)
    LOG.info('Done initializing playback, starting Kodi player at pos %s', pos)
    # By design, PKC will start Kodi playback using Player().play(). Kodi
    # caches paths like our plugin://pkc. If we use Player().play() between
    # 2 consecutive startups of exactly the same Kodi library item, Kodi's
    # cache will have been flushed for some reason. Hence the 2nd call for
    # plugin://pkc will be lost; Kodi will try to startup playback for an empty
    # path: log entry is "CGUIWindowVideoBase::OnPlayMedia <missing path>"
    thread.start()
    # Ensure that PKC playqueue monitor ignores the changes we just made
    playqueue.pkc_edit = True


def _ensure_resolve(abort=False):
    """
    Will check whether RESOLVE=True and if so, fail Kodi playback startup
    with the path 'PKC_Dummy_Path_Which_Fails' using setResolvedUrl (and some
    pickling)

    This way we're making sure that other Python instances (calling default.py)
    will be destroyed.
    """
    if RESOLVE:
        # Releases the other Python thread without a ListItem
        transfer.send(True)
        # Wait for default.py to have completed xbmcplugin.setResolvedUrl()
        transfer.wait_for_transfer(source='default')
    if abort:
        utils.dialog('notification',
                     heading='{plex}',
                     message=utils.lang(30128),
                     icon='{error}',
                     time=3000)


def resume_dialog(resume):
    """
    Pass the resume [int] point in seconds. Returns True if user chose to
    resume. Returns None if user cancelled
    """
    # "Resume from {0:s}"
    # "Start from beginning"
    resume = datetime.timedelta(seconds=resume)
    answ = utils.dialog('contextmenu',
                        [utils.lang(12022).replace('{0:s}', '{0}').format(unicode(resume)),
                         utils.lang(12021)])
    if answ == -1:
        return
    return answ == 0


def _init_existing_kodi_playlist(playqueue, pos):
    """
    Will take the playqueue's kodi_pl with MORE than 1 element and initiate
    playback (without adding trailers)
    """
    LOG.debug('Kodi playlist size: %s', playqueue.kodi_pl.size())
    kodi_items = js.playlist_get_items(playqueue.playlistid)
    if not kodi_items:
        LOG.error('No Kodi items returned')
        raise PL.PlaylistError('No Kodi items returned')
    item = PL.init_plex_playqueue(playqueue, kodi_item=kodi_items[pos])
    item.force_transcode = app.PLAYSTATE.force_transcode
    # playqueue.py will add the rest - this will likely put the PMS under
    # a LOT of strain if the following Kodi setting is enabled:
    # Settings -> Player -> Videos -> Play next video automatically
    LOG.debug('Done init_existing_kodi_playlist')


def _prep_playlist_stack(xml, resume):
    """
    resume [bool] will set the resume point of the LAST item of the stack, for
    part 1 only
    """
    stack = []
    for i, item in enumerate(xml):
        api = API(item)
        if (app.PLAYSTATE.context_menu_play is False and
                api.plex_type not in (v.PLEX_TYPE_CLIP, v.PLEX_TYPE_EPISODE)):
            # If user chose to play via PMS or force transcode, do not
            # use the item path stored in the Kodi DB
            with PlexDB(lock=False) as plexdb:
                db_item = plexdb.item_by_id(api.plex_id, api.plex_type)
            kodi_id = db_item['kodi_id'] if db_item else None
            kodi_type = db_item['kodi_type'] if db_item else None
        else:
            # We will never store clips (trailers) in the Kodi DB.
            # Also set kodi_id to None for playback via PMS, so that we're
            # using add-on paths.
            # Also do NOT associate episodes with library items for addon paths
            # as artwork lookup is broken (episode path does not link back to
            # season and show)
            kodi_id = None
            kodi_type = None
        for part, _ in enumerate(item[0]):
            api.part = part
            if kodi_id is None:
                # Need to redirect again to PKC to conclude playback
                path = api.path(force_addon=True, force_first_media=True)
                # Using different paths than the ones saved in the Kodi DB
                # fixes Kodi immediately resuming the video if one restarts
                # the same video again after playback
                # WARNING: This fixes startup, but renders Kodi unstable
                # path = path.replace('plugin.video.plexkodiconnect.tvshows',
                #                     'plugin.video.plexkodiconnect', 1)
                # path = path.replace('plugin.video.plexkodiconnect.movies',
                #                     'plugin.video.plexkodiconnect', 1)
                listitem = api.listitem()
                listitem.setPath(path.encode('utf-8'))
            else:
                # Will add directly via the Kodi DB
                path = None
                listitem = None
            stack.append({
                'kodi_id': kodi_id,
                'kodi_type': kodi_type,
                'file': path,
                'xml_video_element': item,
                'listitem': listitem,
                'part': part,
                'playcount': api.viewcount(),
                'offset': api.resume_point(),
                'resume': resume if i + 1 == len(xml) and part == 0 else False,
                'id': api.item_id()
            })
    return stack


def _process_stack(playqueue, stack):
    """
    Takes our stack and adds the items to the PKC and Kodi playqueues.
    """
    # getposition() can return -1
    pos = max(playqueue.kodi_pl.getposition(), 0) + 1
    for item in stack:
        if item['kodi_id'] is None:
            playlist_item = PL.add_listitem_to_Kodi_playlist(
                playqueue,
                pos,
                item['listitem'],
                file=item['file'],
                xml_video_element=item['xml_video_element'])
        else:
            # Directly add element so we have full metadata
            playlist_item = PL.add_item_to_kodi_playlist(
                playqueue,
                pos,
                kodi_id=item['kodi_id'],
                kodi_type=item['kodi_type'],
                xml_video_element=item['xml_video_element'])
        playlist_item.playcount = item['playcount']
        playlist_item.offset = item['offset']
        playlist_item.part = item['part']
        playlist_item.id = item['id']
        playlist_item.force_transcode = app.PLAYSTATE.force_transcode
        playlist_item.resume = item['resume']
        pos += 1


def _set_resume(listitem, item, api):
    if item.plex_type in (v.PLEX_TYPE_SONG, v.PLEX_TYPE_CLIP):
        return
    if item.resume is True:
        # Do NOT use item.offset directly but get it from the DB
        # (user might have initiated same video twice)
        with PlexDB(lock=False) as plexdb:
            db_item = plexdb.item_by_id(item.plex_id, item.plex_type)
        if db_item:
            file_id = db_item['kodi_fileid']
            with KodiVideoDB(lock=False) as kodidb:
                item.offset = kodidb.get_resume(file_id)
        LOG.info('Resuming playback at %s', item.offset)
        if v.KODIVERSION >= 18 and api:
            # Kodi 18 Alpha 3 broke StartOffset
            try:
                percent = (item.offset or api.resume_point()) / api.runtime() * 100.0
            except ZeroDivisionError:
                percent = 0.0
            LOG.debug('Resuming at %s percent', percent)
            listitem.setProperty('StartPercent', str(percent))
        else:
            listitem.setProperty('StartOffset', str(item.offset))
            listitem.setProperty('resumetime', str(item.offset))
    elif v.KODIVERSION >= 18:
        # Make sure that the video starts from the beginning
        listitem.setProperty('StartPercent', '0')


def _conclude_playback(playqueue, pos):
    """
    ONLY if actually being played (e.g. at 5th position of a playqueue).

        Decide on direct play, direct stream, transcoding
        path to
            direct paths: file itself
            PMS URL
            Web URL
        audiostream (e.g. let user choose)
        subtitle stream (e.g. let user choose)
        Init Kodi Playback (depending on situation):
            start playback
            return PKC listitem attached to result
    """
    LOG.info('Concluding playback for playqueue position %s', pos)
    item = playqueue.items[pos]
    if item.xml is not None:
        # Got a Plex element
        api = API(item.xml)
        api.part = item.part or 0
        listitem = api.listitem(listitem=transfer.PKCListItem)
        set_playurl(api, item)
    else:
        listitem = transfer.PKCListItem()
        api = None
    if not item.file:
        LOG.info('Did not get a playurl, aborting playback silently')
        _ensure_resolve()
        return
    listitem.setPath(item.file.encode('utf-8'))
    if item.playmethod == 'DirectStream':
        listitem.setSubtitles(api.cache_external_subs())
    elif item.playmethod == 'Transcode':
        playutils.audio_subtitle_prefs(listitem)
    _set_resume(listitem, item, api)
    transfer.send(listitem)
    LOG.info('Done concluding playback')


def process_indirect(key, offset, resolve=True):
    """
    Called e.g. for Plex "Play later" - Plex items where we need to fetch an
    additional xml for the actual playurl. In the PMS metadata, indirect="1" is
    set.

    Will release default.py with setResolvedUrl

    Set resolve to False if playback should be kicked off directly, not via
    setResolvedUrl
    """
    LOG.info('process_indirect called with key: %s, offset: %s, resolve: %s',
             key, offset, resolve)
    global RESOLVE
    RESOLVE = resolve
    offset = int(v.PLEX_TO_KODI_TIMEFACTOR * float(offset)) if offset != '0' else None
    if key.startswith('http') or key.startswith('{server}'):
        xml = PF.get_playback_xml(key, app.CONN.server_name)
    elif key.startswith('/system/services'):
        xml = PF.get_playback_xml('http://node.plexapp.com:32400%s' % key,
                                  'plexapp.com',
                                  authenticate=False,
                                  token=app.ACCOUNT.plex_token)
    else:
        xml = PF.get_playback_xml('{server}%s' % key, app.CONN.server_name)
    if xml is None:
        _ensure_resolve(abort=True)
        return

    api = API(xml[0])
    listitem = api.listitem(listitem=transfer.PKCListItem)
    playqueue = PQ.get_playqueue_from_type(
        v.KODI_PLAYLIST_TYPE_FROM_PLEX_TYPE[api.plex_type])
    playqueue.clear()
    item = PL.playlist_item_from_xml(xml[0])
    item.offset = offset
    item.playmethod = 'DirectStream'

    # Need to get yet another xml to get the final playback url
    try:
        xml = PF.get_playback_xml('http://node.plexapp.com:32400%s'
                                  % xml[0][0][0].attrib['key'],
                                  'plexapp.com',
                                  authenticate=False,
                                  token=app.ACCOUNT.plex_token)
    except (TypeError, IndexError, AttributeError):
        LOG.error('XML malformed: %s', xml.attrib)
        xml = None
    if xml is None:
        _ensure_resolve(abort=True)
        return

    try:
        playurl = xml[0].attrib['key']
    except (TypeError, IndexError, AttributeError):
        LOG.error('Last xml malformed: %s', xml.attrib)
        _ensure_resolve(abort=True)
        return

    item.file = playurl
    listitem.setPath(utils.try_encode(playurl))
    playqueue.items.append(item)
    if resolve is True:
        transfer.send(listitem)
    else:
        thread = Thread(target=app.APP.player.play,
                        args={'item': utils.try_encode(playurl),
                              'listitem': listitem})
        thread.setDaemon(True)
        LOG.info('Done initializing PKC playback, starting Kodi player')
        thread.start()


def play_xml(playqueue, xml, offset=None, start_plex_id=None):
    """
    Play all items contained in the xml passed in. Called by Plex Companion.

    Either supply the ratingKey of the starting Plex element. Or set
    playqueue.selectedItemID
    """
    offset = int(offset) if offset else None
    LOG.info("play_xml called with offset %s, start_plex_id %s",
             offset, start_plex_id)
    start_item = start_plex_id if start_plex_id is not None \
        else playqueue.selectedItemID
    for startpos, video in enumerate(xml):
        api = API(video)
        if api.plex_id == start_item:
            break
    else:
        startpos = 0
    stack = _prep_playlist_stack(xml, resume=False)
    if offset:
        stack[startpos]['resume'] = True
    _process_stack(playqueue, stack)
    LOG.debug('Playqueue after play_xml update: %s', playqueue)
    thread = Thread(target=threaded_playback,
                    args=(playqueue.kodi_pl, startpos, offset))
    LOG.info('Done play_xml, starting Kodi player at position %s', startpos)
    thread.start()


def threaded_playback(kodi_playlist, startpos, offset):
    """
    Seek immediately after kicking off playback is not reliable.
    """
    app.APP.player.play(kodi_playlist, None, False, startpos)
    if offset and offset != '0':
        i = 0
        while not app.APP.is_playing or not js.get_player_ids():
            app.APP.monitor.waitForAbort(0.1)
            i += 1
            if i > 100:
                LOG.error('Could not seek to %s', offset)
                return
        js.seek_to(int(offset))
