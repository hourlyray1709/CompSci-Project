from matplotlib import pyplot as plt 
from matplotlib.figure import Figure 
from tkinter import * 
from tkinter import ttk 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import math 

class dataPoint: 
    def __init__(self, x,y, dragged=False): 
        self.x = x 
        self.y = y 
        self.dragged = dragged

dataPoint1 = dataPoint(0,70)
dataPoint2 = dataPoint(10,50)
dataPoint3 = dataPoint(30,10)
dataPoints = [dataPoint1, dataPoint2, dataPoint3]
xVals = [i.x for i in dataPoints]
yVals = [i.y for i in dataPoints]
window = Tk()                                            # create a window 
width = 700 
height = 700
window.geometry("{}x{}".format(str(width), str(height)))
fig = Figure()                              # create a figure 
plot = fig.add_subplot()                                 # create a plot 
plot.scatter(xVals, yVals)                      # some random data to plot 
canvas = FigureCanvasTkAgg(figure=fig, master=window)    # creata a canvas to plot the data on 
canvas.draw()                                            # draw the canvas 
canvas.get_tk_widget().grid(row=0, column=0)                             # pack it into the window using grid function 

mouse = [0,0] 

invert = plot.transData.inverted() 
ylim = plot.get_ylim()
ylim = ylim[1]-ylim[0]
print(ylim)

def distance_from(pointA, pointB):
    dX = pointB[0] - pointA[0]
    dY = pointB[1] - pointA[1]
    return math.sqrt(dX**2 + dY**2)



def on_move(event):                                 
    changed = False 
    for i in dataPoints:                           # iterate over all the data points 
        if i.dragged == True:                      # if it is currently being dragged 
            i.x = event.xdata                      # update the position of the data point 
            i.y = event.ydata 
            changed = True                         # record that we have changed something 
     
    if changed: 
        plot.clear()
        xVals = [i.x for i in dataPoints]
        yVals = [i.y for i in dataPoints]
        plot.scatter(xVals, yVals)                      # some random data to plot  
        canvas.draw()                                            # draw the canvas 
        canvas.get_tk_widget().grid(row=0, column=0)                             # pack it into the window using grid function 

def on_click(event): 
    if event.inaxes:                                                        # check if mouse is within the limits of the graph 
        print("clicked")
        for i in dataPoints:                                                # iterate over the datapoints
            distance = distance_from([event.xdata, event.ydata], [i.x, i.y]) 
            if  distance < 1: # if the distance between the mouse and the data point is small, do this 
                print("toggled")
                if i.dragged == True:                                       # if currently being dragged, stop it from being dragged 
                    i.dragged = False 
                    print(i.dragged)
                else:
                    i.dragged = True                                        # otherwise, turn dragged to true 
                    print(i.dragged)
                    

canvas.callbacks.connect('motion_notify_event', on_move)
canvas.callbacks.connect('button_press_event', on_click)

window.mainloop()                                        # call the main loop 5