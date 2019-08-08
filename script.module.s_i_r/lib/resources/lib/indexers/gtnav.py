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
        self.addDirectoryItem(32001, 'deepmovieNavigator', 'gticon.png', 'DefaultMovies.png')
        self.addDirectoryItem(32002, 'deeptvNavigator', 'gticon.png', 'DefaultTVShows.png')
        #self.addDirectoryItem('NightMare Reborn', 'nightNavigator', 'gticon.png', 'DefaultMovies.png')
        #if not control.setting('lists.widget') == '0':
            #self.addDirectoryItem(32003, 'myRENAMEmovieNavigator', 'gticon.png', 'DefaultVideoPlaylists.png')
            #self.addDirectoryItem(32004, 'mytvNavigator', 'gticon.png', 'DefaultVideoPlaylists.png')

        #if not control.setting('movie.widget') == '0':
            #self.addDirectoryItem(32005, 'movieWidget', 'gticon.png', 'DefaultRecentlyAddedMovies.png')

        #if (traktIndicators == True and not control.setting('tv.widget.alt') == '0') or (traktIndicators == False and not control.setting('tv.widget') == '0'):
            #self.addDirectoryItem(32006, 'tvWidget', 'gticon.png', 'DefaultRecentlyAddedEpisodes.png')

        #self.addDirectoryItem(32007, 'channels', 'gticon.png', 'gticon.png')

        #self.addDirectoryItem(32008, 'toolNavigator', 'gticon.png', 'DefaultAddonProgram.png')

        #downloads = True if control.setting('downloads') == 'true' and (len(control.listDir(control.setting('movie.download.path'))[0]) > 0 or len(control.listDir(control.setting('tv.download.path'))[0]) > 0) else False
        #if downloads == True:
            #self.addDirectoryItem(32009, 'downloadNavigator', 'gticon.png', 'DefaultFolder.png')

        #self.addDirectoryItem(32010, 'searchNavigator', 'gticon.png', 'DefaultFolder.png')

        self.endDirectory()


    def movies(self, lite=False):
        self.addDirectoryItem(32011, 'deepmovieGenres', 'gticon.png', 'DefaultMovies.png')
        self.addDirectoryItem(32012, 'deepmovieYears', 'gticon.png', 'DefaultMovies.png')
        #self.addDirectoryItem(32013, 'deepmoviePersons', 'gticon.png', 'DefaultMovies.png')
        self.addDirectoryItem(32014, 'deepmovieLanguages', 'gticon.png', 'DefaultMovies.png')
        self.addDirectoryItem(32015, 'deepmovieCertificates', 'gticon.png', 'DefaultMovies.png')
        self.addDirectoryItem(32017, 'wwmovies&url=trending', 'gticon.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem(32018, 'wwmovies&url=popular', 'gticon.png', 'DefaultMovies.png')
        self.addDirectoryItem(32019, 'wwmovies&url=views', 'gticon.png', 'DefaultMovies.png')
        self.addDirectoryItem(32020, 'wwmovies&url=boxoffice', 'gticon.png', 'DefaultMovies.png')
        self.addDirectoryItem(32021, 'wwmovies&url=oscars', 'gticon.png', 'DefaultMovies.png')
        self.addDirectoryItem(32022, 'wwmovies&url=theaters', 'gticon.png', 'DefaultRecentlyAddedMovies.png')
        #self.addDirectoryItem(32005, 'movieWidget', 'gticon.png', 'DefaultRecentlyAddedMovies.png')

        #if lite == False:
            #if not control.setting('lists.widget') == '0':
                #self.addDirectoryItem(32003, 'mymovieliteNavigator', 'gticon.png', 'DefaultVideoPlaylists.png')

            #self.addDirectoryItem(32028, 'moviePerson', 'gticon.png', 'DefaultMovies.png')
            #self.addDirectoryItem(32010, 'movieSearch', 'gticon.png', 'DefaultMovies.png')

        self.endDirectory()
    def certificationsnew(self):
        self.addDirectoryItem('G', 'wwmovies&url=certificationmg', 'gticon.png', 'DefaultMovies.png')
        self.addDirectoryItem('PG', 'wwmovies&url=certificationmpg', 'gticon.png', 'DefaultMovies.png')
        self.addDirectoryItem('PG-13', 'wwmovies&url=certificationmpgt', 'gticon.png', 'DefaultMovies.png')
        self.addDirectoryItem('R', 'wwmovies&url=certificationmr', 'gticon.png', 'DefaultMovies.png')
        self.addDirectoryItem('NC-17', 'wwmovies&url=certificationncseven', 'gticon.png', 'DefaultRecentlyAddedMovies.png')

        self.endDirectory()

    def mymovies(self, lite=False):
        self.accountCheck()

        if traktCredentials == True and imdbCredentials == True:
            self.addDirectoryItem(32032, 'wwmovies&url=traktcollection', 'gticon.png', 'DefaultMovies.png', queue=True, context=(32551, 'moviesToLibrary&url=traktcollection'))
            self.addDirectoryItem(32033, 'wwmovies&url=traktwatchlist', 'gticon.png', 'DefaultMovies.png', queue=True, context=(32551, 'moviesToLibrary&url=traktwatchlist'))
            self.addDirectoryItem(32034, 'wwmovies&url=imdbwatchlist', 'gticon.png', 'DefaultMovies.png', queue=True)

        elif traktCredentials == True:
            self.addDirectoryItem(32032, 'wwmovies&url=traktcollection', 'gticon.png', 'DefaultMovies.png', queue=True, context=(32551, 'moviesToLibrary&url=traktcollection'))
            self.addDirectoryItem(32033, 'wwmovies&url=traktwatchlist', 'gticon.png', 'DefaultMovies.png', queue=True, context=(32551, 'moviesToLibrary&url=traktwatchlist'))

        elif imdbCredentials == True:
            self.addDirectoryItem(32032, 'wwmovies&url=imdbwatchlist', 'gticon.png', 'DefaultMovies.png', queue=True)
            self.addDirectoryItem(32033, 'wwmovies&url=imdbwatchlist2', 'gticon.png', 'DefaultMovies.png', queue=True)

        if traktCredentials == True:
            self.addDirectoryItem(32035, 'wwmovies&url=traktfeatured', 'gticon.png', 'DefaultMovies.png', queue=True)

        elif imdbCredentials == True:
            self.addDirectoryItem(32035, 'wwmovies&url=featured', 'gticon.png', 'DefaultMovies.png', queue=True)

        if traktIndicators == True:
            self.addDirectoryItem(32036, 'wwmovies&url=trakthistory', 'gticon.png', 'DefaultMovies.png', queue=True)

        self.addDirectoryItem(32039, 'movieUserlists', 'gticon.png', 'DefaultMovies.png')

        if lite == False:
            self.addDirectoryItem(32031, 'movieliteNavigator', 'gticon.png', 'DefaultMovies.png')
            self.addDirectoryItem(32028, 'moviePerson', 'gticon.png', 'DefaultMovies.png')
            self.addDirectoryItem(32010, 'movieSearch', 'gticon.png', 'DefaultMovies.png')

        self.endDirectory()


    def tvshows(self, lite=False):
        self.addDirectoryItem(32011, 'deeptvGenres', 'gticon.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32016, 'deeptvNetworks', 'gticon.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32014, 'deeptvLanguages', 'lpng', 'DefaultTVShows.png')
        self.addDirectoryItem(32015, 'deeptvCertificates', 'gticon.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32012, 'deeptvYears', 'gticon.png', 'gticon.png')
        self.addDirectoryItem(32017, 'wwtvshows&url=trending', 'gticon.png', 'DefaultRecentlyAddedEpisodes.png')
        self.addDirectoryItem(32018, 'wwtvshows&url=popular', 'gticon.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32023, 'wwtvshows&url=rating', 'gticon.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32019, 'wwtvshows&url=views', 'gticon.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32024, 'wwtvshows&url=airing', 'gticon.png', 'DefaultTVShows.png')
        #self.addDirectoryItem(32025, 'wwtvshows&url=active', 'gticon.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32026, 'wwtvshows&url=premiere', 'gticon.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32006, 'calendar&url=added', 'gticon.png', 'DefaultRecentlyAddedEpisodes.png', queue=True)
        self.addDirectoryItem(32027, 'calendars', 'gticon.png', 'DefaultRecentlyAddedEpisodes.png')

        #if lite == False:
            #if not control.setting('lists.widget') == '0':
                #self.addDirectoryItem(32004, 'mytvliteNavigator', 'gticon.png', 'DefaultVideoPlaylists.png')

            #self.addDirectoryItem(32028, 'tvPerson', 'gticon.png', 'DefaultTVShows.png')
            #self.addDirectoryItem(32010, 'tvSearch', 'gticon.png', 'DefaultTVShows.png')

        self.endDirectory()

    def certificationsnewtv(self):
        self.addDirectoryItem('TV-PG', 'wwtvshows&url=certificationtvpg', 'gticon.png', 'DefaultMovies.png')
        self.addDirectoryItem('TV-14', 'wwtvshows&url=certificationtvpgt', 'gticon.png', 'DefaultMovies.png')
        self.addDirectoryItem('TV-MA', 'wwtvshows&url=certificationtvr', 'gticon.png', 'DefaultMovies.png')
        self.endDirectory()
	
    def mytvshows(self, lite=False):
        self.accountCheck()

        if traktCredentials == True and imdbCredentials == True:
            self.addDirectoryItem(32032, 'wwtvshows&url=traktcollection', 'gticon.png', 'DefaultTVShows.png', context=(32551, 'tvshowsToLibrary&url=traktcollection'))
            self.addDirectoryItem(32033, 'wwtvshows&url=traktwatchlist', 'gticon.png', 'DefaultTVShows.png', context=(32551, 'tvshowsToLibrary&url=traktwatchlist'))
            self.addDirectoryItem(32034, 'wwtvshows&url=imdbwatchlist', 'gticon.png', 'DefaultTVShows.png')

        elif traktCredentials == True:
            self.addDirectoryItem(32032, 'wwtvshows&url=traktcollection', 'gticon.png', 'DefaultTVShows.png', context=(32551, 'tvshowsToLibrary&url=traktcollection'))
            self.addDirectoryItem(32033, 'wwtvshows&url=traktwatchlist', 'gticon.png', 'DefaultTVShows.png', context=(32551, 'tvshowsToLibrary&url=traktwatchlist'))

        elif imdbCredentials == True:
            self.addDirectoryItem(32032, 'wwtvshows&url=imdbwatchlist', 'gticon.png', 'DefaultTVShows.png')
            self.addDirectoryItem(32033, 'wwtvshows&url=imdbwatchlist2', 'gticon.png', 'DefaultTVShows.png')

        if traktCredentials == True:
            self.addDirectoryItem(32035, 'wwtvshows&url=traktfeatured', 'gticon.png', 'DefaultTVShows.png')

        elif imdbCredentials == True:
            self.addDirectoryItem(32035, 'wwtvshows&url=trending', 'gticon.png', 'DefaultMovies.png', queue=True)

        if traktIndicators == True:
            self.addDirectoryItem(32036, 'calendar&url=trakthistory', 'gticon.png', 'DefaultTVShows.png', queue=True)
            self.addDirectoryItem(32037, 'calendar&url=progress', 'gticon.png', 'DefaultRecentlyAddedEpisodes.png', queue=True)
            self.addDirectoryItem(32038, 'calendar&url=mycalendar', 'gticon.png', 'DefaultRecentlyAddedEpisodes.png', queue=True)

        self.addDirectoryItem(32040, 'tvUserlists', 'gticon.png', 'DefaultTVShows.png')

        if traktCredentials == True:
            self.addDirectoryItem(32041, 'episodeUserlists', 'gticon.png', 'DefaultTVShows.png')

        if lite == False:
            self.addDirectoryItem(32031, 'tvliteNavigator', 'gticon.png', 'DefaultTVShows.png')
            self.addDirectoryItem(32028, 'tvPerson', 'gticon.png', 'DefaultTVShows.png')
            self.addDirectoryItem(32010, 'tvSearch', 'gticon.png', 'DefaultTVShows.png')

        self.endDirectory()


    def tools(self):
        self.addDirectoryItem(32043, 'openSettings&query=0.0', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32044, 'openSettings&query=3.1', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32045, 'openSettings&query=1.0', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32046, 'openSettings&query=6.0', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32047, 'openSettings&query=2.0', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32556, 'libraryNavigator', 'gticon.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32048, 'openSettings&query=5.0', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32049, 'viewsNavigator', 'gticon.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32050, 'clearSources', 'gticon.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32604, 'clearCacheSearch', 'gticon.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32052, 'clearCache', 'gticon.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32073, 'authTrakt', 'gticon.png', 'DefaultAddonProgram.png')

        self.endDirectory()

    def library(self):
        self.addDirectoryItem(32557, 'openSettings&query=4.0', 'gticon.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32558, 'updateLibrary&query=tool', 'gticon.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32559, control.setting('library.movie'), 'gticon.png', 'DefaultMovies.png', isAction=False)
        self.addDirectoryItem(32560, control.setting('library.tv'), 'gticon.png', 'DefaultTVShows.png', isAction=False)

        if trakt.getTraktCredentialsInfo():
            self.addDirectoryItem(32561, 'moviesToLibrary&url=traktcollection', 'gticon.png', 'DefaultMovies.png')
            self.addDirectoryItem(32562, 'moviesToLibrary&url=traktwatchlist', 'gticon.png', 'DefaultMovies.png')
            self.addDirectoryItem(32563, 'tvshowsToLibrary&url=traktcollection', 'gticon.png', 'DefaultTVShows.png')
            self.addDirectoryItem(32564, 'tvshowsToLibrary&url=traktwatchlist', 'gticon.png', 'DefaultTVShows.png')

        self.endDirectory()

    def downloads(self):
        movie_downloads = control.setting('movie.download.path')
        tv_downloads = control.setting('tv.download.path')

        if len(control.listDir(movie_downloads)[0]) > 0:
            self.addDirectoryItem(32001, movie_downloads, 'gticon.png', 'DefaultMovies.png', isAction=False)
        if len(control.listDir(tv_downloads)[0]) > 0:
            self.addDirectoryItem(32002, tv_downloads, 'gticon.png', 'DefaultTVShows.png', isAction=False)

        self.endDirectory()


    def search(self):
        self.addDirectoryItem(32001, 'movieSearch', 'gticon.png', 'DefaultMovies.png')
        self.addDirectoryItem(32002, 'tvSearch', 'gticon.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32029, 'moviePerson', 'gticon.png', 'DefaultMovies.png')
        self.addDirectoryItem(32030, 'tvPerson', 'gticon.png', 'DefaultTVShows.png')

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
