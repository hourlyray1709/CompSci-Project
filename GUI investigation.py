from tkinter import * 
from tkinter import ttk 
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

pos_var = "" 
vel_var = "" 
min_var = "" 
max_var = ""

window = Tk() #-----------creates an empty window 
notebook = ttk.Notebook(window)
notebook.pack()
tab1 = ttk.Frame(notebook)
tab2 = ttk.Frame(notebook)
notebook.add(tab1,text="tab1")
notebook.add(tab2,text="tab2")

position_label = Label(tab1, text="enter position") #-----create a label that shows the text 
position_label.grid(row=0, column=0)
position_field = Entry(tab1, textvariable=pos_var) #-----------creates a field to collect user input 
position_field.grid(row=0, column=1)
velocity_label = Label(tab2, text="enter velocity")
velocity_label.grid(row=1, column=0)
velocity_field = Entry(tab2, textvariable=vel_var) #---------create another field 
velocity_field.grid(row=1,column=1)

scrollMax = 100
scrollMin = -100
scrollbar = Scale(tab1, orient=HORIZONTAL, from_ = scrollMin, to = scrollMax)
scrollbar.grid(row=2,column=0)

popup = Menu(window) #-------------------------------------create a new menu 
popup.add_command(label="Change position") #---------------add a function to it 
popup.add_command(label="Change velocity") 
popup.add_command(label="Change acceleration")

def popup_menu(event): 
    popup.tk_popup(event.x_root, event.y_root, 0) #-------define it to popup at the mouse location 

window.bind("<Button-3>", popup_menu) #-------------------bind it to right click 

y_values = [i**2 for i in range(0,100)] #----------------create data to plot 
fig = Figure((5,5), 100) #-------------------------------create a figure on which to display the data 
plot = fig.add_subplot() #-------------------------------plot the data 
plot.plot(y_values)
canvas = FigureCanvasTkAgg(fig, master=tab1) #-----------create a canvas 
canvas.draw()
canvas.get_tk_widget().grid(row=2,column=0) #------------pack it into tab1
toolbar_frame = Frame(tab1)
toolbar = NavigationToolbar2Tk(canvas, toolbar_frame) #-----------create toolbar for manipulating the graph 
toolbar_frame.grid(row=3,column=0)
toolbar.update() #---------------------------------------not sure what this does 
canvas.get_tk_widget().grid(row=2, column=0) #-----------pack the toolbar into the graph



entry_value = { #------------------------------------initialise a dictionary that holds entry-value pairs 
    position_field:"", 
    velocity_field:"",
    scrollbar:"",
}

def fetch_entry_values(event=None): 
    entries = [i for i in entry_value] #-------------fetch all entry objects for which we need to find the value of 
    for i in entries: 
        entry_value[i] = i.get() #-------------------fetch the values of those entry objects and map it in the dictionary 
    print(entry_value)
    return entry_value #-----------------------------return the dictionary 

window.bind("<Return>", fetch_entry_values)

window.mainloop() #----------------------------------------the main loop 
