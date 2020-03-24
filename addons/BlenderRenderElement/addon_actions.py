import bpy


class ELEMENT_OT_output(bpy.types.Operator):
    bl_idname = 'ELEMENT_OT_output'

    @classmethod
    def tester(cls):
        print ('testing ELEMENT_OT_output')


class ELEMENT_OT_render_layer(bpy.types.Operator):
    bl_idname='ELEMENT_OT_render_layer'

    @classmethod
    def tester(cls):
        print ('testing ELEMENT_OT_render_layer')