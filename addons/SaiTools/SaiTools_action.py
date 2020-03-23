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
from bpy.props import IntProperty, BoolProperty, FloatProperty, EnumProperty
from mathutils import Vector, Euler 

#---------------------------------------------------#
#-----------------ObjectOperator--------------------#
#---------------------------------------------------#

class ObjectOperator(object):
    
    @classmethod
    def CleanUnuseData(cls):

        def cleanData(datatype):
            for data in datatype:
                if data.users == 0:
                    datatype.remove(data)
                    
        cleanData(bpy.data.meshes)
        cleanData(bpy.data.materials)
        cleanData(bpy.data.textures)
    @classmethod
    def SetOriginHere(cls):
        """Set Object Origin Here"""
        savePos = bpy.context.scene.cursor_location.copy()
        
        if bpy.context.mode == 'EDIT_MESH':
            bpy.ops.view3d.snap_cursor_to_selected()
            bpy.ops.object.editmode_toggle()
            bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
            bpy.ops.object.editmode_toggle()
            bpy.context.scene.cursor_location = savePos 
        
        else:
            bpy.ops.view3d.snap_cursor_to_selected()
            bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
            bpy.context.scene.cursor_location = savePos 

        return{'FINISHED'}
        
    @classmethod
    def AlignOriginNormal(cls):
        """Align Obect Origin as Manipulator's Normal"""
        ObjectOperator.SetOriginHere()
        
        fixobj = bpy.context.object
        bpy.ops.transform.create_orientation(name='temprot' ,use=False ,overwrite = True)
        tempeula = bpy.context.scene.orientations['temprot'].matrix.to_euler('XYZ')
        # backup 3d cursor pos
        bak_cursor = bpy.context.scene.cursor_location.copy()
        
        if bpy.context.mode == 'EDIT_MESH':

            bpy.ops.view3d.snap_cursor_to_selected()
            temppos = bpy.context.scene.cursor_location
            bpy.ops.object.mode_set(mode='OBJECT',toggle=False)
            
            # create Alignnode and change object's origin 
            bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN') 
            bpy.ops.object.empty_add(type='PLAIN_AXES', view_align=False, location=temppos , rotation=tempeula)
            bpy.context.object.name = 'SaveOriginnode'   
            bpy.ops.object.empty_add(type='PLAIN_AXES', view_align=False, location=temppos , rotation=tempeula)
            bpy.context.object.name = 'NewOriginnode'
            fixobj.select = True
            bpy.context.scene.objects.active = bpy.data.objects['NewOriginnode']
            bpy.ops.object.parent_set(type='OBJECT', xmirror=False, keep_transform=True)
            bpy.data.objects['NewOriginnode'].rotation_euler = (Euler((0, 0, 0), 'XYZ'))
            bpy.context.scene.objects.active = fixobj
            bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
            bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
            fixobj.rotation_euler = bpy.data.objects['SaveOriginnode'].rotation_euler
            bpy.ops.object.select_all(action='TOGGLE')
            bpy.data.objects['NewOriginnode'].select = True
            bpy.data.objects['SaveOriginnode'].select = True
            bpy.ops.object.delete(use_global=False)
            fixobj.select = True
            
            # return 3d cursor pos
            bpy.context.scene.cursor_location = bak_cursor
            bpy.ops.object.mode_set(mode='EDIT',toggle=False)
            
        return{'FINISHED'}

    def MoveToZero():
        for obj in bpy.context.selected_objects:
            obj.location = (0,0,0)
            
        return {'FINISHED'}

#---------------------------------------------------#
#----------------MaterialOperator-------------------#
#---------------------------------------------------#
      
