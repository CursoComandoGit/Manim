from manim import *
import random
import numpy as np

class Crack(VGroup):
    def __init__(self, startingPoint=[0, 0, 0], endPoint=[0, 0, 0],
                 thinFactor=0.5, numberOfLines=5, color=BLACK,
                 *vmobjects, **kwargs):
        super().__init__(*vmobjects, **kwargs)

        start = np.array(startingPoint)
        end = np.array(endPoint)
        
        path_vector = end - start
        #Preciso que chegue a uma distancia
        total_dist = np.linalg.norm(path_vector)
        
        if total_dist == 0:
            return 
            
        unit_vector = path_vector/total_dist
        
        perp_vector = np.array([-unit_vector[1], unit_vector[0], 0])
        
        points = [start]
        
        #para cada linha adiciona os pontos de inicio e fim de cada linha
        for i in range(1, numberOfLines):
            alpha = i / numberOfLines
            base_point = interpolate(start, end, alpha)
            
            jitter_max = total_dist * 0.15 
            offset_magnitude = random.uniform(-jitter_max, jitter_max)
            
            offset = offset_magnitude * perp_vector
            points.append(base_point + offset)
            
        points.append(end)

        base_thickness = 12 
        #Cria as linhas e adiciona no Vgroup
        for i in range(numberOfLines):
            current_thickness = interpolate(
                base_thickness,
                base_thickness * thinFactor,
                i / max(1, numberOfLines - 1) 
            )
            line = Line(points[i], points[i+1], color=color)
            line.set_stroke(width=current_thickness)
            self.add(line)
