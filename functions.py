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

# reload modified datas
def reloadModifiedDatas(datas):
    modified = []
    missing = []
    for item in datas:
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

# reload all datas
def reloadDatas(datas):
    is_missing = False
    for item in datas:
        try:
            path=absolute_path(item.filepath)
            item.modification_time=str(os.path.getmtime(path))
        except FileNotFoundError:
            item.modification_time="missing"
            is_missing = True
    return is_missing

# handler
@persistent
def reload_startup(scene):
    wm = bpy.data.window_managers['WinMan']
    if reloadDatas(bpy.data.images): wm.autoreloadMissingImages = True
    else: wm.autoreloadMissingImages = False
    if reloadDatas(bpy.data.libraries): wm.autoreloadMissingLibraries = True
    else: wm.autoreloadMissingLibraries = False
    print(handler)