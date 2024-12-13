import bpy
import os
import re
from bpy.app.handlers import persistent

from .addon_prefs import get_addon_preferences

# TODO Reload sounds waveform
# TODO Cache files sequence ?
# TODO Add reload for images in sequence strip

object_types = [
    "images",
    "movieclips",
    "sounds",
    "libraries",
    "cache_files",
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
            
    if get_addon_preferences().debug:
        print(
            "AUTORELOAD --- File sequence found for "
            f"{filepath} : {len(seq_files)} files"
        )
    
    return seq_files


def get_image_moddate(image, filepath):
    
    new_moddate = 0
    
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

        new_moddate = get_file_list_moddate(tile_list)
    
    # Sequence
    elif image.source == "SEQUENCE":
        new_moddate = get_file_list_moddate(
            get_filesequence_from_file(filepath)
        )
    
    # Single file
    else:
        
        # Invalid filepath
        if not os.path.isfile(filepath):
            return str(new_moddate)
        
        new_moddate = os.path.getmtime(filepath)
        
    return str(new_moddate)
        
        
def get_file_moddate(object, filepath):
    
    # Invalid filepath
    if not os.path.isfile(filepath):
        return str(0)
    
    # Valid filepath
    else:
        return str(os.path.getmtime(filepath))
    
    
def reload_file_moddate(new_moddate, object):
    
    # Save new file_modif_date
    if new_moddate != object.file_modif_date:

        # Find if images previously been checked
        checked = True
        if object.file_modif_date == 0:
            checked = False
        
        object.file_modif_date = new_moddate
        
        if get_addon_preferences().debug:
            print(
                f"AUTORELOAD --- {object.name} modification date - "
                f"Old:{object.file_modif_date}, New:{new_moddate}"
            )
        
        return checked
    
    return False


def get_file_list_moddate(file_list):
    
    moddate = 0
    
    for filepath in file_list:
        if os.path.isfile:
            moddate += os.path.getmtime(filepath)
            
    return moddate
        

def get_files_moddate(obj_type):
    
    obj_to_reload = []
    
    for obj in getattr(bpy.data, obj_type):

        # Avoid builtin
        if obj.filepath in ["<builtin>", ""]:
            continue
        
        path = bpy.path.abspath(obj.filepath)
        
        # Get new modification date
        if obj_type == "images":
            new_moddate = get_image_moddate(obj, path)
            
        else:
            new_moddate = get_file_moddate(obj, path)
        
        # Reload file modification date
        if reload_file_moddate(
            new_moddate,
            obj,
        ):
            obj_to_reload.append(obj)
                
    return obj_to_reload


@persistent
def startup_refresh_file_moddate(scene):
    
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
    
    print("AUTORELOAD --- Reloading external files")
    reload_modified_objects()
            

def update_3d_viewers():
    
    if get_addon_preferences().debug:
        print("AUTORELOAD --- Updating 3D Viewports")
    
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
        # TODO update_sound_waveform(sound)
        
        
def reload_libraries(library_list):
    
    for lib in library_list:
        lib.reload()
        
        
def reload_cache_files(cache_list):
    
    for cache in cache_list:
        cache.filepath = cache.filepath

    
def reload_modified_objects():
    
    props = bpy.context.window_manager.autoreload_properties
    
    obj_to_reload = {}
    
    # Get objects to reload
    for obj_type in object_types:
        obj_to_reload[obj_type] = []
        
        # Check if obj type autoreloaded from property
        if getattr(props, f"autoreload_{obj_type}"):
            obj_to_reload[obj_type] = get_files_moddate(obj_type)
    
    # Reload objects
    if get_addon_preferences().debug:
        print("AUTORELOAD --- Objects to reload :")
        print(obj_to_reload)
    
    reload_images(obj_to_reload["images"])
    reload_movieclips(obj_to_reload["movieclips"])
    reload_sounds(obj_to_reload["sounds"])
    reload_libraries(obj_to_reload["libraries"])
    reload_cache_files(obj_to_reload["cache_files"])


def timer_reload_files():
    
    interval = get_addon_preferences().timer_frequency
    
    props = bpy.context.window_manager.autoreload_properties
    
    # Pause
    if not props.autoreload_run:
        return interval
    
    if get_addon_preferences().debug:
        print("AUTORELOAD --- Timer")
    
    reload_modified_objects()

    return interval

    
### REGISTER ---
def register():
    bpy.app.handlers.load_post.append(startup_refresh_file_moddate)
    bpy.app.timers.register(timer_reload_files, persistent=True)

def unregister():
    bpy.app.handlers.load_post.remove(startup_refresh_file_moddate)
    bpy.app.timers.unregister(timer_reload_files)
            
            
