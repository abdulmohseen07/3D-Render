#Node, Primitive, Sphere, Cube, and HierarchicalNode classes
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import random
from aabb import AABB
from color import COLORS, MIN_COLOR, MAX_COLOR

def create_cube_display_list():
    """
    Create a display list for a cube.
    """
    vertices = [
        # Front face
        [-0.5, -0.5,  0.5], [0.5, -0.5,  0.5], [0.5,  0.5,  0.5], [-0.5,  0.5,  0.5],
        # Back face
        [-0.5, -0.5, -0.5], [0.5, -0.5, -0.5], [0.5,  0.5, -0.5], [-0.5,  0.5, -0.5],
        # Top face
        [-0.5,  0.5, -0.5], [0.5,  0.5, -0.5], [0.5,  0.5,  0.5], [-0.5,  0.5,  0.5],
        # Bottom face
        [-0.5, -0.5, -0.5], [0.5, -0.5, -0.5], [0.5, -0.5,  0.5], [-0.5, -0.5,  0.5],
        # Left face
        [-0.5, -0.5, -0.5], [-0.5,  0.5, -0.5], [-0.5,  0.5,  0.5], [-0.5, -0.5,  0.5],
        # Right face
        [0.5, -0.5, -0.5], [0.5,  0.5, -0.5], [0.5,  0.5,  0.5], [0.5, -0.5,  0.5]
    ]

    indices = [
        [0, 1, 2, 3],  # Front
        [4, 5, 6, 7],  # Back
        [8, 9, 10, 11],  # Top
        [12, 13, 14, 15],  # Bottom
        [16, 17, 18, 19],  # Left
        [20, 21, 22, 23]   # Right
    ]

    display_list = glGenLists(1)
    glNewList(display_list, GL_COMPILE)
    glBegin(GL_QUADS)
    for face in indices:
        for vertex in face:
            glVertex3fv(vertices[vertex])
    glEnd()
    glEndList()
    return display_list

def create_sphere_display_list(radius=0.5, slices=16, stacks=16):
    """
    Create a display list for a sphere.
    """
    display_list = glGenLists(1)
    glNewList(display_list, GL_COMPILE)
    quadric = gluNewQuadric()
    gluSphere(quadric, radius, slices, stacks)
    gluDeleteQuadric(quadric)
    glEndList()
    return display_list



class Node:
    def __init__(self):
        self.color_index = random.randint(MIN_COLOR, MAX_COLOR)
        self.aabb = AABB([0.0, 0.0, 0.0], [0.5, 0.5, 0.5])
        self.translation_matrix = np.identity(4)
        self.scaling_matrix = np.identity(4)
        self.selected = False

    def render(self):
        glPushMatrix()
        glMultMatrixf(np.transpose(self.translation_matrix))
        glMultMatrixf(self.scaling_matrix)
        cur_color = COLORS[self.color_index]
        glColor3f(cur_color[0], cur_color[1], cur_color[2])
        if self.selected:
            glMaterialfv(GL_FRONT, GL_EMISSION, [0.3, 0.3, 0.3])

        self.render_self()

        if self.selected:
            glMaterialfv(GL_FRONT, GL_EMISSION, [0.0, 0.0, 0.0])
        glPopMatrix()

    def render_self(self):
        raise NotImplementedError("The abstract node does not define render_self")

    def translate(self, x, y, z):
        self.translation_matrix = np.dot(self.translation_matrix, translation([x, y, z]))

    def scale(self, up):
        s = 1.1 if up else 0.9
        self.scaling_matrix = np.dot(self.scaling_matrix, scaling([s, s, s]))
        self.aabb.scale(s)

    def rotate_color(self, forward):
        self.color_index += 1 if forward else -1
        if self.color_index > MAX_COLOR:
            self.color_index = MIN_COLOR
        if self.color_index < MIN_COLOR:
            self.color_index = MAX_COLOR

    def pick(self, start, direction, mat):
        newmat = np.dot(np.dot(mat, self.translation_matrix), np.linalg.inv(self.scaling_matrix))
        return self.aabb.ray_hit(start, direction, newmat)

    def select(self, select=None):
        if select is not None:
            self.selected = select
        else:
            self.selected = not self.selected
class Primitive(Node):
    def __init__(self):
        super(Primitive, self).__init__()
        self.call_list = None

    def render_self(self):
        if self.call_list is None:
            self._init_display_list()
        glCallList(self.call_list)

    def _init_display_list(self):
        raise NotImplementedError("Subclasses must implement this method")

class Cube(Primitive):
    def __init__(self):
        super(Cube, self).__init__()

    def _init_display_list(self):
        self.call_list = create_cube_display_list()

class Sphere(Primitive):
    def __init__(self):
        super(Sphere, self).__init__()

    def _init_display_list(self):
        self.call_list = create_sphere_display_list()


class HierarchicalNode(Node):
    def __init__(self):
        super(HierarchicalNode, self).__init__()
        self.child_nodes = []

    def render_self(self):
        for child in self.child_nodes:
            child.render()

class SnowFigure(HierarchicalNode):
    def __init__(self):
        super(SnowFigure, self).__init__()
        self.child_nodes = [Sphere(), Sphere(), Sphere()]
        self.child_nodes[0].translate(0, -0.6, 0)
        self.child_nodes[1].translate(0, 0.1, 0)
        self.child_nodes[1].scaling_matrix = np.dot(self.scaling_matrix, scaling([0.8, 0.8, 0.8]))
        self.child_nodes[2].translate(0, 0.75, 0)
        self.child_nodes[2].scaling_matrix = np.dot(self.scaling_matrix, scaling([0.7, 0.7, 0.7]))
        for child_node in self.child_nodes:
            child_node.color_index = MIN_COLOR
        self.aabb = AABB([0.0, 0.0, 0.0], [0.5, 1.1, 0.5])

def translation(displacement):
    t = np.identity(4)
    t[0, 3] = displacement[0]
    t[1, 3] = displacement[1]
    t[2, 3] = displacement[2]
    return t

def scaling(scale):
    s = np.identity(4)
    s[0, 0] = scale[0]
    s[1, 1] = scale[1]
    s[2, 2] = scale[2]
    s[3, 3] = 1
    return s