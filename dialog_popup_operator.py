import bpy


class AUTORELOAD_OT_dialog_popups(bpy.types.Operator):
    bl_idname = "autoreload.dialog_popups"
    bl_label = "Auto Reload Infos"
    bl_options = {'INTERNAL'}
 
    message : bpy.props.StringProperty()
    icon : bpy.props.StringProperty()
    operator : bpy.props.StringProperty()
    operator_text : bpy.props.StringProperty()
    operator_icon : bpy.props.StringProperty()
    operator_url : bpy.props.StringProperty()
 
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
 
    def draw(self, context):
        
        layout = self.layout

        if self.message:
            row = layout.row()
            row.label(text = self.message)
        
            if self.icon:
                row.label(text = "", icon = self.icon)

        if self.operator:
            row = layout.row()

            if self.operator_text and self.operator_icon:
                op = row.operator(self.operator, text = self.operator_text, icon = self.operator_icon)

            elif self.operator_text:
                op = row.operator(self.operator, text = self.operator_text)

            elif self.operator_icon:
                op = row.operator(self.operator, icon = self.operator_icon)

            else:
                op = row.operator(self.operator)

            if self.operator_url:
                op.url = self.operator_url
            

    def execute(self, context):
        return {'FINISHED'}


### REGISTER ---

def register():
    bpy.utils.register_class(AUTORELOAD_OT_dialog_popups)

def unregister():
    bpy.utils.unregister_class(AUTORELOAD_OT_dialog_popups)