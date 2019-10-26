import bpy
import os
import time
import gpu
import blf

from gpu_extras.batch import batch_for_shader

from .functions import update_viewers, get_my_dir, reloadModifiedDatas
from .addon_prefs import get_addon_preferences
from .global_variables import timer_start, timer_end, sign, reloaded, no_modif, missing

class AUTORELOAD_OT_reload_datas(bpy.types.Operator):
    bl_idname = "autoreload.reload_datas"
    bl_label = "Reload Datas"
    bl_description = "Reload Datas in the blend. if modified"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        wm = context.window_manager
        return wm.autoreloadImages or wm.autoreloadLibraries

    def execute(self, context):
        wm = bpy.context.window_manager
        modified_list=[]
        missing_list=[]
        if wm.autoreloadImages:
            mod, miss = reloadModifiedDatas(bpy.data.images)
            modified_list += mod
            missing_list += miss
            if len(mod)!=0: update_viewers(context)
            if len(miss) == 0: wm.autoreloadMissingImages = False
            else: wm.autoreloadMissingImages = True
        if wm.autoreloadLibraries:
            mod, miss = reloadModifiedDatas(bpy.data.libraries)
            modified_list += mod
            missing_list += miss
            if len(miss) == 0: wm.autoreloadMissingLibraries = False
            else: wm.autoreloadMissingLibraries = True
        for m in modified_list: print(sign + m + reloaded)
        for m in missing_list: print(sign + m + missing)
        if len(modified_list)==0 and len(missing_list)==0: print(no_modif)
        return {"FINISHED"}

### UI ###

def load_font(self):
    if self.font_id is not None:
        return
    try:
        self.font_id = blf.load(self.font_path)   
    except:
        raise Exception

def unload_font(self):
    if self.font_id is not None:
        self.font_id = None
        blf.unload(self.font_path)   

def draw_prepare(self):
    blf.color(self.font_id, *self.prefs.icon_color, 1)
    blf.size(self.font_id, self.prefs.icon_size, 72)
    blf.position(self.font_id, self.prefs.icon_offset_x, self.prefs.icon_offset_y, 0)

# callback for loading bar in 3D view 
def draw_callback_px(self, context):
    # Text
    text = "T"
    blf.draw(self.font_id, text)
        

class AUTORELOAD_OT_reload_timer(bpy.types.Operator):
    bl_idname = "autoreload.reload_timer"
    bl_label = "Reload Datas timer"
    bl_description = "Look for modified Datas every N seconds and reload them"

    font_id = None
    font_path = os.path.join(get_my_dir(), os.path.join("misc", "heydings_icons.ttf"))
    _timer = None
    oldtimer : bpy.props.FloatProperty()
    prefs = None

    @classmethod
    def poll(cls, context):
        chk = 0
        wm = context.window_manager
        if wm.autoreloadImages: chk = 1
        elif wm.autoreloadLibraries: chk = 1
        return not wm.reload_modal and chk == 1
    
    def __init__(self):     
        bpy.context.window_manager.reload_modal=True
        print(timer_start)
        self.prefs = get_addon_preferences()
        if self.prefs.icon_toggle :
            load_font(self)
            draw_prepare(self)

    def modal(self, context, event):
        wm=context.window_manager
        # redraw area
        if self.prefs.icon_toggle :
            try:
                for area in context.screen.areas:
                    if area.type == 'PROPERTIES': area.tag_redraw()
            except AttributeError: pass

        if wm.reload_modal==False:
            self.finish(context)
            return {'FINISHED'}

        elif not wm.autoreloadImages and not wm.autoreloadLibraries:
            self.cancel(context)
            return {'FINISHED'}

        elif event.type == 'TIMER':
            if self.oldtimer!=self._timer.time_duration:
                if wm.autoreloadImages:
                    modified_list, missing_list = reloadModifiedDatas(bpy.data.images)
                    if len(modified_list)!=0: update_viewers(context)
                    if len(missing_list)==0: wm.autoreloadMissingImages=False
                    else: wm.autoreloadMissingImages=True
                    for m in modified_list: print(sign + m + reloaded)
                    for m in missing_list: print(sign + m + missing)
                    self.oldtimer=self._timer.time_duration
                if wm.autoreloadLibraries:
                    modified_list, missing_list = reloadModifiedDatas(bpy.data.libraries)
                    if len(missing_list)==0: wm.autoreloadMissingLibraries=False
                    else: wm.autoreloadMissingLibraries=True
                    for m in modified_list: print(sign + m + reloaded)
                    for m in missing_list: print(sign + m + missing)
                    self.oldtimer=self._timer.time_duration

        return {'PASS_THROUGH'}

    def execute(self, context):
        addon_preferences = get_addon_preferences()
        freq=addon_preferences.check_frequency

        wm = context.window_manager
        # the arguments we pass the callback
        args = (self, context)
        self._timer = wm.event_timer_add(freq, window=context.window)
        if self.prefs.icon_toggle :
            self._handle = bpy.types.SpaceProperties.draw_handler_add(draw_callback_px, args, 'WINDOW', 'POST_PIXEL')
        wm.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def finish(self, context):
        if self.prefs.icon_toggle:
            bpy.types.SpaceProperties.draw_handler_remove(self._handle, 'WINDOW')
            unload_font(self)
        wm = context.window_manager
        wm.event_timer_remove(self._timer)
        print(timer_end)

    def cancel(self, context):
        if self.prefs.icon_toggle:
            bpy.types.SpaceProperties.draw_handler_remove(self._handle, 'WINDOW')
            unload_font(self)
        wm = context.window_manager
        wm.event_timer_remove(self._timer)
        wm.reload_modal = False
        print(timer_end)