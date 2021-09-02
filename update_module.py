import bpy
import socket
import requests
import addon_utils

from .global_variables import print_statement

addon_name                      = "Auto Reload"
check_addon_version_statement   = print_statement + "Checking for Addon New Version"
no_internet_statement           = print_statement + "No internet connection"
addon_new_version_statement     = print_statement + "New version of the addon found"
addon_up_to_date_statement      = print_statement + "Addon up to date"
error_statement                 = print_statement + "Error : "
addon_version_url               = "https://raw.githubusercontent.com/samytichadou/Auto_Reload_Blender_addon/master/addon_version.json"


# check for internet connection
def is_connected(host="8.8.8.8", port=53, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error as ex:
        print(error_statement + ex)
        return False


# read an online json
def read_online_json(url):
    file_object = requests.get(url)

    return file_object.json()


# get addon version 
def get_addon_version(addon_name):

    for addon in addon_utils.modules():

        if addon.bl_info['name'] == addon_name:
            addon_version = ""

            for n in addon.bl_info.get('version', (-1,-1,-1)):
                addon_version += str(n) + "."

            addon_version = addon_version[:-1]
            return addon_version

    return None


# check for addon new version
def check_addon_version(winman):

    print(check_addon_version_statement)

    if not is_connected():
        print(no_internet_statement)
        return False

    props = winman.autoreload_properties

    new_addon_infos = read_online_json(addon_version_url)
    if new_addon_infos["version"] != get_addon_version(addon_name):
        props.autoreload_update_message = new_addon_infos["message"]
        props.autoreload_update_download_url = new_addon_infos["download_url"]
        props.autoreload_update_needed = True
    
        print(addon_new_version_statement)

        return True

    print(addon_up_to_date_statement)
    
    return True


# check for updates
class AUTORELOAD_OT_check_addon_updates(bpy.types.Operator):
    bl_idname = "autoreload.check_addon_updates"
    bl_label = "Check Addon Updates"
    bl_description = "Check if a new version of the addon is available."
    bl_options = {"REGISTER"}

    def execute(self, context):
        wm = context.window_manager

        check_addon_version(wm)

        return {"FINISHED"}


### REGISTER ---

def register():
    bpy.utils.register_class(AUTORELOAD_OT_check_addon_updates)

def unregister():
    bpy.utils.unregister_class(AUTORELOAD_OT_check_addon_updates)