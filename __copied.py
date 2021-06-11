import bpy
import math
import mathutils
from mathutils import Euler, Matrix
import pprint

import sys
import os
sys.path.append('C:\\ws3_ox\\Blender_small_scripts')

import tower
import numpy as np
import pydevd
from random import randrange

# =====================================================
# Magic is there

# Example of use 

# co = get_co(obj)
# co_help_me = np.copy(co)
# co[:, 2] += co[:, 2] * co[:, 1] * 0.005
# set_co(obj, co)

# =====================================================


def set_global(ob):
    count = len(ob.data.vertices)
    co = np.empty(count * 3, dtype=np.float32)
    ob.data.vertices.foreach_get("co", co)
    co.shape = (count, 3)
    
    matrix_world = ob.matrix_world
    co[:, 0] += matrix_world[0][3]
    co[:, 1] += matrix_world[1][3]
    co[:, 2] += matrix_world[2][3]
     
    ob.matrix_world[0][3] = 0.0
    ob.matrix_world[1][3] = 0.0
    ob.matrix_world[2][3] = 0.0 
    
    ob.data.vertices.foreach_set("co", co.ravel())
    ob.data.update()
    bpy.context.view_layer.update()
    

def get_co(ob):
    count = len(ob.data.vertices)
    co = np.empty(count * 3, dtype=np.float32)
    ob.data.vertices.foreach_get("co", co)
    co.shape = (count, 3)
    matrix_world = ob.matrix_world
#     co[:, 0] += matrix_world[0][3]
#     co[:, 1] += matrix_world[1][3]
#     co[:, 2] += matrix_world[2][3]
# 
#     loc = ob.location
#     co[:, 0] += loc[0]
#     co[:, 1] += loc[1]
#     co[:, 2] += loc[2]    
    return co


def set_co(ob, co):
#     mid = np.mean(co, axis=0)
#     
#     ob.location = mathutils.Vector((mid[0], mid[1], mid[2]))
#     co[:, 0] -= mid[0]
#     co[:, 1] -= mid[1]
#     co[:, 2] -= mid[2]
    
    ob.data.vertices.foreach_set("co", co.ravel())
    ob.data.update()
    bpy.context.view_layer.update()
    
# =====================================================
# End of magic
# =====================================================


def open_main_file():
    file_name = 'C:\\ws3_ox\\Blender_Marmalade_Shapes\\marmelad.blend'
    bpy.ops.wm.open_mainfile(filepath=file_name)


def primitive_cube():
    bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(3, 3, 3))


def primitive_sphere():
    bpy.ops.mesh.primitive_uv_sphere_add(enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(2, 2, 2))


def primitive_cylinder():
    bpy.ops.mesh.primitive_cylinder_add(radius=1, depth=2, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(2, 2, 2))


def primitive_cone():
    bpy.ops.mesh.primitive_cone_add(radius1=1, radius2=0, depth=2, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(2, 2, 2))


def primitive_torus():          
    bpy.ops.mesh.primitive_torus_add(align='WORLD', location=(0, 0, 0), rotation=(0, 0, 0), major_radius=1.5, minor_radius=0.5, abso_major_rad=1.25, abso_minor_rad=0.75)


def create_one_central_object(p_key):
    primitive = []
    primitive.append(primitive_cube)
    primitive.append(primitive_sphere)
    primitive.append(primitive_cylinder)
    # primitive.append(primitive_cone)
    primitive.append(primitive_torus)
    primitive_length = len(primitive)
    if p_key < 0:
        primitive_key = randrange(primitive_length)
    else:
        primitive_key = p_key
    
    print(primitive_length, primitive_key)
    mesh_function = primitive[primitive_key ]
    mesh_function()
    new_object = bpy.context.view_layer.objects.active
    return new_object, primitive_key


