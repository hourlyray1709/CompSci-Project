#import the classes I need 

from vector_class import vector 
from planet_class import planet, find_resultant_force
from simulate import simulate 

from tkinter import * 
from tkinter import ttk
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib import animation 

#-----------------------------------------------------------------------------------------------------------------------Core variables 
planet1 = planet(position=vector(0,0), mass=1.98*10**30, velocity=vector(0,0))
planet2 = planet(position=vector(150000000000,0), mass= 5.28*10**24, velocity=vector(0,25000))
planet3 = planet(position=vector(104120012,502002), mass=1.4039 * 10 ** 23, velocity=vector(500,0))
grav_const = 6.67430 * 10 ** -11 
time_step_size = 0.01 
planet_list = [planet1, planet2, planet3]
update_every = 1 #------------------------------each frame will represent this number in seconds 
frames = int(update_every / time_step_size)
#-----------------------------------------------------------------------------------------------------------------------Core variables 

#--------------------------------------------------------------------------------------------------------------------GUI stuff 
main_window = Tk()

notebook = ttk.Notebook(main_window)
notebook.pack() #------------------------------initiate notebook for tab control 

main_tab = ttk.Frame(notebook) #---------------create tab for main window 
settings_tab = ttk.Frame(notebook) #-----------create tab for settings 
notebook.add(main_tab, text="Main Window")
notebook.add(settings_tab, text="Settings") #--add tabs to notebook 

simulation_figure = Figure(figsize=(5,5), dpi=100)
simulation_plot = simulation_figure.add_subplot()
# plot something 
simulation_canvas = FigureCanvasTkAgg(simulation_figure, master=main_tab) #------create the canvas 
simulation_canvas.draw()
simulation_canvas.get_tk_widget().grid(row=0,column=0) #-------------------put the simulation plot into tkinter 
simulation_toolbar_frame = Frame(main_tab)
simulation_toolbar = NavigationToolbar2Tk(simulation_canvas, simulation_toolbar_frame) #---create the toolbar 
simulation_toolbar_frame.grid(row=1,column=0) #--------------------------------------------pack it below the plot
simulation_toolbar.update()
simulation_canvas.get_tk_widget().grid(row=0,column=0) #-----------------------------------pack it into the tab

t_step_size_label = Label(settings_tab, text="Time Step Size: ") #-------------------------create a text label 
t_step_size_label.grid(row=0, column=0)
t_step_scale = Scale(settings_tab, orient=HORIZONTAL) #------------------------------------create a scroll bar 
t_step_scale.grid(row=0,column=1)

g_const_label = Label(settings_tab, text="Grav. Constant Value: ") #-----------------------create a label 
g_const_label.grid(row=1,column=0)
g_const_scale = Scale(settings_tab, orient=HORIZONTAL, from_ = 0, to = 9.99) #-------------create a scrollbar 
g_const_scale.grid(row=1,column=1)

g_expo_label = Label(settings_tab, text="Grav. Exponent: ") #------------------------------create a label 
g_expo_label.grid(row=1, column=2)
g_expo_spinbox = Spinbox(settings_tab, from_ = -100, to=100, state="readonly") #-------------create a spinbox 
g_expo_spinbox.grid(row=1,column=3)

play_button = Button(main_tab, text="Play/Pause")
play_button.grid(row=2,column=0)

reset_button = Button(main_tab, text="Reset simulation")
reset_button.grid(row=3,column=0)

def fetch_positions(planet_list): 
    x_pos = []
    y_pos = [] 
    for i in planet_list: 
        x_pos.append(i.position.x) #-----------append the planet's position's x value to the array 
        y_pos.append(i.position.y) #-----------append the planet's position's y value to the array 
    return [x_pos,y_pos] #---------------------return it 

def update_plot(planet_list): 
    positions = fetch_positions(planet_list) #----------------------------------fetch the positions of the planets 
    x_coords = positions[0]
    y_coords = positions[1]
    simulation_figure = Figure((5,5), dpi=100) 
    simulation_plot = simulation_figure.add_subplot() #-------------------------create a plot to draw the planets on 
    simulation_plot.plot(x_coords, y_coords, "bo")
    #simulation_plot.autoscale(False)
    simulation_canvas = FigureCanvasTkAgg(simulation_figure, master=main_tab)
    simulation_canvas.draw() 
    simulation_canvas.get_tk_widget().grid(row=0, column=0) #-------------------pack the plot into tkinter 

anim = animation.FuncAnimation()
#-----------------------------------------------------------------------------------------------------------------------GUI stuff 

while True: 
    print("{} {} {}".format(planet1.position >> planet2.position, planet1.resultant_force.size, planet2.resultant_force.size))
    for i in range(frames):
        simulate(planet_list,grav_const,time_step_size)
    update_plot(planet_list)
    main_window.update()



