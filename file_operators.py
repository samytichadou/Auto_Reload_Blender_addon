import bpy
import os
import platform
import subprocess

from . import functions
from .addon_prefs import get_addon_preferences
from . import global_variables


# reveal in explorer
def reveal_in_explorer(path) :
    #windows
    if platform.system() == "Windows":
            #os.startfile(path)
            #subprocess.Popen(['explorer', path])
            # subprocess.Popen(r'explorer /select,%s' % path)
            #subprocess.call("explorer %s" % path, shell=True)
            subprocess.Popen(r'explorer /select, %s' % path)
    #mac
    elif platform.system() == "Darwin":
            subprocess.Popen(["open", path])
    #linux
    else:
            subprocess.Popen(["xdg-open", path])


class AUTORELOAD_OT_reveal_explorer(bpy.types.Operator):
    bl_idname = "autorelad.reveal_explorer"
    bl_label = "Reveal"
    bl_description = "Reveal in Explorer."
    bl_options = {'REGISTER', 'INTERNAL'}

    name : bpy.props.StringProperty()
    library : bpy.props.BoolProperty()
    
    def execute(self, context):

        if self.library:
            item = bpy.data.libraries[self.name]
        else:
            item = bpy.data.images[self.name]

        path = functions.absolute_path(item.filepath)

        if os.path.isfile(path):
            reveal_in_explorer(path)
            print(global_variables.print_statement + path + global_variables.opening_msg)
        else:
            item.autoreload_modification_time = "missing"
            print(global_variables.print_statement + path + global_variables.missing_msg)

        return {'FINISHED'}


# open library
def open_library(path) :
    subprocess.Popen([bpy.app.binary_path, path])


class AUTORELOAD_OT_open_library(bpy.types.Operator):
    bl_idname = "autorelad.open_library"
    bl_label = "Open"
    bl_description = "Open Library in Blender instance."
    bl_options = {'REGISTER', 'INTERNAL'}

    name : bpy.props.StringProperty()
    
    def execute(self, context):
        lib = bpy.data.libraries[self.name]
        path = functions.absolute_path(lib.filepath)
        if os.path.isfile(path):
            open_library(path)
            print(global_variables.print_statement + path + global_variables.opening_msg)
        else:
            lib.autoreload_modification_time = "missing"
            print(global_variables.print_statement + path + global_variables.missing_msg)

        return {'FINISHED'}


# modify image
def modify_image(path) :
    img_exe = get_addon_preferences().image_executable

    subprocess.Popen([img_exe, path])


class AUTORELOAD_OT_modify_image(bpy.types.Operator):
    bl_idname = "autorelad.modify_image"
    bl_label = "Modify"
    bl_description = "Modify image with specified Program."
    bl_options = {'REGISTER', 'INTERNAL'}

    name : bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        return os.path.isfile(get_addon_preferences().image_executable)
    
    def execute(self, context):
        image = bpy.data.images[self.name]
        path = functions.absolute_path(image.filepath)
        if os.path.isfile(path):
            modify_image(path)
            print(global_variables.print_statement + path + global_variables.opening_msg)
        else:
            image.autoreload_modification_time = "missing"
            print(global_variables.print_statement + path + global_variables.missing_msg)

        return {'FINISHED'}


class AUTORELOAD_OT_remove_image(bpy.types.Operator):
    bl_idname = "autorelad.remove_image"
    bl_label = "Remove"
    bl_description = "Remove this Image from the Blend file."
    bl_options = {'REGISTER', 'INTERNAL', 'UNDO'}

    name : bpy.props.StringProperty()

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def draw(self, context):
        self.layout.label(text="Delete %s ?" % self.name, icon='ERROR')
    
    def execute(self, context):
        bpy.data.images.remove(bpy.data.images[self.name])
        functions.update_textures_no_images()
        print(global_variables.print_statement + self.name + global_variables.remove__msg)
        return {'FINISHED'}


class AUTORELOAD_OT_remove_library(bpy.types.Operator):
    bl_idname = "autorelad.remove_library"
    bl_label = "Remove"
    bl_description = "Remove this Library from the Blend file."
    bl_options = {'REGISTER', 'INTERNAL', 'UNDO'}

    name : bpy.props.StringProperty()

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def draw(self, context):
        self.layout.label(text="Delete %s ?" % self.name, icon='ERROR')
            
    def execute(self, context):
        bpy.data.libraries.remove(bpy.data.libraries[self.name])
        print(global_variables.print_statement + self.name + global_variables.remove__msg)
        return {'FINISHED'}


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
    bpy.utils.register_class(AUTORELOAD_OT_reveal_explorer)
    bpy.utils.register_class(AUTORELOAD_OT_open_library)
    bpy.utils.register_class(AUTORELOAD_OT_modify_image)
    bpy.utils.register_class(AUTORELOAD_OT_remove_image)
    bpy.utils.register_class(AUTORELOAD_OT_remove_library)
    bpy.utils.register_class(AUTORELOAD_OT_save_revert)

def unregister():
    bpy.utils.unregister_class(AUTORELOAD_OT_reveal_explorer)
    bpy.utils.unregister_class(AUTORELOAD_OT_open_library)
    bpy.utils.unregister_class(AUTORELOAD_OT_modify_image)
    bpy.utils.unregister_class(AUTORELOAD_OT_remove_image)
    bpy.utils.unregister_class(AUTORELOAD_OT_remove_library)
    bpy.utils.unregister_class(AUTORELOAD_OT_save_revert)