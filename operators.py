import bpy
import os
import time

from .functions import reload_images, update_viewers
from .addon_prefs import get_addon_preferences
from .global_messages import timer_start, timer_end, sign, reloaded, no_modif

class AUTORELOAD_OT_reload_images(bpy.types.Operator):
    bl_idname = "autoreload.reload_images"
    bl_label = "Reload Images"
    bl_description = "Reload Images in the blend. if modified"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        modified=reload_images()
        if len(modified)!=0:
            update_viewers(context)
            for m in modified :
                print(sign + m + reloaded)
        else:
            print(no_modif)
        return {"FINISHED"}
        

class AUTORELOAD_OT_reload_timer(bpy.types.Operator):
    bl_idname = "autoreload.reload_timer"
    bl_label = "Reload Images timer"
    bl_description = "Look for modified Images every N seconds and reload them"

    _timer = None
    oldtimer : bpy.props.FloatProperty()

    @classmethod
    def poll(cls, context):
        return not bpy.data.window_managers['WinMan'].reload_modal
    
    def __init__(self):     
        print(timer_start)
        bpy.data.window_managers['WinMan'].reload_modal=True

    def modal(self, context, event):
        if bpy.data.window_managers['WinMan'].reload_modal==False:
            self.cancel(context)
            return {'CANCELLED'}

        if event.type == 'TIMER':
            if self.oldtimer!=self._timer.time_duration:
                modified = reload_images()
                if len(modified)!=0:
                    update_viewers(context)
                    for m in modified :
                        print(sign + m + reloaded)
                self.oldtimer=self._timer.time_duration

        return {'PASS_THROUGH'}

    def execute(self, context):
        addon_preferences = get_addon_preferences()
        freq=addon_preferences.check_frequency
        wm = context.window_manager
        self._timer = wm.event_timer_add(freq, window=context.window)
        wm.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def cancel(self, context):
        wm = context.window_manager
        wm.event_timer_remove(self._timer)
        print(timer_end)