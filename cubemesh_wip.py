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

    # Set up the 3D Viewport for better visualization
    bpy.ops.view3d.view_all()

# Call the main function
main()
