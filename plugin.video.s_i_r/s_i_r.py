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


import urlparse,sys,urllib

params = dict(urlparse.parse_qsl(sys.argv[2].replace('?','')))

action = params.get('action')

name = params.get('name')

title = params.get('title')

year = params.get('year')

imdb = params.get('imdb')

tvdb = params.get('tvdb')

tmdb = params.get('tmdb')

season = params.get('season')

episode = params.get('episode')

tvshowtitle = params.get('tvshowtitle')

premiered = params.get('premiered')

url = params.get('url')

image = params.get('image')

meta = params.get('meta')

select = params.get('select')

query = params.get('query')

source = params.get('source')

content = params.get('content')

windowedtrailer = params.get('windowedtrailer')
windowedtrailer = int(windowedtrailer) if windowedtrailer in ("0","1") else 0


if action == None:
    from resources.lib.indexers import navigator
    from resources.lib.modules import cache
    cache.cache_version_check()
    navigator.navigator().root()

elif action == 'movieNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().movies()

elif action == 'movieliteNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().movies(lite=True)

elif action == 'mymovieNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().mymovies()

elif action == 'mymovieliteNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().mymovies(lite=True)

elif action == 'tvNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().tvshows()

elif action == 'tvliteNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().tvshows(lite=True)

elif action == 'mytvNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().mytvshows()

elif action == 'mytvliteNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().mytvshows(lite=True)

elif action == 'downloadNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().downloads()

elif action == 'libraryNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().library()

elif action == 'toolNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().tools()

elif action == 'searchNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().search()

elif action == 'viewsNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().views()

elif action == 'clearCache':
    from resources.lib.indexers import navigator
    navigator.navigator().clearCache()

elif action == 'clearCacheSearch':
    from resources.lib.indexers import navigator
    navigator.navigator().clearCacheSearch()
    
elif action == 'infoCheck':
    from resources.lib.indexers import navigator
    navigator.navigator().infoCheck('')

elif action == 'movies':
    from resources.lib.indexers import movies
    movies.movies().get(url)

elif action == 'moviePage':
    from resources.lib.indexers import movies
    movies.movies().get(url)

elif action == 'movieWidget':
    from resources.lib.indexers import movies
    movies.movies().widget()

elif action == 'movieSearch':
    from resources.lib.indexers import movies
    movies.movies().search()

elif action == 'movieSearchnew':
    from resources.lib.indexers import movies
    movies.movies().search_new()

elif action == 'movieSearchterm':
    from resources.lib.indexers import movies
    movies.movies().search_term(name)

elif action == 'moviePerson':
    from resources.lib.indexers import movies
    movies.movies().person()

elif action == 'movieGenres':
    from resources.lib.indexers import movies
    movies.movies().genres()

elif action == 'movieLanguages':
    from resources.lib.indexers import movies
    movies.movies().languages()

elif action == 'movieCertificates':
    from resources.lib.indexers import movies
    movies.movies().certifications()

elif action == 'movieYears':
    from resources.lib.indexers import movies
    movies.movies().years()

elif action == 'moviePersons':
    from resources.lib.indexers import movies
    movies.movies().persons(url)

elif action == 'movieUserlists':
    from resources.lib.indexers import movies
    movies.movies().userlists()

elif action == 'channels':
    from resources.lib.indexers import channels
    channels.channels().get()

elif action == 'tvshows':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().get(url)

elif action == 'tvshowPage':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().get(url)

elif action == 'tvSearch':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().search()

elif action == 'tvSearchnew':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().search_new()

elif action == 'tvSearchterm':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().search_term(name)
    
elif action == 'tvPerson':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().person()

elif action == 'tvGenres':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().genres()

elif action == 'tvNetworks':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().networks()

elif action == 'tvLanguages':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().languages()

elif action == 'tvCertificates':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().certifications()

elif action == 'tvPersons':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().persons(url)

elif action == 'tvUserlists':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().userlists()

elif action == 'seasons':
    from resources.lib.indexers import episodes
    episodes.seasons().get(tvshowtitle, year, imdb, tvdb)

elif action == 'episodes':
    from resources.lib.indexers import episodes
    episodes.episodes().get(tvshowtitle, year, imdb, tvdb, season, episode)

