import numpy as np

class Trackball:
    def __init__(self, theta=-25, distance=15):
        self.theta = theta
        self.distance = distance
        self.matrix = np.identity(4)
        self.last_pos = None

    def drag_to(self, x, y, dx, dy):
        """
        Update the rotation matrix based on mouse drag.
        """
        if self.last_pos is None:
            self.last_pos = (x, y)
            return

        # Calculate rotation angles
        delta_x = dx * 0.01
        delta_y = dy * 0.01

        # Create rotation matrices
        rot_x = np.identity(4)
        rot_x[1:3, 1:3] = [
            [np.cos(delta_x), -np.sin(delta_x)],
            [np.sin(delta_x), np.cos(delta_x)]
        ]

        rot_y = np.identity(4)
        rot_y[0:3:2, 0:3:2] = [
            [np.cos(delta_y), np.sin(delta_y)],
            [-np.sin(delta_y), np.cos(delta_y)]
        ]

        # Update the trackball matrix
        self.matrix = np.dot(self.matrix, np.dot(rot_x, rot_y))
        self.last_pos = (x, y)