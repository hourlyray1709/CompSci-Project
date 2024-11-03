#import the classes I need 

from vector_class import vector 
from planet_class import planet, find_resultant_force
from simulate import simulate 
from queue_class import queue 
import matplotlib
from tkinter import * 
from tkinter import ttk
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib import pyplot as plt, animation 
from functools import partial 
import math 
import numpy as np 
from matplotlib import cm
import scipy.stats as stats 
from matplotlib.collections import LineCollection
from matplotlib.lines import Line2D
#-----------------------------------------------------------------------------------------------------------------------Core variables 
time_step_size = 3000
max_trail_length = int(50 * (1000/time_step_size)) #-------------------------how many past positions to keep track of when generating a trail of the planets 
planet1 = planet(position=vector(0,0), mass=1.989*10**30, velocity=vector(0,10000), past_positions=queue([], max_trail_length))
planet2 = planet(position=vector(250*10**8, 0), mass=5.972*10**24, velocity=vector(0, 35000), past_positions=queue([], max_trail_length))
planet3 = planet(position=vector(-250*10**8, 0), mass=10.972*10**24, velocity=vector(0, -35000), past_positions=queue([], max_trail_length))
planet4 = planet(position=vector(-500*10**8, 0), mass=5.972*10**24, velocity=vector(0, -50000), past_positions=queue([], max_trail_length))
planet5 = planet(position=vector(-125*10**8, 0), mass=3.20*10**24, velocity=vector(0, -50000), past_positions=queue([], max_trail_length))
planet6 = planet(position=vector(5*10**10, 0), mass=10.20*10**28, velocity=vector(0, 25000), past_positions=queue([], max_trail_length))
grav_const = 6.67430 * 10 ** -11 
grav_expo = -11
planet_list = [planet1, planet2, planet3, planet4, planet5, planet6]
#planet_list = []
update_every = 120000 #------------------------------each frame will represent this number in seconds 
frames_ = int(update_every / time_step_size)
fps = 24
paused = False  
dragging = None 
tabPause = True  
selected = None
vectorField_toggle = False 

init_attributes = []
for i in planet_list: 
    attributes = [i.position, i.mass, i.velocity, i.v_half_step, i.acceleration]      # fetch all starting attributes 
    init_attributes.append(attributes)



#-----------------------------------------------------------------------------------------------------------------------Core variables 

#--------------------------------------------------------------------------------------------------------------------GUI stuff 
main_window = Tk()
main_window.title("Gravity Simulation")
main_window.configure(background="grey", padx=0, pady=0)
style = ttk.Style()
style.configure("TFrame", background="grey")

notebook = ttk.Notebook(main_window, )
notebook.pack() #------------------------------initiate notebook for tab control 

main_tab = ttk.Frame(notebook, style="TFrame") #---------------create tab for main window 
settings_tab = ttk.Frame(notebook, style="TFrame") #-----------create tab for settings 
notebook.add(main_tab, text="Main Window")
notebook.add(settings_tab, text="Settings") #--add tabs to notebook 

simulation_figure = Figure(figsize=(8,8), dpi=100, facecolor="grey")
max_val = 10**12
simulation_plot = simulation_figure.add_subplot(xlim=(-max_val, max_val), ylim=(-max_val, max_val))
simulation_plot.set_facecolor("black")
dots = simulation_plot.scatter([],[])
plt.grid()
# plot something 
simulation_canvas = FigureCanvasTkAgg(simulation_figure, master=main_tab) #------create the canvas 
simulation_canvas.draw()
simulation_canvas.get_tk_widget().grid(row=0,column=0) #-------------------put the simulation plot into tkinter 
simulation_toolbar_frame = ttk.Frame(main_tab, style="TFrame")
simulation_toolbar = NavigationToolbar2Tk(simulation_canvas, simulation_toolbar_frame) #---create the toolbar 
simulation_toolbar_frame.grid(row=1,column=0) #--------------------------------------------pack it below the plot
simulation_toolbar.update()
simulation_canvas.get_tk_widget().grid(row=0,column=0) #-----------------------------------pack it into the tab

t_step_size_label = Label(settings_tab, text="Time Step Size: ", bg="grey") #-------------------------create a text label 
t_step_size_label.grid(row=0, column=0)
t_step_scale = Scale(settings_tab, orient=HORIZONTAL, from_=1, to=100000, resolution=0.01, bg="grey", troughcolor="grey") #------------------------------------create a scroll bar 
t_step_scale.set(time_step_size)
t_step_scale.grid(row=0,column=1)