elif action == 'calendar':
    from resources.lib.indexers import episodes
    episodes.episodes().calendar(url)

elif action == 'tvWidget':
    from resources.lib.indexers import episodes
    episodes.episodes().widget()

elif action == 'calendars':
    from resources.lib.indexers import episodes
    episodes.episodes().calendars()

elif action == 'episodeUserlists':
    from resources.lib.indexers import episodes
    episodes.episodes().userlists()

elif action == 'refresh':
    from resources.lib.modules import control
    control.refresh()

elif action == 'queueItem':
    from resources.lib.modules import control
    control.queueItem()

elif action == 'openSettings':
    from resources.lib.modules import control
    control.openSettings(query)

elif action == 'artwork':
    from resources.lib.modules import control
    control.artwork()

elif action == 'addView':
    from resources.lib.modules import views
    views.addView(content)

elif action == 'moviePlaycount':
    from resources.lib.modules import playcount
    playcount.movies(imdb, query)

elif action == 'episodePlaycount':
    from resources.lib.modules import playcount
    playcount.episodes(imdb, tvdb, season, episode, query)

elif action == 'tvPlaycount':
    from resources.lib.modules import playcount
    playcount.tvshows(name, imdb, tvdb, season, query)

elif action == 'trailer':
    from resources.lib.modules import trailer
    trailer.trailer().play(name, url, windowedtrailer)

elif action == 'traktManager':
    from resources.lib.modules import trakt
    trakt.manager(name, imdb, tvdb, content)

elif action == 'authTrakt':
    from resources.lib.modules import trakt
    trakt.authTrakt()

elif action == 'smuSettings':
    try: import resolveurl
    except: pass
    resolveurl.display_settings()

elif action == 'download':
    import json
    from resources.lib.modules import sources
    from resources.lib.modules import downloader
    try: downloader.download(name, image, sources.sources().sourcesResolve(json.loads(source)[0], True))
    except: pass

elif action == 'play':
    from resources.lib.modules import sources
    sources.sources().play(title, year, imdb, tvdb, season, episode, tvshowtitle, premiered, meta, select)

elif action == 'addItem':
    from resources.lib.modules import sources
    sources.sources().addItem(title)

elif action == 'playItem':
    from resources.lib.modules import sources
    sources.sources().playItem(title, source)

elif action == 'alterSources':
    from resources.lib.modules import sources
    sources.sources().alterSources(url, meta)

elif action == 'clearSources':
    from resources.lib.modules import sources
    sources.sources().clearSources()

elif action == 'random':
    rtype = params.get('rtype')
    if rtype == 'movie':
        from resources.lib.indexers import movies
        rlist = movies.movies().get(url, create_directory=False)
        r = sys.argv[0]+"?action=play"
    elif rtype == 'episode':
        from resources.lib.indexers import episodes
        rlist = episodes.episodes().get(tvshowtitle, year, imdb, tvdb, season, create_directory=False)
        r = sys.argv[0]+"?action=play"
    elif rtype == 'season':
        from resources.lib.indexers import episodes
        rlist = episodes.seasons().get(tvshowtitle, year, imdb, tvdb, create_directory=False)
        r = sys.argv[0]+"?action=random&rtype=episode"
    elif rtype == 'show':
        from resources.lib.indexers import tvshows
        rlist = tvshows.tvshows().get(url, create_directory=False)
        r = sys.argv[0]+"?action=random&rtype=season"
    from resources.lib.modules import control
    from random import randint
    import json
    try:
        rand = randint(1,len(rlist))-1
        for p in ['title','year','imdb','tvdb','season','episode','tvshowtitle','premiered','select']:
            if rtype == "show" and p == "tvshowtitle":
                try: r += '&'+p+'='+urllib.quote_plus(rlist[rand]['title'])
                except: pass
            else:
                try: r += '&'+p+'='+urllib.quote_plus(rlist[rand][p])
                except: pass
        try: r += '&meta='+urllib.quote_plus(json.dumps(rlist[rand]))
        except: r += '&meta='+urllib.quote_plus("{}")
        if rtype == "movie":
            try: control.infoDialog(rlist[rand]['title'], control.lang(32536).encode('utf-8'), time=30000)
            except: pass
        elif rtype == "episode":
            try: control.infoDialog(rlist[rand]['tvshowtitle']+" - Season "+rlist[rand]['season']+" - "+rlist[rand]['title'], control.lang(32536).encode('utf-8'), time=30000)
            except: pass
        control.execute('RunPlugin(%s)' % r)
    except:
        control.infoDialog(control.lang(32537).encode('utf-8'), time=8000)

