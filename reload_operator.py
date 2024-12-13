import bpy
from . import reload

from .addon_prefs import get_addon_preferences


class AUTORELOAD_OT_reload(bpy.types.Operator):
    bl_idname = "autoreload.reload"
    bl_label = "Reload Datas"
    bl_description = "Reload datas if modified."
    bl_options = {"REGISTER", "UNDO", "INTERNAL"}
    
    behavior : bpy.props.StringProperty()

    def execute(self, context):
        props = context.window_manager.autoreload_properties
        
        if self.behavior == "all":
            reload.reload_modified_objects()
            
        else:
            obj_to_reload = reload.get_files_moddate(self.behavior)
            
            if get_addon_preferences().debug:
                print("AUTORELOAD --- Objects to reload :")
                print(obj_to_reload)
            
            if self.behavior == "images":
                reload.reload_images(obj_to_reload)
            elif self.behavior == "movieclips":
                reload.reload_movieclips(obj_to_reload)
            elif self.behavior == "sounds":
                reload.reload_sounds(obj_to_reload)
            elif self.behavior == "libraries":
                reload.reload_libraries(obj_to_reload)
            elif self.behavior == "cache_files":
                reload.reload_cache_files(obj_to_reload)
                
        self.report({'INFO'}, f"{self.behavior.capitalize()} modified datas reloaded")
        
        return {"FINISHED"}

    
### REGISTER ---
def register():
    bpy.utils.register_class(AUTORELOAD_OT_reload)

def unregister():
    bpy.utils.unregister_class(AUTORELOAD_OT_reload)
            
