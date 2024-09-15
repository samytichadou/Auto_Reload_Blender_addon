import bpy


# File menu
class AUTORELOAD_MT_file_popover(bpy.types.Panel):
    bl_label = "Auto Reload"
    bl_space_type = 'TOPBAR'
    bl_region_type = 'HEADER'
    bl_ui_units_x = 8

    def draw(self, context):
        props = context.window_manager.autoreload_properties

        layout = self.layout
        
        layout.prop(props, "autoreload_images", text="Images")
        layout.prop(props, "autoreload_movieclips", text="Movie Clips")
        layout.prop(props, "autoreload_sounds", text="Sounds")
        layout.prop(props, "autoreload_libraries", text="Libraries")
        layout.prop(props, "autoreload_cache_files", text="Cache Files")

# File menu drawer
def file_menu_drawer(self, context):
    if context.region.alignment == 'RIGHT':
        row= self.layout.row(align=True)
        
        props = context.window_manager.autoreload_properties
            
        row.prop(
            props,
            "autoreload_run",
            text="",
            icon="TIME",
        )
        row.popover(
            panel="AUTORELOAD_MT_file_popover",
            text="AR",
            )
        # self.layout.menu('AUTORELOAD_MT_file_menu', text="AR")


### REGISTER ---
def register():
    bpy.utils.register_class(AUTORELOAD_MT_file_popover)
    bpy.types.TOPBAR_HT_upper_bar.prepend(file_menu_drawer)

def unregister():
    bpy.utils.unregister_class(AUTORELOAD_MT_file_popover)
    bpy.types.TOPBAR_HT_upper_bar.remove(file_menu_drawer)
