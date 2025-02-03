import numpy as np

class AABB:
    def __init__(self, min_corner, max_corner):
        self.min_corner = np.array(min_corner, dtype=np.float32)
        self.max_corner = np.array(max_corner, dtype=np.float32)

    def ray_hit(self, ray_origin, ray_direction, model_matrix):
        """
        Check if a ray intersects with the AABB.
        """
        # Transform the ray into model space
        inv_model_matrix = np.linalg.inv(model_matrix)
        ray_origin = np.dot(inv_model_matrix, np.append(ray_origin, 1.0))[:3]
        ray_direction = np.dot(inv_model_matrix, np.append(ray_direction, 0.0))[:3]

        # Calculate intersections with the AABB
        tmin = (self.min_corner - ray_origin) / ray_direction
        tmax = (self.max_corner - ray_origin) / ray_direction

        tmin, tmax = np.minimum(tmin, tmax), np.maximum(tmin, tmax)
        tmin_max = np.max(tmin)
        tmax_min = np.min(tmax)

        if tmax_min >= tmin_max and tmax_min >= 0:
            return True, tmin_max
        return False, float('inf')

    def scale(self, factor):
        """
        Scale the AABB by a factor.
        """
        center = (self.min_corner + self.max_corner) / 2
        self.min_corner = center + (self.min_corner - center) * factor
        self.max_corner = center + (self.max_corner - center) * factor