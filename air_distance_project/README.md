# code_test
A python program to return the air distance between pairs of locations in a set of ___n___ randomly generated locations. The program also returns the average air distance between all location-pairs and highlights the location-pair with the air distance closest to this average.

Air distance is calculated by use of the Great Circle Distance formula where the radius is set to _6371 km_ (the approximate radius of Earth).

## Versions
There are two versions of the program which both achieve the same output.

The first version _task1_basic.py_ will execute solely in the command prompt or terminal. It will also require user input inside the command prompt / terminal.

The alternative version _task1_gui.py_ will execute as a Graphical User Interface in a new window when called. 

Both versions were written in Python v 3.7.2 (on a Windows PC) but should be compatible with any version of Python 3 or later.

## Required libraries
The packages required by **both versions** of the program are:
- os
- pandas
- random
- numpy
- math

The additional packages required by the **GUI version** are:
- tkinter

Please ensure your version of Python has these packages installed before using. (Visit https://packaging.python.org/tutorials/installing-packages/ for assistance). 


## How to use:
### To execute the plain version:
1. Clone the code_test repository on GitHub. (It is sufficient to have a local folder with task1_basic.py and places.csv only but the instructions will assume you have a cloned repo.)
2. Open the command prompt or terminal.
3. Navigate to the code_test folder using the command prompt or terminal (Visit http://www.openforis.org/tools/sepal/tutorials/using-the-command-line.html for assistance).
4. Type task1_basic.py.
5. Follow the prompts in the command prompt/terminal to display results.

### To execute the gui version:
1. Clone the code_test repository on GitHub if you have not already done so. 
2. Open the command prompt or terminal.
3. Navigate to the code_test folder using the command prompt or terminal.
4. Type task1_gui.py.
5. A new window should open called "Show Air Distances". Enter an integer greater than 1 in the entry box (or leave blank to demo) and click "Get Air Distances".
6. Output will be displayed in a new window.

