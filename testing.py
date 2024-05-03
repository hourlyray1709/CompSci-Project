from lib.vector_class import vector
from lib.planet_class import planet, find_pairs, find_resultant_force
import matplotlib.pyplot as plt #---------------------------------------------------import all necessary libraries for testing

GRAVITATIONAL_CONSTANT = 6.6743 * 10 ** -11 #---------------------------------------define g

planet1 = planet(position=vector(216920000, 863192000), mass=3.049*10**24)
planet2 = planet(position=vector(1062459200, 1376320000), mass=6.13*10**24)
planet3 = planet(position=vector(9080720000, 15334000000), mass=2.29*10**23)
planet4 = planet(position=vector(568480000, 1900219200), mass=1.477*10**25)
planet5 = planet(position=vector(15646664000, 6706568000), mass=9.0144*10**23) #----define all planets with the test data 

planet_list = [planet1, planet2, planet3, planet4, planet5]


def test_find_force():
    test_data = [vector(1.09016E+21, 6.61581E+20), #---------------------------------test data generated using physics constant 
                vector(8.45269E+16, 1.37996E+17), 
                vector(8.04829E+20, 2.37407E+21),
                vector(6.30193E+17, 2.3866E+17),
                vector(1.80118E+17, 3.13538E+17), 
                vector(-7.99558E+21, 8.47987E+21),
                vector(1.43668E+18, 5.25081E+17),
                vector(-4.77726E+17, -7.53934E+17),
                vector(7.09861E+16, -9.32734E+16),
                vector(3.38052E+18, 1.07758E+18),
                ] #-------------------------------------------------------------------import test data by hand 

    pairs_list = find_pairs(planet_list)
    for i in range(len(pairs_list)): #-------------------------------------------------find the force each planet exerts on each other 
        force = pairs_list[i][0].find_force(pairs_list[i][1], GRAVITATIONAL_CONSTANT)
        x_diff = abs(test_data[i].x - force.x)
        y_diff = abs(test_data[i].y - force.y)
        percentage_error_x = (x_diff / test_data[i].x) * 100 
        percentage_error_y = (y_diff / test_data[i].y) * 100 #-------------------------compare it to test data. if percentage error less than 1, pass
    
        if percentage_error_x < 0.01 and percentage_error_y < 0.01: 
            passed = True 
        print("{}, {}, {}".format(force.x, force.y, passed)) #-------------------------show results 

def test_find_resultant_force(): 
    test_data = [ #---------------------------------test data obtained using constant from physics, not user defined constant
        vector(1.89571E+21, 3.03603E+21),
        vector(-9.08413E+21, 7.81913E+21),
        vector(-6.71385E+17, -1.29874E+18), 
        vector(7.19461E+21, -1.08521E+22),
        vector(-5.51839E+18, -1.74805E+18)
    ]
    find_resultant_force(planet_list, GRAVITATIONAL_CONSTANT)
    
    for i in range(len(planet_list)): 
        passed = False #-----------------------------------------------------------------------------------------assume failed, and calculate percentage errors 
        x_percent_error = (abs(planet_list[i].resultant_force.x - test_data[i].x) / test_data[i].x) * 100 
        y_percent_error = (abs(planet_list[i].resultant_force.y - test_data[i].y) / test_data[i].y) * 100
        if x_percent_error < 0.01 and y_percent_error < 0.01: #--------------------------------------------------if error is small enough then say passed
            passed = True 
        print("{}, {}, {}".format(planet_list[i].resultant_force.x, planet_list[i].resultant_force.y, passed))

def test_find_acceleration(): 
    test_data = [ #---------------------------------------------------import the test data generated using excel 
        vector(0.000621747, 0.000995747),
        vector(-0.001481913, 0.001275551),
        vector(-2.93181E-06, -5.67136E-06), 
        vector(0.00048711, -0.00073474),
        vector(-6.12174E-06, -1.93917E-06),
    ]
    find_resultant_force(planet_list, GRAVITATIONAL_CONSTANT) #------find the resultant force for each planet 
    for i in range(len(planet_list)): 
        passed = False 
        planet_list[i].find_acceleration() #--------------------------------------calculuate the acceleration for each planet 
        acceleration = planet_list[i].acceleration 
        x_value = acceleration.x 
        y_value = acceleration.y #-----------------------------------fetch the x and y components of the acceleration of each planet 
        x_diff = abs(test_data[i].x - x_value) 
        y_diff = abs(test_data[i].y - y_value)  #----find the difference between test data and actual output 
        x_percent_error = (x_diff / test_data[i].x) * 100  
        y_percent_error = (y_diff / test_data[i].y) * 100  #-------find the percentage error for both 
        if x_percent_error < 0.01 and y_percent_error < 0.01: 
            passed = True 
        print("{}, {}, {}".format(x_value, y_value, passed))

def test_v_half_step(time_step_size): 
    test_data = [ #----------------------------------------------------import the test data generated from excel 
        vector(6.21747E-05, 9.95747E-05),
        vector(-0.000148191, 0.000127555),
        vector(-2.93181E-07, -5.67136E-07),
        vector(4.8711E-05, -7.3474E-05),
        vector(-6.12174E-07, -1.93917E-07), 
    ]
    find_resultant_force(planet_list, GRAVITATIONAL_CONSTANT) #-------find the resultant force on each planet 
    for i in range(len(planet_list)): 
        passed = False  #---------------------------------------------assume failed 
        planet_list[i].find_acceleration() #--------------------------find the acceleration of the planet 
        planet_list[i].find_v_half_step(time_step_size) #-------------find the velocity half a time step away 
        x_value = planet_list[i].v_half_step.x 
        y_value = planet_list[i].v_half_step.y 
        x_diff = abs(test_data[i].x - x_value)
        y_diff = abs(test_data[i].y - y_value) #----------------------find the difference between the expected output and actual output 
        x_percent_error = (x_diff / test_data[i].x) * 100 
        y_percent_error = (y_diff / test_data[i].y) * 100 
        if x_percent_error < 0.01 and y_percent_error < 0.01: #-------if difference is small, accept it 
            passed = True 
        print("{}, {}, {}".format(x_value, y_value, passed)) #--------show result of test 

def test_new_pos(time_step_size):
    test_data = [ #---------------------------------------------------import the test data generated in excel 
        vector(216920155.4, 863192248.9), 
        vector(1062458830, 1376320319), 
        vector(9080719999, 15333999999), 
        vector(568480121.8, 1900219016), 
        vector(15646663998, 6706568000), 
    ]
    find_resultant_force(planet_list, GRAVITATIONAL_CONSTANT) #------find the resultant force on each planet 
    for i in range(len(planet_list)): 
        passed = False 
        planet_list[i].find_acceleration() #-------------------------find the acceleration of each planet 
        planet_list[i].find_v_half_step(time_step_size) #------------find the velocity at half a time step away for each planet 
        planet_list[i].find_new_pos(time_step_size) #----------------find the new position of each planet 
        x_value = planet_list[i].position.x 
        y_value = planet_list[i].position.y 
        x_diff = abs(test_data[i].x - x_value)
        y_diff = abs(test_data[i].y - y_value) #---------------------calculate the deviation from the expected answer 
        x_percent_error = (x_diff / test_data[i].x) * 100 
        y_percent_error = (y_diff / test_data[i].y) * 100 #----------find the percentage error using the deviation 
        if x_percent_error < 0.01 and y_percent_error < 0.01: #------if deviation is small, show that the test passed 
            passed = True 
        print("{}, {}, {}".format(x_value, y_value, passed)) #-------print the results 
        
test_new_pos(500)