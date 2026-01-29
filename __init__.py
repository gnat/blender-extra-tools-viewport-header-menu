bl_info = {
	"name": "Extra Tools for Viewport Header Menu",
	"author": "gnat",
	"version": (1, 1),
	"blender": (5, 0, 0),
	"location": "3D Viewport Header",
	"description": "Adds extra conveniences for Search, Import / Export, Undo / Redo and common Views",
	"category": "Interface",
}

import bpy

# Operator for Global Search (F3)
class WM_OT_open_global_search(bpy.types.Operator):
	bl_idname = "wm.open_global_search"
	bl_label = "Global Search"

	def execute(self, context):
		bpy.ops.wm.search_menu('INVOKE_DEFAULT')
		return {'FINISHED'}

# Draw function for the 3D View header
def draw_viewport_header_tools(self, context):
	layout = self.layout
	row = layout.row(align=True)
	
	#layout.separator_spacer()
	#layout.separator()
	row.separator(factor=1.5)

	# View buttons
	row.operator("view3d.view_axis", text="", icon='HOME').type = 'FRONT'
	row.operator("view3d.view_axis", text="", icon='SPLIT_VERTICAL').type = 'TOP'
	row.operator("view3d.view_axis", text="", icon='SNAP_FACE').type = 'BOTTOM'
	row.operator("view3d.view_axis", text="", icon='TRIA_LEFT').type = 'LEFT'
	row.operator("view3d.view_axis", text="", icon='TRIA_RIGHT').type = 'RIGHT'
	row.operator("view3d.view_axis", text="", icon='FILE_REFRESH').type = 'BACK'

	row.separator()

	# Undo / Redo buttons
	row.operator("ed.undo", text="", icon='LOOP_BACK')
	row.operator("ed.redo", text="", icon='LOOP_FORWARDS')

	row.separator()

	# Import dropdown
	row.menu(
		"TOPBAR_MT_file_import",
		text="",
		icon='IMPORT'
	)

	# Export dropdown
	row.menu(
		"TOPBAR_MT_file_export",
		text="",
		icon='EXPORT'
	)

	row.separator()

	# Global Search button
	row.operator(
		"wm.open_global_search",
		text="",
		icon='VIEWZOOM'
	)

def register():
	bpy.utils.register_class(WM_OT_open_global_search)
	bpy.types.VIEW3D_HT_header.append(draw_viewport_header_tools)

def unregister():
	bpy.types.VIEW3D_HT_header.remove(draw_viewport_header_tools)
	bpy.utils.unregister_class(WM_OT_open_global_search)

if __name__ == "__main__":
	register()
