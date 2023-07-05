import bpy
import random
import math
import numpy as np

def create_sphere(x, y, height, collection, sphere_scale=0.2):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=sphere_scale)
    sphere_object = bpy.context.active_object
    sphere_object.location = (x, y, height)
    sphere_object.scale = (sphere_scale, sphere_scale, sphere_scale)

    # Add sphere to collection
    collection.objects.link(sphere_object)

def create_ground_plane(grid_size, collection, sphere_scale):
    spacing = 2.0  # Spacing between spheres
    plane_size = (grid_size - 1) * spacing + sphere_scale

    bpy.ops.mesh.primitive_plane_add(size=plane_size)
    plane_object = bpy.context.active_object
    plane_object.location = ((grid_size - 1) * spacing / 2.0, (grid_size - 1) * spacing / 2.0, 0.0)

    # Add ground plane to collection
    collection.objects.link(plane_object)

def concave_function(x, y):
    amplitude = 2.0  # Maximum amplitude of the sine wave
    frequency = 2.0  # Frequency of the sine wave
    center = (0, 0)  # Center position of the matrix
    
    distance = np.sqrt((x - center[0])**2 + (y - center[1])**2)
    normalized_distance = distance / np.max(distance)
    heights = amplitude * np.sin(frequency * np.pi * normalized_distance)
    
    return heights

def create_city(spheres_in_grid=20):
    # Create city collection
    city_collection = bpy.data.collections.new("city")

    # Link the collection to the scene
    bpy.context.scene.collection.children.link(city_collection)

    # Create ground plane
    #create_ground_plane(spheres_in_grid, city_collection, sphere_scale)

    # Generate random height matrix
    heights = np.empty((spheres_in_grid, spheres_in_grid))
    
    #Number of rows:
    n = 20  # Number of rows
    m = 20  # Number of columns

    x = np.linspace(-1, 1, n)
    y = np.linspace(-1, 1, m)
    X, Y = np.meshgrid(x, y)
    heights = concave_function(X, Y)
    spherescale = 1; 
    
    
    for i in range(spheres_in_grid):
        for j in range(spheres_in_grid):
            # Calculate sphere position
            x = i * 2.0
            y = j * 2.0
            z = heights[i, j]

            # Create sphere
            create_sphere(x, y, z, city_collection, spherescale)

    # Set up the 3D Viewport for better visualization
    #bpy.ops.view3d.view_all()


# Call the create_city function
create_city()
