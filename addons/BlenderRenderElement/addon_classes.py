import bpy
from bpy.types import Panel, Menu
from bpy.props import (
    FloatProperty,
    BoolProperty,
    IntProperty,
)

class ELEMENT_properties(bpy.types.PropertyGroup):

    # output_path : bpy.props.StringProperty(
    #     default = bpy.path.abspath("//"),
    #     subtype="FILE_PATH",
    #     name = "Texture Folder"
    # )
    suffix_basecolor : bpy.props.StringProperty(
        default = "_BaseColor",
        name = "BaseColor Suffix",
    )

class COMPOSITOR_PT_RenderElement(Panel):
    bl_idname = 'COMPOSITOR_PT_RenderElement'
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'Item'
    # bl_options = {"DEFAULT_CLOSED"}
    # @classmethod
    # def poll(cls, context):
    #     cls.active_node = context.scene.node_tree.nodes.active
    #     cls.scene = context.scene
    #     cls.renderer = context.scene.render
    #     cls.view_layers = context.scene.view_layers
    #     cls.cycles_view_layer = context.view_layer.cycles
    #     return True

class ELEMENT_PT_main_menu(COMPOSITOR_PT_RenderElement, Panel):
    bl_idname = 'ELEMENT_PT_main_menu'
    bl_label = 'Render Elements Tools'

    def draw(self, context):
        pass

class ELEMENT_PT_render_layers(COMPOSITOR_PT_RenderElement, Panel):
    bl_idname = 'ELEMENT_PT_render_layers'
    bl_label = 'render_layers'
    bl_parent_id = 'ELEMENT_PT_main_menu'

    @classmethod
    def poll(cls, context):
        active_node = context.scene.node_tree.nodes.active
        return type(active_node) is bpy.types.CompositorNodeRLayers
        
    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False
        row = layout.row(align=True)
        row.operator('element.operators', text='Create Output').action = 'Create Output'

