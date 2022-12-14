import bpy


from .timer_function import update_timer_function
from .global_variables import preview_texture


# update function for update_needed property
def update_function_updateneeded(self, context):
    if self.autoreload_update_needed:
        bpy.ops.autoreload.dialog_popups(
            'INVOKE_DEFAULT',
            message = self.autoreload_update_message,
            operator = "wm.url_open",
            operator_text = "New addon version available",
            operator_icon = "URL",
            operator_url = self.autoreload_update_download_url
            )


# create preview texture if needed
def create_preview_texture():
    try:
        bpy.data.textures[preview_texture]
    except KeyError:
        bpy.data.textures.new(preview_texture, "IMAGE")


# remove preview texture if needed
def remove_preview_texture():
    try:
        bpy.data.textures.remove(bpy.data.textures[preview_texture])
    except KeyError:
        pass


# update image preview functions
def update_image_preview(self, context):
    create_preview_texture()
    texture = bpy.data.textures[preview_texture]
    texture.image = bpy.data.images[self.autoreload_active_image_index]


class AUTORELOAD_PR_properties(bpy.types.PropertyGroup) :

    # inspectors
    autoreload_active_image_index : bpy.props.IntProperty(
        name='Image Index',
        update=update_image_preview,
        )
    autoreload_active_library_index : bpy.props.IntProperty(name='Library Index')
    
    # timer
    autoreload_is_timer : bpy.props.BoolProperty(
        name='Image Timer',
        description="Start Timer to fetch modified Images every n seconds.",
        update=update_timer_function,
        )

    # update
    autoreload_update_needed : bpy.props.BoolProperty(
        name='Update Needed',
        update=update_function_updateneeded,
        )
    autoreload_update_message : bpy.props.StringProperty(name='Update Message')
    autoreload_update_download_url : bpy.props.StringProperty(name='Update Download URL')

    # image editor
    autoreload_is_editor_executable : bpy.props.BoolProperty(name='Is Image Editor available')


### REGISTER ---

def register():
    bpy.utils.register_class(AUTORELOAD_PR_properties)

    bpy.types.WindowManager.autoreload_properties = \
        bpy.props.PointerProperty(type = AUTORELOAD_PR_properties, name="Auto Reload Properties")

    bpy.types.Image.autoreload_modification_time = \
        bpy.props.StringProperty(name='File Modification Date', default='')
    bpy.types.Library.autoreload_modification_time = \
        bpy.props.StringProperty(name='File Modification Date', default='')
    bpy.types.Library.autoreload_modified = \
        bpy.props.BoolProperty(name='Library modified')
    bpy.types.Library.autoreload_automatically_reload = \
        bpy.props.BoolProperty(name='Automatically reload')

def unregister():
    if bpy.context.window_manager.autoreload_properties.autoreload_is_timer:
        bpy.context.window_manager.autoreload_properties.autoreload_is_timer = False

    del bpy.types.WindowManager.autoreload_properties

    bpy.utils.unregister_class(AUTORELOAD_PR_properties)

    del bpy.types.Image.autoreload_modification_time
    del bpy.types.Library.autoreload_modification_time
    del bpy.types.Library.autoreload_modified
    del bpy.types.Library.autoreload_automatically_reload

    remove_preview_texture()