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
        row = layout.row(align=True)
        row.operator('reload.reload_all', text='',
                     icon='FILE_REFRESH')
        if bpy.data.window_managers['WinMan'].reload_modal == True:
            row.prop(bpy.data.window_managers['WinMan'],
                     'reload_modal', text='', icon='CANCEL')
        else:
            row.operator('reload.reload_timer', text='', icon='TIME')