def morph_the_objects(object_pairs, b=6.4, l=20):
    for pair in object_pairs:
        left = pair['Left']
        right = pair['Right']
        direction = right.name[0]
        if direction == 'L':
            bb = b * (-1.0)
        else:
            bb = b 
        
        co_left = get_co(left)
        
        length_data = np.zeros_like(co_left)
        
        co_zero = np.zeros_like(co_left)
        
        # Distance from camera to dot = L
        length_data[:, 0] = np.sqrt(co_left[:, 0] * co_left[:, 0] + co_left[:, 1] * co_left[:, 1] + co_left[:, 2] * co_left[:, 2])
        
        # Xb = X0 + BB * ( y - l ) / y
        co_zero[:, 0] = co_left[:, 0] * l / co_left[:, 1] + bb * (co_left[:, 1] - l) / co_left[:, 1]
        co_left = get_co(left)
        
        # Y0 = l
        co_zero[:, 1] = l
        # Z0 = z * l / y
        co_zero[:, 2] = co_left[:, 2] * l / co_left[:, 1]
        
        co_left = get_co(left)
        
        # ksi - length from camera to pixel on screen
        length_data[:, 1] = np.sqrt(co_zero[:, 0] * co_zero[:, 0] + co_zero[:, 1] * co_zero[:, 1] + co_zero[:, 2] * co_zero[:, 2])
        
        # End coordinate is simple a coordinate of point co_zero * L / ksi
        co_right = np.copy(co_zero)
        co_right[:, 0] = co_zero[:, 0] * length_data[:, 0] / length_data[:, 1]
        co_right[:, 1] = co_zero[:, 1] * length_data[:, 0] / length_data[:, 1]
        co_right[:, 2] = co_zero[:, 2] * length_data[:, 0] / length_data[:, 1]
        set_co(right, co_right)
        
        co_left = get_co(left)
        co_right = get_co(right)

        
def get_transp_materials():
    materials = []
    for m_c in range(4):
        material_name = 'Transp_' + str(m_c + 1)
        # Get material
        mat = bpy.data.materials.get(material_name)
        if mat is None:
            # create material
            mat = bpy.data.materials(material_name)   
            materials.append(mat)
        materials.append(mat)      
    return materials    

         
def set_transp_material_to_object(mat_key, materials, obj):         
    if obj.data.materials:
        # assign to 1st material slot
        obj.data.materials[0] = materials[mat_key]
    else:
        # no slots
        obj.data.materials.append(materials[mat_key]) 
                
                         
def create_central_objects(y_start=10, y_end=30, y_count=3, x_shift=6.4, x_count=7, l=20, z_count=7):
    object_pairs = []   
    central_objects = [] 
    
    collection_name = 'Objects'
    new_collection = bpy.data.collections.new(collection_name)
    bpy.context.scene.collection.children.link(new_collection)
    
    materials = get_transp_materials()
    
    for k in range(y_count):
        for i in range(z_count):
            ki = k * z_count + i
            
            new_object, prim_key = create_one_central_object(-1)
            new_collection.objects.link(new_object)
            new_object.name = 'Object_C' + str(i) + '_' + str(k)
            central_objects.append(new_object)
            
            mat_key = (k * 5 + i) % 4
            
            set_transp_material_to_object(mat_key, materials, new_object)
                
#             nodes = materials[mat_key].node_tree.nodes
#             for node in nodes:
#                 print(node.name)
#                 
#             node_shader = nodes['Mix Shader']
#             node_shader.inputs[0].default_value = 0.7
#             print(node_shader.name)
            
            bpy.context.view_layer.update()
            co = get_co(new_object)
                
            loc = new_object.location
            new_object.location = loc + mathutils.Vector((0, l + y_start + k / y_count * (y_end - y_start), 4 * (i - 3))) 
            
            bpy.context.view_layer.update()            
            set_global(new_object)
            
            bpy.context.view_layer.update()
            co = get_co(new_object)
            
            new_object.data.materials[0].blend_method = 'BLEND' 
            
            pair = {}
            pair['Left'] = new_object 
            # LastLeft = new_object.copy()
            LastLeft, prim_key = create_one_central_object(prim_key)
            set_transp_material_to_object(mat_key, materials, LastLeft)
            
            LastLeft.name = 'LObject_' + str(i) + 'L0' + '_' + str(k)
            pair['Right'] = LastLeft
            object_pairs.append(pair)
            set_global(LastLeft)
            new_collection.objects.link(LastLeft)
            
            # Right Pair
            pair = {}
            pair['Left'] = new_object
            LastRight, prim_key = create_one_central_object(prim_key)  # = new_object.copy()
            set_transp_material_to_object(mat_key, materials, LastRight)
            
            LastRight.name = 'RObject_' + str(i) + 'R0' + '_' + str(k)
            pair['Right'] = LastRight
            object_pairs.append(pair)
            set_global(LastRight)
            new_collection.objects.link(LastRight)
            
            for j in range(int((x_count - 3) / 2)):
                # Left Pair
                pair = {}
                pair['Left'] = LastLeft
                LastLeft, prim_key = create_one_central_object(prim_key)
                set_transp_material_to_object(mat_key, materials, LastLeft)
                LastLeft.name = 'LObject_' + str(i) + 'L' + str(j + 1) + '_' + str(k)
                pair['Right'] = LastLeft
                object_pairs.append(pair)
                new_collection.objects.link(LastLeft)
                
                # Right Pair
                pair = {}
                pair['Left'] = LastRight
                LastRight, prim_key = create_one_central_object(prim_key)
                set_transp_material_to_object(mat_key, materials, LastRight)
                LastRight.name = 'RObject_' + str(i) + 'R' + str(j + 1) + '_' + str(k)
                pair['Right'] = LastRight
                object_pairs.append(pair)
                new_collection.objects.link(LastRight)
            
    return object_pairs, central_objects


