import platform
import subprocess
import sys

# open folder in explorer
def reveal_in_explorer(path) :
    #windows
    if platform.system() == "Windows":
            #os.startfile(path)
            subprocess.Popen(r'explorer /select,%s' % path)
            #subprocess.Popen(['explorer', path])
    #mac
    elif platform.system() == "Darwin":
            subprocess.Popen(["open", path])
    #linux
    else:
            subprocess.Popen(["xdg-open", path])

# open image
def open_image(path) :
    prefs = get_addon_preferences()
    img_exe = prefs.image_executable

    subprocess.Popen([img_exe, path])

# update texture
def update_texture(self, context):
    wm = bpy.data.window_managers['WinMan']
    texture = bpy.data.textures[image_texture]
    texture.image = bpy.data.images[wm.autoreload_index]