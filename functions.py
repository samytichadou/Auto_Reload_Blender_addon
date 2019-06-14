import bpy
import os
import time

from bpy.app.handlers import persistent
from .global_messages import handler

# absolute path
def absolute_path(relpath):
    return os.path.abspath(bpy.path.abspath(relpath))

# get addon path
def get_my_dir():
    """ get current file parent directory absolute path """
    script = os.path.realpath(__file__)
    return os.path.dirname(script)

# reload image if needed
def reload_images():
    modified = []
    for image in bpy.data.images:
        path = absolute_path(image.filepath)
        try:
            if image.modification_time!=str(os.path.getmtime(path)):
                image.reload()
                image.modification_time=str(os.path.getmtime(path))
                modified.append(image.name)
        except FileNotFoundError:
            if image.modification_time != "missing":
                image.reload()
                image.modification_time="missing"
                modified.append(image.name)
    return modified

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

# handler
@persistent
def reload_startup(scene):
    for i in bpy.data.images:
        try:
            path=absolute_path(i.filepath)
            i.modification_time=str(os.path.getmtime(path))
        except FileNotFoundError:
            i.modification_time="missing"
    print(handler)