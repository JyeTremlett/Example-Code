# CITS2401 Lab 3 part 1
# Written by Jye Tremlett 22613744
# Created 2/5//2019
import numpy as np
import matplotlib.pyplot as plt

def microcar(instruct, actual):
    exp_hori, exp_vert, act_hori = np.array([]), np.array([]), np.array([])
    act_vert, exp_dist, act_dist = np.array([]), np.array([]), np.array([])
    def getmap(file): #inner method finds a map of distances in each direction for each file
        with open(file, "r") as file:
            distmap = {"N":0, "S":0, "E":0, "W": 0}
            for line in file:
                listline = line.rstrip().split(',')
                distmap[listline[0]] += (float(listline[1])*float(listline[2]))
        return(distmap)
    for file in instruct:
        filemap = getmap(file)
        exp_hori = np.append(exp_hori, abs(filemap['E'] - filemap['W']))
        exp_vert = np.append(exp_vert, abs(filemap['S'] - filemap['N']))
        exp_dist = np.append(exp_dist, filemap['E'] + filemap['W'] + filemap['N'] + filemap['S'])
    for file in actual:
        filemap = getmap(file)
        act_hori = np.append(act_hori, abs(filemap['E'] - filemap['W']))
        act_vert = np.append(act_vert, abs(filemap['S'] - filemap['N']))
        act_dist = np.append(act_dist, filemap['E'] + filemap['W'] + filemap['N'] + filemap['S'])
    return(exp_hori, exp_vert, act_hori, act_vert, exp_dist, act_dist)



def plotmicrocar(instruct, actual):
    (exp_hori, exp_vert, act_hori, act_vert, exp_dist, act_dist) = microcar(instruct, actual)
    #actual and expected distance bar plot  
    plt.subplot(2, 2, (1,2))
    plt.title("Actual And Expected Distances For Each Car")
    plt.xlabel("Car")
    plt.ylabel("Distance Travelled in Metres")
    names = []
    bar_width = 0.3
    n = len(exp_dist)
    for i in range(n):
        names.append("car" + str(i+1))
    ypos = np.arange(n)
    plt.xticks(ypos, names)
    for i in range(n):
        if(i == 0):
            plt.bar(ypos, exp_dist, bar_width, color = "g", label = "exp")
            plt.bar(ypos+bar_width, act_dist, bar_width, color = "b", label = "actual")
        else:
            plt.bar(ypos, exp_dist, bar_width, color = "g")
            plt.bar(ypos+bar_width, act_dist, bar_width, color = "b")
    plt.xticks(ypos + bar_width /2)
    plt.legend(loc = "upper left")

    #expected displacement scatter
    plt.subplot(2, 2, 3)
    plt.title("Expected Displacement For Each Car")
    plt.xlabel("Horizontal Displacement in Metres")
    plt.ylabel("Vertical Displacement in Metres")
    plt.xlim(0, 60)
    plt.ylim(0, 60)
    for i in range(len(exp_hori)):
        plt.scatter(exp_hori[i], exp_vert[i], label = "car" + str(i+1))
    plt.legend(loc = "upper left")
    
    #actual displacement scatter
    plt.subplot(2, 2, 4)
    plt.title("Actual Displacement For Each Car")
    plt.xlabel("Horizontal Displacement in Metres")
    plt.ylabel("Vertical Displacement in Metres")
    plt.xlim(0, 60)
    plt.ylim(0, 60)
    for i in range(len(act_hori)):
        plt.scatter(act_hori[i], act_vert[i], label = "car" + str(i+1))
    plt.legend(loc = "upper left")
        
    plt.show()
    
    
plotmicrocar(['exp1.csv','exp2.csv'],['act1.csv','act2.csv'])