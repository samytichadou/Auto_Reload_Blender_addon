import bpy
import os

from .functions import absolute_path

# Images
class AUTORELOAD_UL_images_uilist(bpy.types.UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, flt_flag) :
        row = layout.row(align = True)

        # internal files
        if item.source in {'VIEWER','GENERATED'} \
        or not item.filepath:
            row.label(text=item.name, icon="LOCKED")

        # external files
        else:
            
            if item.autoreload_modification_time == "missing":
                row.label(text='', icon="ERROR")              
                row.prop(item, "name", text="", emboss=False)

            else:

                row.prop(item, "name", text="", emboss=False)

                op=row.operator("autorelad.reveal_explorer", text="", icon='ZOOM_ALL')
                op.name = item.name
                op.library = False

                op=row.operator("autorelad.modify_image", text="", icon='GREASEPENCIL')
                op.name = item.name

            op=row.operator("autorelad.remove_image", text="", icon="X")
            op.name = item.name


# Libraries
class AUTORELOAD_UL_libraries_uilist(bpy.types.UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, flt_flag) :
        row = layout.row(align = True)
            
        if item.autoreload_modification_time == "missing":
            row.label(text='', icon="ERROR")
            row.prop(item, "name", text="", emboss=False)

        else:

            if item.autoreload_to_reload:
                row.label(text="", icon="FILE_CACHE")
            
            row.prop(item, "name", text="", emboss=False)

            op=row.operator("autorelad.reveal_explorer", text="", icon='ZOOM_ALL')
            op.name = item.name
            op.library = True

            op = row.operator('autorelad.open_library', text="", icon="BLENDER")
            op.name = item.name

            op = row.operator('autoreload.reload_library', text="", icon="FILE_REFRESH")
            op.name = item.name

        op=row.operator("autorelad.remove_library", text="", icon="X")
        op.name = item.name


### REGISTER ---

def register():
    bpy.utils.register_class(AUTORELOAD_UL_images_uilist)
    bpy.utils.register_class(AUTORELOAD_UL_libraries_uilist)

def unregister():
    bpy.utils.unregister_class(AUTORELOAD_UL_images_uilist)
    bpy.utils.unregister_class(AUTORELOAD_UL_libraries_uilist)