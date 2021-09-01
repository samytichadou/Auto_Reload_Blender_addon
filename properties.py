import bpy


### REGISTER ---

def register():
    bpy.types.Image.modification_time = \
        bpy.props.StringProperty(name='File Modification Date', default='')
    bpy.types.Library.modification_time = \
        bpy.props.StringProperty(name='File Modification Date', default='')
    bpy.types.Library.to_reload = \
        bpy.props.BoolProperty()
    bpy.types.WindowManager.reload_modal = \
        bpy.props.BoolProperty(name='AutoReload Timer')
    bpy.types.WindowManager.autoreloadMissingImages = \
        bpy.props.BoolProperty(name='AutoReload Missing Images')
    bpy.types.WindowManager.autoreloadMissingLibraries = \
        bpy.props.BoolProperty(name='AutoReload Missing Libraries')

def unregister():
    del bpy.types.Image.modification_time
    del bpy.types.Library.modification_time
    del bpy.types.Library.to_reload
    del bpy.types.WindowManager.reload_modal
    del bpy.types.WindowManager.autoreloadMissingImages
    del bpy.types.WindowManager.autoreloadMissingLibraries