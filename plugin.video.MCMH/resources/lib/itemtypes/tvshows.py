#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals
from logging import getLogger

from .common import ItemBase, process_path
from ..plex_api import API
from .. import plex_functions as PF, app, variables as v

LOG = getLogger('PLEX.tvshows')


class TvShowMixin(object):
    def update_userdata(self, xml_element, plex_type):
        """
        Updates the Kodi watched state of the item from PMS. Also retrieves
        Plex resume points for movies in progress.
        """
        api = API(xml_element)
        # Get key and db entry on the Kodi db side
        db_item = self.mchmdb.item_by_id(api.plex_id, plex_type)
        if not db_item:
            LOG.info('Item not yet synced: %s', xml_element.attrib)
            return False
        # Grab the user's viewcount, resume points etc. from PMS' answer
        self.kodidb.update_userrating(db_item['kodi_id'],
                                      db_item['kodi_type'],
                                      api.userrating())
        if plex_type == v.PLEX_TYPE_EPISODE:
            self.kodidb.set_resume(db_item['kodi_fileid'],
                                   api.resume_point(),
                                   api.runtime(),
                                   api.viewcount(),
                                   api.lastplayed())
            if db_item['kodi_fileid_2']:
                self.kodidb.set_resume(db_item['kodi_fileid_2'],
                                       api.resume_point(),
                                       api.runtime(),
                                       api.viewcount(),
                                       api.lastplayed())
        return True

    def remove(self, plex_id, plex_type=None):
        """
        Remove the entire TV shows object (show, season or episode) including
        all associated entries from the Kodi DB.
        """
        db_item = self.mchmdb.item_by_id(plex_id, plex_type)
        if not db_item:
            LOG.debug('Cannot delete plex_id %s - not found in DB', plex_id)
            return
        LOG.debug('Removing %s %s with kodi_id: %s',
                  db_item['plex_type'], plex_id, db_item['kodi_id'])

        # Remove the plex reference
        self.mchmdb.remove(plex_id, db_item['plex_type'])

        # EPISODE #####
        if db_item['plex_type'] == v.PLEX_TYPE_EPISODE:
            # Delete episode, verify season and tvshow
            self.remove_episode(db_item)
            # Season verification
            if (db_item['season_id'] and
                    not self.mchmdb.season_has_episodes(db_item['season_id'])):
                # No episode left for this season - so delete the season
                self.remove_season(db_item['parent_id'])
                self.mchmdb.remove(db_item['season_id'], v.PLEX_TYPE_SEASON)
            # Show verification
            if (not self.mchmdb.show_has_seasons(db_item['show_id']) and
                    not self.mchmdb.show_has_episodes(db_item['show_id'])):
                # No seasons for show left - so delete entire show
                self.remove_show(db_item['grandparent_id'])
                self.mchmdb.remove(db_item['show_id'], v.PLEX_TYPE_SHOW)
        # SEASON #####
        elif db_item['plex_type'] == v.PLEX_TYPE_SEASON:
            # Remove episodes, season, verify tvshow
            episodes = list(self.mchmdb.episode_by_season(db_item['plex_id']))
            for episode in episodes:
                self.remove_episode(episode)
                self.mchmdb.remove(episode['plex_id'], v.PLEX_TYPE_EPISODE)
            # Remove season
            self.remove_season(db_item['kodi_id'])
            # Show verification
            if (not self.mchmdb.show_has_seasons(db_item['show_id']) and
                    not self.mchmdb.show_has_episodes(db_item['show_id'])):
                # There's no other season or episode left, delete the show
                self.remove_show(db_item['parent_id'])
                self.mchmdb.remove(db_item['show_id'], v.PLEX_TYPE_SHOW)
        # TVSHOW #####
        elif db_item['plex_type'] == v.PLEX_TYPE_SHOW:
            # Remove episodes, seasons and the tvshow itself
            seasons = list(self.mchmdb.season_by_show(db_item['plex_id']))
            for season in seasons:
                self.remove_season(season['kodi_id'])
                self.mchmdb.remove(season['plex_id'], v.PLEX_TYPE_SEASON)
            episodes = list(self.mchmdb.episode_by_show(db_item['plex_id']))
            for episode in episodes:
                self.remove_episode(episode)
                self.mchmdb.remove(episode['plex_id'], v.PLEX_TYPE_EPISODE)
            self.remove_show(db_item['kodi_id'])

        LOG.debug('Deleted %s %s from all databases',
                  db_item['plex_type'], db_item['plex_id'])

    def remove_show(self, kodi_id):
        """
        Remove a TV show, and only the show, no seasons or episodes
        """
        self.kodidb.modify_genres(kodi_id, v.KODI_TYPE_SHOW)
        self.kodidb.modify_studios(kodi_id, v.KODI_TYPE_SHOW)
        self.kodidb.modify_tags(kodi_id, v.KODI_TYPE_SHOW)
        self.kodidb.delete_artwork(kodi_id, v.KODI_TYPE_SHOW)
        self.kodidb.remove_show(kodi_id)
        self.kodidb.remove_uniqueid(kodi_id, v.KODI_TYPE_SHOW)
        self.kodidb.remove_ratings(kodi_id, v.KODI_TYPE_SHOW)
        LOG.debug("Removed tvshow: %s", kodi_id)

    def remove_season(self, kodi_id):
        """
        Remove a season, and only a season, not the show or episodes
        """
        self.kodidb.delete_artwork(kodi_id, v.KODI_TYPE_SEASON)
        self.kodidb.remove_season(kodi_id)
        LOG.debug("Removed season: %s", kodi_id)

    def remove_episode(self, db_item):
        """
        Remove an episode, and episode only from the Kodi DB (not Plex DB)
        """
        self.kodidb.modify_people(db_item['kodi_id'], v.KODI_TYPE_EPISODE)
        self.kodidb.remove_file(db_item['kodi_fileid'])
        if db_item['kodi_fileid_2']:
            self.kodidb.remove_file(db_item['kodi_fileid_2'])
        self.kodidb.delete_artwork(db_item['kodi_id'], v.KODI_TYPE_EPISODE)
        self.kodidb.remove_episode(db_item['kodi_id'])
        self.kodidb.remove_uniqueid(db_item['kodi_id'], v.KODI_TYPE_EPISODE)
        self.kodidb.remove_ratings(db_item['kodi_id'], v.KODI_TYPE_EPISODE)
        LOG.debug("Removed episode: %s", db_item['kodi_id'])


