import bpy

from .addon_prefs import get_addon_preferences
from . import global_variables

# timer function
def autoreload_timer_function():

    interval = get_addon_preferences().check_frequency

    # do something
    print("timer")

    return interval


# update timer function
def update_timer_function(self, context):

    if self.autoreload_is_timer:
        print(global_variables.timer_start_statement)
        bpy.app.timers.register(autoreload_timer_function)
    else:
        print(global_variables.timer_end_statement)
        bpy.app.timers.unregister(autoreload_timer_function)