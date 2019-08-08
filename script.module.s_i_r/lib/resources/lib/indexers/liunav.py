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
        self.addDirectoryItem(32001, 'liumovieNavigator', 'liu.png', 'DefaultMovies.png')
        self.addDirectoryItem(32002, 'liutvNavigator', 'liu.png', 'DefaultTVShows.png')
        #self.addDirectoryItem('liu Reborn', 'nightNavigator', 'liu.png', 'DefaultMovies.png')
        #if not control.setting('lists.widget') == '0':
            #self.addDirectoryItem(32003, 'myRENAMEmovieNavigator', 'liu.png', 'DefaultVideoPlaylists.png')
            #self.addDirectoryItem(32004, 'mytvNavigator', 'liu.png', 'DefaultVideoPlaylists.png')

        #if not control.setting('movie.widget') == '0':
            #self.addDirectoryItem(32005, 'movieWidget', 'liu.png', 'DefaultRecentlyAddedMovies.png')

        #if (traktIndicators == True and not control.setting('tv.widget.alt') == '0') or (traktIndicators == False and not control.setting('tv.widget') == '0'):
            #self.addDirectoryItem(32006, 'tvWidget', 'liu.png', 'DefaultRecentlyAddedEpisodes.png')

        #self.addDirectoryItem(32007, 'channels', 'liu.png', 'liu.png')

        #self.addDirectoryItem(32008, 'toolNavigator', 'liu.png', 'DefaultAddonProgram.png')

        #downloads = True if control.setting('downloads') == 'true' and (len(control.listDir(control.setting('movie.download.path'))[0]) > 0 or len(control.listDir(control.setting('tv.download.path'))[0]) > 0) else False
        #if downloads == True:
            #self.addDirectoryItem(32009, 'downloadNavigator', 'liu.png', 'DefaultFolder.png')

        #self.addDirectoryItem(32010, 'searchNavigator', 'liu.png', 'DefaultFolder.png')

        self.endDirectory()


    def movies(self, lite=False):
        self.addDirectoryItem(32011, 'liumovieGenres', 'liu.png', 'DefaultMovies.png')
        self.addDirectoryItem(32012, 'liumovieYears', 'liu.png', 'DefaultMovies.png')
        #self.addDirectoryItem(32013, 'liumoviePersons', 'liu.png', 'DefaultMovies.png')
        self.addDirectoryItem(32014, 'liumovieLanguages', 'liu.png', 'DefaultMovies.png')
        self.addDirectoryItem(32015, 'liumovieCertificates', 'liu.png', 'DefaultMovies.png')
        self.addDirectoryItem(32017, 'nmaremov&url=trending', 'liu.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem(32018, 'nmaremov&url=popular', 'liu.png', 'DefaultMovies.png')
        self.addDirectoryItem(32019, 'nmaremov&url=views', 'liu.png', 'DefaultMovies.png')
        self.addDirectoryItem(32020, 'nmaremov&url=boxoffice', 'liu.png', 'DefaultMovies.png')
        self.addDirectoryItem(32021, 'nmaremov&url=oscars', 'liu.png', 'DefaultMovies.png')
        self.addDirectoryItem(32022, 'nmaremov&url=theaters', 'liu.png', 'DefaultRecentlyAddedMovies.png')
        #self.addDirectoryItem(32005, 'movieWidget', 'liu.png', 'DefaultRecentlyAddedMovies.png')

        #if lite == False:
            #if not control.setting('lists.widget') == '0':
                #self.addDirectoryItem(32003, 'mymovieliteNavigator', 'liu.png', 'DefaultVideoPlaylists.png')

            #self.addDirectoryItem(32028, 'moviePerson', 'liu.png', 'DefaultMovies.png')
            #self.addDirectoryItem(32010, 'movieSearch', 'liu.png', 'DefaultMovies.png')

        self.endDirectory()
    def certificationsnew(self):
        self.addDirectoryItem('G', 'nmaremov&url=certificationmg', 'liu.png', 'DefaultMovies.png')
        self.addDirectoryItem('PG', 'nmaremov&url=certificationmpg', 'liu.png', 'DefaultMovies.png')
        self.addDirectoryItem('PG-13', 'nmaremov&url=certificationmpgt', 'liu.png', 'DefaultMovies.png')
        self.addDirectoryItem('R', 'nmaremov&url=certificationmr', 'liu.png', 'DefaultMovies.png')
        self.addDirectoryItem('NC-17', 'nmaremov&url=certificationncseven', 'liu.png', 'DefaultRecentlyAddedMovies.png')

        self.endDirectory()

    def mymovies(self, lite=False):
        self.accountCheck()

        if traktCredentials == True and imdbCredentials == True:
            self.addDirectoryItem(32032, 'nmaremov&url=traktcollection', 'liu.png', 'DefaultMovies.png', queue=True, context=(32551, 'moviesToLibrary&url=traktcollection'))
            self.addDirectoryItem(32033, 'nmaremov&url=traktwatchlist', 'liu.png', 'DefaultMovies.png', queue=True, context=(32551, 'moviesToLibrary&url=traktwatchlist'))
            self.addDirectoryItem(32034, 'nmaremov&url=imdbwatchlist', 'liu.png', 'DefaultMovies.png', queue=True)

        elif traktCredentials == True:
            self.addDirectoryItem(32032, 'nmaremov&url=traktcollection', 'liu.png', 'DefaultMovies.png', queue=True, context=(32551, 'moviesToLibrary&url=traktcollection'))
            self.addDirectoryItem(32033, 'nmaremov&url=traktwatchlist', 'liu.png', 'DefaultMovies.png', queue=True, context=(32551, 'moviesToLibrary&url=traktwatchlist'))

        elif imdbCredentials == True:
            self.addDirectoryItem(32032, 'nmaremov&url=imdbwatchlist', 'liu.png', 'DefaultMovies.png', queue=True)
            self.addDirectoryItem(32033, 'nmaremov&url=imdbwatchlist2', 'liu.png', 'DefaultMovies.png', queue=True)

        if traktCredentials == True:
            self.addDirectoryItem(32035, 'nmaremov&url=traktfeatured', 'liu.png', 'DefaultMovies.png', queue=True)

        elif imdbCredentials == True:
            self.addDirectoryItem(32035, 'nmaremov&url=featured', 'liu.png', 'DefaultMovies.png', queue=True)

        if traktIndicators == True:
            self.addDirectoryItem(32036, 'nmaremov&url=trakthistory', 'liu.png', 'DefaultMovies.png', queue=True)

        self.addDirectoryItem(32039, 'movieUserlists', 'liu.png', 'DefaultMovies.png')

        if lite == False:
            self.addDirectoryItem(32031, 'movieliteNavigator', 'liu.png', 'DefaultMovies.png')
            self.addDirectoryItem(32028, 'moviePerson', 'liu.png', 'DefaultMovies.png')
            self.addDirectoryItem(32010, 'movieSearch', 'liu.png', 'DefaultMovies.png')

        self.endDirectory()


    def tvshows(self, lite=False):
        self.addDirectoryItem(32011, 'liutvGenres', 'liu.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32016, 'liutvNetworks', 'liu.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32014, 'liutvLanguages', 'lpng', 'DefaultTVShows.png')
        self.addDirectoryItem(32015, 'liutvCertificates', 'liu.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32012, 'liutvYears', 'liu.png', 'liu.png')
        self.addDirectoryItem(32017, 'nmaretv&url=trending', 'liu.png', 'DefaultRecentlyAddedEpisodes.png')
        self.addDirectoryItem(32018, 'nmaretv&url=popular', 'liu.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32023, 'nmaretv&url=rating', 'liu.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32019, 'nmaretv&url=views', 'liu.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32024, 'nmaretv&url=airing', 'liu.png', 'DefaultTVShows.png')
        #self.addDirectoryItem(32025, 'nmaretv&url=active', 'liu.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32026, 'nmaretv&url=premiere', 'liu.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32006, 'calendar&url=added', 'liu.png', 'DefaultRecentlyAddedEpisodes.png', queue=True)
        self.addDirectoryItem(32027, 'calendars', 'liu.png', 'DefaultRecentlyAddedEpisodes.png')

        #if lite == False:
            #if not control.setting('lists.widget') == '0':
                #self.addDirectoryItem(32004, 'mytvliteNavigator', 'liu.png', 'DefaultVideoPlaylists.png')

            #self.addDirectoryItem(32028, 'tvPerson', 'liu.png', 'DefaultTVShows.png')
            #self.addDirectoryItem(32010, 'tvSearch', 'liu.png', 'DefaultTVShows.png')

        self.endDirectory()

    def certificationsnewtv(self):
        self.addDirectoryItem('TV-PG', 'nmaretv&url=certificationtvpg', 'liu.png', 'DefaultMovies.png')
        self.addDirectoryItem('TV-14', 'nmaretv&url=certificationtvpgt', 'liu.png', 'DefaultMovies.png')
        self.addDirectoryItem('TV-MA', 'nmaretv&url=certificationtvr', 'liu.png', 'DefaultMovies.png')
        self.endDirectory()
	
    def mytvshows(self, lite=False):
        self.accountCheck()

        if traktCredentials == True and imdbCredentials == True:
            self.addDirectoryItem(32032, 'nmaretv&url=traktcollection', 'liu.png', 'DefaultTVShows.png', context=(32551, 'tvshowsToLibrary&url=traktcollection'))
            self.addDirectoryItem(32033, 'nmaretv&url=traktwatchlist', 'liu.png', 'DefaultTVShows.png', context=(32551, 'tvshowsToLibrary&url=traktwatchlist'))
            self.addDirectoryItem(32034, 'nmaretv&url=imdbwatchlist', 'liu.png', 'DefaultTVShows.png')

        elif traktCredentials == True:
            self.addDirectoryItem(32032, 'nmaretv&url=traktcollection', 'liu.png', 'DefaultTVShows.png', context=(32551, 'tvshowsToLibrary&url=traktcollection'))
            self.addDirectoryItem(32033, 'nmaretv&url=traktwatchlist', 'liu.png', 'DefaultTVShows.png', context=(32551, 'tvshowsToLibrary&url=traktwatchlist'))

        elif imdbCredentials == True:
            self.addDirectoryItem(32032, 'nmaretv&url=imdbwatchlist', 'liu.png', 'DefaultTVShows.png')
            self.addDirectoryItem(32033, 'nmaretv&url=imdbwatchlist2', 'liu.png', 'DefaultTVShows.png')

        if traktCredentials == True:
            self.addDirectoryItem(32035, 'nmaretv&url=traktfeatured', 'liu.png', 'DefaultTVShows.png')

        elif imdbCredentials == True:
            self.addDirectoryItem(32035, 'nmaretv&url=trending', 'liu.png', 'DefaultMovies.png', queue=True)

        if traktIndicators == True:
            self.addDirectoryItem(32036, 'calendar&url=trakthistory', 'liu.png', 'DefaultTVShows.png', queue=True)
            self.addDirectoryItem(32037, 'calendar&url=progress', 'liu.png', 'DefaultRecentlyAddedEpisodes.png', queue=True)
            self.addDirectoryItem(32038, 'calendar&url=mycalendar', 'liu.png', 'DefaultRecentlyAddedEpisodes.png', queue=True)

        self.addDirectoryItem(32040, 'tvUserlists', 'liu.png', 'DefaultTVShows.png')

        if traktCredentials == True:
            self.addDirectoryItem(32041, 'episodeUserlists', 'liu.png', 'DefaultTVShows.png')

        if lite == False:
            self.addDirectoryItem(32031, 'tvliteNavigator', 'liu.png', 'DefaultTVShows.png')
            self.addDirectoryItem(32028, 'tvPerson', 'liu.png', 'DefaultTVShows.png')
            self.addDirectoryItem(32010, 'tvSearch', 'liu.png', 'DefaultTVShows.png')

        self.endDirectory()


    def tools(self):
        self.addDirectoryItem(32043, 'openSettings&query=0.0', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32044, 'openSettings&query=3.1', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32045, 'openSettings&query=1.0', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32046, 'openSettings&query=6.0', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32047, 'openSettings&query=2.0', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32556, 'libraryNavigator', 'liu.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32048, 'openSettings&query=5.0', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32049, 'viewsNavigator', 'liu.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32050, 'clearSources', 'liu.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32604, 'clearCacheSearch', 'liu.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32052, 'clearCache', 'liu.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32073, 'authTrakt', 'liu.png', 'DefaultAddonProgram.png')

        self.endDirectory()

    def library(self):
        self.addDirectoryItem(32557, 'openSettings&query=4.0', 'liu.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32558, 'updateLibrary&query=tool', 'liu.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32559, control.setting('library.movie'), 'liu.png', 'DefaultMovies.png', isAction=False)
        self.addDirectoryItem(32560, control.setting('library.tv'), 'liu.png', 'DefaultTVShows.png', isAction=False)

        if trakt.getTraktCredentialsInfo():
            self.addDirectoryItem(32561, 'moviesToLibrary&url=traktcollection', 'liu.png', 'DefaultMovies.png')
            self.addDirectoryItem(32562, 'moviesToLibrary&url=traktwatchlist', 'liu.png', 'DefaultMovies.png')
            self.addDirectoryItem(32563, 'tvshowsToLibrary&url=traktcollection', 'liu.png', 'DefaultTVShows.png')
            self.addDirectoryItem(32564, 'tvshowsToLibrary&url=traktwatchlist', 'liu.png', 'DefaultTVShows.png')

        self.endDirectory()

    def downloads(self):
        movie_downloads = control.setting('movie.download.path')
        tv_downloads = control.setting('tv.download.path')

        if len(control.listDir(movie_downloads)[0]) > 0:
            self.addDirectoryItem(32001, movie_downloads, 'liu.png', 'DefaultMovies.png', isAction=False)
        if len(control.listDir(tv_downloads)[0]) > 0:
            self.addDirectoryItem(32002, tv_downloads, 'liu.png', 'DefaultTVShows.png', isAction=False)

        self.endDirectory()


    def search(self):
        self.addDirectoryItem(32001, 'movieSearch', 'liu.png', 'DefaultMovies.png')
        self.addDirectoryItem(32002, 'tvSearch', 'liu.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32029, 'moviePerson', 'liu.png', 'DefaultMovies.png')
        self.addDirectoryItem(32030, 'tvPerson', 'liu.png', 'DefaultTVShows.png')

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
