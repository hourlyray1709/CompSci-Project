from vector_class import vector
from queue_class import queue  
import random 
import matplotlib.colors
def find_pairs(planet_list): 
    temp_planet_list = planet_list
    pair_list = [] 
    for i in range(len(temp_planet_list)): #--------------------------------------------------------loop over all planets 
        exclusive_list = [temp_planet_list[k] for k in range(i+1, len(temp_planet_list))] #---------find all others that pair up with it 
        for k in range(len(exclusive_list)):
            pair = [temp_planet_list[i], exclusive_list[k]] #---------------------------------------save the pair
            pair_list.append(pair)
    return pair_list #------------------------------------------------------------------------------return all pairs 
def find_resultant_force(planet_list, gravitational_constant): 
    if len(planet_list)<2: 
        return 0 
    temp_planet_list = planet_list
    for i in range(len(temp_planet_list)): 
        temp_planet_list[i].resultant_force = vector(0,0)
    for i in range(len(temp_planet_list)): #--------------------------------------------------------loop over all planets 
        exclusive_list = [temp_planet_list[k] for k in range(i+1, len(temp_planet_list))] #---------find all others that pair up with it
        for k in range(len(exclusive_list)):
            pair = [temp_planet_list[i], exclusive_list[k]] #---------------------------------------save the pair
            force_on_temp_planet = pair[0].find_force(pair[1], gravitational_constant) #------------------------------------force exerted ON the temp_planet_list[i]
            force_on_exlusive_planet = force_on_temp_planet * -1
            pair[0].resultant_force += force_on_temp_planet
            pair[1].resultant_force += force_on_exlusive_planet                        # optimised to reduce no. of calculations
class planet: 
    def __init__(self, position, mass, velocity=vector(0,0), acceleration=vector(0,0), resultant_force=vector(0,0), past_positions=queue([], 0), colour=None): 
        self.position = position #---------------------------------------------------initialise all of the attributes 
        self.velocity = velocity 
        self.acceleration = acceleration 
        self.mass = mass 
        self.v_half_step = velocity
        self.resultant_force = resultant_force
        self.past_positions = past_positions
        possible_colors = [i for i in matplotlib.colors.TABLEAU_COLORS]
        if colour == None: 
            self.colour = possible_colors[random.randint(0, len(possible_colors)-1)]
    def find_force(self, planet_input, gravitational_constant): #--------------------finds the force exerted on the planet self
        mass1 = self.mass #----------------------------------------------------------fetch the masses 
        mass2 = planet_input.mass 
        position1 = self.position #--------------------------------------------------fetch the positions 
        position2 = planet_input.position 
        distance = self.position >> planet_input.position #--------------------------find the distance between the planets 
        unit_vec = self.position % planet_input.position #---------------------------find the unit vector from self to planet input 
        force = unit_vec * (gravitational_constant * (mass1 * mass2) / (distance**2))  #use an equivalent form of newton's law of gravitation that makes more sense to me 
        return force 
    def find_acceleration(self): 
        self.acceleration = self.resultant_force / self.mass
        return self.resultant_force / self.mass # -----------------------------------use F = ma, rearrange to a = F/m 
    def find_v_half_step(self, time_step_size): 
        acceleration = self.acceleration #------------------------------------------assume that we have already found the acceleration using the above function 
        self.v_half_step += acceleration * time_step_size #-------------------------store the new velocity at half a time step away 
        return self.v_half_step #---------------------------------------------------return it in case we want to see/test it 
    def find_new_pos(self, time_step_size): 
        self.position += self.v_half_step * time_step_size #------------------------using leapfrog integration, find the new position and replace the current position attribute
        return self.position #------------------------------------------------------return it in case we want to see/test it 




        

                


    