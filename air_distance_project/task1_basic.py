# Import libraries
import os
import pandas as pd
import random
import numpy as np
from math import radians, degrees, sin, cos, asin, acos, sqrt
from random import uniform



# Defining a function - allowing a user to specify n 
def get_n():

    # Ask for input
    user_input = input("Specify the number of coordinates to randomly select for which to report air distances. Press enter to confirm. Leave blank to skip this option:")

    # Defaulting to all locations in file if no argument is given
    if user_input=="":
        print("\n")
        print("Results showing all locations in places.csv.")
        return("")

    # Using a try-except to identify illogical inputs - asking the user to respecify n
    while True:
        try:
            user_input = int(user_input)

            # Input must be greater than 1 - there is no air distance between one location and itself
            if user_input > 1:
                print("\n")
                print("Results will show " + str(user_input) + " randomly selected locations.")
                return(user_input)

            else:
                # else if 1 or smaller
                user_input = input("Please select an integer greater than 1 or leave blank to skip. (Press enter to confirm):")


        except:
            # If not able to be converted to an integer
            user_input = input("Not an integer. Please select an integer greater than 1 or leave blank to skip. (Press enter to confirm):")



# Calling get_n to set n
n = get_n()




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




# Make pairs depending on the value of n
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



# Calling the function to get all unique pairs
pairs = get_pairs(n=n)



# Defining the great circle distance function (from Pete Houston @ Medium)
def great_circle(lat1, lon1, lat2, lon2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    
    # Using approximate radius of the earth at 6371km 
    return 6371 * (
        acos(sin(lat1) * sin(lat2) + cos(lat1) * cos(lat2) * cos(lon1 - lon2))
    )



# Create data frame of location-pair names and air distance between them
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
                'Location1' : [l[0] for l in pairs],
                'Location2' : [l[1] for l in pairs],
                # Apply great circle function to the pair of locations
                'AirDistance': [ great_circle(
                                            l[0][0],
                                            l[0][1],
                                            l[1][0],
                                            l[1][1])
                                            for l in pairs
                                ]
            }
    return(data)



results_table = pd.DataFrame(get_results(n=n,pairs=pairs))



# Sort table in ascending order
results_table = results_table.sort_values(by = "AirDistance", ascending=True)


# Round distances to one decimal place
results = results_table
results.AirDistance = round(results.AirDistance, 1)


# Print results from results table to command line without index
results = results.to_string(index=False)
# If no header required either run:
#results = results.to_string(index=False, header=False)

print("\n\n") #creating spacer for results table
print(results)
print("\n\n") # spacer




# Average distance and closest pair


# Find average air distance - and round to 1 decimal place
average = round(results_table["AirDistance"].mean(), 1)


# Squaring differences from the mean as some differences will be negative
squared_differences = np.square( (np.array(results_table["AirDistance"]) - average) )
results_table["Squared_differences"] = squared_differences


# Finding the lowest squared difference - the closest to the mean
closest_to_mean = results_table[results_table["Squared_differences"] == results_table.Squared_differences.min()]


# Printing final line
print("Average distance:", str(average), "km.",
      "Closest pair:",
      str(closest_to_mean.iloc[0,0]),"-",
      str(closest_to_mean.iloc[0,1]),
      str(round(closest_to_mean.iloc[0,2],1)), "km.", sep =" ")

print("\n") #spacer



