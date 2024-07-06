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
import math 

#-----------------------------------------------------------------------------------------------------------------------Core variables 
time_step_size = 3000
max_trail_length = int(500 * (1000/time_step_size)) #-------------------------how many past positions to keep track of when generating a trail of the planets 
planet1 = planet(position=vector(0,0), mass=1.989*10**30, velocity=vector(0,10000), past_positions=queue([], max_trail_length))
planet2 = planet(position=vector(250*10**8, 0), mass=5.972*10**24, velocity=vector(0, 35000), past_positions=queue([], max_trail_length))
planet3 = planet(position=vector(-250*10**8, 0), mass=10.972*10**24, velocity=vector(0, -35000), past_positions=queue([], max_trail_length))
planet4 = planet(position=vector(-500*10**8, 0), mass=5.972*10**24, velocity=vector(0, -50000), past_positions=queue([], max_trail_length))
planet5 = planet(position=vector(-125*10**8, 0), mass=3.20*10**24, velocity=vector(0, -50000), past_positions=queue([], max_trail_length))
planet6 = planet(position=vector(5*10**10, 0), mass=10.20*10**28, velocity=vector(0, 25000), past_positions=queue([], max_trail_length))
grav_const = 6.67430 * 10 ** -11 
grav_expo = -11
planet_list = [planet1, planet2, planet3, planet4, planet5, planet6]
update_every = 120000 #------------------------------each frame will represent this number in seconds 
frames_ = int(update_every / time_step_size)
fps = 24
paused = False  
dragging = None 
tabPause = True  
selected = None


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
t_step_scale = Scale(settings_tab, orient=HORIZONTAL, from_=1, to=10000, resolution=0.01) #------------------------------------create a scroll bar 
t_step_scale.set(time_step_size)
t_step_scale.grid(row=0,column=1)

g_const_label = Label(settings_tab, text="Grav. Constant Value: ") #-----------------------create a label 
g_const_label.grid(row=1,column=0)
g_const_scale = Scale(settings_tab, orient=HORIZONTAL, from_ = 0, to = 9.99, resolution=0.01) #-------------create a scrollbar 
g_const_scale.set(grav_const / 10 ** grav_expo)
g_const_scale.grid(row=1,column=1)

grav_expo_str = StringVar(main_window)
grav_expo_str.set(grav_expo)
g_expo_label = Label(settings_tab, text="Grav. Exponent: ") #------------------------------create a label 
g_expo_label.grid(row=1, column=2)
g_expo_spinbox = Spinbox(settings_tab, from_ = -100, to=100, state="readonly", increment=1, textvariable=grav_expo_str) #-------------create a spinb
g_expo_spinbox.grid(row=1,column=3)

def createPlanet():                                                                                       # code to create a new planet 
    global paused
    global dragging 
    global init_attributes
    massMantissa = int(mass_scale.get())
    massExpo = int(massExpo_spinbox.get())
    xVelMantissa = int(hvel_scale.get())
    xVelExpo = int(hvelExpo_spinbox.get())
    yVelMantissa = int(vvel_scale.get()) 
    yVelExpo = int(vvelExpo_spinbox.get())         # fetch the relevant values from the editor 

    mass = massMantissa * 10 ** massExpo 
    xVel = xVelMantissa * 10 ** xVelExpo 
    yVel = yVelMantissa * 10 ** yVelExpo           # calculate the actual values fro the planet params 
    vel = vector(xVel,yVel)
    paused = True 
    #anim.pause()                                                                                          # pause the animation 
    newPlanet = planet(position=vector(0,0), mass=mass, past_positions=queue([], max_trail_length), velocity=vel)     # create a new planet using the params
    attributes = [newPlanet.position, newPlanet.mass, newPlanet.velocity, newPlanet.v_half_step, newPlanet.acceleration]
    init_attributes.append(attributes)                                                                    # handle reset for new planet 
    dragging = newPlanet                                                                                  # set it to being dragged 
    planet_list.append(newPlanet)                                                                         # add it to the planet list for sim 

def deletePlanet(): 
    global dragging 
    global planet_list 
    if dragging != None:                                              # if dragging a valid planet 
        #anim.pause()                                                  # pause the animation 
        paused = True 
        planet_list = [i for i in planet_list if i != dragging]       # remove the planet from the list of planets 
        redraw()

def editPlanet():
    global dragging
    global selected 

    massMantissa = float(mass_scale.get()) 
    massExpo = float(massExpo_spinbox.get())
    
    xVelMantissa = float(hvel_scale.get())
    xVelExpo = float(hvelExpo_spinbox.get())

    yVelMantissa = float(vvel_scale.get())
    yVelExpo = float(vvelExpo_spinbox.get())

    selected.mass = massMantissa * 10 ** massExpo 
    selected.v_half_step = vector(xVelMantissa * 10 ** xVelExpo,       yVelMantissa * 10 ** yVelExpo)


    

