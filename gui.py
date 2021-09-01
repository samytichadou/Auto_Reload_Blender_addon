import bpy

class AUTORELOAD_PT_libraries_panel(bpy.types.Panel):
    """Creates a Panel in the scene context of the scene editor"""
    bl_label = "Reload Libraries"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    def draw(self, context):
        wm = context.window_manager

        layout = self.layout

        layout.use_property_split = True # Active single-column layout
        flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=True, align=False)

        row = flow.row(align=True)
        row.operator('autoreload.check_libraries', icon='BLENDER')

        row = flow.row(align=True)
        row.operator('autoreload.save_revert', icon='FILE_TICK')

        for l in bpy.data.libraries:
            row=layout.row(align=True)
            row.label(text=l.name)
            if l.autoreload_to_reload and l.autoreload_modification_time!="missing":
                prop = row.operator('autoreload.reload_library', text="", icon="FILE_REFRESH")
                prop.name = l.name
            elif l.autoreload_modification_time=="missing": row.label(text="", icon="ERROR")
            
        if wm.autoreload_missing_libraries:
            row = layout.row()
            row.label(text="Missing Libraries", icon='ERROR')


# file menu
class AUTORELOAD_MT_file_menu(bpy.types.Menu):
    bl_label = "Auto Reload"

    def draw(self, context):
        wm = context.window_manager

        layout = self.layout
        
        layout.prop(wm, 'autoreload_is_timer', text = "Timer", icon='TIME')
        layout.operator('autoreload.reload_images', icon='FILE_REFRESH')


# file menu drawer
def file_menu_drawer(self, context):
    layout = self.layout
    
    self.layout.separator()
    self.layout.menu('AUTORELOAD_MT_file_menu')


### REGISTER ---

def register():
    bpy.utils.register_class(AUTORELOAD_PT_libraries_panel)
    bpy.utils.register_class(AUTORELOAD_MT_file_menu)

    bpy.types.TOPBAR_MT_file.append(file_menu_drawer)

def unregister():
    bpy.utils.unregister_class(AUTORELOAD_PT_libraries_panel)
    bpy.utils.unregister_class(AUTORELOAD_MT_file_menu)

    bpy.types.TOPBAR_MT_file.remove(file_menu_drawer)