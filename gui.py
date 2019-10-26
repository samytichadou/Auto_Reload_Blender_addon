import bpy

class AUTORELOAD_PT_scenepanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the scene editor"""
    bl_label = "Auto Reload"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    def draw(self, context):
        wm = bpy.context.window_manager
        layout = self.layout
        layout.use_property_split = True # Active single-column layout

        flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=True, align=False)
        row = flow.row(align=True)
        row.operator('autoreload.reload_datas', icon='FILE_REFRESH', text='Reload Datas')
        row = flow.row(align=True)
        row.operator('autoreload.reload_timer', icon='TIME', text='Start Timer')
        if bpy.data.window_managers['WinMan'].reload_modal :
            row.prop(wm, 'reload_modal', text = "", icon='CANCEL')
        box = layout.box()
        flow = box.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=True, align=True)
        row = flow.row(align=True)
        row.prop(wm, 'autoreloadImages', text="Images")
        row = flow.row(align=True)
        row.prop(wm, 'autoreloadLibraries', text="Libraries")
        flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=True, align=True)
        if wm.autoreloadMissingImages:
            row = flow.row()
            row.label(text="Missing Images", icon='ERROR')
        if wm.autoreloadMissingLibraries:
            row = flow.row()
            row.label(text="Missing Libraries", icon='ERROR')