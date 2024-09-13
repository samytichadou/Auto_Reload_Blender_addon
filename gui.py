import bpy


# File menu
class AUTORELOAD_MT_file_menu(bpy.types.Menu):
    bl_label = "Auto Reload"

    def draw(self, context):
        props = context.window_manager.autoreload_properties

        layout = self.layout
        
        layout.label(text = "Images")
        layout.label(text = "Texts")
        layout.label(text = "Movie Clips")
        layout.label(text = "Sounds")
        layout.label(text = "Sequencer Strips")
        layout.label(text = "Fonts")
        

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
