import bpy
import os

from functions import absolute_path, reveal_in_explorer, open_image
from addon_prefs import get_addon_preferences
from global_variables import missing_image

class AUTORELOAD_reveal_explorer(bpy.types.Operator):
    bl_idname = "autorelad.reveal_explorer"
    bl_label = "Reveal"
    bl_description = "Reveal in Explorer"
    bl_options = {'REGISTER'}

    path : bpy.props.StringProperty()
    
    def execute(self, context):
        path = absolute_path(self.path)
        if os.path.isfile(path):
            reveal_in_explorer(path)
        else:
            print(missing_image)

        return {'FINISHED'}

class AUTORELOAD_open_image(bpy.types.Operator):
    bl_idname = "autorelad.open_image"
    bl_label = "Open"
    bl_description = "Open image with specified Program"
    bl_options = {'REGISTER'}

    path : bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        prefs = get_addon_preferences()
        if os.path.isfile(prefs.image_executable):
            return True
    
    def execute(self, context):
        path = absolute_path(self.path)
        if os.path.isfile(path):
            open_image(path)
        else:
            print(missing_image)

        return {'FINISHED'}