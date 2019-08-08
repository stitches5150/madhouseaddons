# -*- coding: utf-8 -*-

'''
    odin Add-on

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
from resources.lib.modules import control


import xbmcgui

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


######################LISTS SCRAPER#################################

if action == 'lists':
    from resources.lib.indexers import lists
    lists.indexer().root()

elif action == 'listsNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().lists()    

elif action == 'directory':
    from resources.lib.indexers import lists
    lists.indexer().get(url)

elif action == 'qdirectory':
    from resources.lib.indexers import lists
    lists.indexer().getq(url)

elif action == 'xdirectory':
    from resources.lib.indexers import lists
    lists.indexer().getx(url)

elif action == 'developer':
    from resources.lib.indexers import lists
    lists.indexer().developer()

elif action == 'tvtuner':
    from resources.lib.indexers import lists
    lists.indexer().tvtuner(url)

elif 'youtube' in str(action):
    from resources.lib.indexers import lists
    lists.indexer().youtube(url, action)

elif action == 'play2':
    from resources.lib.indexers import lists
    lists.player().play(url, content)

elif action == 'browser':
    from resources.lib.indexers import lists
    lists.resolver().browser(url)

elif action == 'queueItem':
    from resources.lib.modules import control
    control.queueItem()

elif action == 'openSettings':
    from resources.lib.modules import control
    control.openSettings()

elif action == 'resolveurlSettings':
    from resources.lib.modules import control
    control.openSettings(id='script.module.resolveurl')

elif action == 'addView':
    from resources.lib.modules import views
    views.addView(content)

elif action == 'downloader':
    from resources.lib.modules import downloader
    downloader.downloader()

elif action == 'addDownload':
    from resources.lib.modules import downloader
    downloader.addDownload(name,url,image)

elif action == 'removeDownload':
    from resources.lib.modules import downloader
    downloader.removeDownload(url)

elif action == 'startDownload':
    from resources.lib.modules import downloader
    downloader.startDownload()

elif action == 'startDownloadThread':
    from resources.lib.modules import downloader
    downloader.startDownloadThread()

elif action == 'stopDownload':
    from resources.lib.modules import downloader
    downloader.stopDownload()

elif action == 'statusDownload':
    from resources.lib.modules import downloader
    downloader.statusDownload()

elif action == 'trailer':
    from resources.lib.modules import trailer
    trailer.trailer().play(name)

elif action == 'clearCache1':
    from resources.lib.modules import cache
    cache.clear() 
#########################bcold#############################################################################

if action == 'bcoldnavNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().bcold()
	
if action == 'docs2navNavigator':
    from resources.lib.indexers import docs2nav
    docs2nav.navigator().root()

if action == 'bioNavigator':
    from resources.lib.indexers import docs2nav
    docs2nav.navigator().bio()

if action == 'natutredocsNavigator':
    from resources.lib.indexers import docs2nav
    docs2nav.navigator().natutredocs()
	
if action == 'thebibleNavigator':
    from resources.lib.indexers import docs2nav
    docs2nav.navigator().bible()

if action == 'ConspiraciesNavigator':
    from resources.lib.indexers import docs2nav
    docs2nav.navigator().Conspiracies()
	
if action == 'mentalNavigator':
    from resources.lib.indexers import docs2nav
    docs2nav.navigator().mental()

if action == 'killersNavigator':
    from resources.lib.indexers import docs2nav
    docs2nav.navigator().killers()
	
if action == 'ufoNavigator':
    from resources.lib.indexers import docs2nav
    docs2nav.navigator().ufo()

if action == 'mythsNavigator':
    from resources.lib.indexers import docs2nav
    docs2nav.navigator().myths()
	
if action == 'addictionNavigator':
    from resources.lib.indexers import docs2nav
    docs2nav.navigator().addiction()

if action == 'kids2Navigator':
    from resources.lib.indexers import kidsnav
    kidsnav.navigator().root()
	
if action == 'toddlerNavigator':
    from resources.lib.indexers import kidsnav
    kidsnav.navigator().toddler()

if action == 'KidsNavigator':
    from resources.lib.indexers import kidsnav
    kidsnav.navigator().Kids()
	
if action == 'TeenNavigator':
    from resources.lib.indexers import kidsnav
    kidsnav.navigator().Teen()

	
if action == 'NatureNavigator':
    from resources.lib.indexers import kidsnav
    kidsnav.navigator().Nature()

if action == 'classicsNavigator':
    from resources.lib.indexers import classicnav
    classicnav.navigator().root()

if action == 'action2Navigator':
    from resources.lib.indexers import classicnav
    classicnav.navigator().action()
	
if action == 'adventure2Navigator':
    from resources.lib.indexers import classicnav
    classicnav.navigator().adventure()

if action == 'animation2Navigator':
    from resources.lib.indexers import classicnav
    classicnav.navigator().animation()
	
if action == 'comedy2Navigator':
    from resources.lib.indexers import classicnav
    classicnav.navigator().comedy()

if action == 'crime2Navigator':
    from resources.lib.indexers import classicnav
    classicnav.navigator().crime()
	
if action == 'drama2Navigator':
    from resources.lib.indexers import classicnav
    classicnav.navigator().drama()

if action == 'family2Navigator':
    from resources.lib.indexers import classicnav
    classicnav.navigator().family()
	
if action == 'fantasy2Navigator':
    from resources.lib.indexers import classicnav
    classicnav.navigator().fantasy()

if action == 'horror2Navigator':
    from resources.lib.indexers import classicnav
    classicnav.navigator().horror()
	
if action == 'mystery2Navigator':
    from resources.lib.indexers import classicnav
    classicnav.navigator().mystery()

if action == 'romance2Navigator':
    from resources.lib.indexers import classicnav
    classicnav.navigator().romance()
	
if action == 'scifi2Navigator':
    from resources.lib.indexers import classicnav
    classicnav.navigator().scifi()

if action == 'thriller2Navigator':
    from resources.lib.indexers import classicnav
    classicnav.navigator().thriller()
	
if action == 'war2Navigator':
    from resources.lib.indexers import classicnav
    classicnav.navigator().war()

if action == 'western2Navigator':
    from resources.lib.indexers import classicnav
    classicnav.navigator().western()
	


if action == 'boxsetsNavigator':
    from resources.lib.indexers import bxsets
    bxsets.navigator().root()
	
elif action == 'actionNavigator':
    from resources.lib.indexers import bxsets
    bxsets.navigator().action()
	
elif action == 'actionliteNavigator':
    from resources.lib.indexers import bxsets
    bxsets.navigator().action(lite=True)

elif action == 'adventureNavigator':
    from resources.lib.indexers import bxsets
    bxsets.navigator().adventure()
	
elif action == 'adventureliteNavigator':
    from resources.lib.indexers import bxsets
    bxsets.navigator().adventure(lite=True)
	
elif action == 'animationNavigator':
    from resources.lib.indexers import bxsets
    bxsets.navigator().animation()
	
elif action == 'animationliteNavigator':
    from resources.lib.indexers import bxsets
    bxsets.navigator().animation(lite=True)
	
elif action == 'comedyNavigator':
    from resources.lib.indexers import bxsets
    bxsets.navigator().comedy()
	
elif action == 'comedyliteNavigator':
    from resources.lib.indexers import bxsets
    bxsets.navigator().comedy(lite=True)
	
elif action == 'crimeNavigator':
    from resources.lib.indexers import bxsets
    bxsets.navigator().crime()
	
elif action == 'crimeliteNavigator':
    from resources.lib.indexers import bxsets
    bxsets.navigator().crime(lite=True)
	
elif action == 'dramaNavigator':
    from resources.lib.indexers import bxsets
    bxsets.navigator().drama()
	
elif action == 'dramaliteNavigator':
    from resources.lib.indexers import bxsets
    bxsets.navigator().drama(lite=True)
	
elif action == 'familyNavigator':
    from resources.lib.indexers import bxsets
    bxsets.navigator().family()
	
elif action == 'familyliteNavigator':
    from resources.lib.indexers import bxsets
    bxsets.navigator().family(lite=True)
	
elif action == 'fantasyNavigator':
    from resources.lib.indexers import bxsets
    bxsets.navigator().fantasy()
	
elif action == 'fantasyliteNavigator':
    from resources.lib.indexers import bxsets
    bxsets.navigator().fantasy(lite=True)

elif action == 'horrorNavigator':
    from resources.lib.indexers import bxsets
    bxsets.navigator().horror()
	
elif action == 'horrorliteNavigator':
    from resources.lib.indexers import bxsets
    bxsets.navigator().horror(lite=True)
	
elif action == 'mysteryNavigator':
    from resources.lib.indexers import bxsets
    bxsets.navigator().mystery()
	
elif action == 'mysteryliteNavigator':
    from resources.lib.indexers import bxsets
    bxsets.navigator().mystery(lite=True)
	
elif action == 'romanceNavigator':
    from resources.lib.indexers import bxsets
    bxsets.navigator().romance()
	
elif action == 'romanceliteNavigator':
    from resources.lib.indexers import bxsets
    bxsets.navigator().romance(lite=True)
	
elif action == 'scifiNavigator':
    from resources.lib.indexers import bxsets
    bxsets.navigator().scifi()
	
elif action == 'scifiliteNavigator':
    from resources.lib.indexers import bxsets
    bxsets.navigator().scifi(lite=True)
	
elif action == 'thrillerNavigator':
    from resources.lib.indexers import bxsets
    bxsets.navigator().thriller()
	
elif action == 'thrillerliteNavigator':
    from resources.lib.indexers import bxsets
    bxsets.navigator().thriller(lite=True)
	
elif action == 'westernNavigator':
    from resources.lib.indexers import bxsets
    bxsets.navigator().western()
	
elif action == 'westernliteNavigator':
    from resources.lib.indexers import bxsets
    bxsets.navigator().western(lite=True)

elif action == 'teamNavigator':
    from resources.lib.indexers import teamnav
    teamnav.navigator().root()

elif action == 'ldmovNavigator':
    from resources.lib.indexers import teamnav
    teamnav.navigator().ldmov()

elif action == 'EnforcermoNavigator':
    from resources.lib.indexers import teamnav
    teamnav.navigator().Enforcermo()
	
elif action == 'warhammermoNavigator':
    from resources.lib.indexers import teamnav
    teamnav.navigator().warhammermo()

elif action == 'katsmoNavigator':
    from resources.lib.indexers import teamnav
    teamnav.navigator().katsmo()
	
elif action == 'stalkermoNavigator':
    from resources.lib.indexers import teamnav
    teamnav.navigator().stalkermo()

elif action == 'oddsNavigator':
    from resources.lib.indexers import oddsnends
    oddsnends.navigator().root()

elif action == 'KfulegNavigator':
    from resources.lib.indexers import oddsnends
    oddsnends.navigator().Kfuleg()

elif action == 'qocNavigator':
    from resources.lib.indexers import oddsnends
    oddsnends.navigator().qoc()

elif action == 'giftsNavigator':
    from resources.lib.indexers import oddsnends
    oddsnends.navigator().gifts()

elif action == 'amNavigator':
    from resources.lib.indexers import oddsnends
    oddsnends.navigator().at()
	
elif action == 'MlNavigator':
    from resources.lib.indexers import oddsnends
    oddsnends.navigator().Tl()

elif action == 'restNavigator':
    from resources.lib.indexers import wishes 
    wishes.navigator().rest()

elif action == 'SwmNavigator':
    from resources.lib.indexers import oddsnends
    oddsnends.navigator().Swm()
	
elif action == 'ClmNavigator':
    from resources.lib.indexers import oddsnends
    oddsnends.navigator().Clts()

elif action == 'metalNavigator':
    from resources.lib.indexers import metal
    metal.navigator().root()

elif action == 'unexplainedNavigator':
    from resources.lib.indexers import oddsnends 
    oddsnends.navigator().unexplained()

elif action == 'metal2Navigator':
    from resources.lib.indexers import metal
    metal.navigator().metal()
	
elif action == 'classicNavigator':
    from resources.lib.indexers import metal
    metal.navigator().classic()

elif action == 'psyNavigator':
    from resources.lib.indexers import metal
    metal.navigator().psy()

elif action == 'grungeNavigator':
    from resources.lib.indexers import metal
    metal.navigator().grunge()

elif action == 'usersNavigator':
    from resources.lib.indexers import oddsnends
    oddsnends.navigator().users()
	
elif action == 'TmNavigator':
    from resources.lib.indexers import oddsnends
    oddsnends.navigator().Tts()

elif action == 'KzmNavigator':
    from resources.lib.indexers import oddsnends
    oddsnends.navigator().Kzt()

elif action == 'BftvNavigator':
    from resources.lib.indexers import teamnav
    teamnav.navigator().Bftv()

elif action == 'KrestsNavigator':
    from resources.lib.indexers import wishes
    wishes.navigator().root()

elif action == 'KrestswNavigator':
    from resources.lib.indexers import wishes
    wishes.navigator().krests()
	
elif action == 'usersNavigator':
    from resources.lib.indexers import oddsnends
    oddsnends.navigator().users()
	
elif action == 'ParamNavigator':
    from resources.lib.indexers import oddsnends
    oddsnends.navigator().Paratv()

elif action == 'DocsNavigator':
    from resources.lib.indexers import oddsnends
    oddsnends.navigator().Docstv()

elif action == 'BrNavigator':
    from resources.lib.indexers import oddsnends
    oddsnends.navigator().Br()

elif action == 'kocNavigator':
    from resources.lib.indexers import oddsnends
    oddsnends.navigator().koc()
	
elif action == 'MhNavigator':
    from resources.lib.indexers import oddsnends
    oddsnends.navigator().Mh()

elif action == 'darktvNavigator':
    from resources.lib.indexers import oddsnends
    oddsnends.navigator().darktv()
	
elif action == 'firestickNavigator':
    from resources.lib.indexers import oddsnends
    oddsnends.navigator().firestick()

elif action == 'oneNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().movies()


elif action == 'tvshows2':
    from resources.lib.indexers import tvshows2
    tvshows2.tvshows().get(url)


elif action == 'movies2':
    from resources.lib.indexers import movies2
    movies2.movies().get(url)

######################IMDB SCRAPER#################################

if action == None:
    from resources.lib.indexers import navigator
    from resources.lib.modules import cache
    cache.cache_version_check()
    navigator.navigator().root()

elif action == "furkNavigator":
    from resources.lib.indexers import navigator
    navigator.navigator().furk()

elif action == "furkMetaSearch":
    from resources.lib.indexers import furk
    furk.furk().furk_meta_search(url)

elif action == "furkSearch":
    from resources.lib.indexers import furk
    furk.furk().search()

elif action == "furkUserFiles":
    from resources.lib.indexers import furk
    furk.furk().user_files()

elif action == "furkSearchNew":
    from resources.lib.indexers import furk
    furk.furk().search_new()

elif action == 'ruSettings':
    from resources.lib.modules import control
    control.openSettings(id='script.module.resolveurl')    

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

elif action == 'paranormalNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().paranormal()

elif action == 'oneclickNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().oneclick()

elif action == 'oneclick2Navigator':
    from resources.lib.indexers import navigator
    navigator.navigator().oneclick2()            

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
    movies.movies().search_new()

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
    tvshows.tvshows().search_new()

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

elif action == 'play1':
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

elif action == 'moviesToLibrarySilent':
    from resources.lib.modules import libtools
    libtools.libmovies().silent(url)

elif action == 'tvshowToLibrary':
    from resources.lib.modules import libtools
    libtools.libtvshows().add(tvshowtitle, year, imdb, tvdb)

elif action == 'tvshowsToLibrary':
    from resources.lib.modules import libtools
    libtools.libtvshows().range(url)

elif action == 'tvshowsToLibrarySilent':
    from resources.lib.modules import libtools
    libtools.libtvshows().silent(url)

elif action == 'updateLibrary':
    from resources.lib.modules import libtools
    libtools.libepisodes().update(query)

elif action == 'service':
    from resources.lib.modules import libtools
    libtools.libepisodes().service()

##############################odin tunes test ####################################################################

elif action == 'radios':
    from resources.lib.indexers import phradios
    phradios.radios()

elif action == 'radioResolve':
    from resources.lib.indexers import phradios
    phradios.radioResolve(url)

elif action == 'radio1fm':
    from resources.lib.indexers import phradios
    phradios.radio1fm()

elif action == 'radio181fm':
    from resources.lib.indexers import phradios
    phradios.radio181fm()

elif action == 'radiocast':
    from resources.lib.indexers import phradios
    phradios.kickinradio()

elif action == 'kickinradiocats':
    from resources.lib.indexers import phradios
    phradios.kickinradiocats(url)

