import bpy
import os

from .addon_prefs import get_addon_preferences
from .functions import absolute_path
from .global_variables import avoid_images

class AUTORELOAD_UL_uilist(bpy.types.UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, flt_flag) :
        row = layout.row(align = True)
        if item.name not in avoid_images :
            row.prop(item, "name", text="", emboss=False)
            if os.path.isfile(absolute_path(item.filepath)):
                op=row.operator("autorelad.reveal_explorer", text="", icon='ZOOM_ALL')
                op.path = item.filepath
                op2=row.operator("autorelad.open_image", text="", icon='GREASEPENCIL')
                op2.path = item.filepath
            else:
                row.label(text='', icon="ERROR")
        else :
            row.label(text=item.name, icon="LOCKED")