elif action == 'movieToLibrary':
    from resources.lib.modules import libtools
    libtools.libmovies().add(name, title, year, imdb, tmdb)

elif action == 'moviesToLibrary':
    from resources.lib.modules import libtools
    libtools.libmovies().range(url)

elif action == 'tvshowToLibrary':
    from resources.lib.modules import libtools
    libtools.libtvshows().add(tvshowtitle, year, imdb, tvdb)

elif action == 'tvshowsToLibrary':
    from resources.lib.modules import libtools
    libtools.libtvshows().range(url)

elif action == 'updateLibrary':
    from resources.lib.modules import libtools
    libtools.libepisodes().update(query)

elif action == 'service':
    from resources.lib.modules import libtools
    libtools.libepisodes().service()

################################################################nightmare reborn#######################################################
if action == 'nightmareNavigator':
    from resources.lib.indexers import nightnav
    nightnav.navigator().root()

elif action == 'nightmaremovieNavigator':
    from resources.lib.indexers import nightnav
    nightnav.navigator().movies()

elif action == 'nightmaretvNavigator':
    from resources.lib.indexers import nightnav
    nightnav.navigator().tvshows()

elif action == 'nightmaremovieCertificates':
    from resources.lib.indexers import nightnav
    nightnav.navigator().certificationsnew()

elif action == 'nightmaretvCertificates':
    from resources.lib.indexers import nightnav
    nightnav.navigator().certificationsnewtv()

elif action == 'nmaremov':
    from resources.lib.indexers import nmaremov
    nmaremov.movies().get(url)


elif action == 'nightmaremovieGenres':
    from resources.lib.indexers import nmaremov
    nmaremov.movies().genres()

elif action == 'nightmaremovieLanguages':
    from resources.lib.indexers import nmaremov
    nmaremov.movies().languages()

elif action == 'nightmaremovieYears':
    from resources.lib.indexers import nmaremov
    nmaremov.movies().years()

elif action == 'nmaretv':
    from resources.lib.indexers import nmaretv
    nmaretv.tvshows().get(url)


elif action == 'nightmaretvGenres':
    from resources.lib.indexers import nmaretv
    nmaretv.tvshows().genres()

elif action == 'nightmaretvNetworks':
    from resources.lib.indexers import nmaretv
    nmaretv.tvshows().networks()

elif action == 'nightmaretvLanguages':
    from resources.lib.indexers import nmaretv
    nmaretv.tvshows().languages()

elif action == 'nightmaretvYears':
    from resources.lib.indexers import nmaretv
    nmaretv.tvshows().years()


################################################################Buffalo Bills True Love#######################################################
if action == 'bbtlNavigator':
    from resources.lib.indexers import bbtlnav
    bbtlnav.navigator().root()

elif action == 'bbtlmovieNavigator':
    from resources.lib.indexers import bbtlnav
    bbtlnav.navigator().movies()

elif action == 'bbtltvNavigator':
    from resources.lib.indexers import bbtlnav
    bbtlnav.navigator().tvshows()

elif action == 'bbtlmovieCertificates':
    from resources.lib.indexers import bbtlnav
    bbtlnav.navigator().certificationsnew()

elif action == 'bbtltvCertificates':
    from resources.lib.indexers import bbtlnav
    bbtlnav.navigator().certificationsnewtv()

elif action == 'dkmov':
    from resources.lib.indexers import dkmov
    dkmov.movies().get(url)


elif action == 'bbtlmovieGenres':
    from resources.lib.indexers import dkmov
    dkmov.movies().genres()

elif action == 'bbtlmovieLanguages':
    from resources.lib.indexers import dkmov
    dkmov.movies().languages()

