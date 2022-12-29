import pandas as pd
from matplotlib import pyplot as plt
from scipy.integrate import quad
import numpy as np


def draw_graph(lambda_function, energy):

    x = np.arange(0, 4, 0.1)
    y = lambda_function(x)

    fig = plt.figure()

    ax = fig.add_subplot(111)

    ax.plot(x,y)
    ax.set_title(f"Total energy expenditure: {energy} J")
    ax.set_xlabel("Travel distance in mm")
    ax.set_ylabel("Force in g")

    plt.show()
    return


def get_switch_data():

    switch_name = input('Name of the switch: ')

    # check if switch exists in the database, if not ask everything else

    db = pd.read_csv('./switches.csv', delimiter=';', index_col=False)

    db_filtered = db[db.name == switch_name]

    if db_filtered.shape[0] == 1:
        print("Switch found in the database. Giving data...")
        entry_array = db_filtered.to_numpy()[0]

        x1 = entry_array[1]
        y1 = entry_array[2]
        x2 = entry_array[3]
        y2 = entry_array[4]
    else:         
        print("Switch not found in the database. Creating entry...")
        x1 = float(input("Point of actuation in mm: "))
        y1 = float(input("Actuation force in g: "))
        x2 = float(input("Point of bottom out in mm: "))
        y2 = float(input("Bottom out force in g: "))

        new_entry_data = {'name': [switch_name], 'af_x': [x1], 'af_y': [y1], 'bof_x': [x2], 'bof_y': [y2] }
        new_entry = pd.DataFrame(data=new_entry_data)
        new_db = pd.concat([db, new_entry], axis=0)

        new_db.to_csv('./switches.csv', sep=';', index=False)

    # create the function (mx + b)

    m = (y2 - y1) / (x2 - x1)

    b = y1 - m * x1

    f = lambda x:m*x+b

    # integrate over function to get the expended energy

    energy = quad(f,0,x2)[0]

    # draw function and show energy

    draw_graph(f, energy)

if __name__ == '__main__':
    get_switch_data()