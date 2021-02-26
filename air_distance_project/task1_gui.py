# Import libraries
import os
import pandas as pd
import random
import numpy as np
from math import radians, degrees, sin, cos, asin, acos, sqrt
import tkinter as tk
from tkinter import *
from tkinter import ttk
from random import uniform

# Setting the current working directory - so code is runnable from another PC
cwd = format(os.getcwd())

# Reading in csv file
places = pd.read_csv(cwd + '\places.csv')



# Parent window for GUI - borrowed AirMine logo
main_window = tk.Tk()
main_window.iconphoto(main_window, PhotoImage(file=cwd + '\logo_icon.png'))
main_window.title("Show Air Distances")
main_window.geometry('400x300')
main_image = PhotoImage(file=cwd + '\logo.png')

# Creat canvas to place buttons and text
canvas1 = tk.Canvas(main_window, width = 400, height = 300, relief = 'raised')
canvas1.pack()

# Put image on canvas
canvas1.create_image(155,20, anchor=NW, image = main_image)

# Create entry window for user input
entry1 = tk.Entry (main_window) 
canvas1.create_window(200, 200, window=entry1)

# Create label telling user what to do
label2 = tk.Label(main_window, text=str("Type the number of locations you want to randomly select."+"\n"+ "(Leave blank to use places.csv)"))
label2.config(font=('helvetica', 10))
canvas1.create_window(200, 150, window=label2)


# Function to get pairs
def get_pairs(n):

    if n == "":
        
        # Read in places.csv and assign to global space for later use
        cwd = format(os.getcwd())
        global places
        places = pd.read_csv(cwd + '\places.csv')

        listed_locations = places["Name"].tolist()

    else:
        listed_locations = get_coords(n)


    all_pairs = [[a, b] for a in listed_locations  
                    for b in listed_locations if a != b]

    # Sorting all pairs alphabetically
    sorted_pairs = [sorted(i) for i in all_pairs]

    # Using an append function to only store unique pairs
    unique_pairs = []
    for j in sorted_pairs:
        if j not in unique_pairs:
            unique_pairs.append(j)
    
    return(unique_pairs)




# Function to get great circle distance (from Pete Houston @ Medium)
def great_circle(lat1, lon1, lat2, lon2):

    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # Using approximate radius of the earth at 6371km 
    return 6371 * (
        acos(sin(lat1) * sin(lat2) + cos(lat1) * cos(lat2) * cos(lon1 - lon2))
    )


# Defining a function to generate n unique random co-ordinates (rounded to 5 decimal places for consistency with places.csv)
def get_coords(n):

    # Empty list to store results
    unique_locs = []

    while len(unique_locs) < n:

        # Create a random [latitude,longitude]
        random_coord = [round(uniform(-90, 90),5), round(uniform(-180,180), 5)]

        if random_coord not in unique_locs:
            unique_locs.append(random_coord)
    
    return(unique_locs)


# Function to create the table of air distances between locations
def get_results(n, pairs):
    if n == '':
        data = {
                'Location1' : [l[0] for l in pairs],
                'Location2' : [l[1] for l in pairs],

                # Apply great circle function to the pair of locations - need to look up coords in places dataframe            
                'AirDistance': [ great_circle(
                                            places.loc[places["Name"] == l[0],"Latitude"], # latitude of location 1
                                            places.loc[places["Name"] == l[0], "Longitude"], # longitude of location 1
                                            places.loc[places["Name"] == l[1], "Latitude"], # latitude of location 2
                                            places.loc[places["Name"] == l[1], "Longitude"]) # longitude of location 2
                                            for l in pairs
                                ]
                }
    else:
        data = {
                'Location1' : [str(l[0]) for l in pairs],
                'Location2' : [str(l[1]) for l in pairs],
                # Apply great circle function to the pair of locations
                'AirDistance': [ great_circle(
                                            l[0][0],
                                            l[0][1],
                                            l[1][0],
                                            l[1][1])
                                            for l in pairs
                                ]
            }

    data = pd.DataFrame(data)

    return(data)



