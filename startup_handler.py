import bpy

from bpy.app.handlers import persistent

from . import functions
from .global_variables import handler_statement

@persistent
def reload_startup(scene):
    wm = bpy.data.window_managers['WinMan']
    if functions.check_images_startup(): wm.autoreload_missing_images = True
    else: wm.autoreload_missing_images = False
    if functions.check_libraries_startup(): wm.autoreload_missing_libraries = True
    else: wm.autoreload_missing_libraries = False
    print(handler_statement)


### REGISTER ---

def register():
    bpy.app.handlers.load_post.append(reload_startup)

def unregister():
    bpy.app.handlers.load_post.remove(reload_startup)