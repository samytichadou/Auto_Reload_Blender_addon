import bpy

from .global_variables import avoid_images

class AUTORELOAD_PT_scenepanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the scene editor"""
    bl_label = "Auto Reload Image"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True # Active single-column layout
        flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=True, align=False)

        row = flow.row(align=True)
        row.operator('autoreload.reload_images', icon='FILE_REFRESH', text='Reload Images')

        row = flow.row(align=True)
        row.operator('autoreload.reload_timer', icon='TIME', text='Start Timer')
        
        if bpy.data.window_managers['WinMan'].reload_modal :
            row.prop(bpy.data.window_managers['WinMan'], 'reload_modal', text = "", icon='CANCEL')

class AUTORELOAD_PT_scenepanel_inspector(bpy.types.Panel):
    """Creates a Panel in the scene context of the scene editor"""
    bl_label = "Inspector"
    bl_parent_id = "AUTORELOAD_PT_scenepanel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        wm = bpy.data.window_managers['WinMan']

        layout = self.layout

        layout.template_list("AUTORELOAD_UL_uilist", "", bpy.data, "images", wm, "autoreload_index", rows = 3)
        if bpy.data.images[wm.autoreload_index].name not in avoid_images:
            layout.prop(bpy.data.images[wm.autoreload_index], 'filepath', text='')