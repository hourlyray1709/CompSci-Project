import tkinter
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib import pyplot as plt, animation
import numpy as np

# importing the relevant libraries 

main_window = tkinter.Tk()
main_window.wm_title("Plotting investigation")

# create a main window 

fig = plt.Figure(dpi=100)                         #-------create a figure 
ax = fig.add_subplot(xlim=(0,2), ylim=(-1,1))   #-------add a plot to the figure 
line, = ax.plot([], [], lw=1)                     #-------create an emtpy line 

canvas = FigureCanvasTkAgg(fig, master=main_window) #-------turn the matplotlib figure into a tkinter object 
canvas.draw() 

toolbar = NavigationToolbar2Tk(canvas, main_window, pack_toolbar=False) #-----turn the matplotlib toolbar into a tkinter object 
toolbar.update()

toolbar.grid(row=1, column=0)                     #-----------pack the toolbar inside of the tkinter window 
canvas.get_tk_widget().grid(row=0, column=0)      #-----------pack the canvas inside of the tkinter window 

myplot = plt.scatter([5,23,40],[100,6,2])
myplot.pack()

tkinter.mainloop()


