import bpy

from .addon_prefs import get_addon_preferences
from . import global_variables
from . import functions

# timer function
def autoreload_timer_function():

    interval = get_addon_preferences().check_frequency
    context = bpy.context
    props = context.window_manager.autoreload_properties

    # IMAGES
    modified_imgs, missing_imgs = functions.reload_modified_images()

    if len(modified_imgs)!=0: 
        functions.update_viewers(context)

    if len(missing_imgs)==0: 
        props.autoreload_missing_images=False
    else: 
        props.autoreload_missing_images=True

    for m in modified_imgs: 
        print(global_variables.print_statement + m + global_variables.reloaded_msg)
    for m in missing_imgs:
        print(global_variables.print_statement + m + global_variables.missing_msg)

    # LIBRARIES
    modified_libs, missing_libs = functions.check_libraries()

    if len(missing_libs)==0: 
        props.autoreload_missing_images=False
    else: 
        props.autoreload_missing_images=True

    for m in modified_libs: 
        print(global_variables.print_statement + m + global_variables.modified_msg)
    for m in missing_libs:
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