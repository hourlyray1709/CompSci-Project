from my_classes import vector 
from my_classes import planet 

planet_list = [] 

earth = planet('earth', 5.972*10**24, vector(0,0), vector(10,10), vector(0,5))
jupiter = planet('jupiter', 2*10**27, vector(10,3), vector(30,5), vector(5,1))

planet_list = [earth,jupiter]

resultant_force = earth.resultant_force(planet_list,6.67430*10**-11)
print(resultant_force.magnitude())