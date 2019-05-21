import bpy
import os
import time

from bpy.app.handlers import persistent


def reload_images():
    #reload all images
    for i in bpy.data.images:
        i.reload()

    #update viewers
    wman=bpy.data.window_managers['WinMan']
    for win in wman.windows:
        scr = win.screen
        for area in win.screen.areas:
            area.tag_redraw()
            #redraw if viewport in rendered mode
            region = [region for region in area.regions if region.type == 'WINDOW']
            if area.type=='VIEW_3D':
                for space in area.spaces: # iterate through spaces in current VIEW_3D area
                    #print(space.shading.type)
                    if False and space.type == 'VIEW_3D' and space.shading.type in ['MATERIAL','RENDERED']: # check if space is a 3D view
                        override = {'window':win,
                        'screen':scr,
                        'area'  :area,
                        'region':region,
                        'scene' :bpy.context.scene,
                        'blend_data' :bpy.context.blend_data
                        }
                        bpy.ops.view3d.toggle_render(override)
                        bpy.ops.view3d.toggle_render(override)
            elif area.type=='IMAGE_EDITOR':
                for space in area.spaces:
                    if space.type == 'IMAGE_EDITOR':
                        s=space
                override = {'window':win,
                'screen':scr,
                'area'  :area,
                'region':region,
                'scene' :bpy.context.scene,
                'blend_data' :bpy.context.blend_data,
                'edit_image' :s.image
                }
                bpy.ops.image.reload(override)
            elif area.type=='NODE_EDITOR':
                for space in area.spaces:
                    if space.type == 'NODE_EDITOR':
                        if space.show_backdrop == True:
                            space.show_backdrop = True

                
                
    return{"FINISHED"}

def get_modification_times():
    for i in bpy.data.images:
        try:
            path=os.path.abspath(bpy.path.abspath(i.filepath))
            i.modification_time=str(os.path.getmtime(path))
        except FileNotFoundError:
            i.modification_time="missing"
    return{"FINISHED"}

@persistent
def reload_startup(scene):
    for i in bpy.data.images:
        try:
            path=os.path.abspath(bpy.path.abspath(i.filepath))
            i.modification_time=str(os.path.getmtime(path))
        except FileNotFoundError:
            i.modification_time="missing"
    print("Auto Reload Images --- All images modification time updated")