import bpy

# TODO Update timer function if timer_frequency modified

class AUTORELOAD_PF_addon_prefs(bpy.types.AddonPreferences):
    bl_idname = __package__
    
    timer_frequency: bpy.props.FloatProperty(
        name = 'Check Timer Frequency (s)', 
        precision = 1, 
        min = 0.1, 
        max = 3600.0, 
        default = 5.0, 
        description = "Frequency for checking modified files in seconds.",
        )
    
    startup_images : bpy.props.BoolProperty(
        name='Autoreload Images',
        default = True,
        )
    startup_movieclips : bpy.props.BoolProperty(
        name='Autoreload Movie Clips',
        )
    startup_sounds : bpy.props.BoolProperty(
        name='Autoreload Sounds',
        )
    startup_libraries : bpy.props.BoolProperty(
        name='Autoreload Libraries',
        )
    startup_cache_files : bpy.props.BoolProperty(
        name='Autoreload Cache Files',
        )
    startup_run : bpy.props.BoolProperty(
        name='Autoreload Run',
        )
    debug : bpy.props.BoolProperty(
        name='Debug',
        )

    def draw(self, context):
        layout = self.layout
        
        row = layout.row()
        sub = row.row()
        sub.alignment = "LEFT"
        sub.prop(self, "timer_frequency")
        sub = row.row()
        sub.alignment = "RIGHT"
        sub.prop(self, "debug")
        
        col = layout.column(align=True)
        
        col.label(text="On startup :")
        
        col.prop(self, "startup_run")
        col.separator()
        col.prop(self, "startup_images")
        col.prop(self, "startup_movieclips")
        col.prop(self, "startup_sounds")
        col.prop(self, "startup_libraries")
        col.prop(self, "startup_cache_files")
        

        
# get addon preferences
def get_addon_preferences():
    addon = bpy.context.preferences.addons.get(__package__)
    return getattr(addon, "preferences", None)


### REGISTER ---
def register():
    bpy.utils.register_class(AUTORELOAD_PF_addon_prefs)

def unregister():
    bpy.utils.unregister_class(AUTORELOAD_PF_addon_prefs)