elif action == 'bbtlmovieYears':
    from resources.lib.indexers import dkmov
    dkmov.movies().years()

elif action == 'dktvshows':
    from resources.lib.indexers import dktvshows
    dktvshows.tvshows().get(url)


elif action == 'bbtltvGenres':
    from resources.lib.indexers import dktvshows
    dktvshows.tvshows().genres()

elif action == 'bbtltvNetworks':
    from resources.lib.indexers import dktvshows
    dktvshows.tvshows().networks()

elif action == 'bbtltvLanguages':
    from resources.lib.indexers import dktvshows
    dktvshows.tvshows().languages()

elif action == 'bbtltvYears':
    from resources.lib.indexers import dktvshows
    dktvshows.tvshows().years()
	

################################################################Buffalo Bills True Love#######################################################
if action == 'jcanavigator':
    from resources.lib.indexers import jcanav
    jcanav.navigator().root()

elif action == 'jcamovieNavigator':
    from resources.lib.indexers import jcanav
    jcanav.navigator().movies()

elif action == 'jcatvNavigator':
    from resources.lib.indexers import jcanav
    jcanav.navigator().tvshows()

elif action == 'jcamovieCertificates':
    from resources.lib.indexers import jcanav
    jcanav.navigator().certificationsnew()

elif action == 'jcatvCertificates':
    from resources.lib.indexers import jcanav
    jcanav.navigator().certificationsnewtv()

elif action == 'apmovies':
    from resources.lib.indexers import apmovies
    apmovies.movies().get(url)


elif action == 'jcamovieGenres':
    from resources.lib.indexers import apmovies
    apmovies.movies().genres()

elif action == 'jcamovieLanguages':
    from resources.lib.indexers import apmovies
    apmovies.movies().languages()

elif action == 'jcamovieYears':
    from resources.lib.indexers import apmovies
    apmovies.movies().years()

elif action == 'aptvshows':
    from resources.lib.indexers import aptvshows
    aptvshows.tvshows().get(url)


elif action == 'jcatvGenres':
    from resources.lib.indexers import aptvshows
    aptvshows.tvshows().genres()

elif action == 'jcatvNetworks':
    from resources.lib.indexers import aptvshows
    aptvshows.tvshows().networks()

elif action == 'jcatvLanguages':
    from resources.lib.indexers import aptvshows
    aptvshows.tvshows().languages()

elif action == 'jcatvYears':
    from resources.lib.indexers import aptvshows
    aptvshows.tvshows().years()


################################################################Buffalo Bills True Love#######################################################
if action == 'deepnavigator':
    from resources.lib.indexers import deepnav
    deepnav.navigator().root()

elif action == 'deepmovieNavigator':
    from resources.lib.indexers import deepnav
    deepnav.navigator().movies()

elif action == 'deeptvNavigator':
    from resources.lib.indexers import deepnav
    deepnav.navigator().tvshows()

elif action == 'deepmovieCertificates':
    from resources.lib.indexers import deepnav
    deepnav.navigator().certificationsnew()

elif action == 'deeptvCertificates':
    from resources.lib.indexers import deepnav
    deepnav.navigator().certificationsnewtv()

elif action == 'asmovies':
    from resources.lib.indexers import asmovies
    asmovies.movies().get(url)


elif action == 'deepmovieGenres':
    from resources.lib.indexers import asmovies
    asmovies.movies().genres()

elif action == 'deepmovieLanguages':
    from resources.lib.indexers import asmovies
    asmovies.movies().languages()

elif action == 'deepmovieYears':
    from resources.lib.indexers import asmovies
    asmovies.movies().years()

elif action == 'astvshows':
    from resources.lib.indexers import astvshows
    astvshows.tvshows().get(url)


elif action == 'deeptvGenres':
    from resources.lib.indexers import astvshows
    astvshows.tvshows().genres()

elif action == 'deeptvNetworks':
    from resources.lib.indexers import astvshows
    astvshows.tvshows().networks()

elif action == 'deeptvLanguages':
    from resources.lib.indexers import astvshows
    astvshows.tvshows().languages()

elif action == 'deeptvYears':
    from resources.lib.indexers import astvshows
    astvshows.tvshows().years()
	

