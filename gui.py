import bpy


# File menu
class AUTORELOAD_MT_file_menu(bpy.types.Menu):
    bl_label = "Auto Reload"

    def draw(self, context):
        props = context.window_manager.autoreload_properties

        layout = self.layout
        
        layout.prop(props, "autoreload_images", text="Images")
        layout.prop(props, "autoreload_movieclips", text="Movie Clips")
        layout.prop(props, "autoreload_sounds", text="Sounds")
        layout.prop(props, "autoreload_libraries", text="Libraries")
        layout.prop(props, "autoreload_sequencerstrips", text="Sequencer Strips")
        layout.prop(props, "autoreload_texts", text="Texts")
        layout.prop(props, "autoreload_fonts", text="Fonts")

# File menu drawer
def file_menu_drawer(self, context):
    if context.region.alignment == 'RIGHT':
        layout = self.layout
        self.layout.menu('AUTORELOAD_MT_file_menu', text="AR")


### REGISTER ---
def register():
    bpy.utils.register_class(AUTORELOAD_MT_file_menu)
    bpy.types.TOPBAR_HT_upper_bar.prepend(file_menu_drawer)

def unregister():
    bpy.utils.unregister_class(AUTORELOAD_MT_file_menu)
    bpy.types.TOPBAR_HT_upper_bar.remove(file_menu_drawer)