# Function for "Go" button - An extended function of get_n() to run everything off tkinter GUI
def get_n():

    # Enabling reset button
    button2['state'] = NORMAL

    # Making the text label a global variable
    global label1

    # Setting the range between 2 and the maximum number of locations as we cannot find the distance between 1 or less locations and cannot have more locations than all those that exist
    user_input = entry1.get()

    # Defaulting to all locations in file if no argument is given
    if user_input=="":
        label1 = tk.Label(main_window, text= "Output showing locations from the file places.csv")
        canvas1.create_window(200, 290, window=label1)
        button1['state'] = DISABLED


        # No input set - places.csv will be used
        n = ""
        
        

    # Using a try-except to identify illogical inputs - asking the user to respecify n
    else:
        try:
            user_input = int(user_input)

            # Input must be greater than 1 - there is no air distance between one location and itself
            if user_input > 1:
                
                label1 = tk.Label(main_window, text= "Output showing " + str(user_input) + " locations.")
                canvas1.create_window(200, 290, window=label1)
                button1['state'] = DISABLED

                # n is the maximum possible
                n = user_input

            
            else:
                # else if not a valid integer
                label1 = tk.Label(main_window, text="Please select an integer greater than 1.")
                canvas1.create_window(200, 290, window=label1)
                button1['state'] = DISABLED
                return(None)



        except:
            # If not able to be converted to an integer
            button1['state'] = DISABLED
            label1 = tk.Label(main_window, text="Not an integer. Please select an integer greater than 1.")
            canvas1.create_window(200, 290, window=label1)
            return(None)


    # Continuing if n is set
        
    # Getting all unique pairs
    pairs = get_pairs(n=n)


    # Getting the results
    results_table = get_results(n=n,pairs=pairs)


    # Sort in ascending order
    results_table = results_table.sort_values(by = "AirDistance", ascending=True)


    # Round distances to one decimal place
    results = results_table
    results.AirDistance = round(results.AirDistance, 1)


    # Make neater
    results = results.reset_index(drop=True)



    # Got results - now to print to GUI

    
    # Will show results in a new window with a vertical scrollbar(from Codemy.com Tkinter GUI Tutorial #96)
    top = Tk()
    top.title("Output")
    top.geometry("600x600")

    # Create mainframe to hold everything
    frame = Frame(top)
    frame.pack(fill=BOTH, expand=1)

    # Create canvas which will hold scrollbar
    canvas = Canvas(frame)
    canvas.pack(side=LEFT, fill=BOTH, expand=1)

    # Create scrollbar
    scrollbar = ttk.Scrollbar(frame, orient = VERTICAL, command = canvas.yview)
    scrollbar.pack(side=RIGHT, fill=Y)

    # Configure canvas to work with scrollbar
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

    # Create new frame in canvas to put data
    inner_frame = Frame(canvas)
    canvas.create_window((0,0), window=inner_frame, anchor="nw")


    # Print results to inside frame
    for c, name in enumerate(results.columns):
        Label(inner_frame, text = name, font=("Calibri", 10)).grid(row=0, column = c, sticky = 'w', padx=(10,10))
    for i in range(0,results.shape[0]):
        line = results.iloc[i,:]
        record = list(line)
        for j in range(0,len(record)):
            rec = record[j]
            Label(inner_frame, text=rec, font=("Calibri", 10)).grid(row=i+1, column=j, sticky = 'w', padx=(10,10))

    # Printing the final line
    
    # Find average air distance - and round to 1 decimal place
    average = round(results_table["AirDistance"].mean(), 1)

    # Squaring differences from the mean as some differences will be negative
    squared_differences = np.square( (np.array(results_table["AirDistance"]) - average) )
    results_table["Squared_differences"] = squared_differences

    # Finding the lowest squared difference - the closest to the mean
    closest_to_mean = results_table[results_table["Squared_differences"] == results_table.Squared_differences.min()]

    # Adding spacer at the beginning of final line
    Label(inner_frame, text = "\n").grid(row=results.shape[0]+2, columnspan=3, sticky = 'w', padx=(10,10))


    # Final line
    fl = str("Average distance: " +
             str(average) + " km." +
             " Closest pair: " +
             str(closest_to_mean.iloc[0,0])+ " - " +
             str(closest_to_mean.iloc[0,1])+ " " +
             str(round(closest_to_mean.iloc[0,2],1)) + " km.")

    
    
    # Adding in last line (average and closest)
    Label(inner_frame, text = fl, font = ("Calibri", 10)).grid(row=results.shape[0]+3, columnspan=3, sticky = 'w', padx=(10,10))

    # Adding spacer at the end
    Label(inner_frame, text = "\n\n").grid(row=results.shape[0]+4, columnspan=3, sticky = 'w', padx=(10,10))
    
    top.mainloop()



# Creating function for the reset button if user wants to generate more locations
def reset():
    button2['state'] = DISABLED
    label1.destroy()
    entry1.delete(0,tk.END)
    button1['state'] = NORMAL


# Creating the "Go" button
button1 = tk.Button(text='Get Air Distances', command=get_n, bg='#2431ab', fg='white', font=('helvetica', 9, 'bold'))
canvas1.create_window(170, 240, window=button1)

# Creating the "Reset" button
button2 = tk.Button(text='Reset', command=reset, font=('helvetica', 9, 'bold'))
canvas1.create_window(260, 240, window=button2)

# Closing end of window loop
main_window.mainloop()




