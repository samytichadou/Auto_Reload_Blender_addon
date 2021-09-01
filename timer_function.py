import bpy

from .addon_prefs import get_addon_preferences
from . import global_variables
from . import functions

# timer function
def autoreload_timer_function():

    interval = get_addon_preferences().check_frequency
    context = bpy.context
    wm = context.window_manager

    modified_list, missing_list = functions.reload_modified_images()

    if len(modified_list)!=0: 
        functions.update_viewers(context)

    if len(missing_list)==0: 
        wm.autoreload_missing_images=False
    else: 
        wm.autoreload_missing_images=True

    for m in modified_list: 
        print(global_variables.print_statement + m + global_variables.reloaded_msg)
    for m in missing_list:
        print(global_variables.print_statement + m + global_variables.missing_msg)

    return interval


# update timer function
def update_timer_function(self, context):

    if self.autoreload_is_timer:
        print(global_variables.timer_start_statement)
        bpy.app.timers.register(autoreload_timer_function)
    else:
        print(global_variables.timer_end_statement)
        bpy.app.timers.unregister(autoreload_timer_function)