# CITS1401 Project 1: Computing World Happiness Index
# Written by Jye Tremlett 22613744
# Created 4/4/2019
import os.path

#Main function. Requests 3 inputs: filename, metric, and action. Throws an exception if the filepath does not
#result in a file, or if an invalid input is entered for metric and action
def main():
    filename = input("Input the name of the data file:\n\t")
    if(not os.path.isfile(filename)):
        return("Filename is incorrect")
        #I considered using try/catch but throwing an exception directly after the problematic input seemed better than
        #catching the error when the file is actually opened after the other inputs.    
    metric = input('Input the metric by which you would like to calculate from ("min", "mean", "median" or "harmonic_mean"):\n\t')
    if(metric != "min" and metric != "mean" and metric != "median" and metric != "harmonic_mean"):
            return("error: Check that inputs for metric are valid")
    action = input('Input "list" to return a list of countries ordered by the metric entered\nor input "correlation" to return the'
            ' correlation between the computed metric and the Life Ladder score\n\t')
    if(action != "list" and action != "correlation"):
        return("error: Check that inputs for action are valid")
    
    #process the file to eventually find fmetlist (country names with normalised metric values)
    #fprocessed and fnormalised include the name and Life ladder scores, which are unchanged
    file = open(filename,"r")
    minmax, fprocessed = getMinMax(file)
    file.close()
    fnormalised = getNormalised(minmax, fprocessed)
    fmetlist = getMetricList(fnormalised, metric)#check for valid metric inputs in this function
    #return either a correlation coefficient or a list of country-value pairs based off the entered metric
    return(doAction(action, fmetlist))






#processes the file to find the minimum and maximum values in each column, while also creating a copy of the file (fprocessed)
#represented by a list of lists, representing each line. Each of these lines have been, split into individual values, converted
#to floats where necessary, and stripped of newline characters. Where there is no data in a cell, the value is set to nan
#parameters: the file to be processed.
#returns: minmax, a 2D list containing a corresponding maximum and minimum for each column, and fprocessed, a copy of the file that is
#easier to process further.
def getMinMax(file):
    fprocessed = []
    #minmax is a list containing a list of the min (index 0) and max (index 1) for each of the 6 columns we need to consider in order     
    minmax = [[float('nan'),float('nan')],[float('nan'),float('nan')],[float('nan'),float('nan')],[float('nan'),float('nan')],
              [float('nan'),float('nan')],[float('nan'),float('nan')]]
    for line in file.readlines()[1:]:#change this
        linelist = line.rstrip().split(",")
        lprocessed = [linelist[0]] + [float(linelist[1])]
        for value in linelist[2:]:
            minmaxind = linelist.index(value)-2
            if(value != ""):
                value = float(value)
                if(not minmax[minmaxind][0] < value):#If the corresponding min or max is nan, if-statement body will always be executed
                    minmax[minmaxind][0] = value     
                elif(not minmax[minmaxind][1] > value):
                    minmax[minmaxind][1] = value
            else:
                value = float("nan")
                #I chose to use nan here to avoid an unnecessary if-statement (to catch None as suggested in the project 1 details)
                #during my normalise function
            lprocessed.append(value)
        fprocessed.append(lprocessed)
    return(minmax, fprocessed)





   
#normalise the data in fprocessed.
#parameters: minmax (a 2D list containing corresponding minimum and maximum values for each column) and fprocessed (a copy of the
#inputs file, edited as per getMinMax(file) that is easier to process).
#returns: a version of fprocessed with all elements normalised for their respective columns.
def getNormalised(minmax, fprocessed):
    fnormalised = []
    for line in fprocessed:
        normline = line[:2]
        for value in line[2:]:
            if (value == value):#omits all nan values. Useful later when calculating metrics
                valindex = line.index(value)-2
                mini = minmax[valindex][0]
                maxi = minmax[valindex][1]
                if(maxi == mini):
                    normline.append((value-mini)/(1-mini))
                else:
                    normline.append((value-mini)/(maxi-mini))
        fnormalised.append(normline)
    return(fnormalised)




            
            
#find an unsorted 2d list of country names, World Happiness Index, and their normalised score as per the entered metric, for each line
#of the original file.
#parameters: fnormalised (a version of the original file with all elements normalised for their respective columns) and metric (the metric
#entered at the beginning of the program)
#returns: fmetlist (an unsorted 2d list of country names, World Happiness Index, and their normalised score as per the entered metric)
def getMetricList(fnormalised, metric):
    fmetlist = []
    
    if(metric == "min"):
        for line in fnormalised:         
            fmetlist.append([line[0]] + [line[1]] + [min(line[2:])])              
    
    elif(metric == "mean"):
        for line in fnormalised:
            fmetlist.append([line[0]] + [line[1]] + [sum(line[2:])/len(line[2:])])
            
    elif(metric == "median"):
        for line in fnormalised:
            size = len(line)
            midind = size//2
            if(size%2 == 0):
                fmetlist.append([line[0]] + [line[1]] + [(line[midind] + line[midind-1])/2])
            else:
                fmetlist.append([line[0]] + [line[1]] + [line[midind]])
    
    elif(metric == "harmonic_mean"):
        for line in fnormalised:
            zeroes = 0 #number of zero values in a line
            denom = 0 #denominator of the harmonic mean equation
            for value in line[2:]:
                if(value != 0):
                    denom += 1/value
                else:
                    zeroes += 1
            fmetlist.append([line[0]] + [line[1]] + [(len(line[2:])-zeroes)/denom])
    
    else:
        print("error: Check that inputs for metric are valid")
    return fmetlist






#Create a list or correlation coefficient as per the input action, and print it.
#parameters: action (the action input by the user at the beginning of the program) and fmetlist (an unsorted 2d list of country names,
#World Happiness Index, and their normalised score as per the entered metric).
#returns: A list or a correlation coefficient, depending on the input action.
def doAction(action, fmetlist):        
    fmetlist.sort(key = sortByNormalised, reverse = True)
    if(action == "list"):           
        for line in fmetlist:
            print(line[0],line[2])

    elif(action == "correlation"):
        sortWHI = sorted(fmetlist, key = sortByWHI, reverse = True)
        d = 0
        for line in sortWHI:
            d += (fmetlist.index(line) - sortWHI.index(line))**2
        n = len(fmetlist)
        print(1-((6*d)/(n*((n**2)-1))))    
    
    else:
        print("error: Check that inputs for action are valid")






#gets the normalised value from fmetlist
#returns: the third value in a list
#parameters: the list from which the value is to be taken
def sortByNormalised(line):
    return line[2]

#gets the WHI score from fmetlist
#returns: the second value in a list
#parameters: the list from which the value is to be taken
def sortByWHI(line):
    return line[1]
    
