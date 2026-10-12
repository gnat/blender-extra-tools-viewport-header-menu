bl_info = {
	"name": "Extra Tools for Viewport Header Menu",
	"author": "gnat",
	"version": (1, 2),
	"blender": (5, 0, 0),
	"location": "3D Viewport Header",
	"description": "Adds convenient views, search, import/export, undo/redo and Unreal export",
	"category": "Interface",
}

import bpy
import os
import bpy.utils.previews
from bpy_extras.io_utils import ExportHelper
from mathutils import Matrix
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
	row.operator("wm.export_unreal_engine", text="", icon_value=_icons["UNREAL"].icon_id)

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

# Unreal Engine export
class WM_OT_export_unreal_engine(bpy.types.Operator, ExportHelper):
	bl_idname = "wm.export_unreal_engine"
	bl_label = "Unreal Engine"
	bl_options = {'REGISTER', 'UNDO'}
	filename_ext = ".fbx"
	filter_glob: bpy.props.StringProperty(default="*.fbx", options={'HIDDEN'})
	set_object_pivot: bpy.props.BoolProperty(name="Reset Origins", description="Reset objects to the scene origin", default=False)
	selected_only: bpy.props.BoolProperty(name="Selection Only", description="Export selected objects only", default=False)
	combine_child_meshes: bpy.props.BoolProperty(name="Combine Child Meshes", description="Join visible mesh children into their parent mesh", default=False)
	unpack: bpy.props.BoolProperty(name="Unpacked FBX", description="Do not embed textures inside FBX", default=False)
	fix_materials: bpy.props.BoolProperty(name="Fix Roughness and Metallic", description="Blender to Unreal material fix.", default=True)

	# Material helpers for Unreal Engine
	def find_bsdf_node(self, mat):
		if mat.use_nodes:
			for node in mat.node_tree.nodes:
				if node.type == "BSDF_PRINCIPLED":
					return node
		return None

	def find_linked_texture_image_node(self, node, initial_input=None, visited=None):
		if visited is None:
			visited = set()
		if node in visited:
			return None
		visited.add(node)
		if node.type == "TEX_IMAGE":
			return node
		input = initial_input if initial_input is not None else node.inputs.get("Color")
		if input is not None and input.is_linked:
			return self.find_linked_texture_image_node(input.links[0].from_node, visited=visited)
		return None

	def apply_material_fixes(self):
		for mat in bpy.data.materials:
			node = self.find_bsdf_node(mat)
			if node is None:
				continue
			base_color = self.find_linked_texture_image_node(node, node.inputs["Base Color"])
			roughness = self.find_linked_texture_image_node(node, node.inputs["Roughness"])
			metallic = self.find_linked_texture_image_node(node, node.inputs["Metallic"])
			if base_color is not None:
				mat.node_tree.links.new(base_color.outputs["Color"], node.inputs["Base Color"])
			if roughness is not None:
				specular = "Specular" if "Specular" in node.inputs else "Specular IOR Level"
				mat.node_tree.links.new(roughness.outputs["Color"], node.inputs[specular])
			if metallic is not None:
				mat.node_tree.links.new(metallic.outputs["Color"], node.inputs["Roughness"])
				mat.node_tree.links.remove(node.inputs["Metallic"].links[0])

	# Join visible mesh children using the current Blender context API
	def gather_mesh_children(self, target):
		children = []
		for obj in target.children:
			if obj.type == "MESH" and obj.select_get():
				children.append(obj)
				children += self.gather_mesh_children(obj)
		return children

	def join_mesh_children(self, context, target):
		children = self.gather_mesh_children(target)
		if not children:
			return
		objects = [target] + children
		with context.temp_override(active_object=target, selected_objects=objects, selected_editable_objects=objects):
			bpy.ops.object.join()

	def draw(self, context):
		layout = self.layout
		layout.prop(self, "selected_only")
		layout.prop(self, "set_object_pivot")
		layout.prop(self, "combine_child_meshes")
		layout.prop(self, "unpack")
		layout.prop(self, "fix_materials")
		layout.label(text="UNDO changes after export.", icon='INFO')

	def execute(self, context):
		if context.object and context.object.mode != 'OBJECT':
			bpy.ops.object.mode_set(mode='OBJECT')
		for obj in context.view_layer.objects:
			obj.select_set(obj.visible_get())
		if not context.selected_objects:
			self.report({'WARNING'}, "No visible objects to export")
			return {'CANCELLED'}
		if self.fix_materials:
			self.apply_material_fixes()
		if self.combine_child_meshes:
			root_meshes = [obj for obj in context.selected_objects if obj.type == "MESH" and (obj.parent is None or obj.parent.type != "MESH" or not obj.parent.select_get())]
			for mesh in root_meshes:
				self.join_mesh_children(context, mesh)
		if self.set_object_pivot:
			for obj in context.selected_objects:
				if self.combine_child_meshes and obj.parent:
					continue
				obj.matrix_world = Matrix.Identity(4)

		try:
			result = bpy.ops.export_scene.fbx(filepath=self.filepath,
				axis_forward='-Z',
				axis_up='Y',
				check_existing=False,
				object_types={'ARMATURE', 'MESH', 'OTHER', 'EMPTY'}, #'CAMERA', 'LIGHT',
				mesh_smooth_type='FACE', # Prevent undefined smoothing group warnings in Unreal
				use_selection=self.selected_only,
				use_custom_props=True,
				apply_scale_options='FBX_SCALE_NONE',
				bake_anim_use_nla_strips=True,
				bake_anim_use_all_actions=True,
				add_leaf_bones=False,
				use_armature_deform_only=False,
				path_mode='COPY' if self.unpack else 'AUTO',
				embed_textures=self.unpack)
		except (RuntimeError, OSError) as error:
			self.report({'ERROR'}, str(error))
			return {'FINISHED'} # Keep scene changes available to Undo
		if 'FINISHED' in result:
			self.report({'INFO'}, "Export Complete")
		else:
			self.report({'WARNING'}, "Export cancelled; scene changes can be undone")
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
	if os.path.exists(os.path.join(icons_dir, "unreal.svg")):      _icons.load("UNREAL", os.path.join(icons_dir, "unreal.svg"), 'IMAGE')

	bpy.utils.register_class(WM_OT_open_global_search)
	bpy.utils.register_class(WM_OT_export_unreal_engine)
	bpy.types.VIEW3D_HT_header.append(draw_viewport_header_tools)

def unregister():
	bpy.types.VIEW3D_HT_header.remove(draw_viewport_header_tools)
	bpy.utils.unregister_class(WM_OT_export_unreal_engine)
	bpy.utils.unregister_class(WM_OT_open_global_search)
	# Icons
	global _icons
	if _icons:
		bpy.utils.previews.remove(_icons)
		_icons = None

if __name__ == "__main__":
	register()
