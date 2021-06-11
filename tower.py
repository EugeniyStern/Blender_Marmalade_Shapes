import bpy

import math
import mathutils

from mathutils import Euler, Matrix

from math import radians
# import pydevd

import os


# Recursivly transverse layer_collection for a particular name
def recurLayerCollection(layerColl, collName):
    found = None
    if (layerColl.name == collName):
        return layerColl
    for layer in layerColl.children:
        found = recurLayerCollection(layer, collName)
        if found:
            return found

        
def prepare_blender():
    output_dir = 'C:\\STERNEV\\@@@Move\\$$ Dzen\\BlenderRenders\\'
    # rotate_and_render(output_dir=output_dir, output_file_pattern_string="render%d.jpg", rotation_steps=32, rotation_angle=360.0, subject=new_object)
    
    file_name = 'C:\\eclipse\\blender_models\\source\\Sketchfab_280_clean.blend'
    bpy.ops.wm.open_mainfile(filepath=file_name)
    
    layer_collection = bpy.context.view_layer.layer_collection
    layerColl = recurLayerCollection(layer_collection, 'Origin')
    bpy.context.view_layer.active_layer_collection = layerColl


def tower_brick(verts, faces, r_start=0.8, r_end=1.0, n=18, z_up=0.2, alpha_start=0.0, z=0.0):
    # mesh arrays
#     verts = []  # the vertex array
#     faces = []  # the face array
    scale = 1  # the scale of the mesh
    
    # fill verts array
    
    i = len(verts)
    
    alpha = math.pi * 2 / n
    
    verts.append((r_start * scale * math.cos(alpha_start), r_start * scale * math.sin(alpha_start), z))  # vert_0
    verts.append((r_end * scale * math.cos(alpha_start), r_end * scale * math.sin(alpha_start), z))  # vert_1
    
    verts.append((r_start * scale * math.cos(alpha + alpha_start), r_start * scale * math.sin(alpha + alpha_start), z))  # vert_2
    verts.append((r_end * scale * math.cos(alpha + alpha_start), r_end * scale * math.sin(alpha + alpha_start), z))  # vert_3
    
    verts.append((r_start * scale * math.cos(alpha_start), r_start * scale * math.sin(alpha_start), z + z_up))  # vert_4
    verts.append((r_end * scale * math.cos(alpha_start), r_end * scale * math.sin(alpha_start), z + z_up))  # vert_5
    
    verts.append((r_start * scale * math.cos(alpha + alpha_start), r_start * scale * math.sin(alpha + alpha_start), z + z_up))  # vert_6
    verts.append((r_end * scale * math.cos(alpha + alpha_start), r_end * scale * math.sin(alpha + alpha_start), z + z_up))  # vert_7
    
    faces.append((i + 1, i + 0, i + 2, i + 3))  # bottom
    faces.append((i + 0, i + 1, i + 5, i + 4))  # front
    faces.append((i + 4, i + 5, i + 7, i + 6))  # top
    faces.append((i + 3, i + 2, i + 6, i + 7))  # back
    
    faces.append((i + 2, i + 0, i + 4, i + 6))  # left
    faces.append((i + 1, i + 3, i + 7, i + 5))  # right

    
def create_tower():
    verts = []
    faces = []
    
    for i in range(220):
        tower_brick(verts, faces, r_start=7.0, r_end=15.0, n=6, z_up=1.5, alpha_start=i * math.pi * 2 / 18, z=i * 1.5)

    new_mesh = bpy.data.meshes.new(name="New Object Mesh")
    new_mesh.from_pydata(verts, [], faces)
    new_mesh.update()
     
    new_object = bpy.data.objects.new('Tower', new_mesh)

    # Get material
    mat = bpy.data.materials.get("Transp_1")
    if mat is None:
        # create material
        mat = bpy.data.materials("Transp_1")
        
    

    
#     nodes = mat.node_tree.nodes
#   # clear all nodes to start clean
#     nodes.clear()
#     
#     # create emission node
#     node_emission = nodes.new(type='ShaderNodeEmission')
#     node_emission.inputs[0].default_value = (0,1,0,1)  # green RGBA
#     node_emission.inputs[1].default_value = 5.0 # strength
#     node_emission.location = 0,0
#     
#     # create output node
#     node_output = nodes.new(type='ShaderNodeOutputMaterial')   
#     node_output.location = 400,0
#     
#     links = mat.node_tree.links
#     link = links.new(node_emission.outputs[0], node_output.inputs[0])
#     
#     # get specific link
#     from_s = node_emission.outputs[0]
#     to_s = node_output.inputs[0]
#     link = next((l for l in links if l.from_socket == from_s and l.to_socket == to_s), None)
#   
    # Assign it to object
    if new_object.data.materials:
        # assign to 1st material slot
        new_object.data.materials[0] = mat
    else:
        # no slots
        new_object.data.materials.append(mat) 
        
    new_object.data.materials[0].blend_method = 'BLEND'
         
#     make collection
#     new_collection = bpy.data.collections.new('Tower')
#     bpy.context.scene.collection.children.link(new_collection)
#     # add object to scene collection
#     new_collection.objects.link(new_object)
    
    for collection in bpy.data.collections:
        if collection.name == 'Origin':
            collection.objects.link(new_object) 
            
    return new_object


# def main():
#     prepare_blender()
#     create_tower()
# 
# 
# if __name__ == "__main__":
#     main()
