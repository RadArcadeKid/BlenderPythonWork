import bpy
import random

def create_cube(x, y, height_variance, cube_size, collection):
    bpy.ops.mesh.primitive_cube_add(size=cube_size)
    cube_object = bpy.context.active_object
    cube_object.location = (x, y, height_variance / 2.0)
    cube_object.scale.z = height_variance

    # Add cube to collection
    collection.objects.link(cube_object)

def create_ground_plane(grid_size, cube_size, collection):
    spacing = 2.0  # Spacing between cubes
    plane_size = (grid_size - 1) * spacing + cube_size

    bpy.ops.mesh.primitive_plane_add(size=plane_size)
    plane_object = bpy.context.active_object
    plane_object.location = ((grid_size - 1) * spacing / 2.0, (grid_size - 1) * spacing / 2.0, 0.0)

    # Add ground plane to collection
    collection.objects.link(plane_object)

def create_city_collection():
    # Create a new collection named "city"
    city_collection = bpy.data.collections.new("city")

    # Link the collection to the scene
    bpy.context.scene.collection.children.link(city_collection)

    return city_collection

def create_glass_material():
    material = bpy.data.materials.new(name="glasscubemat")
    material.use_nodes = True

    # Get the material's node tree
    material_node_tree = material.node_tree

    # Clear the existing nodes
    material_node_tree.nodes.clear()

    # Create a Glass BSDF node
    glass_node = material_node_tree.nodes.new('ShaderNodeBsdfGlass')

    # Create a Material Output node
    material_output_node = material_node_tree.nodes.new('ShaderNodeOutputMaterial')

    # Link the nodes
    material_node_tree.links.new(glass_node.outputs['BSDF'], material_output_node.inputs['Surface'])

    return material

def create_point_light(location, color):
    bpy.ops.object.light_add(type='POINT', location=location)
    light_object = bpy.context.active_object
    light_object.data.energy = 10.0  # Adjust light intensity
    light_object.data.color = color

    return light_object

def main():
    # Clear existing objects
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete()

    # Create city collection
    city_collection = create_city_collection()

    # Create cubes in a grid
    grid_size = 20
    cube_size = 1.0
    ramdom_glass_param = 0.2 #20%
    random_light_param = 0.5 #50%

    create_ground_plane(grid_size, cube_size, city_collection)

    for i in range(grid_size):
        for j in range(grid_size):
            # Calculate cube position
            x = i * 2.0
            y = j * 2.0

            # Calculate random height variance
            height_variance = random.uniform(1.0, 4.0) * cube_size

            # Create cube
            create_cube(x, y, height_variance, cube_size, city_collection)

    # Create a single glass material
    glass_material = create_glass_material()

    # Assign glass material to cubes randomly
    city_collection = bpy.data.collections["city"]
    cube_objects = [obj for obj in city_collection.objects if obj.type == 'MESH']
    for cube_object in cube_objects:
        
        if random.random() < 0.2:
            #Append the glass material to the cube
            cube_object.data.materials.append(glass_material)
            
            
            # Get the cube's location
            location = cube_object.location
            # Generate a random color
            color = (
                0.0, 1.0, 0.698
            ) if random.random() < 0.5 else (
                1.0, 0.0, 0.8
            )
            # Create a point light at the cube's location with the random color
            create_point_light(location, color)

# Call the main function
main()