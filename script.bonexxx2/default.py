import xbmcaddon
import xbmcgui
 
addon       = xbmcaddon.Addon()
addonname   = addon.getAddonInfo('name')
 
line1 = "Hello kodi leaches"
line2 = "Since its ok to make up false shit"
line3 = "its ok i tell you all to fuck off well not all of you but most of you"
 
xbmcgui.Dialog().ok(addonname, line1, line2, line3)
