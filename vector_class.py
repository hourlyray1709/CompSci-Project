class vector: 
    def __init__(self, x,y): #----------------------------------initialising the vector class
        self.x = x 
        self.y = y 
        self.size = self.magnitude()
    
    def __add__(self, vector_input): #--------------------------adds another vector to itself, returns a vector 
        x = self.x + vector_input.x #---------------------------adds the x component of the two vectors together 
        y = self.y + vector_input.y #---------------------------adds the y components of the two vectors together 
        new_vec = vector(x,y) #---------------------------------creates a new vector based on the results 
        return new_vec #----------------------------------------returns the new vector 
    
    def __sub__(self, vector_input): 
        x = self.x - vector_input.x #---------------------------adds the x component of the two vectors together 
        y = self.y - vector_input.y #---------------------------adds the y components of the two vectors together 
        new_vec = vector(x,y) #---------------------------------creates a new vector based on the results 
        return new_vec #----------------------------------------return the new vector
    
    def __matmul__(self, vector_input): #-----------------------dot product operator @
        x = self.x * vector_input.x 
        y = self.y * vector_input.y 
        sum_ = x + y #------------------------------------------the dot product multiplies each component together then returns their sum 
        return sum_
    
    def __mul__(self, scalar): 
        x = self.x * scalar #-----------------------------------multiply the x component with the scalar input 
        y = self.y * scalar #-----------------------------------multiply the y component with the scalar input 
        return vector(x,y) #------------------------------------return the vector from the multiplication 
    
    def __truediv__(self,scalar):  
        x = self.x / scalar #-----------------------------------divide the x component with the scalar input 
        y = self.y / scalar #-----------------------------------divide the y component with the scalar input 
        return vector(x,y) #------------------------------------return the vector from the division 
    
    def magnitude(self): 
        return (self.x ** 2 + self.y ** 2)**0.5 #---------------pythagora's theorem 
    
    def __mod__(self, vector_input): #--------------------------unit vector operator %
        vectorTo = vector_input - self #------------------------find the vector that takes you from self to the vector input 
        size = vectorTo.magnitude() #---------------------------find the magnitude of the vector 
        unitVectorTo = vectorTo / size #------------------------find the unit vector to that vector 
        return unitVectorTo #-----------------------------------return it 
    
    def __rshift__(self, vector_input): #-----------------------distance to operator >> 
        vectorTo = vector_input - self #------------------------take the vector that takes you from self to the vector input 
        size = vectorTo.size #----------------------------------get its magnitude 
        return size #-------------------------------------------return it 
    




    
    