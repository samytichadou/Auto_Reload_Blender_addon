import bpy


### REGISTER ---

def register():
    bpy.types.Image.autoreload_modification_time = \
        bpy.props.StringProperty(name='File Modification Date', default='')
    bpy.types.Library.autoreload_modification_time = \
        bpy.props.StringProperty(name='File Modification Date', default='')

    bpy.types.WindowManager.autoreload_reload_modal = \
        bpy.props.BoolProperty(name='Auto Reload Timer')

    bpy.types.WindowManager.autoreload_missing_images = \
        bpy.props.BoolProperty(name='Auto Reload Missing Images')
    bpy.types.WindowManager.autoreload_missing_libraries = \
        bpy.props.BoolProperty(name='Auto Reload Missing Libraries')

    bpy.types.WindowManager.autoreload_is_timer = \
        bpy.props.BoolProperty(name='Auto Reload Timer')

def unregister():
    del bpy.types.Image.autoreload_modification_time
    del bpy.types.Library.autoreload_modification_time
   
    del bpy.types.WindowManager.autoreload_reload_modal

    del bpy.types.WindowManager.autoreload_missing_images
    del bpy.types.WindowManager.autoreload_missing_libraries

    del bpy.types.WindowManager.autoreload_is_timer