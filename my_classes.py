class planet: 
    def __init__(self,name,mass,position,velocity,acceleration): 
        self.name = name 
        self.mass = mass 
        self.position = position 
        self.velocity = velocity 
        self.acceleration = acceleration 

class vector: 
    def __init__(self,x,y): 
        self.x=x
        self.y=y 
    def multiply(self,vector): 
        x = self.x * vector.x 
        y = self.y * vector.y 
        return x + y 
    def add(self,vector): 
        
    