import bpy
import os
import time

from .functions import reload_images, get_modification_times
from .addon_prefs import get_addon_preferences

class Reload_reload_all(bpy.types.Operator):
    bl_idname = "reload.reload_all"
    bl_label = "Reload all Images"
    bl_description = "Reload all Images in the blend."
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        reload_images()
        get_modification_times()
        print("All images reloaded")
        return {"FINISHED"}
        

class Reload_reload_timer(bpy.types.Operator):
    bl_idname = "reload.reload_timer"
    bl_label = "Reload Images timer"

    _timer = None
    oldtimer : bpy.props.FloatProperty()
    
    def __init__(self):
        
        print("Reload Images timer started")
        bpy.data.window_managers['WinMan'].reload_modal=True

    def modal(self, context, event):
        if bpy.data.window_managers['WinMan'].reload_modal==False:
            self.cancel(context)
            return {'CANCELLED'}

        if event.type == 'TIMER':
            if self.oldtimer!=self._timer.time_duration:
                chk=0
                for i in bpy.data.images:
                    path=os.path.abspath(bpy.path.abspath(i.filepath))
                    try:
                        if i.modification_time!=str(os.path.getmtime(path)):
                            chk=1
                    except FileNotFoundError:
                        if i.modification_time!="missing":
                            chk=1
                if chk==1:
                    reload_images()
                    get_modification_times()
                    print("Modified images reloaded")
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
        print("Reload Images timer ended")