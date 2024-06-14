from planet_class import planet, find_resultant_force

def simulate(planet_list, grav_const, t_step_size): 
    find_resultant_force(planet_list, grav_const) #---------find resultant force exerted on each planet 
    for i in planet_list: 
        i.find_acceleration() #-----------------------------find new acceleration of each planet 
        i.find_v_half_step(t_step_size) #-------------------find velocity at half a time step away 
        i.find_new_pos(t_step_size)
        i.past_positions.enqueue(i.position)