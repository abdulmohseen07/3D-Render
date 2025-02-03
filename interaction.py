from collections import defaultdict
from OpenGL.GLUT import *

# Trackball class to handle the matrix
class Trackball:
    def __init__(self):
        self.matrix = self.create_identity_matrix()  # Store identity matrix by default

    def create_identity_matrix(self):
        # Return a 4x4 identity matrix (a list of lists)
        return [
            [1.0, 0.0, 0.0, 0.0],
            [0.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 1.0]
        ]

# Interaction class for handling user input
class Interaction(object):
    def __init__(self):
        self.pressed = None
        self.translation = [0, 0, 0]
        self.mouse_loc = defaultdict(list)
        self.callbacks = {}
        self.trackball = Trackball()  # Use Trackball class to initialize trackball
        self.register()

    def register(self):
        glutMouseFunc(self.handle_mouse_button)
        glutMotionFunc(self.handle_mouse_move)
        glutKeyboardFunc(self.handle_keystroke)
        glutSpecialFunc(self.handle_keystroke)
        
    def translate(self, x, y, z):
        self.translation[0] += x
        self.translation[1] += y
        self.translation[2] += z
        
    def handle_mouse_button(self, button, mode, x, y):
        xSize, ySize = glutGet(GLUT_WINDOW_WIDTH), glutGet(GLUT_WINDOW_HEIGHT)
        y = ySize - y
        self.mouse_loc = (x, y)
        
        if mode == GLUT_DOWN:
            self.pressed = button
        if button == GLUT_RIGHT_BUTTON:
            pass
        elif button == GLUT_LEFT_BUTTON:
            self.trigger('pick', x, y)
        elif button == 3:
            self.translate(0, 0, 1.0)
        elif button == 4:
            self.translate(0, 0, -1.0)
        else:
            self.pressed = None
        glutPostRedisplay()
        
    def handle_mouse_move(self, x, screen_y):
        xSize, ySize = glutGet(GLUT_WINDOW_WIDTH), glutGet(GLUT_WINDOW_HEIGHT)
        y = ySize - screen_y
        if self.pressed is not None:
            dx = x - self.mouse_loc[0]
            dy = y - self.mouse_loc[1]
            if self.pressed == GLUT_RIGHT_BUTTON:
                self.trigger('rotate', dx, dy)
            elif self.pressed == GLUT_LEFT_BUTTON:
                self.trigger('move', x, y)
            elif self.pressed == GLUT_MIDDLE_BUTTON:
                self.translate(dx / 60.0, dy / 60.0, 0)
            glutPostRedisplay()
        self.mouse_loc = (x, y)

    def handle_keystroke(self, key, x, screen_y):
        xSize, ySize = glutGet(GLUT_WINDOW_WIDTH), glutGet(GLUT_WINDOW_HEIGHT)
        y = ySize - screen_y
        if key == b's':
            self.trigger('place', 'sphere', x, y)
        elif key == b'c':
            self.trigger('place', 'cube', x, y)
        elif key == GLUT_KEY_UP:
            self.trigger('scale', up=True)
        elif key == GLUT_KEY_DOWN:
            self.trigger('scale', up=False)
        elif key == GLUT_KEY_LEFT:
            self.trigger('rotate_color', forward=True)
        elif key == GLUT_KEY_RIGHT:
            self.trigger('rotate_color', forward=False)
        glutPostRedisplay()

    def register_callback(self, name, func):
        if name not in self.callbacks:
            self.callbacks[name] = []  # Initialize the list if it doesn't exist
        self.callbacks[name].append(func)  # Now we can safely append the function

    def trigger(self, name, *args, **kwargs):
        for func in self.callbacks[name]:
            func(*args, **kwargs)
