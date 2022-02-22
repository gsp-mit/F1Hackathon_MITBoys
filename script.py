import bpy
import json
import math
import requests

#IMPORTANT NOTE: SCRIPT MAY TAKE 30-60 SECONDS TO RUN DUE TO SLOW HTTP GET REQUEST FROM API. RUNNING SCRIPT WITH LOCALLY SAVED INPUT FILES WILL ONLY TAKE 5-10 SECONDS.


#ENTER SESSION IDS HERE
idCenter = "6424586751601551341"
idLeft = "14723197675720646148"
idRight = "3447308828675135472"

"""
SAMPLE SESSION IDS
MELBOURNE
idCenter = "6424586751601551341"
idLeft = "14723197675720646148"
idRight = "3447308828675135472"

BAHRAIN
idCenter = "3370806962101808516"
idLeft = "7991677079664725642"
idRight = "9065767181428164173"

TEXAS
idCenter = "12959366596380051521"
idLeft = "12739104041678494733"
idRight = "9742647087467354271"
"""


#OBTAIN JSON DATA FROM API AND STORE IN LOCAL FILES FOR BETTER RENDER TIMES
baseurl = "https://apigw.withoracle.cloud/formulaai/v2/trackData/"

urlLeft = baseurl + idLeft + "/1"
urlRight = baseurl + idRight + "/1"
urlCenter = baseurl + idCenter + "/1"

r = requests.get(urlLeft).text
Left = open("left.txt","w")
Left.write(r)
Left.close()
Left = open("left.txt","r")
Ldata = json.load(Left)      #LOAD JSON DATA INTO VARIABLE

r = requests.get(urlRight).text
Right = open("right.txt","w")
Right.write(r)
Right.close()
Right = open("right.txt","r")
Rdata = json.load(Right)

r = requests.get(urlCenter).text
Center = open("center.txt","w")
Center.write(r)
Center.close()
Center = open("center.txt","r")
Cdata = json.load(Center)

offset = 0

#NORMALIZE Z-AXIS OFFSET TO ACCOUNT FOR UNEVEN INPUT
count = 0
for i,j in enumerate(Ldata):
    if(count==1):
        break
    count = count + 1
    z = j["WORLDPOSZ"]
    offset = - z
    offset = offset + 5


#UNHIDE ALL OBJECTS
bpy.ops.object.select_all(action='DESELECT')
for obj in bpy.data.objects:
    obj.hide_viewport = False
    obj.hide_render = False 
    obj.hide_set(False) 
    obj.hide_select = False


#CREATE LEFT PART OF TRACK

coords = []
for i,j in enumerate(Ldata):
    x = j["WORLDPOSX"]
    y = j["WORLDPOSY"]
    z = j["WORLDPOSZ"] + offset
    coords.append([x,y,z])
    
curveData = bpy.data.curves.new('LEFT', type='CURVE')

curveData.dimensions = '3D'
curveData.resolution_u = 2

polyline = curveData.splines.new('POLY')   #PLOT COORDINATES AS POLYLINE
polyline.points.add(len(coords))
count = 0
for i, coord in enumerate(coords):
    count = count + 1
    x,y,z = coord
    polyline.points[i].co = (x*0.01, y*0.01, z*0.01, 1)


curveOB = bpy.data.objects.new('LEFT', curveData)
bpy.context.scene.collection.objects.link(curveOB)
bpy.context.view_layer.objects.active = curveOB

bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.curve.de_select_last()
bpy.ops.curve.delete(type='VERT')
bpy.ops.object.mode_set(mode='OBJECT')



#CREATE RIGHT PART OF TRACK

coords = []
for i,j in enumerate(Rdata):
    x = j["WORLDPOSX"]
    y = j["WORLDPOSY"]
    z = j["WORLDPOSZ"] + offset
    coords.append([x,y,z])
    
curveData = bpy.data.curves.new('RIGHT', type='CURVE')
curveData.dimensions = '3D'
curveData.resolution_u = 2

