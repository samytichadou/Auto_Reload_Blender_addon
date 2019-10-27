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

        box = layout.box()
        box.label(text="Images")
        flow = box.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=True, align=False)
        row = flow.row(align=True)
        row.operator('autoreload.reload_images', icon='FILE_REFRESH', text='Reload')
        row = flow.row(align=True)
        row.operator('autoreload.reload_images_timer', icon='TIME', text='Timer')
        if bpy.data.window_managers['WinMan'].reload_modal :
            row.prop(wm, 'reload_modal', text = "", icon='CANCEL')
        if wm.autoreloadMissingImages:
            row = box.row(align=True)
            row.label(text="Missing Images", icon='ERROR')

        box = layout.box()
        box.label(text="Libraries")
        flow = box.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=True, align=False)
        row = flow.row(align=True)
        row.operator('autoreload.check_libraries', icon='BLENDER')
        row = flow.row(align=True)
        row.operator('autoreload.save_revert', icon='FILE_TICK')
        for l in bpy.data.libraries:
            row=box.row(align=True)
            row.label(text=l.name)
            if l.to_reload and l.modification_time!="missing":
                prop = row.operator('autoreload.reload_library', text="", icon="FILE_REFRESH")
                prop.name = l.name
            elif l.modification_time=="missing": row.label(text="", icon="ERROR")
        if wm.autoreloadMissingLibraries:
            row = box.row()
            row.label(text="Missing Libraries", icon='ERROR')