# =====================================================
def rotate_and_move_cetral_objects(central_objects, counter):
    
    qr_step = np.pi / 15
    
    qr = np.cos(qr_step / 2)
    qi = 1.0
    qj = 0.0
    qk = 1.0
    
    shift_x = 0.0
    shift_y = 0.0
    shift_z = 0.0
    
    length_to_be = 1 - np.sqrt(qr * qr)
    
    length = np.sqrt(qi * qi + qj * qj + qk * qk)
    if length == 0.0 :
        qi = 1.0
        length = 1.0
    
    qi = qi * length_to_be / length
    qj = qj * length_to_be / length
    qk = qk * length_to_be / length
    
    a00 = 1 - 2.0 * (qj * qj + qk * qk)
    a01 = 2.0 * (qi * qj - qk * qr)
    a02 = 2.0 * (qi * qk + qj * qr)
    
    a10 = 2.0 * (qi * qj + qk * qr)
    a11 = 1 - 2.0 * (qi * qi + qk * qk)
    a12 = 2.0 * (qj * qk - qi * qr)
    
    a20 = 2.0 * (qi * qk - qj * qr)
    a21 = 2.0 * (qj * qk + qi * qr) 
    a22 = 1 - 2.0 * (qi * qi + qj * qj)
    
    for central_obj in central_objects:
        co = get_co(central_obj)
        
        mid = np.mean(co, axis=0)

        co[:, 0] -= mid[0]
        co[:, 1] -= mid[1]
        co[:, 2] -= mid[2]
         
        co_copy = np.copy(co)
         
        co[:, 0] = a00 * co_copy[:, 0] + a01 * co_copy[:, 1] + a02 * co_copy[:, 2]
        co[:, 1] = a10 * co_copy[:, 0] + a11 * co_copy[:, 1] + a12 * co_copy[:, 2]
        co[:, 2] = a20 * co_copy[:, 0] + a21 * co_copy[:, 1] + a22 * co_copy[:, 2]
        
        co[:, 0] += mid[0]
        co[:, 1] += mid[1]
        co[:, 2] += mid[2]
                 
        set_co(central_obj, co)


def run_main():
    apply_modifiers = True
    settings = 'RENDER'
    
    open_main_file()
    
#     obj = tower.create_tower()
#     scene = bpy.context.scene
#     mesh = obj.to_mesh()
    
    #pydevd.settrace()
#     
#     for collection in bpy.data.collections:  
#         print(collection.name)  
   
    object_pairs, central_objects = create_central_objects(y_start=20, y_end=30, y_count=2, x_shift=6.4, x_count=15, z_count=7)

    for jj in range(1):
        
        rotate_and_move_cetral_objects(central_objects=central_objects, counter=jj)
        morph_the_objects(object_pairs, b=6.4)

        step = jj  
        output_dir = 'C:\\STERNEV\\@@@Move\\$$ Dzen\\BlenderRenders\\'
        output_file_pattern_string = 'render%d.jpg'          
        bpy.context.scene.render.filepath = os.path.join(output_dir, (output_file_pattern_string % step))
        bpy.ops.render.render(write_still=True)
    

if __name__ == "__main__":
    run_main()
