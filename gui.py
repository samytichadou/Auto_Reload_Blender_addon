import bpy


# File menu
class AUTORELOAD_PT_file_popover(bpy.types.Panel):
    bl_label = "Auto Reload"
    bl_space_type = 'TOPBAR'
    bl_region_type = 'HEADER'
    bl_ui_units_x = 8

    def draw(self, context):
        props = context.window_manager.autoreload_properties

        layout = self.layout
        
        col = layout.column(align = True)
        
        row = col.row()
        row.prop(props, "autoreload_select_all", text="All")
        op = row.operator("autoreload.reload", text="", icon="FILE_REFRESH", emboss=False)
        op.behavior = "all"
        
        col.separator()
        
        row = col.row()
        row.prop(props, "autoreload_images", text="Images")
        op = row.operator("autoreload.reload", text="", icon="FILE_REFRESH", emboss=False)
        op.behavior = "images"
        
        row = col.row()
        row.prop(props, "autoreload_movieclips", text="Movie Clips")
        op = row.operator("autoreload.reload", text="", icon="FILE_REFRESH", emboss=False)
        op.behavior = "movieclips"
        
        row = col.row()
        row.prop(props, "autoreload_sounds", text="Sounds")
        op = row.operator("autoreload.reload", text="", icon="FILE_REFRESH", emboss=False)
        op.behavior = "sounds"
        
        row = col.row()
        row.prop(props, "autoreload_libraries", text="Libraries")
        op = row.operator("autoreload.reload", text="", icon="FILE_REFRESH", emboss=False)
        op.behavior = "libraries"
        
        row = col.row()
        row.prop(props, "autoreload_cache_files", text="Cache Files")
        op = row.operator("autoreload.reload", text="", icon="FILE_REFRESH", emboss=False)
        op.behavior = "cache_files"
        
        
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
            panel="AUTORELOAD_PT_file_popover",
            text="AR",
            )


### REGISTER ---
def register():
    bpy.utils.register_class(AUTORELOAD_PT_file_popover)
    bpy.types.TOPBAR_HT_upper_bar.prepend(file_menu_drawer)

def unregister():
    bpy.utils.unregister_class(AUTORELOAD_PT_file_popover)
    bpy.types.TOPBAR_HT_upper_bar.remove(file_menu_drawer)