def redraw(): 
    xlim = simulation_plot.get_xlim() 
    ylim = simulation_plot.get_ylim()                          # get the x and y limits of the graph 
    simulation_plot.clear() 
    simulation_plot.set_xlim(xlim)
    simulation_plot.set_ylim(ylim)
    x = [i.position.x for i in planet_list]
    y = [i.position.y for i in planet_list]                    # fetch the positions of the planets 
    for i in planet_list: 
        trailx = [k.x for k in i.past_positions.arr]
        traily = [k.y for k in i.past_positions.arr]
        simulation_plot.plot(trailx, traily, c="r")            # draw the trails 
    simulation_plot.scatter(x,y,c="k")
    simulation_canvas.draw() 
    simulation_canvas.get_tk_widget().grid(row=0, column=0)    # draw the planets 


sidebar_frame = Frame(main_tab)                                                                           # create a collection that holds everything in the side menu 
sidebar_frame.grid(row=0, column=1)                    

title = Label(sidebar_frame, text="Planet Editor")                                                        # create a text title for the side menu
title.grid(row=0, column=0)

mass_label = Label(sidebar_frame, text="Mass: ")                                                          # GUI for adjusting mass 
mass_label.grid(row=1, column=0)
mass_scale = Scale(sidebar_frame, orient=HORIZONTAL, from_=0, to=10, resolution=0.001)
mass_scale.set(5)
mass_scale.grid(row=1, column=1)

massExpo_label = Label(sidebar_frame, text="Mass Exponent: ")
massExpo_label.grid(row=1, column=2)
massExp_strVar = StringVar(sidebar_frame, "23")
massExpo_spinbox = Spinbox(sidebar_frame, from_=-100, to=100, state="readonly", increment=1, textvariable=massExp_strVar)
massExpo_spinbox.grid(row=1, column=3)

velMin = -9.99 
velMax = 9.99 
velRes = 0.01

hvel_label = Label(sidebar_frame, text="Horizontal Velocity: ")                                           # GUI for adjusting velocity in x axis 
hvel_label.grid(row=2,column=0)
hvel_scale = Scale(sidebar_frame, orient=HORIZONTAL, from_=velMin, to=velMax, resolution=velRes)
hvel_scale.grid(row=2, column=1)
hvelExpo_label = Label(sidebar_frame, text="Horizontal Velocity Exponent: ")
hvelExpo_label.grid(row=2, column=2)
hvelStringVar = StringVar(sidebar_frame, "0")
hvelExpo_spinbox = Spinbox(sidebar_frame, from_=-100, to=100, state="readonly", increment=1, textvariable=hvelStringVar)
hvelExpo_spinbox.grid(row=2, column=3)

vvel_label = Label(sidebar_frame, text="Vertical Velocity: ")                                             # GUI for adjusting velocity in y axis 
vvel_label.grid(row=3, column=0)
vvel_scale = Scale(sidebar_frame, orient=HORIZONTAL, from_= velMin, to=velMax, resolution=velRes)
vvel_scale.grid(row=3, column=1)
vvelExpo_label = Label(sidebar_frame, text="Vertical Velocity Exponent: ")
vvelExpo_label.grid(row=3, column=2)
vvelStringVar = StringVar(sidebar_frame, "0")
vvelExpo_spinbox = Spinbox(sidebar_frame, from_=-100, to=100, state="readonly", increment=1, textvariable=vvelStringVar)
vvelExpo_spinbox.grid(row=3, column=3)

create_planet_button = Button(sidebar_frame, text="Create Planet", command=createPlanet)                  # Button to create planet 
create_planet_button.grid(row=4, column=0)
edit_planet_button = Button(sidebar_frame, text="Edit Planet", command=editPlanet)
edit_planet_button.grid(row=4, column=1)
delete_planet_button = Button(sidebar_frame, text="Delete Planet", command=deletePlanet)                                        # Button to destroy planet 
delete_planet_button.grid(row=4, column=2)

def tabChange(event): 
    global paused 
    global tabPause
    global grav_const 
    global grav_expo 
    global time_step_size
    g_const_val = g_const_scale.get() 
    g_expo_val = g_expo_spinbox.get() 
    time_step_val = t_step_scale.get() 
    print(f"Before tab change, variable values are {grav_const} ,  {grav_expo} ,  {time_step_size}")
    print(f"Before tab change, GUI values are {g_const_val} {g_expo_val} {time_step_val}")
    tabPause = not tabPause                           # invert tabPause 
    if tabPause:                                      # if need to pause 
        paused = True                                 # pause 
        #anim.pause() 
    elif not tabPause:                                # if dont need to pause 
        grav_expo = float(g_expo_val) 
        grav_const = float(g_const_val) * 10 **float(grav_expo)
        time_step_size = time_step_val
        print(f"After tab change, variable values are {grav_const} ,  {grav_expo} ,  {time_step_size}")
        paused = False                                # unpause 
        #anim.resume() 

notebook.bind("<<NotebookTabChanged>>", tabChange)