class Show(TvShowMixin, ItemBase):
    """
    For Plex library-type TV shows
    """
    def add_update(self, xml, section_name=None, section_id=None,
                   children=None):
        """
        Process a single show
        """
        api = API(xml)
        if not self.sync_this_item(api.library_section_id()):
            LOG.debug('Skipping sync of %s %s: %s - section %s not synched to '
                      'Kodi', api.plex_type, api.plex_id, api.title(),
                      api.library_section_id())
            return
        plex_id = api.plex_id
        show = self.mchmdb.show(plex_id)
        if not show:
            update_item = False
            kodi_id = self.kodidb.new_show_id()
        else:
            update_item = True
            kodi_id = show['kodi_id']
            kodi_pathid = show['kodi_pathid']

        # GET THE FILE AND PATH #####
        if app.SYNC.direct_paths:
            # Direct paths is set the Kodi way
            playurl = api.validate_playurl(api.tv_show_path(),
                                           api.plex_type,
                                           folder=True)
            if playurl is None:
                return
            path, toplevelpath = process_path(playurl)
            toppathid = self.kodidb.add_path(toplevelpath,
                                             content='tvshows',
                                             scraper='metadata.local')
        else:
            # Set plugin path
            toplevelpath = "plugin://%s.tvshows/" % v.ADDON_ID
            path = "%s%s/" % (toplevelpath, plex_id)
            # Do NOT set a parent id because addon-path cannot be "stacked"
            toppathid = None

        kodi_pathid = self.kodidb.add_path(path,
                                           date_added=api.date_created(),
                                           id_parent_path=toppathid)
        # UPDATE THE TVSHOW #####
        if update_item:
            LOG.info("UPDATE tvshow plex_id: %s - %s", plex_id, api.title())
            # update new ratings Kodi 17
            rating_id = self.kodidb.get_ratingid(kodi_id, v.KODI_TYPE_SHOW)
            self.kodidb.update_ratings(kodi_id,
                                       v.KODI_TYPE_SHOW,
                                       "default",
                                       api.rating(),
                                       api.votecount(),
                                       rating_id)
            if api.provider('tvdb') is not None:
                uniqueid = self.kodidb.get_uniqueid(kodi_id,
                                                    v.KODI_TYPE_SHOW)
                self.kodidb.update_uniqueid(kodi_id,
                                            v.KODI_TYPE_SHOW,
                                            api.provider('tvdb'),
                                            'tvdb',
                                            uniqueid)
            else:
                self.kodidb.remove_uniqueid(kodi_id, v.KODI_TYPE_SHOW)
                uniqueid = -1
            self.kodidb.modify_people(kodi_id,
                                      v.KODI_TYPE_SHOW,
                                      api.people())
            if app.SYNC.artwork:
                self.kodidb.modify_artwork(api.artwork(),
                                           kodi_id,
                                           v.KODI_TYPE_SHOW)
            # Update the tvshow entry
            self.kodidb.update_show(api.title(),
                                    api.plot(),
                                    rating_id,
                                    api.premiere_date(),
                                    api.list_to_string(api.genres()),
                                    api.title(),
                                    uniqueid,
                                    api.content_rating(),
                                    api.list_to_string(api.studios()),
                                    api.sorttitle(),
                                    kodi_id)
        # OR ADD THE TVSHOW #####
        else:
            LOG.info("ADD tvshow plex_id: %s - %s", plex_id, api.title())
            # Link the path
            self.kodidb.add_showlinkpath(kodi_id, kodi_pathid)
            rating_id = self.kodidb.get_ratingid(kodi_id, v.KODI_TYPE_SHOW)
            self.kodidb.add_ratings(rating_id,
                                    kodi_id,
                                    v.KODI_TYPE_SHOW,
                                    "default",
                                    api.rating(),
                                    api.votecount())
            if api.provider('tvdb'):
                uniqueid = self.kodidb.add_uniqueid_id()
                self.kodidb.add_uniqueid(uniqueid,
                                         kodi_id,
                                         v.KODI_TYPE_SHOW,
                                         api.provider('tvdb'),
                                         'tvdb')
            else:
                uniqueid = -1
            self.kodidb.add_people(kodi_id,
                                   v.KODI_TYPE_SHOW,
                                   api.people())
            if app.SYNC.artwork:
                self.kodidb.add_artwork(api.artwork(),
                                        kodi_id,
                                        v.KODI_TYPE_SHOW)
            # Create the tvshow entry
            self.kodidb.add_show(kodi_id,
                                 api.title(),
                                 api.plot(),
                                 rating_id,
                                 api.premiere_date(),
                                 api.list_to_string(api.genres()),
                                 api.title(),
                                 uniqueid,
                                 api.content_rating(),
                                 api.list_to_string(api.studios()),
                                 api.sorttitle())
        self.kodidb.modify_genres(kodi_id, v.KODI_TYPE_SHOW, api.genres())
        # Process studios
        self.kodidb.modify_studios(kodi_id, v.KODI_TYPE_SHOW, api.studios())
        # Process tags: view, PMS collection tags
        tags = [section_name]
        tags.extend([i for _, i in api.collections()])
        self.kodidb.modify_tags(kodi_id, v.KODI_TYPE_SHOW, tags)
        self.mchmdb.add_show(plex_id=plex_id,
                             checksum=api.checksum(),
                             section_id=section_id,
                             kodi_id=kodi_id,
                             kodi_pathid=kodi_pathid,
                             last_sync=self.last_sync)


