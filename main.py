#import the classes I need 

from vector_class import vector 
from planet_class import planet, find_resultant_force
from simulate import simulate 
from queue_class import queue 

from tkinter import * 
from tkinter import ttk
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib import pyplot as plt, animation 
from functools import partial 

#-----------------------------------------------------------------------------------------------------------------------Core variables 
max_trail_length = 500 #-------------------------how many past positions to keep track of when generating a trail of the planets 
planet1 = planet(position=vector(0,0), mass=1.989*10**30, velocity=vector(0,0), past_positions=queue([], max_trail_length))
planet2 = planet(position=vector(250*10**8, 0), mass=5.972*10**24, velocity=vector(0, 35000), past_positions=queue([], max_trail_length))
planet3 = planet(position=vector(-250*10**8, 0), mass=10.972*10**24, velocity=vector(0, -35000), past_positions=queue([], max_trail_length))
planet4 = planet(position=vector(-500*10**8, 0), mass=5.972*10**24, velocity=vector(0, -50000), past_positions=queue([], max_trail_length))
planet5 = planet(position=vector(-125*10**8, 0), mass=3.20*10**24, velocity=vector(0, -50000), past_positions=queue([], max_trail_length))
grav_const = 6.67430 * 10 ** -11 
time_step_size = 1000
planet_list = [planet1, planet2, planet3, planet4, planet5]
update_every = 120000 #------------------------------each frame will represent this number in seconds 
frames_ = int(update_every / time_step_size)
fps = 24
paused = False  

init_attributes = []
for i in planet_list: 
    attributes = [i.position, i.mass, i.velocity, i.v_half_step, i.acceleration]      # fetch all starting attributes 
    init_attributes.append(attributes)



#-----------------------------------------------------------------------------------------------------------------------Core variables 

#--------------------------------------------------------------------------------------------------------------------GUI stuff 
main_window = Tk()

style = ttk.Style()
style.configure("TFrame", background="grey")

notebook = ttk.Notebook(main_window)
notebook.pack() #------------------------------initiate notebook for tab control 

main_tab = ttk.Frame(notebook, style="TFrame") #---------------create tab for main window 
settings_tab = ttk.Frame(notebook) #-----------create tab for settings 
notebook.add(main_tab, text="Main Window")
notebook.add(settings_tab, text="Settings") #--add tabs to notebook 

simulation_figure = Figure(figsize=(8,8), dpi=100, facecolor="grey")
max_val = 10**12
simulation_plot = simulation_figure.add_subplot(xlim=(-max_val, max_val), ylim=(-max_val, max_val))
simulation_plot.set_facecolor("white")
dots = simulation_plot.scatter([],[])
plt.grid()
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

def pause_func(): 
    global paused              # use the globally defined paused variable to check if the animation is currently paused
    if paused == True: 
        paused = False       
    else: 
        paused = True          # swap the Boolean values, so when user presses it, it changes to true, and if it was true then it changes to false 
    if paused == True: 
        anim.pause()           # if needed to pause, pause it 
    else: 
        anim.resume()          # if needed to resume, resume it 
def reset(): 
    global planet_list 
    global init_planets 
    global anim 
    for i in range(len(planet_list)): 
        planet_list[i].position = init_attributes[i][0]
        planet_list[i].mass = init_attributes[i][1] 
        planet_list[i].velocity = init_attributes[i][2]
        planet_list[i].v_half_step = init_attributes[i][3]
        planet_list[i].acceleration = init_attributes[i][4]

    

play_button = Button(main_tab, text="Play/Pause", command=pause_func)
play_button.grid(row=2,column=0)

reset_button = Button(main_tab, text="Reset simulation", command=reset)
reset_button.grid(row=3,column=0)

def animate(i): 
    x = [] 
    y = []
    trails = [] 
    for i in range(frames_): 
        simulate(planet_list, grav_const, time_step_size) #-----------update the position of all the planets 
    for i in planet_list:
        trail_x = [] 
        trail_y = []  
        x.append(i.position.x)                        #--------------append the CURRENT positions of each planet 
        y.append(i.position.y)
        for position_ in i.past_positions.arr:
            trail_x.append(position_.x)
            trail_y.append(position_.y)              #---------------fetch all OLD positions of each planet 
        trail = simulation_plot.plot(trail_x,trail_y, "r")  #----------plot the OLD positions of each planet 
        trails.append(trail[0])                            #---------save the artist 
    dots = simulation_plot.scatter(x,y, c="k") #------------plot the scatter graph
    trails.append(dots)                       #-------------save all artists 
    return trails                            #------------return the iterable of the artists

anim = animation.FuncAnimation(simulation_figure, animate, frames=100, blit=True) #-------use animation to update the graph
button_values = {
    t_step_scale:"", 
    g_const_scale:"", 
    g_expo_spinbox:"", 
}

while True: 
    try:
        main_window.update() #---------------------------------------run the main loop, this allows me to handle widget interactions 
    except: 
        print("Crashed")
        quit()



