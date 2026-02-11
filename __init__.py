bl_info = {
	"name": "Extra Tools for Viewport Header Menu",
	"author": "gnat",
	"version": (1, 3),
	"blender": (5, 0, 0),
	"location": "3D Viewport Header",
	"description": "Adds extra conveniences for Search, Import / Export, Undo / Redo and common Views",
	"category": "Interface",
}

import bpy
import os
import bpy.utils.previews
_icons = None

# Draw function for the 3D View header
def draw_viewport_header_tools(self, context):
	layout = self.layout
	row = layout.row(align=True)
	row.separator(factor=1.5)

	# View buttons with icons
	row.operator("view3d.view_axis", text="", icon_value=_icons["FRONT"].icon_id).type = 'FRONT'
	row.operator("view3d.view_axis", text="", icon_value=_icons["TOP"].icon_id).type = 'TOP'
	row.operator("view3d.view_axis", text="", icon_value=_icons["BOTTOM"].icon_id).type = 'BOTTOM'
	row.operator("view3d.view_axis", text="", icon_value=_icons["LEFT"].icon_id).type = 'LEFT'
	row.operator("view3d.view_axis", text="", icon_value=_icons["RIGHT"].icon_id).type = 'RIGHT'
	row.operator("view3d.view_axis", text="", icon_value=_icons["BACK"].icon_id).type = 'BACK'

	row.separator()

	# Undo / Redo
	row.operator("ed.undo", text="", icon='LOOP_BACK')
	row.operator("ed.redo", text="", icon='LOOP_FORWARDS')

	row.separator()

	# Import / Export
	row.menu("TOPBAR_MT_file_import", text="", icon='IMPORT')
	row.menu("TOPBAR_MT_file_export", text="", icon='EXPORT')

	row.separator()

	# Global Search
	row.operator("wm.open_global_search", text="", icon='VIEWZOOM')

# Operator for Global Search (F3)
class WM_OT_open_global_search(bpy.types.Operator):
	bl_idname = "wm.open_global_search"
	bl_label = "Global Search"
	def execute(self, context):
		bpy.ops.wm.search_menu('INVOKE_DEFAULT')
		return {'FINISHED'}

def register():
	# Icons
	global _icons
	_icons = bpy.utils.previews.new()
	icons_dir = os.path.join(os.path.dirname(__file__), "icons")
	if os.path.exists(os.path.join(icons_dir, "view_front.svg")):  _icons.load("FRONT", os.path.join(icons_dir, "view_front.svg"), 'IMAGE')
	if os.path.exists(os.path.join(icons_dir, "view_top.svg")):    _icons.load("TOP", os.path.join(icons_dir, "view_top.svg"), 'IMAGE')
	if os.path.exists(os.path.join(icons_dir, "view_bottom.svg")): _icons.load("BOTTOM", os.path.join(icons_dir, "view_bottom.svg"), 'IMAGE')
	if os.path.exists(os.path.join(icons_dir, "view_left.svg")):   _icons.load("LEFT", os.path.join(icons_dir, "view_left.svg"), 'IMAGE')
	if os.path.exists(os.path.join(icons_dir, "view_right.svg")):  _icons.load("RIGHT", os.path.join(icons_dir, "view_right.svg"), 'IMAGE')
	if os.path.exists(os.path.join(icons_dir, "view_back.svg")):   _icons.load("BACK", os.path.join(icons_dir, "view_back.svg"), 'IMAGE')

	bpy.utils.register_class(WM_OT_open_global_search)
	bpy.types.VIEW3D_HT_header.append(draw_viewport_header_tools)

def unregister():
	bpy.types.VIEW3D_HT_header.remove(draw_viewport_header_tools)
	bpy.utils.unregister_class(WM_OT_open_global_search)
	# Icons
	global _icons
	if _icons:
		bpy.utils.previews.remove(_icons)
		_icons = None

if __name__ == "__main__":
	register()
