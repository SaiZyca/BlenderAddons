import bpy
import bmesh
from bpy import data, context
from mathutils import Vector

currentMesh =  bmesh.from_edit_mesh(context.active_object.data)
fixHistory = (currentMesh.select_history)

for vert in ((currentMesh).verts):
    if vert.select:
        print ('vertexIndex = {0},{1}'.format(vert.index,"Yes Selected!!"))
    else:
        print ('vertexIndex = {0},{1}'.format(vert.index,"No!!"))
#for key in dir(currentMesh):
#    print (key)