g_const_label = Label(settings_tab, text="Grav. Constant Value: ", bg="grey") #-----------------------create a label 
g_const_label.grid(row=1,column=0)
g_const_scale = Scale(settings_tab, orient=HORIZONTAL, from_ = 0, to = 9.99, resolution=0.01, bg="grey", troughcolor="grey") #------------create a scrollbar 
g_const_scale.set(grav_const / 10 ** grav_expo)
g_const_scale.grid(row=1,column=1)

grav_expo_str = StringVar(main_window)
grav_expo_str.set(grav_expo)
g_expo_label = Label(settings_tab, text="Grav. Exponent: ", bg="grey") #------------------------------create a abel 
g_expo_label.grid(row=1, column=2)
g_expo_spinbox = Spinbox(settings_tab, from_ = -100, to=100, state="readonly", increment=1, textvariable=grav_expo_str, bg="grey") #-------------create a spinb
g_expo_spinbox.grid(row=1,column=3)

def toggleVectorField(): 
    global vectorField_toggle 
    vectorField_toggle = not vectorField_toggle

vectorField_label = Label(settings_tab, text="Toggle vector field: ", bg="grey")
vectorField_label.grid(row=2, column=0)
vectorField_button = Button(settings_tab, text="Turn Vector Field On/Off", command=toggleVectorField, bg="grey")
vectorField_button.grid(row=2, column=1)

def createPlanet():                                                                                       # code to create a new planet 
    global paused
    global dragging 
    global init_attributes
    if dragging == None: 
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
        paused_label.configure(text="paused", bg="red")
        #anim.pause()                                                                                          # pause the animation 
        newPlanet = planet(position=vector(1,1), mass=mass, past_positions=queue([], max_trail_length), velocity=vel)     # create a new planet using the params
        attributes = [newPlanet.position, newPlanet.mass, newPlanet.velocity, newPlanet.v_half_step, newPlanet.acceleration]
        init_attributes.append(attributes)                                                                    # handle reset for new planet 
        dragging = newPlanet                                                                                  # set it to being dragged 
        planet_list.append(newPlanet)                                                                         # add it to the planet list for sim 

def deletePlanet(): 
    global dragging 
    global planet_list 
    global selected
    if dragging != None:                                              # if dragging a valid planet 
        #anim.pause()                                                  # pause the animation 

        index = planet_list.index(dragging)                            # fetch the position the planet is in
        init_attributes.pop(index)                                     # delete its attributes which are used when resetting the simulation 

        planet_list = [i for i in planet_list if i != dragging]       # remove the planet from the list of planets 
        dragging = None 
        redraw()
    if selected != None: 

        index = planet_list.index(selected)                            # fetch the position the planet is in 
        init_attributes.pop(index)                                     # delete its attributes which are used when resetting the simulation 

        planet_list = [i for i in planet_list if i != selected]
        selected = None 
        redraw()


def editPlanet():
    global dragging
    global selected 

    massMantissa = float(mass_scale.get()) 
    massExpo = float(massExpo_spinbox.get())
    
    xVelMantissa = float(hvel_scale.get())
    xVelExpo = float(hvelExpo_spinbox.get())

    yVelMantissa = float(vvel_scale.get())
    yVelExpo = float(vvelExpo_spinbox.get())             # fetch 5all values 

    selected.mass = massMantissa * 10 ** massExpo 
    selected.v_half_step = vector(xVelMantissa * 10 ** xVelExpo,       yVelMantissa * 10 ** yVelExpo)     # edit the planet currently selected

def calcForce(x,y): 
    simPlanet = planet(vector(x,y), 10**1)
    resForce = vector(0,0)

    for i in planet_list: 
        if i.position.x == None or i.position.y == None: 
            continue  
        force = simPlanet.find_force(i, grav_const)
        resForce += force 

    return resForce 

def checkPos(x=None,y=None): 
    xmin, xmax = simulation_plot.get_xlim()
    ymin, ymax = simulation_plot.get_ylim()
    xmin, xmax = int(xmin)*2, int(xmax)*2
    ymin, ymax = int(ymin)*2, int(ymax)*2
    dif = (xmax - xmin) * 0.01
    for i in planet_list: 
        if x != None: 
            if abs(i.position.x - x) < dif: 
                if y != None: 
                    if abs(i.position.y -y) < dif: 
                        return False 
        if x == None and y == None: 
            return False 
    return True 

