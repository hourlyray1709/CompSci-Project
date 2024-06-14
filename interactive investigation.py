from matplotlib import pyplot as plt 
from matplotlib.figure import Figure 
from tkinter import * 
from tkinter import ttk 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

window = Tk()                                            # create a window 
fig = Figure()                                           # create a figure 
plot = fig.add_subplot()                                 # create a plot 
plot.scatter([0,10,30], [70,50,10])                      # some random data to plot 
canvas = FigureCanvasTkAgg(figure=fig, master=window)    # creata a canvas to plot the data on 
canvas.draw()                                            # draw the canvas 
canvas.get_tk_widget().grid(row=0, column=0)             # pack it into the window using grid function 

def click_handler(event): 
    print(event.x)
    print(event.y)

window.bind("<Button-1>", click_handler)



window.mainloop()                                        # call the main loop 