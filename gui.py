import bpy

#menu draw
def reload_menu_draw(self, context):
    layout = self.layout
    row=layout.row(align=True)
    row.operator('reload.reload_all', text='', icon='FILE_REFRESH', emboss=False)
    if bpy.data.window_managers['WinMan'].reload_modal==True:
        row.prop(bpy.data.window_managers['WinMan'], 'reload_modal', text='', icon='CANCEL')
    else:
        row.operator('reload.reload_timer', text='', icon='TIME', emboss=False)