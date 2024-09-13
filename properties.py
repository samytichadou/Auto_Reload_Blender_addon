import bpy


class AUTORELOAD_PR_properties(bpy.types.PropertyGroup) :
    
    # Timers type
    autoreload_images : bpy.props.BoolProperty(
        name='Autoreload Images',
        )
    autoreload_texts : bpy.props.BoolProperty(
        name='Autoreload Texts',
        )
    autoreload_movie_clips : bpy.props.BoolProperty(
        name='Autoreload Movie Clips',
        )
    autoreload_sounds : bpy.props.BoolProperty(
        name='Autoreload Sounds',
        )
    autoreload_sequencer_strips : bpy.props.BoolProperty(
        name='Autoreload Sequencer Strips',
        )
    autoreload_fonts : bpy.props.BoolProperty(
        name='Autoreload Fonts',
        )


### REGISTER ---

def register():
    bpy.utils.register_class(AUTORELOAD_PR_properties)
    bpy.types.WindowManager.autoreload_properties = \
        bpy.props.PointerProperty(type = AUTORELOAD_PR_properties, name="Auto Reload Properties")

def unregister():
    bpy.utils.unregister_class(AUTORELOAD_PR_properties)
    del bpy.types.WindowManager.autoreload_properties
