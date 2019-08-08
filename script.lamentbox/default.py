# -*- coding: utf8 -*-
############################################################################################
# Copyright (C) 2015 - Philipp Temminghoff <phil65@kodi.tv>
# This program is Free Software see LICENSE file for details
#
# ___       ________  ________  ___  __    ________  ________  ___       __   ________      
#|\  \     |\   __  \|\   ____\|\  \|\  \ |\   ___ \|\   __  \|\  \     |\  \|\   ___  \    
#\ \  \    \ \  \|\  \ \  \___|\ \  \/  /|\ \  \_|\ \ \  \|\  \ \  \    \ \  \ \  \\ \  \   
# \ \  \    \ \  \\\  \ \  \    \ \   ___  \ \  \ \\ \ \  \\\  \ \  \  __\ \  \ \  \\ \  \  
#  \ \  \____\ \  \\\  \ \  \____\ \  \\ \  \ \  \_\\ \ \  \\\  \ \  \|\__\_\  \ \  \\ \  \ 
#   \ \_______\ \_______\ \_______\ \__\\ \__\ \_______\ \_______\ \____________\ \__\\ \__\
#    \|_______|\|_______|\|_______|\|__| \|__|\|_______|\|_______|\|____________|\|__| \|__|
#                                                                                           
#                                                                                           
#                                                                                           
# _____ ______   ________  ________  ___  ___  ___  ________   _______                      
#|\   _ \  _   \|\   __  \|\   ____\|\  \|\  \|\  \|\   ___  \|\  ___ \                     
#\ \  \\\__\ \  \ \  \|\  \ \  \___|\ \  \\\  \ \  \ \  \\ \  \ \   __/|                    
# \ \  \\|__| \  \ \   __  \ \  \    \ \   __  \ \  \ \  \\ \  \ \  \_|/__                  
#  \ \  \    \ \  \ \  \ \  \ \  \____\ \  \ \  \ \  \ \  \\ \  \ \  \_|\ \                 
#   \ \__\    \ \__\ \__\ \__\ \_______\ \__\ \__\ \__\ \__\\ \__\ \_______\                
#    \|__|     \|__|\|__|\|__|\|_______|\|__|\|__|\|__|\|__| \|__|\|_______|                
#                                                                                           
#                                                                                           
#                                                                                           
###########################################################################################

import sys
import xbmc
from resources.lib.process import start_info_actions
from resources.lib.Utils import *


class Main:

    def __init__(self):
        xbmc.log("version %s started" % ADDON_VERSION)
        xbmc.executebuiltin('SetProperty(lamentbox_running,True,home)')
        if xbmc.getCondVisibility('Skin.String(WindowColorMain,'+COLORMAIN+')') == False: xbmc.executebuiltin('Skin.SetString(WindowColorMain,'+COLORMAIN+')')
        elif xbmc.getCondVisibility('Skin.String(WindowColorThemed,'+COLORTHEMED+')') == False: xbmc.executebuiltin('Skin.SetString(WindowColorThemed,'+COLORTHEMED+')')
        self._parse_argv()
        if self.infos:
            start_info_actions(self.infos, self.params)
        else:
            HOME.setProperty('infodialogs.active', "true")
            from resources.lib.WindowManager import wm
            wm.open_video_list()
            HOME.clearProperty('infodialogs.active')
        xbmc.executebuiltin('ClearProperty(lamentbox_running,home)')

    def _parse_argv(self):
        self.handle = None
        self.infos = []
        self.params = {"handle": None,
                       "control": None}
        for arg in sys.argv:
            if arg == 'script.lamentbox':
                continue
            param = arg.replace('"', '').replace("'", " ")
            if param.startswith('info='):
                self.infos.append(param[5:])
            else:
                try:
                    self.params[param.split("=")[0].lower()] = "=".join(param.split("=")[1:]).strip()
                except:
                    pass

if (__name__ == "__main__"):
    Main()
xbmc.log('finished')

############################################################################################
# Copyright (C) 2015 - Philipp Temminghoff <phil65@kodi.tv>
# This program is Free Software see LICENSE file for details
#
# ___       ________  ________  ___  __    ________  ________  ___       __   ________      
#|\  \     |\   __  \|\   ____\|\  \|\  \ |\   ___ \|\   __  \|\  \     |\  \|\   ___  \    
#\ \  \    \ \  \|\  \ \  \___|\ \  \/  /|\ \  \_|\ \ \  \|\  \ \  \    \ \  \ \  \\ \  \   
# \ \  \    \ \  \\\  \ \  \    \ \   ___  \ \  \ \\ \ \  \\\  \ \  \  __\ \  \ \  \\ \  \  
#  \ \  \____\ \  \\\  \ \  \____\ \  \\ \  \ \  \_\\ \ \  \\\  \ \  \|\__\_\  \ \  \\ \  \ 
#   \ \_______\ \_______\ \_______\ \__\\ \__\ \_______\ \_______\ \____________\ \__\\ \__\
#    \|_______|\|_______|\|_______|\|__| \|__|\|_______|\|_______|\|____________|\|__| \|__|
#                                                                                           
#                                                                                           
#                                                                                           
# _____ ______   ________  ________  ___  ___  ___  ________   _______                      
#|\   _ \  _   \|\   __  \|\   ____\|\  \|\  \|\  \|\   ___  \|\  ___ \                     
#\ \  \\\__\ \  \ \  \|\  \ \  \___|\ \  \\\  \ \  \ \  \\ \  \ \   __/|                    
# \ \  \\|__| \  \ \   __  \ \  \    \ \   __  \ \  \ \  \\ \  \ \  \_|/__                  
#  \ \  \    \ \  \ \  \ \  \ \  \____\ \  \ \  \ \  \ \  \\ \  \ \  \_|\ \                 
#   \ \__\    \ \__\ \__\ \__\ \_______\ \__\ \__\ \__\ \__\\ \__\ \_______\                
#    \|__|     \|__|\ __|\|__|\|_______|\|__|\|__|\|__|\|__| \|__|\|_______|                
#                                                                                           
#                                                                                           
#                                                                                           
###########################################################################################
