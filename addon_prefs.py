import bpy
import os

from .gui import draw_update_button

addon_name = os.path.basename(os.path.dirname(__file__))


# update function for external image editor prop
def update_image_executable(self, context):
        props = context.window_manager.autoreload_properties
        if os.path.isfile(self.image_executable):
                props.autoreload_is_editor_executable = True
        else:
                props.autoreload_is_editor_executable = False


class AUTORELOAD_PT_addon_prefs(bpy.types.AddonPreferences):
    bl_idname = addon_name
    
    check_frequency : bpy.props.FloatProperty(
            name = 'Image Timer Frequency (s)', 
            precision = 1, 
            min = 0.1, 
            max = 3600.0, 
            default = 3.0, 
            description = "Frequency for fetching for modified Images in seconds.",
            )

    startup_launch : bpy.props.BoolProperty(
            name = "Launch Image Reload Timer on Startup",
            description = "Launch Image Timer on every Blender startup to fetch modified images.",
            )

    timer_libraries : bpy.props.BoolProperty(
            name = "Include Libraries Check in the Reload Timer",
            description = "Also check for modified Libraries through the Reload Timer, then update them manually.",
            default = True
            )

    update_check_launch : bpy.props.BoolProperty(
            name = "Check for Updates on Startup",
            description = "Check online for new version of the Addon on every Blender startup.",
            default = True, 
            )

    image_executable : bpy.props.StringProperty(
            name = "Image Editor",
            description = "Path to the Executable of the Image Editor used to modify images.",
            subtype = "FILE_PATH",
            update = update_image_executable,
            )


    def draw(self, context):
        props = context.window_manager.autoreload_properties
        
        layout = self.layout

        layout.prop(self, "check_frequency")
        
        row = layout.row(align=True)
        if not props.autoreload_is_editor_executable:
                row.label(text="", icon="ERROR")
        row.prop(self, "image_executable")

        # startup
        col = layout.column(align=True)
        col.prop(self, "startup_launch")
        col.prop(self, "timer_libraries")
        col.prop(self, "update_check_launch")

        # updates
        col.separator()
        col.operator("autoreload.check_addon_updates")
        draw_update_button(context, col)

        
# get addon preferences
def get_addon_preferences():
    addon = bpy.context.preferences.addons.get(addon_name)
    return getattr(addon, "preferences", None)


### REGISTER ---

def register():
    bpy.utils.register_class(AUTORELOAD_PT_addon_prefs)

def unregister():
    bpy.utils.unregister_class(AUTORELOAD_PT_addon_prefs)