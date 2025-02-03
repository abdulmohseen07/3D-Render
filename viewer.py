# Viewer Class and main Rendering Logic

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
from scene import Scene
from interaction import Interaction

class Viewer(object):
    def __init__(self):
        self.init_interface()
        self.init_opengl()
        self.init_scene()
        self.init_interaction()
        
    def init_interface(self):
        glutInit()
        glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB | GLUT_DEPTH)
        glutInitWindowSize(640, 480)
        glutCreateWindow(b"3D Render")
        glutDisplayFunc(self.render)
        
    def init_opengl(self):      
        glEnable(GL_CULL_FACE)
        glCullFace(GL_BACK)
        
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)
        
        glEnable(GL_LIGHT0)
        position = np.array([0.0, 0.0, 1.0, 0.0], dtype=np.float32)
        direction = np.array([0.0, 0.0, 0.0, -1.0], dtype=np.float32)
        glLightfv(GL_LIGHT0, GL_POSITION, position)
        glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, direction)
        
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
        
        glClearColor(0.4, 0.4, 0.4, 0.0)
        glClearDepth(1.0)
        
    def init_scene(self):
        self.scene = Scene()
        self.create_sample_scene()
        
    def create_sample_scene(self):
        from node import Cube, Sphere, SnowFigure
        cube_node = Cube()
        cube_node.translate(2, 0, 2)
        cube_node.color_index = 2
        self.scene.add_node(cube_node)
        
        sphere_node = Sphere()
        sphere_node.translate(2, 0, 2)
        sphere_node.color_index = 1
        self.scene.add_node(sphere_node)
        
        hierarchical_node = SnowFigure()
        hierarchical_node.translate(-2, 0, -2)
        self.scene.add_node(hierarchical_node)
        
    def init_interaction(self):
        self.interaction = Interaction()
        self.interaction.register_callback('pick', self.pick)
        self.interaction.register_callback('move', self.move)
        self.interaction.register_callback('place', self.place)
        self.interaction.register_callback('rotate_color', self.rotate_color)
        self.interaction.register_callback('scale', self.scale)
        
    def main_loop(self):
        glutMainLoop()
        
    def render(self):
        self.init_view()
        glEnable(GL_LIGHTING)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        loc = self.interaction.translation
        glTranslated(loc[0], loc[1], loc[2])
        glMultMatrixf(self.interaction.trackball.matrix)
        
        currentModeView = np.array(glGetFloatv(GL_MODELVIEW_MATRIX))
        self.modelView = np.transpose(currentModeView)
        self.inverseModelView = np.linalg.inv(self.modelView)
        
        # Draw grid lines before rendering the scene
        self.draw_grid()

        # Render the scene
        self.scene.render()
        
        glDisable(GL_LIGHTING)
        glCallList(1)
        glPopMatrix()
        
        glFlush()

    def draw_grid(self, grid_size=10, step=1.0):
        """
        Draws a 2D grid on the X-Y plane.
        
        :param grid_size: Size of the grid.
        :param step: Spacing between grid lines.
        """
        glColor3f(0.5, 0.5, 0.5)  # Light grey color for grid lines
        glBegin(GL_LINES)
        
        # Draw vertical lines
        for x in range(-grid_size, grid_size + 1):
            glVertex2f(x * step, -grid_size * step)
            glVertex2f(x * step, grid_size * step)
        
        # Draw horizontal lines
        for y in range(-grid_size, grid_size + 1):
            glVertex2f(-grid_size * step, y * step)
            glVertex2f(grid_size * step, y * step)
        
        glEnd()

    def init_view(self):
        xSize, ySize = glutGet(GLUT_WINDOW_WIDTH), glutGet(GLUT_WINDOW_HEIGHT)
        aspect_ratio = float(xSize)/ float(ySize)
        
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glViewport(0, 0, xSize, ySize)
        gluPerspective(70, aspect_ratio, 0.1, 1000.0)
        glTranslated(0, 0, -15)
        
    def pick(self, x, y):
        start, direction = self.get_ray(x, y)
        self.scene.pick(start, direction, self.modelView)
        
    def move(self, x, y):
        start, direction = self.get_ray(x, y)
        self.scene.move_selected(start, direction, self.inverseModelView)
    
    def rotate_color(self, forward):
        self.scene.rotate_selected_color(forward)
        
    def scale(self, up):
        self.scene.scale_selected(up)
        
    def place(self, shape, x, y):
        start, direction = self.get_ray(x, y)
        self.scene.place(shape, start, direction, self.inverseModelView)
        
    def get_ray(self, x, y):
        self.init_view()
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        start = np.array(gluUnProject(x, y, 0.001))
        end = np.array(gluUnProject(x, y, 0.999))
        direction = end - start
        direction = direction / np.linalg.norm(direction)
        return start, direction
