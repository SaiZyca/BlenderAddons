import bpy
import bmesh
from bpy import data, context
from mathutils import Vector
from operator import itemgetter, attrgetter


currentMesh =  bmesh.from_edit_mesh(context.active_object.data)

def CollectSelectData():
    currentMesh =  bmesh.from_edit_mesh(context.active_object.data)
    collectSelectVert = [vert for vert in currentMesh.verts if vert.select == True] 
    collectSelectEdges = [edge for edge in currentMesh.edges if edge.select == True]   
    
    return (collectSelectVert,collectSelectEdges)




def Sort_VertsIndex_By_Edgeloop(verts,edges):
    
    singleVert = []
    multiVert = []
    startVert = None
    startEdge = None
    #separate data
    for vert in verts:
        if (len(set(vert.link_edges) & set(edges))) > 1:
            multiVert.append(vert)
        else:
            singleVert.append(vert)
    #get start vert
    if len(singleVert) == 0 and len(multiVert) == 0:
        startVert = None
        starEdge = None
    elif len(singleVert) >= 1 :
        startVert = singleVert[0]
    else:
        startVert = multiVert[0]
    #get start edge
    startEdge = [edge for edge in startVert.link_edges if edge in edges]
    #sort by edgeloop
    sortedVerts = []
    sortedEdges = []   
    if len(startEdge) >= 1:
        sortedVerts.append(startVert)
        count = 0
        while count < len(verts):
            index = len(sortedVerts) - 1
            nextEdge = [edge for edge in sortedVerts[index].link_edges if (edge in edges) and (edge not in sortedEdges)]
            if len(nextEdge) >= 1:
                sortedEdges.append(nextEdge[0]) 
                nextVert = [vert for vert in nextEdge[0].verts if vert not in sortedVerts]
                if len(nextVert) == 1:
                    sortedVerts.append(nextVert[0])
            count += 1
            
    return (sortedVerts,sortedEdges)


def SimpifyVerts():
    
    def _getlength(x):
        return (x.calc_length())
    
    bm = bmesh.from_edit_mesh(context.active_object.data)
    edges = CollectSelectData()[1]
    targetCount = 13 
    edgeCount = len(edges)
    while edgeCount > targetCount:
        edgeCount -= 1
        
        bm = bmesh.from_edit_mesh(context.active_object.data)
        edges = CollectSelectData()[1]
        
        allVerts = []
        for edge in edges:
            for vert in edge.verts:
                allVerts.append(vert)
        freezeVert = [vert for vert in allVerts if allVerts.count(vert) == 1 ]
        for vert in freezeVert:
            for edge in vert.link_edges:
                if edge in edges:
                    edges.remove(edge)
        
        tempList = sorted(edges, key=_getlength)
        fixedEdge=[]
        fixedEdge.append(tempList[0])
        bmesh.ops.collapse(bm, edges=fixedEdge, uvs=True)
    
        # avoid bmesh.ops.collapse crash
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.mode_set(mode='EDIT')



def Draw_Curve_From_Verts(curveName,verts):
    w = 1
    pointArray = [context.active_object.matrix_world*vert.co for vert in verts]
    # define curve data
    if data.curves.get(curveName) == None:
        curvedata = bpy.data.curves.new(name=curveName, type='CURVE')
        curvedata.dimensions = '3D'
        
    else:
        ## inital curve display
        myCurveData = data.curves[curveName]
        myCurveData.show_handles = False
        myCurveData.show_normal_face = False
    
    # link curve data to curve object 
    if data.objects.get(curveName) == None:
        objectdata = data.objects.new(curveName, myCurveData)
        objectdata.location = (0,0,0) #object origin
        bpy.context.scene.objects.link(objectdata)
    
    # add spline to curve data
    if len(myCurveData.splines) > 0:
        for spline in myCurveData.splines:
            myCurveData.splines.remove(spline)

    polyline = myCurveData.splines.new('POLY')
    polyline.points.add(len(pointArray)-1)
    
    
    for num in range(len(pointArray)):
        x, y, z = pointArray[num]
        polyline.points[num].co = (x, y, z, w)
            
    polyline.type = 'BEZIER'
    
    for bezierPoint in polyline.bezier_points:
        bezierPoint.handle_left_type = 'AUTO'
        bezierPoint.handle_right_type = 'AUTO'

    

def PrintTest():
    verts = (CollectSelectData())[0]
    edges = (CollectSelectData())[1]
    data = (Sort_VertsIndex_By_Edgeloop(verts,edges))
    #pointArray = [vert.co for vert in data[0]]
    #print (pointArray)
    Draw_Curve_From_Verts('TestCurve',data[0])

SimpifyVerts()


def Get_Vertex_From_EdgeLoop(edges):
    allVerts = []
    singleVerts = []
    multiVerts = []
    
    for edge in edges:
        for vert in edge.verts:
            allVerts.append(vert)
    
    uniqueVerts = set(allVerts)
    
    for vert in uniqueVerts:
        if allVerts.count(vert) == 1 :
            singleVerts.append(vert)
        else:
            multiVerts.append(vert)
    
    if len(singleVerts) > 0 :
        allVerts = singleVerts + multiVerts
    

    return (allVerts)


def SortVerts(allVerts,selectedEdges):
    startVert = allVerts[0]
    startEdge = [edge for edge in selectedEdges if (edge in startVert.link_edges)][0]
    resortEdges = []
    resortVerts = []
    resortEdges.append(startEdge)
    resortVerts.append(startVert)
    count = 0
    while len(resortEdges) <= len(selectedEdges):
        print (count)
        nextVert = [vert for vert in resortEdges[count].verts if vert not in resortVerts][0]
        nextEdge = [edge for edge in selectedEdges if (edge in nextVert.link_edges) and (edge not in resortEdges)][0]
        resortEdges.append(nextEdge)
        resortVerts.append(nextVert)
        count += 1
    for c in resortVerts:
        print (c.index)
    #print (startEdge,startVert)



def printDir():
    currentMesh =  bmesh.from_edit_mesh(context.active_object.data)
    for key in dir(currentMesh.edges):
        print (key)



