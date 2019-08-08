def real_check(uninstall=True):
    import xbmcvfs
    import xbmc
    bad_addons = ['repository.misfitmods', 'plugin.program.misfitmods', 'plugin.video.eternal', 'plugin.video.EternalTv', 'plugin.video.eternal', 'plugin.video.x-wing', 'plugin.video.ds', 'plugin.video.firecat', 'plugin.video.justsports', 'plugin.video.kratos', 'plugin.video.life', 'plugin.video.lol','plugin.video.oneclick', 'plugin.video.outlaw', 'plugin.video.playground', 'plugin.video.rockthemic', 'plugin.video.slamming', 'plugin.video.slaughterhouse', 'plugin.video.wallhangers', 'plugin.video.whodoneit', 'plugin.video.wow', 'plugin.program.ukodi1', 'plugin.video.arrakis' , 'plugin.video.atreides' , 'repository.atreides' , 'script.atreides.artwork' , 'script.atreides.metadata' , 'script.module.atreides'  ]


    has_bad_addon = any(xbmc.getCondVisibility('System.HasAddon(%s)' % (addon)) for addon in bad_addons)
    if has_bad_addon:
        import xbmcgui
        import sys
        line2 = 'Press OK to uninstall this addon' if uninstall else 'Press OK to exit this addon'
        xbmcgui.Dialog().ok('My Addon do as i like', 'This addon will not work with some of the addons  you have installed clicking ok auto deletes this anything to do with the bone crusher addon', line2)
        if uninstall:
            import xbmcaddon
            import shutil
            addon_path = xbmcaddon.Addon().getAddonInfo('path').decode('utf-8')
            ADDON_PATH2 = xbmc.translatePath('special://home/addons/script.module.bonecrusher/')
            ADDON_PATH3 = xbmc.translatePath('special://home/addons/script.bonecrusher.artwork/')
            ADDON_PATH4 = xbmc.translatePath('special://home/addons/script.bonecrusher.metadata/')
            ADDON_PATH5 = xbmc.translatePath('special://home/addons/script.module.openscrapers/')
            shutil.rmtree(addon_path)
            shutil.rmtree(ADDON_PATH2)
            shutil.rmtree(ADDON_PATH3)
            shutil.rmtree(ADDON_PATH4)
            shutil.rmtree(ADDON_PATH5)
        return False
    return False