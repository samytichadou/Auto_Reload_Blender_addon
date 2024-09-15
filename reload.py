import bpy
import os
import re
from bpy.app.handlers import persistent

from .addon_prefs import get_addon_preferences

# TODO Cache files
# TODO Sequencer strips
# TODO Reload sounds waveform

object_types = [
    "images",
    "movieclips",
    "sounds",
    "libraries",
]


def get_filesequence_from_file(filepath):
    
    seq_files = []
    
    folderpath, filename_ext = os.path.split(filepath)
    filename, ext = os.path.splitext(filename_ext)
    
    str_nb = re.search(r'\d+$', filename)
    
    if str_nb is None:
        return seq_files
    
    str_nb = str_nb.group()
    pattern = filename.replace(str_nb, "")
    
    for file in os.listdir(folderpath):
        if pattern in file and ext in file:
            seq_files.append(os.path.join(folderpath, file))
    
    return seq_files


def get_image_size(image, filepath):
    
    new_size = 0
    
    # UDIM
    if image.source == "TILED":
        tile_list = []

        for tile in image.tiles:
            tile_list.append(
                filepath.replace(
                    "<UDIM>",
                    str(tile.number),
                )
            )

        new_size = get_file_list_size(tile_list)
    
    # Sequence
    if image.source == "SEQUENCE":
        new_size = get_file_list_size(
            get_filesequence_from_file(filepath)
        )
    
    # Single file
    else:
        
        # Invalid filepath
        if not os.path.isfile(filepath):
            return new_size
        
        new_size = os.path.getsize(filepath)
        
    return new_size
        
        
def get_file_size(object, filepath):
    
    # Invalid filepath
    if not os.path.isfile(filepath):
        return 0
    
    # Valid filepath
    else:
        return os.path.getsize(filepath)
    
    
def reload_file_size(new_size, object):
    
    # Save new file_size
    if new_size != object.file_size:

        # Find if images previously been checked
        checked = True
        if object.file_size == 0:
            checked = False
        
        object.file_size = new_size
        
        return checked
    
    return False


def get_file_list_size(file_list):
    
    size = 0
    
    for filepath in file_list:
        if os.path.isfile:
            size += os.path.getsize(filepath)
            
    return size
        

def get_files_size(obj_type):
    
    obj_to_reload = []
    
    for obj in getattr(bpy.data, obj_type):

        # Avoid builtin
        if obj.filepath in ["<builtin>", ""]:
            continue
        
        path = bpy.path.abspath(obj.filepath)
        
        # Get new size
        if obj_type == "images":
            new_size = get_image_size(obj, path)
            
        else:
            new_size = get_file_size(obj, path)

        # Reload file size
        if reload_file_size(
            new_size,
            obj,
        ):
            obj_to_reload.append(obj)
            
            
                
    # TODO Deal with sequencer strips
                
    return obj_to_reload


@persistent
def startup_refresh_file_size(scene):
    
    print("AUTORELOAD --- Refreshing external files size")
    for obj_type in object_types:
        get_files_size(obj_type)
        
    print("AUTORELOAD --- Setting autoreload categories")
    props = bpy.context.window_manager.autoreload_properties
    prefs = get_addon_preferences()
    
    for obj_type in object_types:
        setattr(
            props,
            f"autoreload_{obj_type}",
            getattr(prefs, f"startup_{obj_type}"),
        )
    props.autoreload_run = prefs.startup_run
            

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


def update_sound_waveform(sound):
    
    for scn in bpy.data.scenes:
        for strip in scn.sequence_editor.sequences_all:
            if strip.type == "SOUND"\
            and strip.show_waveform\
            and strip.sound == sound:
                strip.show_waveform = True
                
                
def reload_images(image_list):
    
    for img in image_list:
        
        # Hack to prevent pink sequence
        if img.source == "SEQUENCE":
            img.source = "FILE"
            img.reload()
            img.source = "SEQUENCE"
            
        else:
            img.reload()
    
    if image_list:
        update_3d_viewers()
    
        
def reload_movieclips(mov_list):
    
    for mov in mov_list:
        mov.filepath = mov.filepath
        

def reload_sounds(sound_list):
    
    for sound in sound_list:
        sound.filepath = sound.filepath
        update_sound_waveform(sound)
        
        
def reload_libraries(library_list):
    
    for lib in library_list:
        lib.reload()

    
def reload_modified_objects():
    
    props = bpy.context.window_manager.autoreload_properties
    
    obj_to_reload = {}
    
    # Get objects to reload
    for obj_type in object_types:
        obj_to_reload[obj_type] = []
        
        # Check if obj type autoreloaded from property
        if getattr(props, f"autoreload_{obj_type}"):
            obj_to_reload[obj_type] = get_files_size(obj_type)
    
    for obj_type in object_types:
        function = f"reload_{obj_type}(obj_to_reload[obj_type])"
        exec(function)

    # Reload objects
    print("AUTORELOAD --- Objects to reload :")
    print(obj_to_reload)
    print()


def timer_reload_files():
    
    interval = get_addon_preferences().timer_frequency
    
    props = bpy.context.window_manager.autoreload_properties
    
    # Pause
    if not props.autoreload_run:
        return interval
    
    print("AUTORELOAD --- Timer")
    
    reload_modified_objects()

    return interval

    
### REGISTER ---
def register():
    bpy.app.handlers.load_post.append(startup_refresh_file_size)
    bpy.app.timers.register(timer_reload_files, persistent=True)

def unregister():
    bpy.app.handlers.load_post.remove(startup_refresh_file_size)
    bpy.app.timers.unregister(timer_reload_files)
            
            
