import bpy
import bmesh
from bpy import data, context
from mathutils import Vector

w = 1 # weight
listOfVectors = [Vector((0,0,0)),Vector((1,0,0)),Vector((2,0,0)),Vector((2,3,0)),
        Vector((0,2,1))]

def my_CreateCurve(curveName, pointArray):
    if data.curves.get(curveName) == None:
        curvedata = bpy.data.curves.new(name=curveName, type='CURVE')
        curvedata.dimensions = '3D'
        
    else:
        ## inital curve display
        myCurveData = data.curves[curveName]
        myCurveData.show_handles = False
        myCurveData.show_normal_face = False
    
    if data.objects.get(curveName) == None:
        objectdata = data.objects.new(curveName, myCurveData)
        objectdata.location = (0,0,0) #object origin
        bpy.context.scene.objects.link(objectdata)

    if len(myCurveData.splines) == 0:
        polyline = myCurveData.splines.new('POLY')
        polyline.points.add(len(pointArray)-1)
        
        
        for num in range(len(pointArray)):
            x, y, z = pointArray[num]
            polyline.points[num].co = (x, y, z, w)
                
        polyline.type = 'BEZIER'
        
        for bezierPoint in polyline.bezier_points:
            bezierPoint.handle_left_type = 'AUTO'
            bezierPoint.handle_right_type = 'AUTO'

# my_CreateCurve("NameOfMyCurveObject", listOfVectors)

# def getMeshCurve: