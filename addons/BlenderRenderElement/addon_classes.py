import bpy
from bpy.types import Panel, Menu
from bpy.props import (
    FloatProperty,
    BoolProperty,
)


class ELEMENT_properties(bpy.types.PropertyGroup):

    output_path : bpy.props.StringProperty(
        default = bpy.path.abspath("//"),
        subtype="FILE_PATH",
        name = "Texture Folder"
    )
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
    @classmethod
    def poll(cls, context):
        cls.active_node = context.scene.node_tree.nodes.active
        cls.scene = context.scene
        cls.renderer = context.scene.render
        cls.view_layers = context.scene.view_layers
        
        cls.cycles_view_layer = context.view_layer.cycles
        return type(cls.active_node) is bpy.types.CompositorNodeRLayers

class ELEMENT_PT_main(COMPOSITOR_PT_RenderElement, Panel):
    bl_idname = 'ELEMENT_PT_main'
    bl_label = 'Render Element'

    def draw(self, context):
        pass

class ELEMENT_PT_data(COMPOSITOR_PT_RenderElement, Panel):
    bl_idname = 'ELEMENT_PT_data'
    bl_label = 'Data'
    bl_parent_id = 'ELEMENT_PT_main'

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
        row.prop(self.active_layer, 'use_pass_mist',text='Mist/Fog', toggle=True)
        row = layout.row(align=True)
        row.prop(self.active_layer, 'use_pass_normal',text='Normal', toggle=True)
        row = layout.row(align=True)
        row.prop(self.active_layer, 'use_pass_vector',text='Motion Vector', toggle=True)
        # row.active = not rd.use_motion_blur
        row = layout.row(align=True)
        row.prop(self.active_layer, 'use_pass_uv', text='UV', toggle=True)
        row = layout.row(align=True)
        row.prop(self.active_layer, 'use_pass_object_index',text='Object Index', toggle=True)
        row = layout.row(align=True)
        row.prop(self.active_layer, 'use_pass_material_index',text='Material Index', toggle=True)



class ELEMENT_PT_lights(COMPOSITOR_PT_RenderElement, Panel):
    bl_idname = 'ELEMENT_PT_lights'
    bl_label = 'Light'
    bl_parent_id = 'ELEMENT_PT_main'

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
        row.prop(self.active_layer, "use_pass_shadow", toggle=True)
        row = layout.row(align=True)
        row.prop(self.active_layer, "use_pass_ambient_occlusion", text="Ambient Occlusion", toggle=True)
        row = layout.row(align=True)
        row.prop(self.active_layer, "use_pass_emit", text="Emission", toggle=True)
        row = layout.row(align=True)
        row.prop(self.active_layer, "use_pass_environment", toggle=True)

        split = layout.split(factor=0.35)
        split.use_property_split = False
        split.label(text="Diffuse")
        row = split.row(align=True)
        row.prop(self.active_layer, "use_pass_diffuse_direct", text="Direct", toggle=True)
        row.prop(self.active_layer, "use_pass_diffuse_indirect", text="Indirect", toggle=True)
        row.prop(self.active_layer, "use_pass_diffuse_color", text="Color", toggle=True)

        split = layout.split(factor=0.35)
        split.use_property_split = False
        split.label(text="Glossy")
        row = split.row(align=True)
        row.prop(self.active_layer, "use_pass_glossy_direct", text="Direct", toggle=True)
        row.prop(self.active_layer, "use_pass_glossy_indirect", text="Indirect", toggle=True)
        row.prop(self.active_layer, "use_pass_glossy_color", text="Color", toggle=True)

        split = layout.split(factor=0.35)
        split.use_property_split = False
        split.label(text="Transmission")
        row = split.row(align=True)
        row.prop(self.active_layer, "use_pass_transmission_direct", text="Direct", toggle=True)
        row.prop(self.active_layer, "use_pass_transmission_indirect", text="Indirect", toggle=True)
        row.prop(self.active_layer, "use_pass_transmission_color", text="Color", toggle=True)

        split = layout.split(factor=0.35)
        split.use_property_split = False
        split.label(text="Volume")
        row = split.row(align=True)
        row.prop(self.active_layer.cycles, "use_pass_volume_direct", text="Direct", toggle=True)
        row.prop(self.active_layer.cycles, "use_pass_volume_indirect", text="Indirect", toggle=True)



class ELEMENT_PT_cryptomatte(COMPOSITOR_PT_RenderElement, Panel):
    bl_idname = 'ELEMENT_PT_cryptomatte'
    bl_label = 'Cryptomatte'
    bl_parent_id = 'ELEMENT_PT_main'

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
    bl_label = 'Debug/Denoise'
    bl_parent_id = 'ELEMENT_PT_main'

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