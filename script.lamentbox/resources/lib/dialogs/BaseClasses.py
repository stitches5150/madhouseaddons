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

import xbmcgui


class WindowXML(xbmcgui.WindowXML):

    def __init__(self, *args, **kwargs):
        xbmcgui.WindowXML.__init__(self)
        self.window_type = "window"

    def onInit(self):
        self.window_id = xbmcgui.getCurrentWindowId()
        self.window = xbmcgui.Window(self.window_id)


class DialogXML(xbmcgui.WindowXMLDialog):

    def __init__(self, *args, **kwargs):
        xbmcgui.WindowXMLDialog.__init__(self)
        self.window_type = "dialog"

    def onInit(self):
        self.window_id = xbmcgui.getCurrentWindowDialogId()
        self.window = xbmcgui.Window(self.window_id)