################################################################Buffalo Bills True Love#######################################################
if action == 'hddnavigator':
    from resources.lib.indexers import hddnav
    hddnav.navigator().root()

elif action == 'hddmovieNavigator':
    from resources.lib.indexers import hddnav
    hddnav.navigator().movies()

elif action == 'hddtvNavigator':
    from resources.lib.indexers import hddnav
    hddnav.navigator().tvshows()

elif action == 'hddmovieCertificates':
    from resources.lib.indexers import hddnav
    hddnav.navigator().certificationsnew()

elif action == 'hddtvCertificates':
    from resources.lib.indexers import hddnav
    hddnav.navigator().certificationsnewtv()

elif action == 'hmmm':
    from resources.lib.indexers import hmmm
    hmmm.movies().get(url)


elif action == 'hddmovieGenres':
    from resources.lib.indexers import hmmm
    hmmm.movies().genres()

elif action == 'hddmovieLanguages':
    from resources.lib.indexers import hmmm
    hmmm.movies().languages()

elif action == 'hddmovieYears':
    from resources.lib.indexers import hmmm
    hmmm.movies().years()

elif action == 'hmmtv':
    from resources.lib.indexers import hmmtv
    hmmtv.tvshows().get(url)


elif action == 'hddtvGenres':
    from resources.lib.indexers import hmmtv
    hmmtv.tvshows().genres()

elif action == 'hddtvNetworks':
    from resources.lib.indexers import hmmtv
    hmmtv.tvshows().networks()

elif action == 'hddtvLanguages':
    from resources.lib.indexers import hmmtv
    hmmtv.tvshows().languages()

elif action == 'hddtvYears':
    from resources.lib.indexers import hmmtv
    hmmtv.tvshows().years()
	

################################################################Buffalo Bills True Love#######################################################
if action == 'liunavigator':
    from resources.lib.indexers import liunav
    liunav.navigator().root()

elif action == 'liumovieNavigator':
    from resources.lib.indexers import liunav
    liunav.navigator().movies()

elif action == 'liutvNavigator':
    from resources.lib.indexers import liunav
    liunav.navigator().tvshows()

elif action == 'liumovieCertificates':
    from resources.lib.indexers import liunav
    liunav.navigator().certificationsnew()

elif action == 'liutvCertificates':
    from resources.lib.indexers import liunav
    liunav.navigator().certificationsnewtv()

elif action == 'lhmovies':
    from resources.lib.indexers import lhmovies
    lhmovies.movies().get(url)


elif action == 'liumovieGenres':
    from resources.lib.indexers import lhmovies
    lhmovies.movies().genres()

elif action == 'liumovieLanguages':
    from resources.lib.indexers import lhmovies
    lhmovies.movies().languages()

elif action == 'liumovieYears':
    from resources.lib.indexers import lhmovies
    lhmovies.movies().years()

elif action == 'lhtvshows':
    from resources.lib.indexers import lhtvshows
    lhtvshows.tvshows().get(url)


elif action == 'liutvGenres':
    from resources.lib.indexers import lhtvshows
    lhtvshows.tvshows().genres()

elif action == 'liutvNetworks':
    from resources.lib.indexers import lhtvshows
    lhtvshows.tvshows().networks()

elif action == 'liutvLanguages':
    from resources.lib.indexers import lhtvshows
    lhtvshows.tvshows().languages()

elif action == 'liutvYears':
    from resources.lib.indexers import lhtvshows
    lhtvshows.tvshows().years()

################################################################Buffalo Bills True Love#######################################################
if action == 'nightnavigator':
    from resources.lib.indexers import nightnav
    nightnav.navigator().root()

elif action == 'nightmaremovieNavigator':
    from resources.lib.indexers import nightnav
    nightnav.navigator().movies()

elif action == 'nightmaretvNavigator':
    from resources.lib.indexers import nightnav
    nightnav.navigator().tvshows()

elif action == 'nightmaremovieCertificates':
    from resources.lib.indexers import nightnav
    nightnav.navigator().certificationsnew()

elif action == 'nightmaretvCertificates':
    from resources.lib.indexers import nightnav
    nightnav.navigator().certificationsnewtv()

