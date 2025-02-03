
# 3D Render Engine

A 3D rendering engine built using OpenGL and Python. This project allows for the creation, manipulation, and interaction with 3D objects in a virtual space. Objects such as cubes, spheres, and hierarchical figures can be rendered, moved, scaled, rotated, and colored using mouse interactions and keyboard inputs.

## Features

- **3D Object Creation**: Includes basic 3D shapes like cubes and spheres, as well as a hierarchical snow figure.
- **Object Manipulation**: Supports moving, scaling, rotating, and color-changing of selected objects.
- **Interactive Control**: Implements mouse drag for object movement/rotation, keyboard controls for scaling and color changes.
- **Scene Management**: Multiple objects can be added to the scene, and objects can be selected for manipulation.
- **Ray Picking**: Click-to-select objects using ray picking, useful for interacting with 3D objects in the scene.
- **Modular Design**: The engine is modular, with separate components for rendering, scene management, and object interaction.

## Getting Started

### Prerequisites

- Python 3.x
- OpenGL (PyOpenGL)

### Installing

1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/yourusername/3D-Render.git
   ```

2. Install the required dependencies:
   ```bash
   pip install PyOpenGL
   ```

3. Run the main script:
   ```bash
   python main.py
   ```

### Controls

- **Mouse Drag**: Move or rotate objects in the scene based on mouse movement.
- **Up/Down Arrow**: Scale selected object.
- **Left/Right Arrow**: Rotate the selected object based on color or orientation.
- **Left Mouse Click**: Select objects in the scene.
- **R Key**: Add a new object (cube, sphere, or figure) to the scene at the clicked position.

## Folder Structure

- `main.py`: Entry point of the program, runs the application.
- `viewer.py`: Handles OpenGL rendering and the main viewer logic.
- `scene.py`: Manages the scene, including adding, rendering, and interacting with objects.
- `node.py`: Defines the 3D objects (e.g., Cube, Sphere) and their transformations.
- `utils.py`: Utility functions (e.g., scaling, translation matrices).
- `aabb.py`: Axis-aligned bounding box (AABB) implementation for collision detection.
- `color.py`: Contains color definitions for objects.

