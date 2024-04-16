class vector: 
    def __init__(self, x,y): #----------------------------------initialising the vector class
        self.x = x 
        self.y = y 
    
    def add(self, vector_input): #------------------------------adds another vector to itself, returns a vector 
        x = self.x + vector_input.x #---------------------------adds the x component of the two vectors together 
        y = self.y + vector_input.y #---------------------------adds the y components of the two vectors together 
        new_vec = vector(x,y) #---------------------------------creates a new vector based on the results 
        return new_vec #----------------------------------------returns the new vector 