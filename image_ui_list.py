import bpy
import os

from .functions import absolute_path

class AUTORELOAD_UL_images_uilist(bpy.types.UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, flt_flag) :
        row = layout.row(align = True)

        # internal files
        if item.source in {'VIEWER','GENERATED'} \
        or not item.filepath:
            row.label(text=item.name, icon="LOCKED")

        # external files
        else:
            
            row.prop(item, "name", text="", emboss=False)

            if item.autoreload_modification_time != "missing":
                op=row.operator("autorelad.reveal_explorer", text="", icon='ZOOM_ALL')
                op.path = item.filepath
                op2=row.operator("autorelad.modify_image", text="", icon='GREASEPENCIL')
                op2.path = item.filepath
            else:
                row.label(text='', icon="ERROR")



### REGISTER ---

def register():
    bpy.utils.register_class(AUTORELOAD_UL_images_uilist)

def unregister():
    bpy.utils.unregister_class(AUTORELOAD_UL_images_uilist)