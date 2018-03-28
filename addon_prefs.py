import bpy
import os

addon_name = os.path.basename(os.path.dirname(__file__))

class Reload_AddonPrefs(bpy.types.AddonPreferences):
    bl_idname = addon_name
    
    check_frequency = bpy.props.FloatProperty(name='Checking Frequency', precision=2, min=0.01, max=3600.00, default=1, description='Frequency for checking for modified Images in seconds')

    def draw(self, context):
        layout = self.layout
        row=layout.row()
        row.prop(self, "check_frequency", text='Checking Frequency in seconds')
        


# get addon preferences
def get_addon_preferences():
    addon = bpy.context.user_preferences.addons.get(addon_name)
    return getattr(addon, "preferences", None)