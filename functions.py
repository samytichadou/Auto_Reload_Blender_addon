import bpy
import os
import time

from .addon_prefs import get_addon_preferences

# absolute path
def absolute_path(relpath):
    return os.path.abspath(bpy.path.abspath(relpath))

# get addon path
def get_current_dir():
    """ get current file parent directory absolute path """
    script = os.path.realpath(__file__)
    return os.path.dirname(script)

# check libraries
def check_libraries():
    modified = []
    missing_msg = []
    for item in bpy.data.libraries:
        path = absolute_path(item.filepath)
        try:
            if item.autoreload_modification_time != str(os.path.getmtime(path)):
                item.autoreload_modification_time = str(os.path.getmtime(path))
                item.autoreload_to_reload=True
                modified.append(item.name)
            else:
                item.autoreload_to_reload=False
        except FileNotFoundError:
            item.autoreload_modification_time = "missing_msg"
            item.autoreload_to_reload = True
            missing_msg.append(item.name)
    return modified, missing_msg

# reload library
def reload_library(name):
    lib = bpy.data.libraries[name]
    lib.reload()
    lib.autoreload_to_reload=False
    lib.autoreload_modification_time = str(os.path.getmtime(absolute_path(lib.filepath)))


# reload modified datas
def reload_modified_images():
    modified = []
    missing_msg = []

    # reload images
    for item in bpy.data.images:
        if not item.library and not item.packed_file:
            path = absolute_path(item.filepath)
            try:
                if item.autoreload_modification_time!=str(os.path.getmtime(path)):
                    item.reload()
                    item.autoreload_modification_time=str(os.path.getmtime(path))
                    modified.append(item.name)
            except FileNotFoundError:
                item.autoreload_modification_time="missing_msg"
                missing_msg.append(item.name)

    # update textures
    for tex in bpy.data.textures:
        if tex.type == "IMAGE" and tex.image.name in modified:
            tex.image = bpy.data.images[tex.image.name]

    # update strips
    for s in bpy.context.scene.sequence_editor.sequences_all:
        if s.type == "IMAGE":
            for e in s.elements:
                if e.filename in modified:
                    e.filename = e.filename

    return modified, missing_msg


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
def check_images_startup():
    is_missing_msg = False
    for item in bpy.data.images:
        if not item.library and not item.packed_file:
            try:
                path=absolute_path(item.filepath)
                item.autoreload_modification_time=str(os.path.getmtime(path))
            except FileNotFoundError:
                item.autoreload_modification_time="missing_msg"
                is_missing_msg = True
    return is_missing_msg

# check all libraries at startup
def check_libraries_startup():
    is_missing_msg = False
    for item in bpy.data.libraries:
        try:
            path=absolute_path(item.filepath)
            item.autoreload_modification_time=str(os.path.getmtime(path))
            item.autoreload_to_reload = False
        except FileNotFoundError:
            item.autoreload_modification_time="missing_msg"
            is_missing_msg = True
    return is_missing_msg