import bpy

# TODO Update timer function if timer_frequency modified

class AUTORELOAD_PF_addon_prefs(bpy.types.AddonPreferences):
    bl_idname = __package__
    
    timer_frequency: bpy.props.FloatProperty(
        name = 'Image Timer Frequency (s)', 
        precision = 1, 
        min = 0.1, 
        max = 3600.0, 
        default = 5.0, 
        description = "Frequency for fetching for modified Images in seconds.",
        )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "timer_frequency")

        
# get addon preferences
def get_addon_preferences():
    addon = bpy.context.preferences.addons.get(__package__)
    return getattr(addon, "preferences", None)


### REGISTER ---
def register():
    bpy.utils.register_class(AUTORELOAD_PF_addon_prefs)

def unregister():
    bpy.utils.unregister_class(AUTORELOAD_PF_addon_prefs)
