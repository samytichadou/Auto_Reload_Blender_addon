import bpy

from .reload import object_types


def select_all_callback(self, context):
    value = self.autoreload_select_all
    for obj_type in object_types:
        setattr(self, f"autoreload_{obj_type}", value)

class AUTORELOAD_PR_properties(bpy.types.PropertyGroup) :
    
    # Timers type
    autoreload_images : bpy.props.BoolProperty(
        name = 'Autoreload Images',
    )
    autoreload_movieclips : bpy.props.BoolProperty(
        name = 'Autoreload Movie Clips',
    )
    autoreload_sounds : bpy.props.BoolProperty(
        name = 'Autoreload Sounds',
    )
    autoreload_libraries : bpy.props.BoolProperty(
        name = 'Autoreload Libraries',
    )
    autoreload_cache_files : bpy.props.BoolProperty(
        name = 'Autoreload Cache Files',
        )
    
    autoreload_run : bpy.props.BoolProperty(
        name = "Autoreload Run",
    )
    
    autoreload_select_all : bpy.props.BoolProperty(
        name = 'Autoreload Select All',
        update = select_all_callback,
        )


### REGISTER ---

def register():
    bpy.utils.register_class(AUTORELOAD_PR_properties)
    bpy.types.WindowManager.autoreload_properties = \
        bpy.props.PointerProperty(type = AUTORELOAD_PR_properties, name="Auto Reload Properties")
    
    bpy.types.Image.file_modif_date = \
        bpy.props.StringProperty(name="File Modification Date")
    bpy.types.MovieClip.file_modif_date = \
        bpy.props.StringProperty(name="File Modification Date")
    bpy.types.Sound.file_modif_date = \
        bpy.props.StringProperty(name="File Modification Date")
    bpy.types.Library.file_modif_date = \
        bpy.props.StringProperty(name="File Modification Date")
    bpy.types.CacheFile.file_modif_date = \
        bpy.props.StringProperty(name="File Modification Date")

def unregister():
    bpy.utils.unregister_class(AUTORELOAD_PR_properties)
    del bpy.types.WindowManager.autoreload_properties
    
    del bpy.types.Image.file_modif_date
    del bpy.types.MovieClip.file_modif_date
    del bpy.types.Sound.file_modif_date
    del bpy.types.Library.file_modif_date
    del bpy.types.CacheFile.file_modif_date
