planet_list = [] 

class planet: 
    def __init__(self,name,mass,position,velocity,acceleration): # use vectors for position, velocity and acceleration 
        self.name = name 
        self.mass = mass 
        self.position = position 
        self.velocity = velocity 
        self.acceleration = acceleration
    def distance_from(self,planet): 
        position_vector1 = self.position 
        position_vector2 = planet.position 
        distance = position_vector1.distance_to(position_vector2)
        return distance
    def resultant_force(self, planet_list, gravitational_constant): 
        resultant_force = vector(0,0) 
        for i in planet_list: 
            if i != self:
                unit_vector = self.position.unit_vector_to(i.position)
                mass_product = self.mass * i.mass 
                distance_squared = self.distance_from(i)**2
                multiple = -gravitational_constant * mass_product / distance_squared 
                force = unit_vector.multiply_by(multiple) # using vector form of newton's law of gravitation. this is rearranged so the unit vector is in front 
                resultant_force = resultant_force.add(force)
        return resultant_force
    def find_acceleration(self,planet_list,gravitational_constant): 
        resultant_force = self.resultant_force(planet_list,gravitational_constant)
        acceleration = resultant_force.divide_by(self.mass)
        return acceleration
class vector: 
    def __init__(self,x,y): 
        self.x=x
        self.y=y 
    def multiply(self,vector): 
        x = self.x * vector.x 
        y = self.y * vector.y 
        return x + y
    def print_position(self): 
        print(self.x)
        print(self.y)
    def get_position(self): 
        return [self.x,self.y]
    def magnitude(self): 
        magnitude_ = (self.x**2 + self.y**2)**0.5
        return magnitude_ 
    def unit_vector_to(self,vector1): 
        displacement_vector = vector1.sub(self)
        distance = displacement_vector.magnitude()
        unit_vector = displacement_vector.divide_by(distance)
        return unit_vector 

    
def add(self,vector1): 
    x = self.x + vector1.x 
    y = self.y + vector1.y 
    return vector(x,y)
vector.add = add 
def sub(self,vector1): 
    x = self.x - vector1.x 
    y = self.y - vector1.y 
    return vector(x,y)
vector.sub = sub 
def distance_to(self,vector1): 
    diff_vector = self.sub(vector1)
    return diff_vector.magnitude()
vector.distance_to = distance_to
def divide_by_constant(self,constant): 
    x = self.x/constant 
    y = self.y/constant 
    return vector(x,y)
vector.divide_by=divide_by_constant
def multiply_by_constant(self,constant): 
    x = self.x * constant 
    y = self.y * constant 
    return vector(x,y)
vector.multiply_by = multiply_by_constant






        
    