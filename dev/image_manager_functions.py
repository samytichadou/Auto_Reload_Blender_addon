import bpy


# update texture
def update_texture(self, context):
    wm = bpy.data.window_managers['WinMan']
    texture = bpy.data.textures[image_texture]
    texture.image = bpy.data.images[wm.autoreload_index]