def vectorField(density): 
    xmin, xmax = simulation_plot.get_xlim()                                 # get the bounds of my graph 
    ymin, ymax = simulation_plot.get_ylim()
    dif = xmax - xmin                                                       # get the length of the graph 
    xmin, xmax, ymin, ymax = int(xmin), int(xmax), int(ymin), int(ymax)
    step = dif / density                                              
    x = np.arange(xmin, xmax, step)                                # x-y coords for the arrows 
    y = np.arange(ymin, ymax, step)
    
    X,Y = np.meshgrid(x,y)                                                  # make a meshgrid 
    xForceArr = [] 
    yForceArr = [] 
    sizes = [] 
    maxForce = 0 
    colors = [] 
    for y_ in y: 
        for x_ in x: 
            force = calcForce(x_,y_)                                        # calculate the vector force experienced by a planet at that location 
            if force.size > maxForce: 
                maxForce = force.size 
            xForce = force.x / force.size
            yForce = force.y / force.size                                             # resolve components 
            xForceArr.append(xForce)                                        # save it 
            yForceArr.append(yForce)
            sizes.append(force.size)
    for y_ in y: 
        for x_ in x: 
            force = calcForce(x_,y_) 
            size = force.size
            percentile = stats.percentileofscore(sizes, size, kind="rank")
            colour = 1 * percentile / 100 
            colors.append((colour, colour, colour, colour))

    xForceArr = np.array(xForceArr)
    yForceArr = np.array(yForceArr)
    u = xForceArr.reshape(X.shape)
    v = yForceArr.reshape(Y.shape)                                          # use the components to find direction and size 

    simulation_plot.quiver(X, Y, u, v, color=colors, angles="xy")                          # plot the quiver plot 


            
    
    
def redraw(): 
    xlim = simulation_plot.get_xlim() 
    ylim = simulation_plot.get_ylim()                          # get the x and y limits of the graph 
    simulation_plot.clear() 
    simulation_plot.set_xlim(xlim)
    simulation_plot.set_ylim(ylim)                # fetch the positions of the planets 

    xPositions = [] 
    yPositions= []
    colours = [] 
    linecol = []
    linecolor = []                               # create a list of the line's data 

    masses = [math.log10(i.mass) for i in planet_list]
    marker_sizes = [] 
    baseAmt = 2
    for i in planet_list: 
        trail = []
        for k in i.past_positions.arr: 
            trail.append((k.x, k.y))            # add the positions to the line data 

        xPositions.append(i.position.x)
        yPositions.append(i.position.y)
        colours.append(i.colour)
    
        if len(trail) != 0: 
            linecol.append(trail)
            linecolor.append(i.colour)         # save info about the colours of the line 

        mass_percentile = stats.percentileofscore(masses, math.log10(i.mass), "rank")
        marker_sizes.append(baseAmt * mass_percentile)

    linecol = LineCollection(linecol, colors=linecolor)       # create a line collection 
    simulation_plot.add_collection(linecol)                   # draw all lines using one function call 
    simulation_plot.scatter(xPositions, yPositions, c=colours, s=marker_sizes)
    if vectorField_toggle:
        vectorField(20)
    simulation_canvas.draw() 
    simulation_canvas.get_tk_widget().grid(row=0, column=0)    # draw the planets 


sidebar_frame = Frame(main_tab, bg="grey")                                                                           # create a collection that holds everything in the side menu 
sidebar_frame.grid(row=0, column=1)                    

title = Label(sidebar_frame, text="Planet Editor", bg="grey")                                                        # create a text title for the side menu
title.grid(row=0, column=0)

mass_label = Label(sidebar_frame, text="Mass: ", bg="grey")                                                          # GUI for adjusting mass 
mass_label.grid(row=1, column=0)
mass_scale = Scale(sidebar_frame, orient=HORIZONTAL, from_=1, to=9.999, resolution=0.001, bg="grey", troughcolor="grey")
mass_scale.set(5)
mass_scale.grid(row=1, column=1)

massExpo_label = Label(sidebar_frame, text="Mass Exponent: ", bg="grey")
massExpo_label.grid(row=1, column=2)
massExp_strVar = StringVar(sidebar_frame, "23")
massExpo_spinbox = Spinbox(sidebar_frame, from_=-100, to=100, state="readonly", increment=1, textvariable=massExp_strVar, bg="grey")
massExpo_spinbox.grid(row=1, column=3)

velMin = -9.99 
velMax = 9.99 
velRes = 0.01

