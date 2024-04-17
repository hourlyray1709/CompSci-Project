def isNum(n): 
    n = str(n) # -----------------------------------------------turn n into a string 
    if "-" in n or "." in n: #----------------------------------checks for these two characters as they are allowed, but triggers isnumeric to be false
        n = "".join([i for i in n if i not in "-."]) #-------------------use list comprehension to compress the code 
    if n.isnumeric(): #-----------------------------------------if it is a number then accept it 
        return True 
    else:
        return False 
class vector: 
    def __init__(self, x,y): #----------------------------------initialising the vector class
        if isNum(x): #---------------------------check if the input x is valid before accepting it
            self.x = x 
        else: 
            self.x = None #-------------------------------------otherwise we set it to None 
        if isNum(y): #---------------------------check if the input y is valid before accepting it 
            self.y = y 
        else: 
            self.y = None #-------------------------------------otherwise we set it to None
    
    def add(self, vector_input): #------------------------------adds another vector to itself, returns a vector 
        for i in [self.x, self.y, vector_input.x, vector_input.y]: 
            if i == None: #-------------------------------------iterate over all components, if it is none, void the operation 
                return vector(None, None) 
        x = self.x + vector_input.x #---------------------------adds the x component of the two vectors together 
        y = self.y + vector_input.y #---------------------------adds the y components of the two vectors together 
        new_vec = vector(x,y) #---------------------------------creates a new vector based on the results 
        return new_vec #----------------------------------------returns the new vector 
    
    def subtract(self, vector_input): 
        for i in [self.x, self.y, vector_input.x, vector_input.y]: 
            if i == None: #-------------------------------------iterate over all the components, if it is none, void the operation 
                return vector(None, None)
        x = self.x - vector_input.x #---------------------------adds the x component of the two vectors together 
        y = self.y - vector_input.y #---------------------------adds the y components of the two vectors together 
        new_vec = vector(x,y) #---------------------------------creates a new vector based on the results 
        return new_vec #----------------------------------------return the new vector
    
    def dot(self, vector_input): 
        for i in [self.x, self.y, vector_input.x, vector_input.y]: 
            if i == None: #-------------------------------------iterate over all the components, if it is none, void the operation 
                return None #-----------------------------------we return None instead of (None, None) because we expect a scalar output in normal use
        x = self.x * vector_input.x 
        y = self.y * vector_input.y 
        sum_ = x + y #------------------------------------------the dot product multiplies each component together then returns their sum 
        return sum_
    
    def multiply(self, scalar): 
        if not isNum(scalar): #---------------------------------as the scalar is an outside input and not a vector, we have to check manually
            scalar = None 
        for i in [self.x, self.y, scalar]: 
            if i == None: 
                return vector(None, None) #---------------------return (None,None) vector if invalid, as we expect vector output
        x = self.x * scalar #-----------------------------------multiply the x component with the scalar input 
        y = self.y * scalar #-----------------------------------multiply the y component with the scalar input 
        return vector(x,y) #------------------------------------return the vector from the multiplication 
    
    def divide(self,scalar): 
        if not isNum(scalar): #---------------------------------as the scalar is an outside input and not a vector, we have to check manually 
            scalar = None 
        for i in [self.x, self.y, scalar]: 
            if i == None: 
                return vector(None, None) #---------------------return (None,None) vector if invalid, as we expect vector output 
        x = self.x / scalar #-----------------------------------divide the x component with the scalar input 
        y = self.y / scalar #-----------------------------------divide the y component with the scalar input 
        return vector(x,y) #------------------------------------return the vector from the division 


    
    