# -*- coding: utf-8 -*-

'''
    Still i Rise Add-on

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''


import os,sys,urlparse

from resources.lib.modules import control
from resources.lib.modules import trakt
from resources.lib.modules import cache

sysaddon = sys.argv[0] ; syshandle = int(sys.argv[1]) ; control.moderator()

artPath = control.artPath() ; addonFanart = control.addonFanart()

imdbCredentials = False if control.setting('imdb.user') == '' else True

traktCredentials = trakt.getTraktCredentialsInfo()

traktIndicators = trakt.getTraktIndicatorsInfo()

queueMenu = control.lang(32065).encode('utf-8')


class navigator:
    def root(self):
        self.addDirectoryItem(32001, 'hddmovieovieNavigator', 'hdd.png', 'DefaultMovies.png')
        self.addDirectoryItem(32002, 'hddtvNavigator', 'hdd.png', 'DefaultTVShows.png')
        #self.addDirectoryItem('NightMare Reborn', 'nightNavigator', 'hdd.png', 'DefaultMovies.png')
        #if not control.setting('lists.widget') == '0':
            #self.addDirectoryItem(32003, 'myRENAMEmovieNavigator', 'hdd.png', 'DefaultVideoPlaylists.png')
            #self.addDirectoryItem(32004, 'mytvNavigator', 'hdd.png', 'DefaultVideoPlaylists.png')

        #if not control.setting('movie.widget') == '0':
            #self.addDirectoryItem(32005, 'movieWidget', 'hdd.png', 'DefaultRecentlyAddedMovies.png')

        #if (traktIndicators == True and not control.setting('tv.widget.alt') == '0') or (traktIndicators == False and not control.setting('tv.widget') == '0'):
            #self.addDirectoryItem(32006, 'tvWidget', 'hdd.png', 'DefaultRecentlyAddedEpisodes.png')

        #self.addDirectoryItem(32007, 'channels', 'hdd.png', 'hdd.png')

        #self.addDirectoryItem(32008, 'toolNavigator', 'hdd.png', 'DefaultAddonProgram.png')

        #downloads = True if control.setting('downloads') == 'true' and (len(control.listDir(control.setting('movie.download.path'))[0]) > 0 or len(control.listDir(control.setting('tv.download.path'))[0]) > 0) else False
        #if downloads == True:
            #self.addDirectoryItem(32009, 'downloadNavigator', 'hdd.png', 'DefaultFolder.png')

        #self.addDirectoryItem(32010, 'searchNavigator', 'hdd.png', 'DefaultFolder.png')

        self.endDirectory()


    def movies(self, lite=False):
        self.addDirectoryItem(32011, 'hddmovieGenres', 'hdd.png', 'DefaultMovies.png')
        self.addDirectoryItem(32012, 'hddmovieYears', 'hdd.png', 'DefaultMovies.png')
        #self.addDirectoryItem(32013, 'hddmoviePersons', 'hdd.png', 'DefaultMovies.png')
        self.addDirectoryItem(32014, 'hddmovieLanguages', 'hdd.png', 'DefaultMovies.png')
        self.addDirectoryItem(32015, 'hddmovieCertificates', 'hdd.png', 'DefaultMovies.png')
        self.addDirectoryItem(32017, 'hmmm&url=trending', 'hdd.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem(32018, 'hmmm&url=popular', 'hdd.png', 'DefaultMovies.png')
        self.addDirectoryItem(32019, 'hmmm&url=views', 'hdd.png', 'DefaultMovies.png')
        self.addDirectoryItem(32020, 'hmmm&url=boxoffice', 'hdd.png', 'DefaultMovies.png')
        self.addDirectoryItem(32021, 'hmmm&url=oscars', 'hdd.png', 'DefaultMovies.png')
        self.addDirectoryItem(32022, 'hmmm&url=theaters', 'hdd.png', 'DefaultRecentlyAddedMovies.png')
        #self.addDirectoryItem(32005, 'movieWidget', 'hdd.png', 'DefaultRecentlyAddedMovies.png')

        #if lite == False:
            #if not control.setting('lists.widget') == '0':
                #self.addDirectoryItem(32003, 'mymovieliteNavigator', 'hdd.png', 'DefaultVideoPlaylists.png')

            #self.addDirectoryItem(32028, 'moviePerson', 'hdd.png', 'DefaultMovies.png')
            #self.addDirectoryItem(32010, 'movieSearch', 'hdd.png', 'DefaultMovies.png')

        self.endDirectory()
    def certificationsnew(self):
        self.addDirectoryItem('G', 'hmmm&url=certificationmg', 'hdd.png', 'DefaultMovies.png')
        self.addDirectoryItem('PG', 'hmmm&url=certificationmpg', 'hdd.png', 'DefaultMovies.png')
        self.addDirectoryItem('PG-13', 'hmmm&url=certificationmpgt', 'hdd.png', 'DefaultMovies.png')
        self.addDirectoryItem('R', 'hmmm&url=certificationmr', 'hdd.png', 'DefaultMovies.png')
        self.addDirectoryItem('NC-17', 'hmmm&url=certificationncseven', 'hdd.png', 'DefaultRecentlyAddedMovies.png')

        self.endDirectory()

    def mymovies(self, lite=False):
        self.accountCheck()

        if traktCredentials == True and imdbCredentials == True:
            self.addDirectoryItem(32032, 'hmmm&url=traktcollection', 'hdd.png', 'DefaultMovies.png', queue=True, context=(32551, 'moviesToLibrary&url=traktcollection'))
            self.addDirectoryItem(32033, 'hmmm&url=traktwatchlist', 'hdd.png', 'DefaultMovies.png', queue=True, context=(32551, 'moviesToLibrary&url=traktwatchlist'))
            self.addDirectoryItem(32034, 'hmmm&url=imdbwatchlist', 'hdd.png', 'DefaultMovies.png', queue=True)

        elif traktCredentials == True:
            self.addDirectoryItem(32032, 'hmmm&url=traktcollection', 'hdd.png', 'DefaultMovies.png', queue=True, context=(32551, 'moviesToLibrary&url=traktcollection'))
            self.addDirectoryItem(32033, 'hmmm&url=traktwatchlist', 'hdd.png', 'DefaultMovies.png', queue=True, context=(32551, 'moviesToLibrary&url=traktwatchlist'))

        elif imdbCredentials == True:
            self.addDirectoryItem(32032, 'hmmm&url=imdbwatchlist', 'hdd.png', 'DefaultMovies.png', queue=True)
            self.addDirectoryItem(32033, 'hmmm&url=imdbwatchlist2', 'hdd.png', 'DefaultMovies.png', queue=True)

        if traktCredentials == True:
            self.addDirectoryItem(32035, 'hmmm&url=traktfeatured', 'hdd.png', 'DefaultMovies.png', queue=True)

        elif imdbCredentials == True:
            self.addDirectoryItem(32035, 'hmmm&url=featured', 'hdd.png', 'DefaultMovies.png', queue=True)

        if traktIndicators == True:
            self.addDirectoryItem(32036, 'hmmm&url=trakthistory', 'hdd.png', 'DefaultMovies.png', queue=True)

        self.addDirectoryItem(32039, 'movieUserlists', 'hdd.png', 'DefaultMovies.png')

        if lite == False:
            self.addDirectoryItem(32031, 'movieliteNavigator', 'hdd.png', 'DefaultMovies.png')
            self.addDirectoryItem(32028, 'moviePerson', 'hdd.png', 'DefaultMovies.png')
            self.addDirectoryItem(32010, 'movieSearch', 'hdd.png', 'DefaultMovies.png')

        self.endDirectory()


    def tvshows(self, lite=False):
        self.addDirectoryItem(32011, 'hddtvGenres', 'hdd.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32016, 'hddtvNetworks', 'hdd.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32014, 'hddtvLanguages', 'lpng', 'DefaultTVShows.png')
        self.addDirectoryItem(32015, 'hddtvCertificates', 'hdd.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32012, 'hddtvYears', 'years.png', 'hdd.png')
        self.addDirectoryItem(32017, 'hmmtv&url=trending', 'hdd.png', 'DefaultRecentlyAddedEpisodes.png')
        self.addDirectoryItem(32018, 'hmmtv&url=popular', 'hdd.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32023, 'hmmtv&url=rating', 'hdd.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32019, 'hmmtv&url=views', 'hdd.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32024, 'hmmtv&url=airing', 'hdd.png', 'DefaultTVShows.png')
        #self.addDirectoryItem(32025, 'hmmtv&url=active', 'hdd.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32026, 'hmmtv&url=premiere', 'hdd.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32006, 'calendar&url=added', 'hdd.png', 'DefaultRecentlyAddedEpisodes.png', queue=True)
        self.addDirectoryItem(32027, 'calendars', 'hdd.png', 'DefaultRecentlyAddedEpisodes.png')

        #if lite == False:
            #if not control.setting('lists.widget') == '0':
                #self.addDirectoryItem(32004, 'mytvliteNavigator', 'hdd.png', 'DefaultVideoPlaylists.png')

            #self.addDirectoryItem(32028, 'tvPerson', 'hdd.png', 'DefaultTVShows.png')
            #self.addDirectoryItem(32010, 'tvSearch', 'hdd.png', 'DefaultTVShows.png')

        self.endDirectory()

    def certificationsnewtv(self):
        self.addDirectoryItem('TV-PG', 'hmmtv&url=certificationtvpg', 'hdd.png', 'DefaultMovies.png')
        self.addDirectoryItem('TV-14', 'hmmtv&url=certificationtvpgt', 'hdd.png', 'DefaultMovies.png')
        self.addDirectoryItem('TV-MA', 'hmmtv&url=certificationtvr', 'hdd.png', 'DefaultMovies.png')
        self.endDirectory()
	
    def mytvshows(self, lite=False):
        self.accountCheck()

        if traktCredentials == True and imdbCredentials == True:
            self.addDirectoryItem(32032, 'hmmtv&url=traktcollection', 'hdd.png', 'DefaultTVShows.png', context=(32551, 'tvshowsToLibrary&url=traktcollection'))
            self.addDirectoryItem(32033, 'hmmtv&url=traktwatchlist', 'hdd.png', 'DefaultTVShows.png', context=(32551, 'tvshowsToLibrary&url=traktwatchlist'))
            self.addDirectoryItem(32034, 'hmmtv&url=imdbwatchlist', 'hdd.png', 'DefaultTVShows.png')

        elif traktCredentials == True:
            self.addDirectoryItem(32032, 'hmmtv&url=traktcollection', 'hdd.png', 'DefaultTVShows.png', context=(32551, 'tvshowsToLibrary&url=traktcollection'))
            self.addDirectoryItem(32033, 'hmmtv&url=traktwatchlist', 'hdd.png', 'DefaultTVShows.png', context=(32551, 'tvshowsToLibrary&url=traktwatchlist'))

        elif imdbCredentials == True:
            self.addDirectoryItem(32032, 'hmmtv&url=imdbwatchlist', 'hdd.png', 'DefaultTVShows.png')
            self.addDirectoryItem(32033, 'hmmtv&url=imdbwatchlist2', 'hdd.png', 'DefaultTVShows.png')

        if traktCredentials == True:
            self.addDirectoryItem(32035, 'hmmtv&url=traktfeatured', 'hdd.png', 'DefaultTVShows.png')

        elif imdbCredentials == True:
            self.addDirectoryItem(32035, 'hmmtv&url=trending', 'hdd.png', 'DefaultMovies.png', queue=True)

        if traktIndicators == True:
            self.addDirectoryItem(32036, 'calendar&url=trakthistory', 'hdd.png', 'DefaultTVShows.png', queue=True)
            self.addDirectoryItem(32037, 'calendar&url=progress', 'hdd.png', 'DefaultRecentlyAddedEpisodes.png', queue=True)
            self.addDirectoryItem(32038, 'calendar&url=mycalendar', 'hdd.png', 'DefaultRecentlyAddedEpisodes.png', queue=True)

        self.addDirectoryItem(32040, 'tvUserlists', 'hdd.png', 'DefaultTVShows.png')

        if traktCredentials == True:
            self.addDirectoryItem(32041, 'episodeUserlists', 'hdd.png', 'DefaultTVShows.png')

        if lite == False:
            self.addDirectoryItem(32031, 'tvliteNavigator', 'hdd.png', 'DefaultTVShows.png')
            self.addDirectoryItem(32028, 'tvPerson', 'hdd.png', 'DefaultTVShows.png')
            self.addDirectoryItem(32010, 'tvSearch', 'hdd.png', 'DefaultTVShows.png')

        self.endDirectory()


    def tools(self):
        self.addDirectoryItem(32043, 'openSettings&query=0.0', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32044, 'openSettings&query=3.1', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32045, 'openSettings&query=1.0', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32046, 'openSettings&query=6.0', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32047, 'openSettings&query=2.0', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32556, 'libraryNavigator', 'hdd.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32048, 'openSettings&query=5.0', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32049, 'viewsNavigator', 'hdd.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32050, 'clearSources', 'hdd.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32604, 'clearCacheSearch', 'hdd.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32052, 'clearCache', 'hdd.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32073, 'authTrakt', 'hdd.png', 'DefaultAddonProgram.png')

        self.endDirectory()

    def library(self):
        self.addDirectoryItem(32557, 'openSettings&query=4.0', 'hdd.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32558, 'updateLibrary&query=tool', 'hdd.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32559, control.setting('library.movie'), 'hdd.png', 'DefaultMovies.png', isAction=False)
        self.addDirectoryItem(32560, control.setting('library.tv'), 'hdd.png', 'DefaultTVShows.png', isAction=False)

        if trakt.getTraktCredentialsInfo():
            self.addDirectoryItem(32561, 'moviesToLibrary&url=traktcollection', 'hdd.png', 'DefaultMovies.png')
            self.addDirectoryItem(32562, 'moviesToLibrary&url=traktwatchlist', 'hdd.png', 'DefaultMovies.png')
            self.addDirectoryItem(32563, 'tvshowsToLibrary&url=traktcollection', 'hdd.png', 'DefaultTVShows.png')
            self.addDirectoryItem(32564, 'tvshowsToLibrary&url=traktwatchlist', 'hdd.png', 'DefaultTVShows.png')

        self.endDirectory()

    def downloads(self):
        movie_downloads = control.setting('movie.download.path')
        tv_downloads = control.setting('tv.download.path')

        if len(control.listDir(movie_downloads)[0]) > 0:
            self.addDirectoryItem(32001, movie_downloads, 'hdd.png', 'DefaultMovies.png', isAction=False)
        if len(control.listDir(tv_downloads)[0]) > 0:
            self.addDirectoryItem(32002, tv_downloads, 'hdd.png', 'DefaultTVShows.png', isAction=False)

        self.endDirectory()


    def search(self):
        self.addDirectoryItem(32001, 'movieSearch', 'hdd.png', 'DefaultMovies.png')
        self.addDirectoryItem(32002, 'tvSearch', 'hdd.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32029, 'moviePerson', 'hdd.png', 'DefaultMovies.png')
        self.addDirectoryItem(32030, 'tvPerson', 'hdd.png', 'DefaultTVShows.png')

        self.endDirectory()

    def views(self):
        try:
            control.idle()

            items = [ (control.lang(32001).encode('utf-8'), 'movies'), (control.lang(32002).encode('utf-8'), 'tvshows'), (control.lang(32054).encode('utf-8'), 'seasons'), (control.lang(32038).encode('utf-8'), 'episodes') ]

            select = control.selectDialog([i[0] for i in items], control.lang(32049).encode('utf-8'))

            if select == -1: return

            content = items[select][1]

            title = control.lang(32059).encode('utf-8')
            url = '%s?action=addView&content=%s' % (sys.argv[0], content)

            poster, banner, fanart = control.addonPoster(), control.addonBanner(), control.addonFanart()

            item = control.item(label=title)
            item.setInfo(type='Video', infoLabels = {'title': title})
            item.setArt({'icon': poster, 'thumb': poster, 'poster': poster, 'banner': banner})
            item.setProperty('Fanart_Image', fanart)

            control.addItem(handle=int(sys.argv[1]), url=url, listitem=item, isFolder=False)
            control.content(int(sys.argv[1]), content)
            control.directory(int(sys.argv[1]), cacheToDisc=True)

            from resources.lib.modules import views
            views.setView(content, {})
        except:
            return


    def accountCheck(self):
        if traktCredentials == False and imdbCredentials == False:
            control.idle()
            control.infoDialog(control.lang(32042).encode('utf-8'), sound=True, icon='WARNING')
            sys.exit()


    def infoCheck(self, version):
        try:
            control.infoDialog('', control.lang(32074).encode('utf-8'), time=5000, sound=False)
            return '1'
        except:
            return '1'


    def clearCache(self):
        control.idle()
        yes = control.yesnoDialog(control.lang(32056).encode('utf-8'), '', '')
        if not yes: return
        from resources.lib.modules import cache
        cache.cache_clear()
        control.infoDialog(control.lang(32057).encode('utf-8'), sound=True, icon='INFO')

    def clearCacheMeta(self):
        control.idle()
        yes = control.yesnoDialog(control.lang(32056).encode('utf-8'), '', '')
        if not yes: return
        from resources.lib.modules import cache
        cache.cache_clear_meta()
        control.infoDialog(control.lang(32057).encode('utf-8'), sound=True, icon='INFO')

    def clearCacheProviders(self):
        control.idle()
        yes = control.yesnoDialog(control.lang(32056).encode('utf-8'), '', '')
        if not yes: return
        from resources.lib.modules import cache
        cache.cache_clear_providers()
        control.infoDialog(control.lang(32057).encode('utf-8'), sound=True, icon='INFO')

    def clearCacheSearch(self):
        control.idle()
        yes = control.yesnoDialog(control.lang(32056).encode('utf-8'), '', '')
        if not yes: return
        from resources.lib.modules import cache
        cache.cache_clear_search()
        control.infoDialog(control.lang(32057).encode('utf-8'), sound=True, icon='INFO')

    def clearCacheAll(self):
        control.idle()
        yes = control.yesnoDialog(control.lang(32056).encode('utf-8'), '', '')
        if not yes: return
        from resources.lib.modules import cache
        cache.cache_clear_all()
        control.infoDialog(control.lang(32057).encode('utf-8'), sound=True, icon='INFO')

    def addDirectoryItem(self, name, query, thumb, icon, context=None, queue=False, isAction=True, isFolder=True):
        try: name = control.lang(name).encode('utf-8')
        except: pass
        url = '%s?action=%s' % (sysaddon, query) if isAction == True else query
        thumb = os.path.join(artPath, thumb) if not artPath == None else icon
        cm = []
        if queue == True: cm.append((queueMenu, 'RunPlugin(%s?action=queueItem)' % sysaddon))
        if not context == None: cm.append((control.lang(context[0]).encode('utf-8'), 'RunPlugin(%s?action=%s)' % (sysaddon, context[1])))
        item = control.item(label=name)
        item.addContextMenuItems(cm)
        item.setArt({'icon': thumb, 'thumb': thumb})
        if not addonFanart == None: item.setProperty('Fanart_Image', addonFanart)
        control.addItem(handle=syshandle, url=url, listitem=item, isFolder=isFolder)

    def endDirectory(self):
        control.content(syshandle, 'addons')
        control.directory(syshandle, cacheToDisc=True)