class MaterialOperator(object):
    
    @classmethod
    def Copy_Material_To_Selection(cls):
        """Copy Actived Material to Selection"""
        context = bpy.context
        data = bpy.data
        activeObject = context.active_object
        
        activeMaterialSlots = len(context.active_object.material_slots)
        removeSwitch = 0
        
        if activeMaterialSlots == 0 :
            bpy.ops.object.material_slot_add()
            removeSwitch = 1
        
        for obj in context.selected_objects:
            if obj.type not in {'MESH', 'SURFACE', 'CURVE', 'META', 'FONT'}:
                obj.select = False

        doArray = (context.selected_objects)
        doArray.remove(context.object)
        
        for obj in doArray:
            context.scene.objects.active = obj
            selfMaterialSlots = len(obj.material_slots)
            
            mCount = activeMaterialSlots - selfMaterialSlots
            
            if selfMaterialSlots < activeMaterialSlots:
                for i in range(activeMaterialSlots-selfMaterialSlots):
                    bpy.ops.object.material_slot_add()
            
            selfMaterialSlots = len(obj.material_slots)        
            
            for i in range(selfMaterialSlots):
                if i <= (activeMaterialSlots-1):
                    obj.material_slots[i].material = activeObject.material_slots[i].material
                else :
                    obj.material_slots[i].material = activeObject.material_slots[(activeMaterialSlots-1)].material
                
        context.scene.objects.active = activeObject
        
        if removeSwitch == 1 :
            bpy.ops.object.material_slot_remove()

        return ('FINISH') 
    #---------------------------------------------------#
    @classmethod
    def PreserveMaterial(cls):
        """Preserve Object's Material """
        context = bpy.context
        data = bpy.data
        activeObject = context.active_object
        
        for obj in context.selected_objects:           
            MArray = []
            for i in range(len(obj.material_slots)):
                MslotID = i
                Mname =  obj.material_slots[i].name
                if Mname == '':
                    Mname = '_undefined'
                temparray = [MslotID,Mname]
                MArray.append(temparray)
                
            strMArray = (str(MArray))
            obj["Mslot"] = (strMArray)
            
            if (len(obj.material_slots)) == 0:
                obj["Mslot"] = str([[0, '_undefined']])
                    
        return{'FINISHED'}
    #---------------------------------------------------# 
    @classmethod
    def RestoreMaterial(cls):
        """Restore Object's Material """
        context = bpy.context
        data = bpy.data
        activeObject = context.active_object

        bpy.ops.object.material_slot_add()
        emptyMaterial = context.object.active_material
        bpy.ops.object.material_slot_remove()
       
        for obj in context.selected_objects:
            if obj.get('Mslot', 'undefined') !=  'undefined':
                MArray = (eval(obj["Mslot"]))
                for m in range(len(MArray)):
                    if ((MArray[m][1]) != '_undefined' and (MArray[m][1]) != '_empty'):
                        obj.material_slots[m].material = data.materials[(MArray[m][1])]
                    else :
                        obj.material_slots[m].material = emptyMaterial 
                           
        context.scene.objects.active = activeObject
            
        return{'FINISHED'}        
    #---------------------------------------------------# 
    @classmethod    
    def CollectMaterials(cls):
        """Collect All Material """
        activeObject = bpy.context.active_object
        materialsBox = bpy.data.objects.get("1_AllMatToMe")
        
        if materialsBox != None:
            delObj = bpy.data.objects.get("1_AllMatToMe") 
            delData = delObj.data
            bpy.data.objects.remove(delObj, True)
            bpy.data.meshes.remove(delData)
        
        bpy.ops.mesh.primitive_cube_add()
        materialsBox = bpy.context.active_object
        materialsBox.name = "1_AllMatToMe"
        bpy.data.objects["1_AllMatToMe"].hide = True

        for mat in bpy.data.materials:
            materialsBox.data.materials.append(mat)
        
        bpy.context.scene.objects.active = activeObject
        if activeObject != None:
            activeObject.select = True
            
        return{'FINISHED'}       
        
    #---------------------------------------------------#

    @classmethod
    def RelinkMaterial(cls):
        """Relink Material Library"""
        linkedMaterial = {}

        for mat in bpy.data.materials:
            if mat.library:
                linkedMaterial[mat.name] = mat
                
        for obj in bpy.data.objects:
            for mat in obj.material_slots:
                if (mat.name) in linkedMaterial.keys():
                    mat.material = linkedMaterial[mat.name]



#---------------------------------------------------#
#------------------MeshOperator---------------------#
#---------------------------------------------------#
                    
class MeshOperator(object):
    
    #---------------------------------------------------# 
    @classmethod    
    def Select_Same_Facecounts_Objs(cls):
        """Select Same Face Counts Mesh"""
        context = bpy.context        
        data = bpy.data
        activeObject = bpy.context.active_object
        
        count = (len(activeObject.data.polygons))
        collectObjs = [obj for obj in data.objects if (obj.type == 'MESH') and (len(obj.data.polygons) == count)]
            
        for obj in collectObjs:
            obj.select = True      

        return ('FINISH') 

class Data_model():
    
    def __init__(self):
        self._context = bpy.context
        self._data = bpy.data
        self._activeObject = context.active_object
        
    def context(self):
        return self._context
        
    def data():
        return self._data
    
    def activeObject(self):
        return self._activeObject
        
# MeshOp = MeshOperator()
# MeshOp.Select_Same_Facecounts_Objs(Data_model())