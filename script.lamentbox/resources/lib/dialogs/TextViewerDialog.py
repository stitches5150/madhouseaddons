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


class TextViewerDialog(xbmcgui.WindowXMLDialog):
    ACTION_PREVIOUS_MENU = [9, 92, 10]

    def __init__(self, *args, **kwargs):
        xbmcgui.WindowXMLDialog.__init__(self)
        self.text = kwargs.get('text')
        self.header = kwargs.get('header')
        self.color = kwargs.get('color')

    def onInit(self):
        window_id = xbmcgui.getCurrentWindowDialogId()
        xbmcgui.Window(window_id).setProperty("WindowColor", self.color)
        self.getControl(1).setLabel(self.header)
        self.getControl(5).setText(self.text)

    def onAction(self, action):
        if action in self.ACTION_PREVIOUS_MENU:
            self.close()

    def onClick(self, control_id):
        pass

    def onFocus(self, control_id):
        pass