polyline = curveData.splines.new('POLY')
polyline.points.add(len(coords))
for i, coord in enumerate(coords):
    x,y,z = coord
    polyline.points[i].co = (x*0.01, y*0.01, z*0.01, 1)

curveOB = bpy.data.objects.new('RIGHT', curveData)
bpy.context.scene.collection.objects.link(curveOB)
bpy.context.view_layer.objects.active = curveOB

bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.curve.de_select_last()
bpy.ops.curve.delete(type='VERT')
bpy.ops.object.mode_set(mode='OBJECT')


#CREATE CENTER PART OF TRACK
coords = []
for i,j in enumerate(Cdata):
    x = j["WORLDPOSX"]
    y = j["WORLDPOSY"]
    z = j["WORLDPOSZ"] + offset
    coords.append([x,y,z])
    
curveData = bpy.data.curves.new('CENTER', type='CURVE')
curveData.dimensions = '3D'
curveData.resolution_u = 2

polyline = curveData.splines.new('POLY')
polyline.points.add(len(coords))
count = 0
for i, coord in enumerate(coords):
    count = count + 1
    x,y,z = coord
    polyline.points[i].co = (x*0.01, y*0.01, z*0.01, 1)
    if(count==1):
        bpy.data.objects["MIDPOINT"].location = (x*0.01,y*0.01,z*0.01)
        
    
curveOB = bpy.data.objects.new('CENTER', curveData)
bpy.context.scene.collection.objects.link(curveOB)
bpy.context.view_layer.objects.active = curveOB

bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.curve.de_select_last()
bpy.ops.curve.delete(type='VERT')
bpy.ops.object.mode_set(mode='OBJECT')


#CREATE RIGHT(CORNERS ONLY) PART OF TRACK
coords = []
for i,j in enumerate(Rdata):
    x = j["WORLDPOSX"]
    y = j["WORLDPOSY"]
    z = j["WORLDPOSZ"] + offset
    coords.append([x,y,z])
    
curveData = bpy.data.curves.new('RIGHTCURB', type='CURVE')
curveData.dimensions = '3D'
curveData.resolution_u = 2

polyline = curveData.splines.new('POLY')
polyline.points.add(len(coords))
for i, coord in enumerate(coords):
    x,y,z = coord
    polyline.points[i].co = (x*0.01, y*0.01, z*0.01, 1)

curveOB = bpy.data.objects.new('RIGHTCURB', curveData)
bpy.context.scene.collection.objects.link(curveOB)
bpy.context.view_layer.objects.active = curveOB

bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.curve.de_select_last()
bpy.ops.curve.delete(type='VERT')
bpy.ops.object.mode_set(mode='OBJECT')


#CONVERT CENTRE TO MESH FOR ROAD
ob = bpy.context.scene.objects['CENTER']      
bpy.ops.object.select_all(action='DESELECT') 
bpy.context.view_layer.objects.active = ob   
ob.select_set(True)
bpy.ops.object.convert(target = 'MESH')
skin_mod = ob.modifiers.new(name='Skin', type='SKIN')
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.transform.skin_resize(value=(1/4, 1/50,0), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, True, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)

bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.modifier_apply(modifier="Skin")     #APPLY SKIN MODIFIER
bpy.ops.object.select_all(action='DESELECT')


