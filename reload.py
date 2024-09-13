import bpy
import os
from bpy.app.handlers import persistent

from .addon_prefs import get_addon_preferences

object_types = [
    "images",
    "movieclips",
    "sounds",
    "libraries",
    "texts",
    "fonts",
]


def check_reload_file_size(object, filepath):
    
    if not os.path.isfile(filepath):
        return None
    
    new_size = os.path.getsize(filepath)
    
    if new_size != object.file_size:

        # Find if images previously been checked
        checked = True
        if object.file_size == 0:
            checked = False
        
        object.file_size = new_size
        
        return checked
    
    return False


def get_files_size(obj_type):
    
    obj_to_reload = []
    
    for obj in getattr(bpy.data, obj_type):
        
        # Avoid builtin
        if obj.filepath in ["<builtin>", ""]:
            continue
        
        # Reload file size
        if check_reload_file_size(
            obj,
            bpy.path.abspath(obj.filepath),
        ):
            obj_to_reload.append(obj)
                
    # TODO Deal with sequencer strips
                
    return obj_to_reload


@persistent
def startup_refresh_file_size(scene):
    
    print("AUTORELOAD --- Refreshing external files size")
    for obj_type in object_types:
        get_files_size(obj_type)


def update_3d_viewers():
    
    # Check if render is compatible with live refresh
    engine = bpy.context.scene.render.engine
    if engine in ['BLENDER_EEVEE','BLENDER_WORKBENCH']:
        return
        
    # Iterate through viewport to update them
    wm = bpy.data.window_managers['WinMan']
    for window in wm.windows :
        for area in window.screen.areas :
            if area.type=='VIEW_3D' :
                for space in area.spaces :
                    if space.type == 'VIEW_3D'\
                    and space.shading.type == 'RENDERED' :
                        space.shading.type = 'SOLID'
                        space.shading.type = 'RENDERED'
    
    
def reload_modified_objects():
    
    props = bpy.context.window_manager.autoreload_properties
    
    obj_to_reload = {}
    
    # Get objects to reload
    for obj_type in object_types:
        obj_to_reload[obj_type] = []
        
        # Check if obj type autoreloaded from property
        if getattr(props, f"autoreload_{obj_type}"):
            obj_to_reload[obj_type] = get_files_size(obj_type)
            
    # Reload objects
    print("AUTORELOAD --- Objects to reload :")
    print(obj_to_reload)
    print()
    

def timer_reload_files():
    
    print("AUTORELOAD --- Timer")

    interval = get_addon_preferences().timer_frequency
    
    reload_modified_objects()

    return interval

    
### REGISTER ---
def register():
    bpy.app.handlers.load_post.append(startup_refresh_file_size)
    bpy.app.timers.register(timer_reload_files, persistent=True)

def unregister():
    bpy.app.handlers.load_post.remove(startup_refresh_file_size)
    bpy.app.timers.unregister(timer_reload_files)
            
            