elif action == 'nmaremov':
    from resources.lib.indexers import nmaremov
    nmaremov.movies().get(url)


elif action == 'nightmaremovieGenres':
    from resources.lib.indexers import nmaremov
    nmaremov.movies().genres()

elif action == 'nightmaremovieLanguages':
    from resources.lib.indexers import nmaremov
    nmaremov.movies().languages()

elif action == 'nightmaremovieYears':
    from resources.lib.indexers import nmaremov
    nmaremov.movies().years()

elif action == 'nmaretv':
    from resources.lib.indexers import nmaretv
    nmaretv.tvshows().get(url)


elif action == 'nightmaretvGenres':
    from resources.lib.indexers import nmaretv
    nmaretv.tvshows().genres()

elif action == 'nightmaretvNetworks':
    from resources.lib.indexers import nmaretv
    nmaretv.tvshows().networks()

elif action == 'nightmaretvLanguages':
    from resources.lib.indexers import nmaretv
    nmaretv.tvshows().languages()

elif action == 'nightmaretvYears':
    from resources.lib.indexers import nmaretv
    nmaretv.tvshows().years()	

################################################################Buffalo Bills True Love#######################################################
if action == 'lfcsnavigator':
    from resources.lib.indexers import lfcsnav
    lfcsnav.navigator().root()

elif action == 'lfcsmovieNavigator':
    from resources.lib.indexers import lfcsnav
    lfcsnav.navigator().movies()

elif action == 'lfcstvNavigator':
    from resources.lib.indexers import lfcsnav
    lfcsnav.navigator().tvshows()

elif action == 'lfcsmovieCertificates':
    from resources.lib.indexers import lfcsnav
    lfcsnav.navigator().certificationsnew()

elif action == 'lfcstvCertificates':
    from resources.lib.indexers import lfcsnav
    lfcsnav.navigator().certificationsnewtv()

elif action == 'lfcsmov':
    from resources.lib.indexers import lfcsmov
    lfcsmov.movies().get(url)


elif action == 'lfcsmovieGenres':
    from resources.lib.indexers import lfcsmov
    lfcsmov.movies().genres()

elif action == 'lfcsmovieLanguages':
    from resources.lib.indexers import lfcsmov
    lfcsmov.movies().languages()

elif action == 'lfcsmovieYears':
    from resources.lib.indexers import lfcsmov
    lfcsmov.movies().years()

elif action == 'lfcstv':
    from resources.lib.indexers import lfcstv
    lfcstv.tvshows().get(url)


elif action == 'lfcstvGenres':
    from resources.lib.indexers import lfcstv
    lfcstv.tvshows().genres()

elif action == 'lfcstvNetworks':
    from resources.lib.indexers import lfcstv
    lfcstv.tvshows().networks()

elif action == 'lfcstvLanguages':
    from resources.lib.indexers import lfcstv
    lfcstv.tvshows().languages()

elif action == 'lfcstvYears':
    from resources.lib.indexers import lfcstv
    lfcstv.tvshows().years()
#####################################drac and friends################
if action == 'dracnavigator':
    from resources.lib.indexers import dafnav
    dafnav.navigator().root()
	
if action == 'dracmov':
    from resources.lib.indexers import dafnav
    dafnav.navigator().movies()
	
if action == 'dractv':
    from resources.lib.indexers import dafnav
    dafnav.navigator().tvshows()
	
elif action == 'movieGenres50':
    from resources.lib.indexers import mcmovies
    mcmovies.movies().genres50()
	
elif action == 'movieGenres60':
    from resources.lib.indexers import mcmovies
    mcmovies.movies().genres60()
	
elif action == 'movieGenres70':
    from resources.lib.indexers import mcmovies
    mcmovies.movies().genres70()
	
elif action == 'movieGenres80':
    from resources.lib.indexers import mcmovies
    mcmovies.movies().genres80()

elif action == 'tvGenres50':
    from resources.lib.indexers import mctvshows
    mctvshows.tvshows().genres50()

	
elif action == 'tvGenres50':
    from resources.lib.indexers import mctvshows
    mctvshows.tvshows().genres50()