#CONVERT RIGHT TO MESH FOR WALL
ob = bpy.context.scene.objects['RIGHT']      
bpy.ops.object.select_all(action='DESELECT') 
bpy.context.view_layer.objects.active = ob   
ob.select_set(True)
bpy.ops.object.convert(target = 'MESH')
skin_mod = ob.modifiers.new(name='Skin', type='SKIN')
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.transform.skin_resize(value=(1/40, 1/20,0), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, True, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.modifier_apply(modifier="Skin")
bpy.ops.transform.translate(value=(0, 0, 0.04))

#ADD CURBS TO RIGHT(ONLY ON CORNERS)
ob = bpy.context.scene.objects['RIGHTCURB']      
bpy.ops.object.select_all(action='DESELECT') 
bpy.context.view_layer.objects.active = ob   
ob.select_set(True)
bpy.ops.object.convert(target = 'MESH')
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.dissolve_limited(angle_limit=0.0872665)      #ISOLATE ONLY CORNER POINTS BY USING LIMITED DISSOLVE
bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.select_all(action='DESELECT') 
ob = bpy.context.scene.objects['CURB']      
bpy.ops.object.select_all(action='DESELECT') 
bpy.context.view_layer.objects.active = ob   
ob.select_set(True)
ob = bpy.context.scene.objects['RIGHTCURB']
bpy.context.view_layer.objects.active = ob   
ob.select_set(True)
bpy.ops.object.parent_set(type='OBJECT', keep_transform=False)
bpy.context.object.instance_type = 'VERTS'                #PARENT TYRE/CURB TO RIGHTCURB OBJECT AND APPLY VERTEX INSTANCES
bpy.ops.object.select_all(action='DESELECT') 
ob = bpy.context.scene.objects['LEFT']      
bpy.ops.object.select_all(action='DESELECT') 
bpy.context.view_layer.objects.active = ob   
ob.select_set(True)
bpy.ops.transform.translate(value=(0, 0, 0.07))
ob = bpy.context.scene.objects['RIGHTCURB']      
bpy.ops.object.select_all(action='DESELECT')        
bpy.context.view_layer.objects.active = ob   
ob.select_set(True)
bpy.ops.transform.translate(value=(0, 0, 0.02))


#ADD TYRES TO LEFT(ONLY ON CORNERS)
ob = bpy.context.scene.objects['LEFT']      
bpy.ops.object.select_all(action='DESELECT') 
bpy.context.view_layer.objects.active = ob   
ob.select_set(True)
bpy.ops.object.convert(target = 'MESH')
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.dissolve_limited(angle_limit=0.0872665)
bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.select_all(action='DESELECT') 
ob = bpy.context.scene.objects['TYRE']      
bpy.ops.object.select_all(action='DESELECT') 
bpy.context.view_layer.objects.active = ob   
ob.select_set(True)
ob = bpy.context.scene.objects['LEFT']
bpy.context.view_layer.objects.active = ob   
ob.select_set(True)
bpy.ops.object.parent_set(type='OBJECT', keep_transform=False)
bpy.context.object.instance_type = 'VERTS'
bpy.ops.object.select_all(action='DESELECT') 
ob = bpy.context.scene.objects['LEFT']      
bpy.ops.object.select_all(action='DESELECT') 
bpy.context.view_layer.objects.active = ob   
ob.select_set(True)
bpy.ops.transform.translate(value=(0, 0, 0.02))



#ADD GRANDSTAND AREA
ob = bpy.context.scene.objects['CENTER']      
bpy.ops.object.select_all(action='DESELECT') 

bpy.context.view_layer.objects.active = ob   
ob.select_set(True)
ob.data.polygons[1].select = True
bpy.ops.object.mode_set(mode='EDIT')

bpy.ops.transform.create_orientation(name="face", overwrite=True)
bpy.context.scene.transform_orientation_slots[0].type = 'face'       #CREATE CUSTOM ORIENTATION TO ALIGN WITH FINISH LINE SPOT CORRECTLY
bpy.ops.mesh.select_all(action='DESELECT')
bpy.ops.object.editmode_toggle()
ob = bpy.context.scene.objects['MIDPOINT']      
bpy.ops.object.select_all(action='DESELECT')        
bpy.context.view_layer.objects.active = ob   
ob.select_set(True)

bpy.ops.transform.transform(mode='ALIGN', value=(0, 0, 0, 0), orient_type='face', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
bpy.ops.transform.rotate(value=1.60919, orient_axis='X', orient_type='face', constraint_axis=(True, False, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
bpy.ops.transform.rotate(value=1.5708, orient_axis='Z', orient_type='face', constraint_axis=(False, False, True), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=0.179859, use_proportional_connected=False, use_proportional_projected=False)

bpy.ops.transform.translate(value=(-0, -0, -0.00916297), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=0.179859, use_proportional_connected=False, use_proportional_projected=False)
bpy.ops.transform.rotate(value=3.14159, orient_axis='Z', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=0.179859, use_proportional_connected=False, use_proportional_projected=False)
bpy.ops.transform.rotate(value=0.0314159, orient_axis='Y', orient_type='face', constraint_axis=(False, True, False), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=0.179859, use_proportional_connected=False, use_proportional_projected=False)


bpy.context.scene.transform_orientation_slots[0].type = 'GLOBAL'



#ADD SECTOR INFO(COLOR ARROWS)
coords = []
for i,j in enumerate(Cdata):
    x = j["WORLDPOSX"]
    y = j["WORLDPOSY"]
    z = j["WORLDPOSZ"] + offset
    sector = j["SECTOR"]
    yaw = j["YAW"]           #USE YAW ANGLE TO PLOT DIRECTIONAL ARROWS
    coords.append([x,y,z,sector,yaw])
    
count = 0
for i, coord in enumerate(coords):
    count = count + 1
    x,y,z,sector,yaw = coord
    if((count%10)==0):
        if(sector==0):       #FOR SECTOR 1 ARROWS
            ob = bpy.context.scene.objects['SECTOR1']      
            bpy.ops.object.select_all(action='DESELECT') 
            bpy.context.view_layer.objects.active = ob   
            ob.select_set(True)
    
            bpy.ops.object.duplicate(linked=0,mode='TRANSLATION')
            new_obj = bpy.context.active_object
            new_obj.location = (x*0.01,y*0.01,z*0.01)
            bpy.context.object.rotation_mode = 'XYZ'
            new_obj.rotation_euler[0] = 0
            new_obj.rotation_euler[1] = 0
            new_obj.rotation_euler[2] = yaw
            bpy.ops.transform.translate(value=(0, 0, 0.02))
            
        if(sector==1):       #FOR SECTOR 2 ARROWS
            ob = bpy.context.scene.objects['SECTOR2']      
            bpy.ops.object.select_all(action='DESELECT') 
            bpy.context.view_layer.objects.active = ob   
            ob.select_set(True)
    
            bpy.ops.object.duplicate(linked=0,mode='TRANSLATION')
            new_obj = bpy.context.active_object
            new_obj.location = (x*0.01,y*0.01,z*0.01)
            bpy.context.object.rotation_mode = 'XYZ'
            new_obj.rotation_euler[0] = 0
            new_obj.rotation_euler[1] = 0
            new_obj.rotation_euler[2] = yaw
            bpy.ops.transform.translate(value=(0, 0, 0.02))
            
        if(sector==2):       #FOR SECTOR 3 ARROWS
            ob = bpy.context.scene.objects['SECTOR3']      
            bpy.ops.object.select_all(action='DESELECT') 
            bpy.context.view_layer.objects.active = ob   
            ob.select_set(True)
    
            bpy.ops.object.duplicate(linked=0,mode='TRANSLATION')
            new_obj = bpy.context.active_object
            new_obj.location = (x*0.01,y*0.01,z*0.01)
            bpy.context.object.rotation_mode = 'XYZ'
            new_obj.rotation_euler[0] = 0
            new_obj.rotation_euler[1] = 0
            new_obj.rotation_euler[2] = yaw
            bpy.ops.transform.translate(value=(0, 0, 0.02))
            
            
         
#ADD MATERIAL TO ROAD            
ob = bpy.context.scene.objects['CENTER']      
bpy.ops.object.select_all(action='DESELECT') 
bpy.context.view_layer.objects.active = ob   
ob.select_set(True)
bpy.context.object.active_material = bpy.data.materials['PitLane']

#ADD MATERIAL TO SIDE WALL
ob = bpy.context.scene.objects['RIGHT']      
bpy.ops.object.select_all(action='DESELECT') 
bpy.context.view_layer.objects.active = ob   
ob.select_set(True)
bpy.context.object.active_material = bpy.data.materials['BoardBackground']

bpy.ops.object.select_all(action='DESELECT')


#END OF CODE