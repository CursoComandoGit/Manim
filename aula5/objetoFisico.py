from manim import *
import numpy as np

class ObjetoFisico(Group):
    def __init__(
        self, 
        mobject : Mobject, #Qualquer objeto pode ir aqui e pular :D
        velocity = np.array([0.0, 0.1, 0.0]),  #default speed, gravity, damping and bounds to bounce
        gravity = np.array([0.0, -9.8, 0.0]),
        damping=0.9,
        xBounds=[-config.frame_width / 2, config.frame_width / 2],
        yBounds=[-config.frame_height / 2, config.frame_height / 2],
        **kwargs
    ):
        super().__init__(**kwargs)
        
        self.mobject = mobject
        self.add(mobject)
        #Saving them attributes
        self.velocity = velocity.astype(float) #numpy stuff
        self.gravity = gravity.astype(float)
        self.damping = damping
        self.active = True
        self.xBounds = xBounds 
        self.yBounds = yBounds
        
        self.add_updater(self.physics_updater)
    
    #pode ser removido ou adicionado (isso interrompe ou inicia bounce)
    def physics_updater(self, mobject, dt):
        #Cancela update se não estiver usando (mantem posição do objeto)
        if not 0 < dt < 0.1 or not self.active:
            return
            
        self.velocity = self.velocity + self.gravity * dt 
        self.shift(self.velocity * dt)
        
        boxHalfWidth = self.width / 2
        boxHalfHeight = self.height / 2
        
        #Detectando bounds e aplicando alterações necessarias
        if self.get_right()[0] >= self.xBounds[1]:
            self.set_x(self.xBounds[1] - boxHalfWidth)
            self.velocity[0] = -self.velocity[0] * self.damping
            
        if self.get_left()[0] <= self.xBounds[0]:
            self.set_x(self.xBounds[0] + boxHalfWidth)
            self.velocity[0] = -self.velocity[0] * self.damping
            
        if self.get_top()[1] >= self.yBounds[1]:
            self.set_y(self.yBounds[1] - boxHalfHeight)
            self.velocity[1] = -self.velocity[1] * self.damping
            
        if self.get_bottom()[1] <= self.yBounds[0]:
            self.set_y(self.yBounds[0] + boxHalfHeight)
            self.velocity[1] = -self.velocity[1] * self.damping