hvel_label = Label(sidebar_frame, text="Horizontal Velocity: ", bg="grey")                                           # GUI for adjusting velocity in x axis 
hvel_label.grid(row=2,column=0)
hvel_scale = Scale(sidebar_frame, orient=HORIZONTAL, from_=velMin, to=velMax, resolution=velRes, bg="grey",troughcolor="grey")
hvel_scale.grid(row=2, column=1)
hvelExpo_label = Label(sidebar_frame, text="Horizontal Velocity Exponent: ", bg="grey")
hvelExpo_label.grid(row=2, column=2)
hvelStringVar = StringVar(sidebar_frame, "0")
hvelExpo_spinbox = Spinbox(sidebar_frame, from_=-100, to=100, state="readonly", increment=1, textvariable=hvelStringVar, bg="grey")
hvelExpo_spinbox.grid(row=2, column=3)

vvel_label = Label(sidebar_frame, text="Vertical Velocity: ", bg="grey")                                             # GUI for adjusting velocity in y axis 
vvel_label.grid(row=3, column=0)
vvel_scale = Scale(sidebar_frame, orient=HORIZONTAL, from_= velMin, to=velMax, resolution=velRes, bg="grey", troughcolor="grey")
vvel_scale.grid(row=3, column=1)
vvelExpo_label = Label(sidebar_frame, text="Vertical Velocity Exponent: ", bg="grey")
vvelExpo_label.grid(row=3, column=2)
vvelStringVar = StringVar(sidebar_frame, "0")
vvelExpo_spinbox = Spinbox(sidebar_frame, from_=-100, to=100, state="readonly", increment=1, textvariable=vvelStringVar, bg="grey")
vvelExpo_spinbox.grid(row=3, column=3)

create_planet_button = Button(sidebar_frame, text="Create Planet", command=createPlanet, bg="grey")                  # Button to create planet 
create_planet_button.grid(row=7, column=0)
edit_planet_button = Button(sidebar_frame, text="Edit Planet", command=editPlanet, bg="grey")
edit_planet_button.grid(row=7, column=1)
delete_planet_button = Button(sidebar_frame, text="Delete Planet", command=deletePlanet, bg='grey')                                        # Button to destroy planet 
delete_planet_button.grid(row=7, column=2)




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
        paused_label.configure(text="paused", bg="red")
        #anim.pause() 
    elif not tabPause:                                # if dont need to pause 
        grav_expo = float(g_expo_val) 
        grav_const = float(g_const_val) * 10 **float(grav_expo)
        time_step_size = time_step_val
        print(f"After tab change, variable values are {grav_const} ,  {grav_expo} ,  {time_step_size}")
        paused = False                                # unpause 
        paused_label.configure(text="playing", bg="green")
        #anim.resume() 

notebook.bind("<<NotebookTabChanged>>", tabChange)

def pause_func(): 
    global paused              # use the globally defined paused variable to check if the animation is currently paused
    if paused == True: 
        paused = False   
        paused_label.configure(text="playing", bg="green")    
    else: 
        paused = True          # swap the Boolean values, so when user presses it, it changes to true, and if it was true then it changes to false 
        paused_label.configure(text="paused", bg="red")
    #if paused == True: 
        #anim.pause()           # if needed to pause, pause it 
    #else:  
        #anim.resume()          # if needed to resume, resume it 
def reset(): 
    global planet_list 
    global init_planets 
    global anim 
    global selected
    global dragging
    for i in range(len(planet_list)): 
        planet_list[i].position = init_attributes[i][0]
        planet_list[i].mass = init_attributes[i][1] 
        planet_list[i].velocity = init_attributes[i][2]
        planet_list[i].v_half_step = init_attributes[i][3]
        planet_list[i].acceleration = init_attributes[i][4]
    selected = None 
    dragging = None


buttons_frame = Frame(main_tab, background="grey")
buttons_frame.grid(row=2, column=0)  

play_button = Button(buttons_frame, text="Play/Pause", command=pause_func)
play_button.grid(row=0,column=0)
reset_button = Button(buttons_frame, text="Reset simulation", command=reset)
reset_button.grid(row=0,column=1)
paused_label = Label(buttons_frame, text="playing", bg="green")
paused_label.grid(row=1, column=0)

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
                    paused_label.configure(bg="red")
                    paused_label.configure(text="paused")
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
    main_window.update() #---------------------------------------run the main loop, this allows me to handle widget interactions 
    if not paused:
        #for i in range(frames_): 
        simulate(planet_list, grav_const, time_step_size) #-----------update the position of all the planets 
        redraw()



