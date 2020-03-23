# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# write by SaiLing, 2013/01/10
# 2017/09/18 rewrite as addon package

   
import bpy
from . import SaiTools_action
from .SaiTools_action import MaterialOperator, MeshOperator, ObjectOperator

## defined Panel and Rollout ui
#-------------------------------------------------------#
## Cursor & Origin Tools Rollout
class CursorOriginPanel(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "SaiToolsKit"
    bl_label = "Object & Data"
    bl_options = {"DEFAULT_CLOSED"}

## defined Tools button ui    
    def draw(self,context):
        layout = self.layout
        ## Data Tools
        row = layout.row(align=False)
        row.operator('sai_ui.ops',text = 'Clean Unused Data').button = 'CleanUnuseData'           
        ## Origin Tools
        row = layout.row(align=False)
        layout.label('Origin Tools')
        row = layout.row(align=False)
        row.operator('sai_ui.ops',text = 'Origin here').button = 'SetOriginHere' 
        row = layout.row(align=False)
        row.operator('sai_ui.ops',text = 'Origin Align Normal').button = 'AlignOriginNormal'
        row =layout.row(align=False)
        row.operator('sai_ui.ops',text = 'move to zero').button = 'MoveToZero'
     
        
## material Tools Rollout
class MaterialToolsPanel(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "SaiToolsKit"
    bl_label = "Material Tools"
    bl_options = {"DEFAULT_CLOSED"}
  
## defined Tools button ui
    def draw(self,context):
        layout = self.layout
        
        ## Material Tool
        #layout.label('Material Tool')
        ## All Material To Me
        row = layout.row(align = True)
        row.operator('sai_ui.ops',text = 'All Material To Me').button = 'collectmaterial'   
        ## Copy Material
        row = layout.row(align = True)
        row.operator('sai_ui.ops',text = 'Copy Material').button = 'copymaterial'   
        
        #layout.label('Preserve/Reload Material')
        row = layout.row(align=True)
        row.scale_y = 1
        row.operator('sai_ui.ops',text = 'Preserve').button = 'preserve'
        row.operator('sai_ui.ops',text = 'Restore').button = 'restore'
        row = layout.row(align = True)
        row.operator('sai_ui.ops',text = 'ReLinkMaterial').button = 'relinkmaterial'
        
## Mesh Tools Rollout
class MeshToolsPanel(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "SaiToolsKit"
    bl_label = "Mesh Tools"
    bl_options = {"DEFAULT_CLOSED"}
    
 ## defined Tools button ui   
    def draw(self,context):
        layout = self.layout
        #layout.label('Mesh Tools')
        row = layout.row(align = True)
        row.operator('sai_ui.ops',text = 'Select same face counts Objs').button = 'selectSameFace'

      
## defined UI operator
        
class Sai_Ui_Ops(bpy.types.Operator):
    """Ui Operator"""
    bl_label ="SaiTools UI Operator"
    bl_idname="sai_ui.ops"

    button=bpy.props.StringProperty(default="")
    
    def execute(self, context):
        button=self.button
        try:
            ## ObjectOperator
            if button=="CleanUnuseData":        ObjectOperator.CleanUnuseData()
            elif button=="SetOriginHere":       ObjectOperator.SetOriginHere()
            elif button=="AlignOriginNormal":   ObjectOperator.AlignOriginNormal()
            elif button=="MoveToZero":          ObjectOperator.MoveToZero()
                
            ## MaterialOperator
            elif button=="collectmaterial":     MaterialOperator.CollectMaterials()
            elif button=="copymaterial":        MaterialOperator.Copy_Material_To_Selection()
            elif button=="preserve":            MaterialOperator.PreserveMaterial()
            elif button=="restore":             MaterialOperator.RestoreMaterial()
            elif button=="materialalpha":       MaterialOperator.ShowMaterialAlpha()
            elif button=="relinkmaterial":      MaterialOperator.RelinkMaterial()
            ## MeshOperator
            elif button=="selectSameFace":      MeshOperator.Select_Same_Facecounts_Objs()
        
            else:
                print ('Not defined !')
        except Exception as e:
            print ('Execute Error:',e)
        
        return {"FINISHED"}
  

