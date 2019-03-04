"""
Copyright (c) 2018 iCyP
Released under the MIT license
https://opensource.org/licenses/mit-license.php

"""

import bpy
from .main import make_mesh,add_mesh,unitdic

bl_info = {
    "name":"Japanese units mesh maker",
    "author": "iCyP",
    "version": (0, 1),
    "blender": (2, 80, 0),
    "location": "3D View->Tools",
    "description": "JP units",
    "warning": "",
    "support": "TESTING",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Mesh"
}


class Make_JP_units(bpy.types.Operator):
    bl_idname = "mesh.jp_units"
    bl_label = "make JP units mesh"
    bl_description = "make JP units mesh"
    bl_options = {'REGISTER', 'UNDO'}

    mode = bpy.props.StringProperty(options={"HIDDEN"})
    base = bpy.props.StringProperty(options={"HIDDEN"})
    adapt = bpy.props.StringProperty(options={"HIDDEN"})
    
    def execute(self,context):
        print("{},{}".format(self.base, self.adapt))
        if self.mode == "OBJECT":
            make_mesh(self.base,self.adapt)
        if self.mode == "EDIT_MESH":
            add_mesh(self.base,self.adapt)
        return {'FINISHED'}


class Make_JP_units_UI_INNER(bpy.types.Menu):
    bl_idname = "Make_JP_units_UI_controller"
    bl_label = "icyp jp units ui"

    @classmethod
    def poll(self, context):
        if context.mode == "OBJECT" or context.mode == "EDIT_MESH":
            return True
        else:
            return False

    def draw(self, context):
        col = self.layout.column(align=True)
        for unit,vals in unitdic.items():
            col.label(text=unit)
            for key in vals.keys():
                ops_button = col.operator(Make_JP_units.bl_idname,text = key)
                ops_button.mode = context.mode
                ops_button.base = unit
                ops_button.adapt = key

classes = (
    Make_JP_units,
    Make_JP_units_UI_INNER
)

def icyp_jp_units_menu(self, context):
    self.layout.menu("Make_JP_units_UI_controller",
                     text="JP_UNIT", icon="PLUGIN")    


# アドオン有効化時の処理
def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.VIEW3D_MT_mesh_add.append(icyp_jp_units_menu)

# アドオン無効化時の処理
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    bpy.types.VIEW3D_MT_mesh_add.remove(icyp_jp_units_menu)

if "__main__" == __name__:
    register()