import bpy
from bpy import data


if data.curves.get('mycurve') == None:
    mycurvedata = data.curves.new(name='mycurve', type='CURVE')
    mycurvedata.dimensions = '3D'

mycurvedata = data.curves('mycurve')
mycurvedata.show_handles = False
mycurvedata.show_normal_face = False


if data.objects.get('mycurve') == None:
    objectdata = data.objects.new('mycurve', mycurvedata )
    bpy.context.scene.objects.link(objectdata)


if len(mycurvedata.splines) == 0:
    polyline = mycurvedata.splines.new('POLY')
    polyline.points.add(3)
    polyline.type = 'BEZIER'
    
polyline = mycurvedata.splines[0]

for bezierPoint in polyline.bezier_points:
    bezierPoint.handle_left_type = 'AUTO'
    bezierPoint.handle_right_type = 'AUTO'

