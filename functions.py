import bpy
import os
import time

from bpy.app.handlers import persistent
from .global_variables import handler
from .addon_prefs import get_addon_preferences

# absolute path
def absolute_path(relpath):
    return os.path.abspath(bpy.path.abspath(relpath))

# get addon path
def get_my_dir():
    """ get current file parent directory absolute path """
    script = os.path.realpath(__file__)
    return os.path.dirname(script)

# check libraries
def checkLibraries():
    modified = []
    missing = []
    for item in bpy.data.libraries:
        path = absolute_path(item.filepath)
        try:
            if item.modification_time != str(os.path.getmtime(path)):
                item.modification_time = str(os.path.getmtime(path))
                item.to_reload=True
                modified.append(item.name)
            else:
                item.to_reload=False
        except FileNotFoundError:
            item.modification_time = "missing"
            item.to_reload = True
            missing.append(item.name)
    return modified, missing

# reload library
def reloadLibrary(name):
    lib = bpy.data.libraries[name]
    lib.reload()
    lib.to_reload=False
    lib.modification_time = str(os.path.getmtime(absolute_path(lib.filepath)))

# reload modified datas
def reloadModifiedImages():
    modified = []
    missing = []
    for item in bpy.data.images:
        if not item.library and not item.packed_file:
            path = absolute_path(item.filepath)
            try:
                if item.modification_time!=str(os.path.getmtime(path)):
                    item.reload()
                    item.modification_time=str(os.path.getmtime(path))
                    modified.append(item.name)
            except FileNotFoundError:
                item.modification_time="missing"
                missing.append(item.name)
    return modified, missing

# update 3d view if in rendered mode and not EEVEE or WORKBENCH
def update_viewers(context):
    if context.scene.render.engine not in ['BLENDER_EEVEE','BLENDER_WORKBENCH']:
        wman = bpy.data.window_managers['WinMan']
        for win in wman.windows :
            for area in win.screen.areas :
                if area.type=='VIEW_3D' :
                    for space in area.spaces :
                        if space.type == 'VIEW_3D' and space.shading.type == 'RENDERED' :
                            space.shading.type = 'SOLID'
                            space.shading.type = 'RENDERED'

# check all images at startup
def checkImagesStartup():
    is_missing = False
    for item in bpy.data.images:
        if not item.library and not item.packed_file:
            try:
                path=absolute_path(item.filepath)
                item.modification_time=str(os.path.getmtime(path))
            except FileNotFoundError:
                item.modification_time="missing"
                is_missing = True
    return is_missing

# check all libraries at startup
def checkLibrariesStartup():
    is_missing = False
    for item in bpy.data.libraries:
        try:
            path=absolute_path(item.filepath)
            item.modification_time=str(os.path.getmtime(path))
            item.to_reload = False
        except FileNotFoundError:
            item.modification_time="missing"
            is_missing = True
    return is_missing

# handler
@persistent
def reload_startup(scene):
    wm = bpy.data.window_managers['WinMan']
    if checkImagesStartup(): wm.autoreloadMissingImages = True
    else: wm.autoreloadMissingImages = False
    if checkLibrariesStartup(): wm.autoreloadMissingLibraries = True
    else: wm.autoreloadMissingLibraries = False
    print(handler)