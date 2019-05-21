import bpy


class MenuPanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "Auto Reload Image"
    bl_idname = "SCENE_PT_AutoReloadImage"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True # Active single-column layout
        flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=True, align=False)

        row = flow.row(align=True)
        row.operator('reload.reload_all',
                     icon='FILE_REFRESH')
        row = flow.row(align=True)
        row.operator('reload.reload_timer', icon='TIME')
        if bpy.data.window_managers['WinMan'].reload_modal :
            row.prop(bpy.data.window_managers['WinMan'],
                     'reload_modal', text = "", icon='CANCEL')

            