class ELEMENT_PT_data(COMPOSITOR_PT_RenderElement, Panel):
    bl_idname = 'ELEMENT_PT_data'
    bl_label = 'Data'
    bl_parent_id = 'ELEMENT_PT_main_menu'

    def draw(self, context):
        
        self.active_layer = self.view_layers[self.active_node.layer]
        if self.renderer.engine == 'BLENDER_EEVEE':
            self.eevee_element(context)
        elif self.renderer.engine == 'CYCLES':
            self.cycles_elelemt(context)

    def eevee_element(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        row = layout.row(align=True)
        row.prop(self.active_layer, 'use_pass_combined',text='Beauty', toggle=True)
        row = layout.row(align=True)
        row.prop(self.active_layer, 'use_pass_z', text='Z Buffer', toggle=True)
        row = layout.row(align=True)
        row.prop(self.active_layer, 'use_pass_mist',text='Mist/Fog', toggle=True)
        row = layout.row(align=True)
        row.prop(self.active_layer, 'use_pass_normal',text='Normal', toggle=True)

    def cycles_elelemt(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        row = layout.row(align=True)
        row.prop(self.active_layer, 'use_pass_combined',text='Beauty', toggle=True)
        row = layout.row(align=True)
        row.prop(self.active_layer, 'use_pass_z', text='Z Buffer', toggle=True)
        row = layout.row(align=True)
        row.prop(self.active_layer, 'use_pass_normal',text='Normal', toggle=True)
        row = layout.row(align=True)
        row.prop(self.active_layer, 'use_pass_vector',text='Motion Vector', toggle=True)
        row.active = not self.renderer.use_motion_blur
        row = layout.row(align=True)
        row.prop(self.active_layer, "use_pass_shadow", toggle=True)
        row = layout.row(align=True)
        row.prop(self.active_layer, "use_pass_ambient_occlusion", text="Ambient Occlusion", toggle=True)
        row = layout.row(align=True)
        row.prop(self.active_layer, 'use_pass_uv', text='UV', toggle=True)
        row = layout.row(align=True)
        row.prop(self.active_layer, 'use_pass_object_index',text='Object Index', toggle=True)
        row = layout.row(align=True)
        row.prop(self.active_layer, 'use_pass_material_index',text='Material Index', toggle=True)
        row = layout.row(align=True)
        row.prop(self.active_layer, 'use_pass_mist',text='Mist/Fog', toggle=True)


class ELEMENT_PT_lights(COMPOSITOR_PT_RenderElement, Panel):
    bl_idname = 'ELEMENT_PT_lights'
    bl_label = 'Light / Surface'
    bl_parent_id = 'ELEMENT_PT_main_menu'

    def draw(self, context):
        self.active_layer = self.view_layers[self.active_node.layer]
        if self.renderer.engine == 'BLENDER_EEVEE':
            self.eevee_element(context)
        elif self.renderer.engine == 'CYCLES':
            self.cycles_elelemt(context)

    def eevee_element(self, context):
        pass

    def cycles_elelemt(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        row = layout.row(align=True)
        row.label(text="Diffuse")
        row = layout.row(align=True)
        row.prop(self.active_layer, "use_pass_diffuse_direct", text="Direct", toggle=True)
        row = layout.row(align=True)
        row.prop(self.active_layer, "use_pass_diffuse_indirect", text="Indirect", toggle=True)
        row = layout.row(align=True)
        row.prop(self.active_layer, "use_pass_diffuse_color", text="Color", toggle=True)

        row = layout.row(align=True)
        row.label(text="Glossy")
        row = layout.row(align=True)
        row.prop(self.active_layer, "use_pass_glossy_direct", text="Direct", toggle=True)
        row = layout.row(align=True)
        row.prop(self.active_layer, "use_pass_glossy_indirect", text="Indirect", toggle=True)
        row = layout.row(align=True)
        row.prop(self.active_layer, "use_pass_glossy_color", text="Color", toggle=True)

        row = layout.row(align=True)
        row.label(text="Transmission")
        row = layout.row(align=True)
        row.prop(self.active_layer, "use_pass_transmission_direct", text="Direct", toggle=True)
        row = layout.row(align=True)
        row.prop(self.active_layer, "use_pass_transmission_indirect", text="Indirect", toggle=True)
        row = layout.row(align=True)
        row.prop(self.active_layer, "use_pass_transmission_color", text="Color", toggle=True)

        row = layout.row(align=True)
        row.label(text="Emit / Env")
        row = layout.row(align=True)
        row.prop(self.active_layer, "use_pass_emit", text="Emission", toggle=True)
        row = layout.row(align=True)
        row.prop(self.active_layer, "use_pass_environment", toggle=True)

        row = layout.row(align=True)
        row.label(text="Volume")
        row = layout.row(align=True)
        row.prop(self.active_layer.cycles, "use_pass_volume_direct", text="Direct", toggle=True)
        row = layout.row(align=True)
        row.prop(self.active_layer.cycles, "use_pass_volume_indirect", text="Indirect", toggle=True)


class ELEMENT_PT_cryptomatte(COMPOSITOR_PT_RenderElement, Panel):
    bl_idname = 'ELEMENT_PT_cryptomatte'
    bl_label = 'Cryptomatte'
    bl_parent_id = 'ELEMENT_PT_main_menu'

    def draw(self, context):
        self.active_layer = self.view_layers[self.active_node.layer]
        if self.renderer.engine == 'BLENDER_EEVEE':
            self.eevee_element(context)
        elif self.renderer.engine == 'CYCLES':
            self.cycles_elelemt(context)

    def eevee_element(self, context):
        pass

    def cycles_elelemt(self, context):
        layout = self.layout
        # layout.use_property_split = True
        layout.use_property_decorate = False

        row = layout.row(align=True)
        row.prop(self.active_layer.cycles, 'use_pass_crypto_object',text='Object', toggle=True)
        row.prop(self.active_layer.cycles, 'use_pass_crypto_material',text='Material', toggle=True)
        row.prop(self.active_layer.cycles, 'use_pass_crypto_asset',text='Asset', toggle=True)
        row = layout.row(align=True)
        row.label(text="Levels")
        row.prop(self.active_layer.cycles, "pass_crypto_depth", text='')
        row = layout.row(align=True)
        row.use_property_split = True
        row.prop(self.active_layer.cycles, "pass_crypto_accurate", text="Accurate Mode")

class ELEMENT_PT_other(COMPOSITOR_PT_RenderElement, Panel):
    bl_idname = 'ELEMENT_PT_other'
    bl_label = 'Debug / Denoise'
    bl_parent_id = 'ELEMENT_PT_main_menu'

    def draw(self, context):
        self.active_layer = self.view_layers[self.active_node.layer]
        if self.renderer.engine == 'BLENDER_EEVEE':
            self.eevee_element(context)
        elif self.renderer.engine == 'CYCLES':
            self.cycles_elelemt(context)

    def eevee_element(self, context):
        pass

    def cycles_elelemt(self, context):
        layout = self.layout
        # layout.use_property_split = True
        layout.use_property_decorate = False

        row = layout.row(align=True)
        row.prop(self.active_layer.cycles, "pass_debug_render_time", text="Render Time", toggle=True)
        row.prop(self.active_layer.cycles, "pass_debug_sample_count", text="Sample Count", toggle=True)
        row = layout.row(align=True)
        row.prop(self.active_layer.cycles, "use_denoising", text="Denoising", toggle=True)
        row.prop(self.active_layer.cycles, "denoising_store_passes", text="Denoising Data", toggle=True)

class ELEMENT_OT_operators(bpy.types.Operator):
    bl_label ="ELEMENT Operators"
    bl_idname="element.operators"
    bl_options = {'REGISTER', 'UNDO'}

    action:bpy.props.StringProperty(default='ELEMENT Actions')
    margin:bpy.props.IntProperty(default=100)
   
    @classmethod
    def description(cls, context, properties):
        return properties.action

    def execute(self, context):
        self.active_node = context.scene.node_tree.nodes.active
        self.scene = context.scene
        self.node_tree = context.scene.node_tree
        self.renderer = context.scene.render
        self.view_layers = context.scene.view_layers
        self.cycles_view_layer = context.view_layer.cycles

        action = self.action
        try:
            ## ObjectOperator
            if action=='Create Output': self.action_create_output()
        
            else:
                print ('Not defined !')
        except Exception as e:
            print ('Execute Error:',e)
        
        return {"FINISHED"}

    def action_create_output(self):
        if type(self.active_node) is bpy.types.CompositorNodeRLayers:
            layer_outputs = self.active_node.outputs
            # create output node
            output_node = self.node_tree.nodes.new("CompositorNodeOutputFile")
            output_node.label = self.active_node.name
            output_node.location.y = self.active_node.location.y
            output_node.location.x =  self.active_node.location.x + self.active_node.width + self.margin
            [output_node.file_slots.new(slot.name) for slot in layer_outputs if slot.enabled]
            