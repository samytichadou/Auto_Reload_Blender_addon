'''
Copyright (C) 2018 Samy Tichadou (tonton)
samytichadou@gmail.com

Created by Samy Tichadou

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

bl_info = {
    "name": "Auto Reload Images",
    "description": "Handy reload for Image Textures",
    "author": "Samy TIchadou (tonton), RenFinkle",
    "version": (1, 1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Material",
    "wiki_url": "https://github.com/samytichadou/Auto_Reload_Images-Blender_addon",
    "tracker_url": "https://github.com/samytichadou/Auto_Reload_Images-Blender_addon/issues/new",
    "category": "Material" }

import bpy


# load and reload submodules
##################################

import importlib, inspect
from . import developer_utils
importlib.reload(developer_utils)
modules = developer_utils.setup_addon_modules(__path__, __name__, "bpy" in locals())
classes = []
for module in modules:
    for name, obj in inspect.getmembers(module):
        if inspect.isclass(obj) and name != "persistent":
            classes.append(obj)
from .functions import reload_startup
#from .gui import reload_menu_draw

# register
##################################

import traceback

def register():
    #try: bpy.utils.register_module(__name__)
    #except: traceback.print_exc()
    
    bpy.types.Image.modification_time = \
        bpy.props.StringProperty(name='File Modification Date', default='')
    bpy.types.WindowManager.reload_modal = \
        bpy.props.BoolProperty(name='Reload Images Timer', default=False)
    bpy.types.WindowManager.reload_frames = \
        bpy.props.BoolProperty(name='Reload Images on Frame changes', default=False)
        
    #bpy.context.window.scene.PROPERTIES.append(reload_menu_draw)
    for cls in classes:
        #print(cls)
        bpy.utils.register_class(cls)
        
    bpy.app.handlers.load_post.append(reload_startup)

    #print("Registered {} with {} modules".format(bl_info["name"], len(modules)))

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
        del cls
    #try: bpy.utils.unregister_module(__name__)
    #except: traceback.print_exc()
    
    del bpy.types.Image.modification_time
    del bpy.types.WindowManager.reload_modal
    del bpy.types.WindowManager.reload_frames
    
    #bpy.types.INFO_HT_header.remove(reload_menu_draw)
    
    bpy.app.handlers.load_post.remove(reload_startup)

    print("Unregistered {}".format(bl_info["name"]))
