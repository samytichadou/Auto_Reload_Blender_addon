import bpy


# draw update button
def draw_update_button(context, container):
    props = context.window_manager.autoreload_properties

    if props.autoreload_update_needed:
        op = container.operator('autoreload.dialog_popups', text="New Version Available", icon='ERROR')
        op.message = props.autoreload_update_message
        op.operator = "bpm.open_url"
        op.operator_text = "New addon version available"
        op.operator_icon = "URL"
        op.operator_url = props.autoreload_update_download_url
        

# libraries panel
class AUTORELOAD_PT_libraries_panel(bpy.types.Panel):
    bl_label = "Libraries Inspector"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    def draw(self, context):
        props = context.window_manager.autoreload_properties
        wm = context.window_manager

        layout = self.layout

        draw_update_button(context, layout)

        if props.autoreload_missing_libraries:
            layout.label(text="Missing Libraries", icon='ERROR')

        layout.use_property_split = True # Active single-column layout
        flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=True, align=False)

        row = flow.row(align=True)
        row.operator('autoreload.check_libraries', icon='BLENDER')

        row = flow.row(align=True)
        row.operator('autoreload.save_revert', icon='FILE_TICK')

        layout.template_list("AUTORELOAD_UL_libraries_uilist", "", bpy.data, "libraries", props, "autoreload_active_library_index", rows=3)

        # selected library path
        active_lib = bpy.data.libraries[props.autoreload_active_library_index]
        layout.prop(active_lib, "filepath", text="")
        

# image inspector panel
class AUTORELOAD_PT_image_inspector_panel(bpy.types.Panel):
    bl_label = "Images Inspector"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    def draw(self, context):
        props = context.window_manager.autoreload_properties

        layout = self.layout

        draw_update_button(context, layout)

        if props.autoreload_missing_images:
            layout.label(text="Missing Images", icon='ERROR')

        layout.use_property_split = True # Active single-column layout
        flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=True, align=False)

        row = flow.row(align=True)
        row.operator('autoreload.reload_images', icon='FILE_REFRESH')

        row = flow.row(align=True)
        row.operator('autoreload.save_revert', icon='FILE_TICK')

        layout.template_list("AUTORELOAD_UL_images_uilist", "", bpy.data, "images", props, "autoreload_active_image_index", rows=3)

        # selected image path
        active_image = bpy.data.images[props.autoreload_active_image_index]
        if active_image.source not in {'VIEWER','GENERATED'}:
            layout.prop(active_image, "filepath", text="")


# file menu
class AUTORELOAD_MT_file_menu(bpy.types.Menu):
    bl_label = "Auto Reload"

    def draw(self, context):
        props = context.window_manager.autoreload_properties

        layout = self.layout
        
        layout.prop(props, 'autoreload_is_timer', text = "Timer", icon='TIME')

        layout.separator()

        layout.operator('autoreload.reload_images', icon='FILE_REFRESH')

        layout.operator('autoreload.check_libraries', icon='BLENDER')

        layout.separator()

        layout.operator('autoreload.save_revert', icon='FILE_TICK')
        
        if props.autoreload_update_needed \
        or props.autoreload_missing_images \
        or props.autoreload_missing_libraries:
            layout.separator()

        # update
        draw_update_button(context, layout)

        # missing images and libs
        if props.autoreload_missing_images:
            layout.label(text="Missing Images", icon='ERROR')
        if props.autoreload_missing_libraries:
            layout.label(text="Missing Libraries", icon='ERROR')


# file menu drawer
def file_menu_drawer(self, context):
    if context.region.alignment == 'RIGHT':
        layout = self.layout
        
        self.layout.separator()
        if context.window_manager.autoreload_properties.autoreload_is_timer:
            self.layout.menu('AUTORELOAD_MT_file_menu', text=" Auto Reload", icon='TIME')
        else:
            self.layout.menu('AUTORELOAD_MT_file_menu')


### REGISTER ---

def register():
    bpy.utils.register_class(AUTORELOAD_PT_libraries_panel)
    bpy.utils.register_class(AUTORELOAD_PT_image_inspector_panel)
    bpy.utils.register_class(AUTORELOAD_MT_file_menu)

    bpy.types.TOPBAR_HT_upper_bar.prepend(file_menu_drawer)

def unregister():
    bpy.utils.unregister_class(AUTORELOAD_PT_libraries_panel)
    bpy.utils.unregister_class(AUTORELOAD_PT_image_inspector_panel)
    bpy.utils.unregister_class(AUTORELOAD_MT_file_menu)

    bpy.types.TOPBAR_HT_upper_bar.remove(file_menu_drawer)