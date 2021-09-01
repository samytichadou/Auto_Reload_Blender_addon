import bpy

from bpy.app.handlers import persistent

from . import functions
from .global_variables import handler

@persistent
def reload_startup(scene):
    wm = bpy.data.window_managers['WinMan']
    if functions.checkImagesStartup(): wm.autoreloadMissingImages = True
    else: wm.autoreloadMissingImages = False
    if functions.checkLibrariesStartup(): wm.autoreloadMissingLibraries = True
    else: wm.autoreloadMissingLibraries = False
    print(handler)


### REGISTER ---

def register():
    bpy.app.handlers.load_post.append(reload_startup)

def unregister():
    bpy.app.handlers.load_post.remove(reload_startup)