def pause_func(): 
    global paused              # use the globally defined paused variable to check if the animation is currently paused
    if paused == True: 
        paused = False       
    else: 
        paused = True          # swap the Boolean values, so when user presses it, it changes to true, and if it was true then it changes to false 
    #if paused == True: 
        #anim.pause()           # if needed to pause, pause it 
    #else:  
        #anim.resume()          # if needed to resume, resume it 
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


buttons_frame = Frame(main_tab)
buttons_frame.grid(row=2, column=0)  

play_button = Button(buttons_frame, text="Play/Pause", command=pause_func)
play_button.grid(row=0,column=0)
reset_button = Button(buttons_frame, text="Reset simulation", command=reset)
reset_button.grid(row=0,column=1)


#--------------------------------------------------------------------------------------------------------------------------------main loop related 
def animate(i): 
    global planet_list 
    global grav_const
    global time_step_size
    xlim = simulation_plot.get_xlim()
    ylim = simulation_plot.get_ylim()
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
    redraw()
    trails.append(dots)                       #-------------save all artists 
    return trails                            #------------return the iterable of the artists

#anim = animation.FuncAnimation(simulation_figure, animate, frames=100, blit=True) #-------use animation to update the graph
#-------------------------------------------------------------------------------------------------------------------------------------handling drag and drop
def checkDist(planet_, event_):
    xmin, xmax = simulation_plot.get_xlim()
    ymin, ymax = simulation_plot.get_ylim()
    threshold = 0.01                                # set threshold percentage 
    dX = (xmax - xmin) * threshold                  # get the threshold x value 
    dY = (ymax - ymin) * threshold                  # get the threshold y value 
    thresDist = math.sqrt((dX**2 + dY **2))         # calculate the threshold distance 
    mouse_pos = vector(event_.xdata, event_.ydata)
    distance = planet_.position >> mouse_pos 
    if distance < thresDist: 
        return True 
    else: 
        return False 

def on_click(event):
    if event.inaxes == False or event.xdata ==None or event.ydata == None:                       # check if the mouse is outside of the graph, if so, stop the function 
        return None 
    global dragging 
    global paused 
    global selected
    if event.button == 1: 
        for i in planet_list:                           # iterate over the planet list 
            if checkDist(i, event):
                if dragging == i:                            # and if the planet is already being dragged 
                    dragging = None                          # remove it from being dragged 
                    redraw()
                else: 
                    dragging = i                        # otherwise set it to being dragged 
                    #anim.pause()                                    # pause the animation 
                    paused = True
    if event.button == 3:                       # if it is a right click 
        for i in planet_list: 
            if checkDist(i,event):              # go over each planet and check if it is close 
                selected = i 
                mass = "{:e}".format(i.mass)
                velocity = i.v_half_step       
                xvel = "{:e}".format(velocity.x)
                yvel = "{:e}".format(velocity.y)               # if close enough, fetch its attributes in scientific form 

                mass = mass.split("e")                         # split it into mantissa and exponent 
                massMantissa = mass[0]
                massExpo = StringVar(sidebar_frame, mass[1])
                mass_scale.set(float(massMantissa))              # write it onto the widigets 
                massExpo_spinbox.config(textvariable=massExpo)

                xvel = xvel.split("e")                         # split it into mantissa and exponent 
                xMantissa = xvel[0]
                xExpo = StringVar(sidebar_frame, xvel[1])
                hvel_scale.set(float(xMantissa))                 # write it onto the widgets 
                hvelExpo_spinbox.config(textvariable=xExpo) 

                yvel = yvel.split("e")                         # split it into mantissa and exponent 
                yMantissa = yvel[0]
                yExpo = StringVar(sidebar_frame, yvel[1])
                vvel_scale.set(float(yMantissa))                  # write it onto the widgets 
                vvelExpo_spinbox.config(textvariable=yExpo)
                
def on_move(event): 
    global dragging      
    if dragging != None:                                             # check if we have a planet being dragged 
        dragging.position.x = event.xdata                            # set its position to be the mouse's x position 
        dragging.position.y = event.ydata                            # set its position to be the mouse's y position 
        xVals = [i.position.x for i in planet_list]                  # fetch the x position of each planet 
        yVals = [i.position.y for i in planet_list]                  # fetch the y position of each planet
        redraw()

simulation_canvas.callbacks.connect("motion_notify_event", on_move)
simulation_canvas.callbacks.connect("button_press_event", on_click)

#-----------------------------------------------------------------------------------------------------------------------------updating values for gravitational constant and time step size






#--------------------------------------------------------------------------------------------------------------------------------------main loop
while True: 
    try:
        main_window.update() #---------------------------------------run the main loop, this allows me to handle widget interactions 
        if not paused:
            for i in range(frames_): 
                simulate(planet_list, grav_const, time_step_size) #-----------update the position of all the planets 
            redraw()
    except: 
        print("run into an unexcepted issue, quitting...")
        quit()


