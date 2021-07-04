bl_info = {
	"name": "Add Hole",
	"author": "Kenetics",
	"version": (0, 1),
	"blender": (2, 93, 0),
	"location": "View3D > Edit Mesh",
	"description": "Adds hole to mesh via different techniques.",
	"warning": "",
	"wiki_url": "",
	"category": "Mesh"
}

import bpy
from bpy.props import EnumProperty, IntProperty, FloatVectorProperty, BoolProperty, FloatProperty, StringProperty
from bpy.types import PropertyGroup, UIList, Operator, Panel, AddonPreferences


## Operators
class AH_OT_add_hole(Operator):
	"""Adds hole to mesh via different techniques."""
	bl_idname = "ah.add_hole"
	bl_label = "Add Hole to Mesh"
	bl_options = {'REGISTER','UNDO'}
	
	# Properties
	inset_type : EnumProperty(
		items=[
			("INSET", "Inset", ""),
			("SCALE", "Scale", "")
		],
		name="Inset Type"
	)
	cap_type : EnumProperty(
		items=[
			("NORMAL", "Normal", ""),
			("DELETE", "Delete", "")
		],
		name="Cap Type"
	)
	
	bridge : BoolProperty(name="Bridge Caps", default=False)
	inset_amount : FloatProperty(name="Inset Amount", default = 0.5)
	use_even_offset : BoolProperty(name="Use Even Offset", default=False)
	sphere_amount : FloatProperty(name="Sphere Amount", default = 1.0, min=0, max=1)
	subdivisions : IntProperty(name="Subdivisions", default = 0, min=0)
	preinset : BoolProperty(name="Pre-Inset", default=False, description="Used to prevent conflicts with other faces.")
	preinset_amount : FloatProperty(name="Pre-Inset Amount", default = 0.01)
	extrude : BoolProperty(name="Extrude", default=False)
	extrude_amount : FloatProperty(name="Hole Depth", default = -0.1)

	def draw(self, context):
		layout = self.layout
		
		layout.prop(self, "inset_type")
		layout.prop(self, "cap_type")
		layout.prop(self, "bridge")
		layout.prop(self, "inset_amount")
		layout.prop(self, "use_even_offset")
		layout.prop(self, "sphere_amount")
		layout.prop(self, "subdivisions")
		
		layout.prop(self, "preinset")
		if self.preinset:
			layout.prop(self, "preinset_amount")
		
		layout.prop(self, "extrude")
		if self.extrude:
			layout.prop(self, "extrude_amount")

	@classmethod
	def poll(cls, context):
		return context.active_object and context.mode == "EDIT_MESH"

	def execute(self, context):
		if self.preinset:
			bpy.ops.mesh.inset(thickness=self.preinset_amount, depth=0)
		
		if self.subdivisions:
			bpy.ops.mesh.subdivide(number_cuts=self.subdivisions)
		
		if self.inset_type == "INSET":
			bpy.ops.mesh.inset(thickness=self.inset_amount, depth=0, use_even_offset=self.use_even_offset)
		else:
			bpy.ops.mesh.inset(thickness=0, depth=0)
			bpy.ops.transform.resize(value=(self.inset_amount, self.inset_amount, self.inset_amount), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL')
		
		bpy.ops.transform.tosphere(value=self.sphere_amount)
		
		if self.extrude:
			bpy.ops.mesh.inset(thickness=0, depth=self.extrude_amount)
			
		if self.cap_type == "DELETE":
			bpy.ops.mesh.delete(type='FACE')
		
		if self.bridge:
			# Handle when there isn't pair of caps
			try:
				bpy.ops.mesh.bridge_edge_loops()
			except RuntimeError:
				pass
		
		return {'FINISHED'}


## Register
def register():
	bpy.utils.register_class(AH_OT_add_hole)

def unregister():
	bpy.utils.unregister_class(AH_OT_add_hole)

if __name__ == "__main__":
	register()