elif action == 'tvGenres60':
    from resources.lib.indexers import mctvshows
    mctvshows.tvshows().genres60()


elif action == 'tvGenres70':
    from resources.lib.indexers import mctvshows
    mctvshows.tvshows().genres70()

elif action == 'tvGenres80':
    from resources.lib.indexers import mctvshows
    mctvshows.tvshows().genres80()

################################################################Buffalo Bills True Love#######################################################
if action == 'jsptnavigator':
    from resources.lib.indexers import jsptnav
    jsptnav.navigator().root()

elif action == 'jsptmovieNavigator':
    from resources.lib.indexers import jsptnav
    jsptnav.navigator().movies()

elif action == 'jspttvNavigator':
    from resources.lib.indexers import jsptnav
    jsptnav.navigator().tvshows()

elif action == 'jsptmovieCertificates':
    from resources.lib.indexers import jsptnav
    jsptnav.navigator().certificationsnew()

elif action == 'jspttvCertificates':
    from resources.lib.indexers import jsptnav
    jsptnav.navigator().certificationsnewtv()

elif action == 'odintoons':
    from resources.lib.indexers import odintoons
    odintoons.movies().get(url)


elif action == 'jsptmovieGenres':
    from resources.lib.indexers import odintoons
    odintoons.movies().genres()

elif action == 'jsptmovieLanguages':
    from resources.lib.indexers import odintoons
    odintoons.movies().languages()

elif action == 'jsptmovieYears':
    from resources.lib.indexers import odintoons
    odintoons.movies().years()

elif action == 'odintvtoons':
    from resources.lib.indexers import odintvtoons
    odintvtoons.tvshows().get(url)


elif action == 'jspttvGenres':
    from resources.lib.indexers import odintvtoons
    odintvtoons.tvshows().genres()

elif action == 'jspttvNetworks':
    from resources.lib.indexers import odintvtoons
    odintvtoons.tvshows().networks()

elif action == 'jspttvLanguages':
    from resources.lib.indexers import odintvtoons
    odintvtoons.tvshows().languages()

elif action == 'jspttvYears':
    from resources.lib.indexers import odintvtoons
    odintvtoons.tvshows().years()
################################################################Buffalo Bills True Love#######################################################
if action == 'gtnavigator':
    from resources.lib.indexers import gtnav
    gtnav.navigator().root()

elif action == 'gtmaremovieNavigator':
    from resources.lib.indexers import gtnav
    gtnav.navigator().movies()

elif action == 'gtmaretvNavigator':
    from resources.lib.indexers import gtnav
    gtnav.navigator().tvshows()

elif action == 'gtmaremovieCertificates':
    from resources.lib.indexers import gtnav
    gtnav.navigator().certificationsnew()

elif action == 'gtmaretvCertificates':
    from resources.lib.indexers import gtnav
    gtnav.navigator().certificationsnewtv()

elif action == 'wwmovies':
    from resources.lib.indexers import wwmovies
    wwmovies.movies().get(url)


elif action == 'gtmaremovieGenres':
    from resources.lib.indexers import wwmovies
    wwmovies.movies().genres()

elif action == 'gtmaremovieLanguages':
    from resources.lib.indexers import wwmovies
    wwmovies.movies().languages()

elif action == 'gtmaremovieYears':
    from resources.lib.indexers import wwmovies
    wwmovies.movies().years()

elif action == 'wwtvshows':
    from resources.lib.indexers import wwtvshows
    wwtvshows.tvshows().get(url)


elif action == 'gtmaretvGenres':
    from resources.lib.indexers import wwtvshows
    wwtvshows.tvshows().genres()

elif action == 'gtmaretvNetworks':
    from resources.lib.indexers import wwtvshows
    wwtvshows.tvshows().networks()

elif action == 'gtmaretvLanguages':
    from resources.lib.indexers import wwtvshows
    wwtvshows.tvshows().languages()

elif action == 'gtmaretvYears':
    from resources.lib.indexers import wwtvshows
    wwtvshows.tvshows().years()
###############################users
elif action == 'usersliNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().usersli()
elif action == 'wolfnav':
    from resources.lib.indexers import navigator
    navigator.navigator().userswf()
##############################################
