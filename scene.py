# Scene Class and Node Management
import numpy as np
from node import Node

class Scene(object):
    PLACE_DEPTH = 15.0
    
    def __init__(self):
        self.node_list = []
        self.selected_node = None
        
    def add_node(self, node):
        self.node_list.append(node)
        
    def render(self):
        for node in self.node_list:
            node.render()
            
    def pick(self, start, direction, mat):
        if self.selected_node is not None:
            self.selected_node.select(False)
            self.selected_node = None
    
        mindist = float('inf')
        closest_node = None
        for node in self.node_list:
            hit, distance = node.pick(start, direction, mat)
            if hit and distance < mindist:
                mindist, closest_node = distance, node
                
        if closest_node is not None:
            closest_node.select()
            closest_node.depth = mindist
            closest_node.selected_loc = start + direction * mindist
            
    def rotate_selected_color(self, forward):
        # Rotate the selected object by color or orientation
        if self.selected_node is not None:
            if forward:
                self.selected_node.rotate_color(True)  # Rotate color forward
            else:
                self.selected_node.rotate_color(False)  # Rotate color backward
        
    def scale_selected(self, up):
        # Scale the selected object
        if self.selected_node is not None:
            scale_factor = 1.1 if up else 0.9
            self.selected_node.scale(scale_factor)
        
    def move_selected(self, start, direction, inv_modelView):
        if self.selected_node is None: 
            return
        node = self.selected_node
        depth = node.depth
        oldloc = node.selected_loc
        newloc = start + direction * depth
        translation = newloc - oldloc
        pre_tran = np.array([translation[0], translation[1], translation[2], 0])
        translation = inv_modelView.dot(pre_tran)
        node.translate(translation[0], translation[1], translation[2])
        node.selected_loc = newloc
        
    def place(self, shape, start, direction, inv_modelView):
        from node import Sphere, Cube, SnowFigure
        new_node = None
        if shape == 'sphere': 
            new_node = Sphere()
        elif shape == 'cube': 
            new_node = Cube()
        elif shape == 'figure': 
            new_node = SnowFigure()
        
        self.add_node(new_node)
        translation = start + direction * self.PLACE_DEPTH
        pre_tran = np.array([translation[0], translation[1], translation[2], 1])
        translation = inv_modelView.dot(pre_tran)
        new_node.translate(translation[0], translation[1], translation[2])