class Season(TvShowMixin, ItemBase):
    def add_update(self, xml, section_name=None, section_id=None,
                   children=None):
        """
        Process a single season of a certain tv show
        """
        api = API(xml)
        if not self.sync_this_item(api.library_section_id()):
            LOG.debug('Skipping sync of %s %s: %s - section %s not synched to '
                      'Kodi', api.plex_type, api.plex_id, api.title(),
                      api.library_section_id())
            return
        plex_id = api.plex_id
        season = self.mchmdb.season(plex_id)
        if not season:
            update_item = False
        else:
            update_item = True
        show_id = api.parent_id()
        show = self.mchmdb.show(show_id)
        if not show:
            LOG.warn('Parent TV show %s not found in DB, adding it', show_id)
            show_xml = PF.GetPlexMetadata(show_id)
            try:
                show_xml[0].attrib
            except (TypeError, IndexError, AttributeError):
                LOG.error("Parent tvshow %s xml download failed", show_id)
                return False
            Show(self.last_sync,
                 mchmdb=self.mchmdb,
                 kodidb=self.kodidb).add_update(show_xml[0],
                                                section_name,
                                                section_id)
            show = self.mchmdb.show(show_id)
            if not show:
                LOG.error('Still could not find parent tv show %s', show_id)
                return
        parent_id = show['kodi_id']
        if app.SYNC.artwork:
            parent_artwork = api.artwork(kodi_id=parent_id,
                                         kodi_type=v.KODI_TYPE_SHOW)
            artwork = api.artwork()
            # Remove all artwork that is identical for the season's show
            for key in parent_artwork:
                if key in artwork and artwork[key] == parent_artwork[key]:
                    del artwork[key]
        if update_item:
            LOG.info('UPDATE season plex_id %s - %s', plex_id, api.title())
            kodi_id = season['kodi_id']
            if app.SYNC.artwork:
                self.kodidb.modify_artwork(artwork,
                                           kodi_id,
                                           v.KODI_TYPE_SEASON)
        else:
            LOG.info('ADD season plex_id %s - %s', plex_id, api.title())
            kodi_id = self.kodidb.add_season(parent_id, api.index())
            if app.SYNC.artwork:
                self.kodidb.add_artwork(artwork,
                                        kodi_id,
                                        v.KODI_TYPE_SEASON)
        self.mchmdb.add_season(plex_id=plex_id,
                               checksum=api.checksum(),
                               section_id=section_id,
                               show_id=show_id,
                               parent_id=parent_id,
                               kodi_id=kodi_id,
                               last_sync=self.last_sync)


