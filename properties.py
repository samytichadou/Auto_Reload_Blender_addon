import bpy


### REGISTER ---

def register():
    bpy.types.Image.autoreload_modification_time = \
        bpy.props.StringProperty(name='File Modification Date', default='')
    bpy.types.Library.autoreload_modification_time = \
        bpy.props.StringProperty(name='File Modification Date', default='')
    bpy.types.Library.autoreload_to_reload = \
        bpy.props.BoolProperty()
    bpy.types.WindowManager.reload_modal = \
        bpy.props.BoolProperty(name='AutoReload Timer')
    bpy.types.WindowManager.autoreload_missing_images = \
        bpy.props.BoolProperty(name='AutoReload Missing Images')
    bpy.types.WindowManager.autoreload_missing_libraries = \
        bpy.props.BoolProperty(name='AutoReload Missing Libraries')

def unregister():
    del bpy.types.Image.autoreload_modification_time
    del bpy.types.Library.autoreload_modification_time
    del bpy.types.Library.autoreload_to_reload
    del bpy.types.WindowManager.reload_modal
    del bpy.types.WindowManager.autoreload_missing_images
    del bpy.types.WindowManager.autoreload_missing_libraries