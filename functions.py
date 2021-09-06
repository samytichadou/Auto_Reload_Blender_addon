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
    missing = []
    for item in bpy.data.libraries:
        path = absolute_path(item.filepath)
        if os.path.isfile(path):
            if item.autoreload_modification_time != str(os.path.getmtime(path)) \
            and not item.autoreload_to_reload:
                item.autoreload_to_reload=True
                modified.append(item.name)
        else:
            item.autoreload_modification_time = "missing"
            item.autoreload_to_reload = True
            missing.append(item.name)
    return modified, missing


# reload library
def reload_library(name):
    lib = bpy.data.libraries[name]
    lib.reload()
    lib.autoreload_to_reload=False
    lib.autoreload_modification_time = str(os.path.getmtime(absolute_path(lib.filepath)))


# reload modified images
def reload_modified_images():
    modified = []
    missing = []

    # reload images
    for item in bpy.data.images:
        if not item.library and not item.packed_file and item.source not in {'VIEWER','GENERATED'}:
            path = absolute_path(item.filepath)
            if os.path.isfile(path):
                if item.autoreload_modification_time!=str(os.path.getmtime(path)):
                    item.reload()
                    item.autoreload_modification_time=str(os.path.getmtime(path))
                    modified.append(item.name)
            else:
                item.autoreload_modification_time="missing"
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


# update textures
def update_textures(modified_image_list):
    for tex in bpy.data.textures:
        if tex.type == "IMAGE":
            if tex.image:
                if modified_image_list:
                    if tex.image.name in modified_image_list:
                        tex.image = bpy.data.images[tex.image.name]
                else:
                    tex.image = bpy.data.images[tex.image.name]


# update textures with no images
def update_textures_no_images():
    for tex in bpy.data.textures:
        if tex.type == "IMAGE":
            if not tex.image:
                tex.use_alpha = tex.use_alpha


# update strips
def update_strips(modified_image_list):
    for s in bpy.context.scene.sequence_editor.sequences_all:
        if s.type == "IMAGE":
            for e in s.elements:
                if modified_image_list:
                    if e.filename in modified_image_list:
                        e.filename = e.filename
                else:
                    e.filename = e.filename


# check all images at startup
def check_images_startup():
    is_missing = False
    for item in bpy.data.images:
        if not item.library and not item.packed_file:
            try:
                path=absolute_path(item.filepath)
                item.autoreload_modification_time=str(os.path.getmtime(path))
            except FileNotFoundError:
                item.autoreload_modification_time="missing"
                is_missing = True
    return is_missing


# check all libraries at startup
def check_libraries_startup():
    is_missing = False
    for item in bpy.data.libraries:
        try:
            path=absolute_path(item.filepath)
            item.autoreload_modification_time=str(os.path.getmtime(path))
            item.autoreload_to_reload = False
        except FileNotFoundError:
            item.autoreload_modification_time="missing"
            is_missing = True
    return is_missing