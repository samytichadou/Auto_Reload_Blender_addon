import bpy
import os

addon_name = os.path.basename(os.path.dirname(__file__))

class Reload_AddonPrefs(bpy.types.AddonPreferences):
    bl_idname = addon_name
    
    check_frequency : bpy.props.FloatProperty(name='Checking Frequency (s)', 
        precision=2, 
        min=0.01, 
        max=3600.00, 
        default=1, 
        description='Frequency for checking for modified Images in seconds')

    icon_toggle: bpy.props.BoolProperty(
        name = "Icon Display",
        description = "Display indicator icon for timer mode",
        default = True,
        )

    icon_offset_x: bpy.props.IntProperty(
        name = "Icon Horizontal offset",
        description = "Space between the icon and view edge",
        default = 10,
        )

    icon_offset_y: bpy.props.IntProperty(
        name = "Icon Vertical offset",
        description = "Space between the icon and view edge",
        default = 10,
        )

    icon_size: bpy.props.IntProperty(
        name = "Icon Size",
        description = "Icon size",
        default = 32,
        )

    icon_color : bpy.props.FloatVectorProperty(
            name = "Icon Color", 
            size = 3,
            min = 0.0,
            max = 1.0,
            default = [1, 1, 1],
            subtype = 'COLOR'
            )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "check_frequency")
        box = layout.box()
        box.prop(self, "icon_toggle")
        if self.icon_toggle:
            col = box.column(align=True)
            row = col.row(align=True)
            row.prop(self, "icon_size", text="Size")
            row.prop(self, "icon_color", text="")
            row = col.row(align=True)
            row.prop(self, "icon_offset_x", text="X Position")
            row.prop(self, "icon_offset_y", text="Y Position")

        


# get addon preferences
def get_addon_preferences():
    addon = bpy.context.preferences.addons.get(addon_name)
    return getattr(addon, "preferences", None)