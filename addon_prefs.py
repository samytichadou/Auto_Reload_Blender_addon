import bpy
import os

from .gui import draw_update_button

addon_name = os.path.basename(os.path.dirname(__file__))

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

    update_check_launch : bpy.props.BoolProperty(
            name = "Check for Updates on Startup",
            default = True, 
            description = "Check online for new version of the Addon on every Blender startup.",
            )

    image_executable : bpy.props.StringProperty(
            name = "Image Editor Executable path",
            description = "Path to the Executable of Image Editor used to modify images.",
            subtype = "FILE_PATH",
            )


    def draw(self, context):
        layout = self.layout

        layout.prop(self, "check_frequency")

        layout.prop(self, "image_executable")

        # startup
        col = layout.column(align=True)
        col.prop(self, "startup_launch")
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