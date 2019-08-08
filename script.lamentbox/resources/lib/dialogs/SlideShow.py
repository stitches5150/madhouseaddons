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

from ..Utils import *
from .BaseClasses import DialogXML


class SlideShow(DialogXML):
    ACTION_PREVIOUS_MENU = [9, 92, 10]

    def __init__(self, *args, **kwargs):
        self.imagelist = kwargs.get('listitems')
        self.index = kwargs.get('index')
        self.image = kwargs.get('image')
        self.action = None

    def onInit(self):
        super(SlideShow, self).onInit()
        if self.imagelist:
            self.getControl(10001).addItems(create_listitems(self.imagelist))
            self.getControl(10001).selectItem(self.index)
            self.setFocusId(10001)
            xbmc.executebuiltin("SetFocus(10001)")

    def onAction(self, action):
        if action in self.ACTION_PREVIOUS_MENU:
            self.position = self.getControl(10001).getSelectedPosition()
            self.close()
