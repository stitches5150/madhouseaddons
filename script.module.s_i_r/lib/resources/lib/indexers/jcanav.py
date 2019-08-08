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
        self.addDirectoryItem(32001, 'jcamovieNavigator', 'jas.png', 'DefaultMovies.png')
        self.addDirectoryItem(32002, 'jcatvNavigator', 'jas.png', 'DefaultTVShows.png')
        #self.addDirectoryItem('NightMare Reborn', 'nightNavigator', 'jas.png', 'DefaultMovies.png')
        #if not control.setting('lists.widget') == '0':
            #self.addDirectoryItem(32003, 'myRENAMEmovieNavigator', 'jas.png', 'DefaultVideoPlaylists.png')
            #self.addDirectoryItem(32004, 'mytvNavigator', 'jas.png', 'DefaultVideoPlaylists.png')

        #if not control.setting('movie.widget') == '0':
            #self.addDirectoryItem(32005, 'movieWidget', 'jas.png', 'DefaultRecentlyAddedMovies.png')

        #if (traktIndicators == True and not control.setting('tv.widget.alt') == '0') or (traktIndicators == False and not control.setting('tv.widget') == '0'):
            #self.addDirectoryItem(32006, 'tvWidget', 'jas.png', 'DefaultRecentlyAddedEpisodes.png')

        #self.addDirectoryItem(32007, 'channels', 'jas.png', 'jas.png')

        #self.addDirectoryItem(32008, 'toolNavigator', 'jas.png', 'DefaultAddonProgram.png')

        #downloads = True if control.setting('downloads') == 'true' and (len(control.listDir(control.setting('movie.download.path'))[0]) > 0 or len(control.listDir(control.setting('tv.download.path'))[0]) > 0) else False
        #if downloads == True:
            #self.addDirectoryItem(32009, 'downloadNavigator', 'jas.png', 'DefaultFolder.png')

        #self.addDirectoryItem(32010, 'searchNavigator', 'jas.png', 'DefaultFolder.png')

        self.endDirectory()


    def movies(self, lite=False):
        self.addDirectoryItem(32011, 'jcamovieGenres', 'jas.png', 'DefaultMovies.png')
        self.addDirectoryItem(32012, 'jcamovieYears', 'jas.png', 'DefaultMovies.png')
        #self.addDirectoryItem(32013, 'jcamoviePersons', 'jas.png', 'DefaultMovies.png')
        self.addDirectoryItem(32014, 'jcamovieLanguages', 'jas.png', 'DefaultMovies.png')
        self.addDirectoryItem(32015, 'jcamovieCertificates', 'jas.png', 'DefaultMovies.png')
        self.addDirectoryItem(32017, 'apmovies&url=trending', 'jas.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem(32018, 'apmovies&url=popular', 'jas.png', 'DefaultMovies.png')
        self.addDirectoryItem(32019, 'apmovies&url=views', 'jas.png', 'DefaultMovies.png')
        self.addDirectoryItem(32020, 'apmovies&url=boxoffice', 'jas.png', 'DefaultMovies.png')
        self.addDirectoryItem(32021, 'apmovies&url=oscars', 'jas.png', 'DefaultMovies.png')
        self.addDirectoryItem(32022, 'apmovies&url=theaters', 'jas.png', 'DefaultRecentlyAddedMovies.png')
        #self.addDirectoryItem(32005, 'movieWidget', 'jas.png', 'DefaultRecentlyAddedMovies.png')

        #if lite == False:
            #if not control.setting('lists.widget') == '0':
                #self.addDirectoryItem(32003, 'mymovieliteNavigator', 'jas.png', 'DefaultVideoPlaylists.png')

            #self.addDirectoryItem(32028, 'moviePerson', 'jas.png', 'DefaultMovies.png')
            #self.addDirectoryItem(32010, 'movieSearch', 'jas.png', 'DefaultMovies.png')

        self.endDirectory()
    def certificationsnew(self):
        self.addDirectoryItem('G', 'apmovies&url=certificationmg', 'jas.png', 'DefaultMovies.png')
        self.addDirectoryItem('PG', 'apmovies&url=certificationmpg', 'jas.png', 'DefaultMovies.png')
        self.addDirectoryItem('PG-13', 'apmovies&url=certificationmpgt', 'jas.png', 'DefaultMovies.png')
        self.addDirectoryItem('R', 'apmovies&url=certificationmr', 'jas.png', 'DefaultMovies.png')
        self.addDirectoryItem('NC-17', 'apmovies&url=certificationncseven', 'jas.png', 'DefaultRecentlyAddedMovies.png')

        self.endDirectory()

    def mymovies(self, lite=False):
        self.accountCheck()

        if traktCredentials == True and imdbCredentials == True:
            self.addDirectoryItem(32032, 'apmovies&url=traktcollection', 'jas.png', 'DefaultMovies.png', queue=True, context=(32551, 'moviesToLibrary&url=traktcollection'))
            self.addDirectoryItem(32033, 'apmovies&url=traktwatchlist', 'jas.png', 'DefaultMovies.png', queue=True, context=(32551, 'moviesToLibrary&url=traktwatchlist'))
            self.addDirectoryItem(32034, 'apmovies&url=imdbwatchlist', 'jas.png', 'DefaultMovies.png', queue=True)

        elif traktCredentials == True:
            self.addDirectoryItem(32032, 'apmovies&url=traktcollection', 'jas.png', 'DefaultMovies.png', queue=True, context=(32551, 'moviesToLibrary&url=traktcollection'))
            self.addDirectoryItem(32033, 'apmovies&url=traktwatchlist', 'jas.png', 'DefaultMovies.png', queue=True, context=(32551, 'moviesToLibrary&url=traktwatchlist'))

        elif imdbCredentials == True:
            self.addDirectoryItem(32032, 'apmovies&url=imdbwatchlist', 'jas.png', 'DefaultMovies.png', queue=True)
            self.addDirectoryItem(32033, 'apmovies&url=imdbwatchlist2', 'jas.png', 'DefaultMovies.png', queue=True)

        if traktCredentials == True:
            self.addDirectoryItem(32035, 'apmovies&url=traktfeatured', 'jas.png', 'DefaultMovies.png', queue=True)

        elif imdbCredentials == True:
            self.addDirectoryItem(32035, 'apmovies&url=featured', 'jas.png', 'DefaultMovies.png', queue=True)

        if traktIndicators == True:
            self.addDirectoryItem(32036, 'apmovies&url=trakthistory', 'jas.png', 'DefaultMovies.png', queue=True)

        self.addDirectoryItem(32039, 'movieUserlists', 'jas.png', 'DefaultMovies.png')

        if lite == False:
            self.addDirectoryItem(32031, 'movieliteNavigator', 'jas.png', 'DefaultMovies.png')
            self.addDirectoryItem(32028, 'moviePerson', 'jas.png', 'DefaultMovies.png')
            self.addDirectoryItem(32010, 'movieSearch', 'jas.png', 'DefaultMovies.png')

        self.endDirectory()


    def tvshows(self, lite=False):
        self.addDirectoryItem(32011, 'jcatvGenres', 'jas.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32016, 'jcatvNetworks', 'jas.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32014, 'jcatvLanguages', 'lpng', 'DefaultTVShows.png')
        self.addDirectoryItem(32015, 'jcatvCertificates', 'jas.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32012, 'jcatvYears', 'jas.png', 'jas.png')
        self.addDirectoryItem(32017, 'aptvshows&url=trending', 'jas.png', 'DefaultRecentlyAddedEpisodes.png')
        self.addDirectoryItem(32018, 'aptvshows&url=popular', 'jas.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32023, 'aptvshows&url=rating', 'jas.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32019, 'aptvshows&url=views', 'jas.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32024, 'aptvshows&url=airing', 'jas.png', 'DefaultTVShows.png')
        #self.addDirectoryItem(32025, 'aptvshows&url=active', 'jas.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32026, 'aptvshows&url=premiere', 'jas.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32006, 'calendar&url=added', 'jas.png', 'DefaultRecentlyAddedEpisodes.png', queue=True)
        self.addDirectoryItem(32027, 'calendars', 'jas.png', 'DefaultRecentlyAddedEpisodes.png')

        #if lite == False:
            #if not control.setting('lists.widget') == '0':
                #self.addDirectoryItem(32004, 'mytvliteNavigator', 'jas.png', 'DefaultVideoPlaylists.png')

            #self.addDirectoryItem(32028, 'tvPerson', 'jas.png', 'DefaultTVShows.png')
            #self.addDirectoryItem(32010, 'tvSearch', 'jas.png', 'DefaultTVShows.png')

        self.endDirectory()

    def certificationsnewtv(self):
        self.addDirectoryItem('TV-PG', 'aptvshows&url=certificationtvpg', 'jas.png', 'DefaultMovies.png')
        self.addDirectoryItem('TV-14', 'aptvshows&url=certificationtvpgt', 'jas.png', 'DefaultMovies.png')
        self.addDirectoryItem('TV-MA', 'aptvshows&url=certificationtvr', 'jas.png', 'DefaultMovies.png')
        self.endDirectory()
	
    def mytvshows(self, lite=False):
        self.accountCheck()

        if traktCredentials == True and imdbCredentials == True:
            self.addDirectoryItem(32032, 'aptvshows&url=traktcollection', 'jas.png', 'DefaultTVShows.png', context=(32551, 'tvshowsToLibrary&url=traktcollection'))
            self.addDirectoryItem(32033, 'aptvshows&url=traktwatchlist', 'jas.png', 'DefaultTVShows.png', context=(32551, 'tvshowsToLibrary&url=traktwatchlist'))
            self.addDirectoryItem(32034, 'aptvshows&url=imdbwatchlist', 'jas.png', 'DefaultTVShows.png')

        elif traktCredentials == True:
            self.addDirectoryItem(32032, 'aptvshows&url=traktcollection', 'jas.png', 'DefaultTVShows.png', context=(32551, 'tvshowsToLibrary&url=traktcollection'))
            self.addDirectoryItem(32033, 'aptvshows&url=traktwatchlist', 'jas.png', 'DefaultTVShows.png', context=(32551, 'tvshowsToLibrary&url=traktwatchlist'))

        elif imdbCredentials == True:
            self.addDirectoryItem(32032, 'aptvshows&url=imdbwatchlist', 'jas.png', 'DefaultTVShows.png')
            self.addDirectoryItem(32033, 'aptvshows&url=imdbwatchlist2', 'jas.png', 'DefaultTVShows.png')

        if traktCredentials == True:
            self.addDirectoryItem(32035, 'aptvshows&url=traktfeatured', 'jas.png', 'DefaultTVShows.png')

        elif imdbCredentials == True:
            self.addDirectoryItem(32035, 'aptvshows&url=trending', 'jas.png', 'DefaultMovies.png', queue=True)

        if traktIndicators == True:
            self.addDirectoryItem(32036, 'calendar&url=trakthistory', 'jas.png', 'DefaultTVShows.png', queue=True)
            self.addDirectoryItem(32037, 'calendar&url=progress', 'jas.png', 'DefaultRecentlyAddedEpisodes.png', queue=True)
            self.addDirectoryItem(32038, 'calendar&url=mycalendar', 'jas.png', 'DefaultRecentlyAddedEpisodes.png', queue=True)

        self.addDirectoryItem(32040, 'tvUserlists', 'jas.png', 'DefaultTVShows.png')

        if traktCredentials == True:
            self.addDirectoryItem(32041, 'episodeUserlists', 'jas.png', 'DefaultTVShows.png')

        if lite == False:
            self.addDirectoryItem(32031, 'tvliteNavigator', 'jas.png', 'DefaultTVShows.png')
            self.addDirectoryItem(32028, 'tvPerson', 'jas.png', 'DefaultTVShows.png')
            self.addDirectoryItem(32010, 'tvSearch', 'jas.png', 'DefaultTVShows.png')

        self.endDirectory()


    def tools(self):
        self.addDirectoryItem(32043, 'openSettings&query=0.0', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32044, 'openSettings&query=3.1', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32045, 'openSettings&query=1.0', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32046, 'openSettings&query=6.0', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32047, 'openSettings&query=2.0', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32556, 'libraryNavigator', 'jas.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32048, 'openSettings&query=5.0', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32049, 'viewsNavigator', 'jas.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32050, 'clearSources', 'jas.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32604, 'clearCacheSearch', 'jas.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32052, 'clearCache', 'jas.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32073, 'authTrakt', 'jas.png', 'DefaultAddonProgram.png')

        self.endDirectory()

    def library(self):
        self.addDirectoryItem(32557, 'openSettings&query=4.0', 'jas.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32558, 'updateLibrary&query=tool', 'jas.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32559, control.setting('library.movie'), 'jas.png', 'DefaultMovies.png', isAction=False)
        self.addDirectoryItem(32560, control.setting('library.tv'), 'jas.png', 'DefaultTVShows.png', isAction=False)

        if trakt.getTraktCredentialsInfo():
            self.addDirectoryItem(32561, 'moviesToLibrary&url=traktcollection', 'jas.png', 'DefaultMovies.png')
            self.addDirectoryItem(32562, 'moviesToLibrary&url=traktwatchlist', 'jas.png', 'DefaultMovies.png')
            self.addDirectoryItem(32563, 'tvshowsToLibrary&url=traktcollection', 'jas.png', 'DefaultTVShows.png')
            self.addDirectoryItem(32564, 'tvshowsToLibrary&url=traktwatchlist', 'jas.png', 'DefaultTVShows.png')

        self.endDirectory()

    def downloads(self):
        movie_downloads = control.setting('movie.download.path')
        tv_downloads = control.setting('tv.download.path')

        if len(control.listDir(movie_downloads)[0]) > 0:
            self.addDirectoryItem(32001, movie_downloads, 'jas.png', 'DefaultMovies.png', isAction=False)
        if len(control.listDir(tv_downloads)[0]) > 0:
            self.addDirectoryItem(32002, tv_downloads, 'jas.png', 'DefaultTVShows.png', isAction=False)

        self.endDirectory()


    def search(self):
        self.addDirectoryItem(32001, 'movieSearch', 'jas.png', 'DefaultMovies.png')
        self.addDirectoryItem(32002, 'tvSearch', 'jas.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32029, 'moviePerson', 'jas.png', 'DefaultMovies.png')
        self.addDirectoryItem(32030, 'tvPerson', 'jas.png', 'DefaultTVShows.png')

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
