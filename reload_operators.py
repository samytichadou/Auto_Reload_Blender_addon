import bpy

from . import global_variables
from . import functions


class AUTORELOAD_OT_reload_images(bpy.types.Operator):
    bl_idname = "autoreload.reload_images"
    bl_label = "Reload Images"
    bl_description = "Reload Images in the blend if modified."
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        props = context.window_manager.autoreload_properties

        modified_list, missing_list = functions.reload_modified_images()

        if len(missing_list) == 0:
            props.autoreload_missing_images = False
        else:
            props.autoreload_missing_images = True

        if len(modified_list)!=0:
            functions.update_viewers(context)
            functions.update_textures(modified_list)
            functions.update_strips(modified_list)

        for m in modified_list:
            print(global_variables.print_statement + m + global_variables.reloaded_msg)

        for m in missing_list:
            print(global_variables.print_statement + m + global_variables.missing_msg)

        if len(modified_list)==0 and len(missing_list)==0:
            print(global_variables.no_modif_statement)

        return {"FINISHED"}


class AUTORELOAD_OT_check_libraries(bpy.types.Operator):
    bl_idname = "autoreload.check_libraries"
    bl_label = "Check Libraries"
    bl_description = "Check if external libraries has changed."
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.data.libraries:
            return True

    def execute(self, context):
        wm = context.window_manager

        modified_list, missing_list = functions.check_libraries()

        if len(missing_list) == 0:
            wm.autoreload_properties.autoreload_missing_libraries = False
        else:
            wm.autoreload_properties.autoreload_missing_libraries = True

        for m in modified_list:
            print(global_variables.print_statement + m + global_variables.modified_msg)
        for m in missing_list:
            print(global_variables.print_statement + m + global_variables.missing_msg)

        return {"FINISHED"}


class AUTORELOAD_OT_reload_library(bpy.types.Operator):
    bl_idname = "autoreload.reload_library"
    bl_label = "Reload Library"
    bl_description = "Reload this external library."
    bl_options = {"INTERNAL", "UNDO"}

    name : bpy.props.StringProperty()

    def execute(self, context):
        functions.reload_library(self.name)
        return {"FINISHED"}


class AUTORELOAD_OT_save_revert(bpy.types.Operator):
    bl_idname = "autoreload.save_revert"
    bl_label = "Save and Revert"
    bl_description = "Save file and revert to reload all Libraries and Images."
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return bpy.data.is_saved

    def execute(self, context):
        bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
        bpy.ops.wm.revert_mainfile()
        return {"FINISHED"}


### REGISTER ---

def register():
    bpy.utils.register_class(AUTORELOAD_OT_reload_images)
    bpy.utils.register_class(AUTORELOAD_OT_check_libraries)
    bpy.utils.register_class(AUTORELOAD_OT_reload_library)
    bpy.utils.register_class(AUTORELOAD_OT_save_revert)

def unregister():
    bpy.utils.unregister_class(AUTORELOAD_OT_reload_images)
    bpy.utils.unregister_class(AUTORELOAD_OT_check_libraries)
    bpy.utils.unregister_class(AUTORELOAD_OT_reload_library)
    bpy.utils.unregister_class(AUTORELOAD_OT_save_revert)