class Episode(TvShowMixin, ItemBase):
    def add_update(self, xml, section_name=None, section_id=None,
                   children=None):
        """
        Process single episode
        """
        api = API(xml)
        if not self.sync_this_item(api.library_section_id()):
            LOG.debug('Skipping sync of %s %s: %s - section %s not synched to '
                      'Kodi', api.plex_type, api.plex_id, api.title(),
                      api.library_section_id())
            return
        plex_id = api.plex_id
        episode = self.mchmdb.episode(plex_id)
        if not episode:
            update_item = False
            kodi_id = self.kodidb.new_episode_id()
        else:
            update_item = True
            kodi_id = episode['kodi_id']
            old_kodi_fileid = episode['kodi_fileid']
            old_kodi_fileid_2 = episode['kodi_fileid_2']
            kodi_pathid = episode['kodi_pathid']

        airs_before_season = "-1"
        airs_before_episode = "-1"

        # The grandparent TV show
        show = self.mchmdb.show(api.show_id())
        if not show:
            LOG.warn('Grandparent TV show %s not found in DB, adding it', api.show_id())
            show_xml = PF.GetPlexMetadata(api.show_id())
            try:
                show_xml[0].attrib
            except (TypeError, IndexError, AttributeError):
                LOG.error("Grandparent tvshow %s xml download failed", api.show_id())
                return False
            Show(self.last_sync,
                 mchmdb=self.mchmdb,
                 kodidb=self.kodidb).add_update(show_xml[0],
                                                section_name,
                                                section_id)
            show = self.mchmdb.show(api.show_id())
            if not show:
                LOG.error('Still could not find grandparent tv show %s', api.show_id())
                return
        grandparent_id = show['kodi_id']

        # The parent Season
        season = self.mchmdb.season(api.season_id())
        if not season and api.season_id():
            LOG.warn('Parent season %s not found in DB, adding it', api.season_id())
            season_xml = PF.GetPlexMetadata(api.season_id())
            try:
                season_xml[0].attrib
            except (TypeError, IndexError, AttributeError):
                LOG.error("Parent season %s xml download failed", api.season_id())
                return False
            Season(self.last_sync,
                   mchmdb=self.mchmdb,
                   kodidb=self.kodidb).add_update(season_xml[0],
                                                  section_name,
                                                  section_id)
            season = self.mchmdb.season(api.season_id())
            if not season:
                LOG.error('Still could not find parent season %s', api.season_id())
                return
        parent_id = season['kodi_id'] if season else None

        # GET THE FILE AND PATH #####
        do_indirect = not app.SYNC.direct_paths
        if app.SYNC.direct_paths:
            playurl = api.file_path(force_first_media=True)
            if playurl is None:
                do_indirect = True
            else:
                playurl = api.validate_playurl(playurl, v.PLEX_TYPE_EPISODE)
                if "\\" in playurl:
                    # Local path
                    filename = playurl.rsplit("\\", 1)[1]
                else:
                    # Network share
                    filename = playurl.rsplit("/", 1)[1]
                path = playurl.replace(filename, "")
                parent_path_id = self.kodidb.parent_path_id(path)
                kodi_pathid = self.kodidb.add_path(path,
                                                   id_parent_path=parent_path_id)
        if do_indirect:
            # Set plugin path - do NOT use "intermediate" paths for the show
            # as with direct paths!
            filename = api.file_name(force_first_media=True)
            path = 'plugin://%s.tvshows/%s/' % (v.ADDON_ID, api.show_id())
            filename = ('%s?plex_id=%s&plex_type=%s&mode=play&filename=%s'
                        % (path, plex_id, v.PLEX_TYPE_EPISODE, filename))
            playurl = filename
            # Root path tvshows/ already saved in Kodi DB
            kodi_pathid = self.kodidb.add_path(path)
            if not app.SYNC.direct_paths:
                # need to set a 2nd file entry for a path without plex show id
                # This fixes e.g. context menu and widgets working as they
                # should
                # A dirty hack, really
                path_2 = 'plugin://%s.tvshows/' % v.ADDON_ID
                # filename_2 is exactly the same as filename
                # so WITH plex show id!
                kodi_pathid_2 = self.kodidb.add_path(path_2)

        # UPDATE THE EPISODE #####
        if update_item:
            LOG.info("UPDATE episode plex_id: %s - %s", plex_id, api.title())
            kodi_fileid = self.kodidb.modify_file(filename,
                                                  kodi_pathid,
                                                  api.date_created())
            if not app.SYNC.direct_paths:
                kodi_fileid_2 = self.kodidb.modify_file(filename,
                                                        kodi_pathid_2,
                                                        api.date_created())
            else:
                kodi_fileid_2 = None

            if kodi_fileid != old_kodi_fileid:
                self.kodidb.remove_file(old_kodi_fileid)
                if not app.SYNC.direct_paths:
                    self.kodidb.remove_file(old_kodi_fileid_2)
            ratingid = self.kodidb.get_ratingid(kodi_id,
                                                v.KODI_TYPE_EPISODE)
            self.kodidb.update_ratings(kodi_id,
                                       v.KODI_TYPE_EPISODE,
                                       "default",
                                       api.rating(),
                                       api.votecount(),
                                       ratingid)
            if api.provider('tvdb'):
                uniqueid = self.kodidb.get_uniqueid(kodi_id,
                                                    v.KODI_TYPE_EPISODE)
                self.kodidb.update_uniqueid(kodi_id,
                                            v.KODI_TYPE_EPISODE,
                                            api.provider('tvdb'),
                                            "tvdb",
                                            uniqueid)
            else:
                self.kodidb.remove_uniqueid(kodi_id, v.KODI_TYPE_EPISODE)
                uniqueid = -1
            self.kodidb.modify_people(kodi_id,
                                      v.KODI_TYPE_EPISODE,
                                      api.people())
            if app.SYNC.artwork:
                self.kodidb.modify_artwork(api.artwork(),
                                           kodi_id,
                                           v.KODI_TYPE_EPISODE)
            self.kodidb.update_episode(api.title(),
                                       api.plot(),
                                       ratingid,
                                       api.list_to_string(api.writers()),
                                       api.premiere_date(),
                                       api.runtime(),
                                       api.list_to_string(api.directors()),
                                       api.season_number(),
                                       api.index(),
                                       api.title(),
                                       airs_before_season,
                                       airs_before_episode,
                                       playurl,
                                       kodi_pathid,
                                       kodi_fileid,  # and NOT kodi_fileid_2
                                       parent_id,
                                       api.userrating(),
                                       kodi_id)
            self.kodidb.set_resume(kodi_fileid,
                                   api.resume_point(),
                                   api.runtime(),
                                   api.viewcount(),
                                   api.lastplayed())
            if not app.SYNC.direct_paths:
                self.kodidb.set_resume(kodi_fileid_2,
                                       api.resume_point(),
                                       api.runtime(),
                                       api.viewcount(),
                                       api.lastplayed())
            self.mchmdb.add_episode(plex_id=plex_id,
                                    checksum=api.checksum(),
                                    section_id=section_id,
                                    show_id=api.show_id(),
                                    grandparent_id=grandparent_id,
                                    season_id=api.season_id(),
                                    parent_id=parent_id,
                                    kodi_id=kodi_id,
                                    kodi_fileid=kodi_fileid,
                                    kodi_fileid_2=kodi_fileid_2,
                                    kodi_pathid=kodi_pathid,
                                    last_sync=self.last_sync)
        # OR ADD THE EPISODE #####
        else:
            LOG.info("ADD episode plex_id: %s - %s", plex_id, api.title())
            kodi_fileid = self.kodidb.add_file(filename,
                                               kodi_pathid,
                                               api.date_created())
            if not app.SYNC.direct_paths:
                kodi_fileid_2 = self.kodidb.add_file(filename,
                                                     kodi_pathid_2,
                                                     api.date_created())
            else:
                kodi_fileid_2 = None

            rating_id = self.kodidb.add_ratingid()
            self.kodidb.add_ratings(rating_id,
                                    kodi_id,
                                    v.KODI_TYPE_EPISODE,
                                    "default",
                                    api.rating(),
                                    api.votecount())
            if api.provider('tvdb'):
                uniqueid = self.kodidb.add_uniqueid_id()
                self.kodidb.add_uniqueid(uniqueid,
                                         kodi_id,
                                         v.KODI_TYPE_EPISODE,
                                         api.provider('tvdb'),
                                         "tvdb")
            self.kodidb.add_people(kodi_id,
                                   v.KODI_TYPE_EPISODE,
                                   api.people())
            if app.SYNC.artwork:
                self.kodidb.add_artwork(api.artwork(),
                                        kodi_id,
                                        v.KODI_TYPE_EPISODE)
            self.kodidb.add_episode(kodi_id,
                                    kodi_fileid,  # and NOT kodi_fileid_2
                                    api.title(),
                                    api.plot(),
                                    rating_id,
                                    api.list_to_string(api.writers()),
                                    api.premiere_date(),
                                    api.runtime(),
                                    api.list_to_string(api.directors()),
                                    api.season_number(),
                                    api.index(),
                                    api.title(),
                                    grandparent_id,
                                    airs_before_season,
                                    airs_before_episode,
                                    playurl,
                                    kodi_pathid,
                                    parent_id,
                                    api.userrating())
            self.kodidb.set_resume(kodi_fileid,
                                   api.resume_point(),
                                   api.runtime(),
                                   api.viewcount(),
                                   api.lastplayed())
            if not app.SYNC.direct_paths:
                self.kodidb.set_resume(kodi_fileid_2,
                                       api.resume_point(),
                                       api.runtime(),
                                       api.viewcount(),
                                       api.lastplayed())
            self.mchmdb.add_episode(plex_id=plex_id,
                                    checksum=api.checksum(),
                                    section_id=section_id,
                                    show_id=api.show_id(),
                                    grandparent_id=grandparent_id,
                                    season_id=api.season_id(),
                                    parent_id=parent_id,
                                    kodi_id=kodi_id,
                                    kodi_fileid=kodi_fileid,
                                    kodi_fileid_2=kodi_fileid_2,
                                    kodi_pathid=kodi_pathid,
                                    last_sync=self.last_sync)

        self.kodidb.modify_streams(kodi_fileid,  # and NOT kodi_fileid_2
                                   api.mediastreams(),
                                   api.runtime())
