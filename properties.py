import bpy


from .timer_function import update_timer_function


# update function for update_needed property
def update_function_updateneeded(self, context):
    if self.autoreload_update_needed:
        wm = context.window_manager

        bpy.ops.autoreload.dialog_popups(
                            'INVOKE_DEFAULT',
                            message = wm.autoreload_update_message,
                            operator = "bpm.open_url",
                            operator_text = "New addon version available",
                            operator_icon = "URL",
                            operator_url = wm.autoreload_update_download_url
                            )


### REGISTER ---

def register():
    bpy.types.Image.autoreload_modification_time = \
        bpy.props.StringProperty(name='File Modification Date', default='')
    bpy.types.Library.autoreload_modification_time = \
        bpy.props.StringProperty(name='File Modification Date', default='')

    bpy.types.WindowManager.autoreload_missing_images = \
        bpy.props.BoolProperty(name='Missing Images')
    bpy.types.WindowManager.autoreload_missing_libraries = \
        bpy.props.BoolProperty(name='Missing Libraries')

    # timer
    bpy.types.WindowManager.autoreload_is_timer = \
        bpy.props.BoolProperty(
            name='Image Timer',
            description="Start Timer to fetch modified Images every n seconds.",
            update=update_timer_function,
            )
    
    # update
    bpy.types.WindowManager.autoreload_update_needed = \
        bpy.props.BoolProperty(
            name='Update Needed',
            update=update_function_updateneeded)
    bpy.types.WindowManager.autoreload_update_message = \
        bpy.props.StringProperty(name='Update Message')
    bpy.types.WindowManager.autoreload_update_download_url = \
        bpy.props.StringProperty(name='Update Download URL')

def unregister():
    del bpy.types.Image.autoreload_modification_time
    del bpy.types.Library.autoreload_modification_time

    del bpy.types.WindowManager.autoreload_missing_images
    del bpy.types.WindowManager.autoreload_missing_libraries

    # timer
    if bpy.context.window_manager.autoreload_is_timer:
        bpy.context.window_manager.autoreload_is_timer = False
    del bpy.types.WindowManager.autoreload_is_timer

    # update
    del bpy.types.WindowManager.autoreload_update_needed
    del bpy.types.WindowManager.autoreload_update_message
    del bpy.types.WindowManager.autoreload_update_download_url