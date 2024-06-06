from matplotlib import pyplot as plt
#%matplotlib inline
import numpy as np
#import pandas as pd
import datetime
# ADC maximumm value 14 bits? == 16383
with open("SMPLOG3_240523.txt") as datasource:
    rawData = datasource.readlines()

# Part 1. Establish fundamental characteristics
print(type(rawData))
# Calculate Unix time
print(rawData[0], rawData[1], rawData[2])

print("Length of raw data is : " + str(len(rawData)) + " elements")

maxValue = 0
minValue = 16384
print("Here I am")
for i in range(len(rawData)):
    val = int(rawData[i])
    # For all values except timestamps, find min/max
    if val < 16384:
        if val > maxValue:
            maxValue = val
        if val < minValue:
            minValue = val

print("Max value is : " + str(maxValue))
print("Min value is : " + str(minValue))

# Part 2. Separate the raw data file, containing both timestamps and sample values, in to 2 separate lists,
# value[] and time[]
# The 2 lists should have the same length, equal to the number of samples in the raw data file
# Every timestamp belongs to the sample right after the timestamp

# Create timestamp list
# Each timestamp holds the time for the next corresponding sample value
# This means moving the first timestamp to new list at same position index as in the original samplelist
# The next timestamp

index = 0
timeStampInserted = False       # For each timestamp in rawFile a sample value should be inserted
value = []
time = []
for i in range(len(rawData)):
    val = int(rawData[i])
    # For all positions sort out values and timestamps
    if val < 16384:
        value.append(val)
        if timeStampInserted == False:
            time.append(int(0))
        else:
            timeStampInserted = False
    else:
        time.append(val)
        timeStampInserted = True

if len(time) != len(value): print("Something wrong. value and time has not equal lengths!!")

# Part 3. Do some checks of timestamps.
# Check if any disrupts of sampling has occured

# Make a list of index, one index value for all positions not containing zero
timeIndexes = []
for i in range(len(time)):
    unixTime = int(time[i])
    if unixTime != 0:
        timeIndexes.append(i)

print(timeIndexes)
#ts = int("1714313815")

for i in range(len(timeIndexes)):
    ts = int(time[timeIndexes[i]])
    timestamp = datetime.datetime.fromtimestamp(ts)
    print(timestamp.strftime('%Y-%m-%d %H:%M:%S : ') + str(time[timeIndexes[i]]))

# Count if number of samples between timestamps are reasonable close to the sampling rate
#Use raw data file
numberOfSamples = 0
lastTimeStamp = 0
distanceInTime = 0
distanceInSamples = 0
firstTimeExecuted = True


nmbOfSamplesBetweenTimestamp = []
#Count the numbers of samples between each timestamp
for i in range(len(rawData)):
    val = int(rawData[i])
    if val < 16384:
        numberOfSamples += 1
    else:
        # timestamp reached
        nmbOfSamplesBetweenTimestamp.append(int(numberOfSamples))
        numberOfSamples = 0

print("Number of samples between each timestamp :    " + str(nmbOfSamplesBetweenTimestamp))

# Count number of seconds ibetween timestamps
numberOfSecondsBetweenTimestamps = []
lastTimeTime = int(timeIndexes[0])
for i in range(len(timeIndexes) - 1):
    thisTimeTime = int(timeIndexes[i+1])
    numberOfSecondsBetweenTimestamps.append(thisTimeTime-lastTimeTime)
    lastTimeTime = thisTimeTime

print("Difference in seconds between each timestamp : " + "0," + str(numberOfSecondsBetweenTimestamps))




  # Create graphical presentation of each timeslot-interval (The samples from a timeslot
  # until the last sample before the next timeslot
  # !!! For this specific input file assuming 1 second between samples are ok

#  U = ns * (5 *77,4/20,4)/16384 =  1,15787* 10^-3 = 0,00115787
# Ufac = 0.00115787
# graph_x1 = []
# graph_y1 = []
#
# timestampvalue = time[timeIndexes[0]]
#
# # Create time axis in seconds
# timestamp = datetime.datetime.fromtimestamp(timestampvalue)
# timestampStartSeconds = int(timestamp.strftime('%S'))
#
# for i in range(nmbOfSamplesBetweenTimestamp[1]):
#     graph_x1.append(Ufac*value[i+nmbOfSamplesBetweenTimestamp[0]])
#  #   print(Ufac*value[i])
#     graph_y1.append(timestampStartSeconds)
#     timestampStartSeconds += 1
#
# plt.plot(graph_y1, graph_x1, color='r', linestyle='--', marker='.')
# plt.xlabel(timestamp.strftime('%Y-%m-%d %H:%M:%S'))
# plt.show()
#
#
# graph_x2 = []
# graph_y2 = []
# timestampvalue = time[timeIndexes[1]]
#
# # Create time axis in seconds
# timestamp = datetime.datetime.fromtimestamp(timestampvalue)
# timestampStartSeconds = int(timestamp.strftime('%S'))
#
# for i in range(nmbOfSamplesBetweenTimestamp[2]):
#     graph_x2.append(Ufac*value[i+nmbOfSamplesBetweenTimestamp[1]])
#     #print(Ufac*value[i])
#     graph_y2.append(timestampStartSeconds)
#     timestampStartSeconds += 1
#
# plt.plot(graph_y2, graph_x2, color='r', linestyle='--', marker='.')
# plt.xlabel(timestamp.strftime('%Y-%m-%d %H:%M:%S'))
# plt.show()
#
# graph_x3 = []
# graph_y3 = []
# timestampvalue = time[timeIndexes[2]]
#
# # Create time axis in seconds
# timestamp = datetime.datetime.fromtimestamp(timestampvalue)
# timestampStartSeconds = int(timestamp.strftime('%S'))
#
# maxValue = 0
# minValue = 16384
#
# for i in range(nmbOfSamplesBetweenTimestamp[3]):
#     graph_x3.append(Ufac*value[i+nmbOfSamplesBetweenTimestamp[2]])
#     #print(Ufac*value[i])
#     graph_y3.append(timestampStartSeconds)
#     timestampStartSeconds += 1
#     val = value[i]
#     if val > maxValue:
#         maxValue = val
#     if val < minValue:
#         minValue = val
#
# print("Max value is : " + str(maxValue))
# print("Min value is : " + str(minValue))
# print(len(graph_x3))
#
#
# plt.plot(graph_y3, graph_x3, color='r', linestyle='--', marker='.')
# plt.xlabel(timestamp.strftime('%Y-%m-%d %H:%M:%S'))
# plt.show()
#
#
# graph_x4 = []
# graph_y4 = []
# timestampvalue = time[timeIndexes[3]]
#
# # Create time axis in seconds
# timestamp = datetime.datetime.fromtimestamp(timestampvalue)
# timestampStartSeconds = int(timestamp.strftime('%S'))
#
# maxValue = 0
# minValue = 16384
# for i in range(nmbOfSamplesBetweenTimestamp[4]):
#     graph_x4.append(Ufac*value[i+nmbOfSamplesBetweenTimestamp[3]])
#     #print(Ufac*value[i])
#     graph_y4.append(timestampStartSeconds)
#     timestampStartSeconds += 1
#
#     val = value[i]
#     if val > maxValue:
#         maxValue = val
#     if val < minValue:
#         minValue = val
#
# print("Max value is : " + str(maxValue))
# print("Min value is : " + str(minValue))
# print(len(graph_x4))
#
# plt.plot(graph_y4, graph_x4, color='r', linestyle='--', marker='.')
# plt.xlabel(timestamp.strftime('%Y-%m-%d %H:%M:%S'))
# plt.show()
#
#
# graph_x5 = []
# graph_y5 = []
# timestampvalue = time[timeIndexes[4]]
#
# # Create time axis in seconds
# timestamp = datetime.datetime.fromtimestamp(timestampvalue)
# timestampStartSeconds = int(timestamp.strftime('%S'))
#
# for i in range(nmbOfSamplesBetweenTimestamp[5]):
#     graph_x5.append(Ufac*value[i+nmbOfSamplesBetweenTimestamp[4]])
#    # print(Ufac*value[i])
#     graph_y5.append(timestampStartSeconds)
#     timestampStartSeconds += 1
#
# plt.plot(graph_y5, graph_x5, color='r', linestyle='--', marker='.')
# plt.xlabel(timestamp.strftime('%Y-%m-%d %H:%M:%S'))
# plt.show()


# Make graphical presentation in single loop, each timestamps starts a new graph

#  U = ns * (5 *77,4/20,4)/16384 =  1,15787* 10^-3 = 0,00115787
Ufac = 0.00115787



for nmbOfTs in range(0, len(nmbOfSamplesBetweenTimestamp)):  # Equals number of timestamps in graph
    timestampvalue = time[timeIndexes[nmbOfTs]]
    # Create time axis in seconds, extracting seconds from unixtime
    timestamp = datetime.datetime.fromtimestamp(timestampvalue)
    timestampStartSeconds = int(timestamp.strftime('%S'))
    # To be reinitialized
    graphx = []
    graphy = []
    for i in range(nmbOfSamplesBetweenTimestamp[nmbOfTs+1]):
        graphy.append(Ufac*value[i+nmbOfSamplesBetweenTimestamp[nmbOfTs]])
        graphx.append(timestampStartSeconds)
        timestampStartSeconds  += 1
#        timestamp = datetime.datetime.fromtimestamp(timestampvalue)
#        timestampStartSeconds = timestamp.strftime('%H:%M:%S')
    plt.plot(graphx, graphy, color='r', linestyle='--', marker='.')
    plt.xlabel(timestamp.strftime('%Y-%m-%d %H:%M:%S'))
    #myVar = plt.axes.Axes.set_axis_locator
    plt.show()

#
# timestampvalue = time[timeIndexes[0]]
# print(str(nmbOfSamplesBetweenTimestamp[1]))
# print(str(timestampvalue))
# for i in range(nmbOfSamplesBetweenTimestamp[1]):
#     graph_x.append(Ufac*value[i])
#     graph_y.append(timestampvalue)
#     timestampvalue += 1
#
# print(str(graph_x))
# print(graph_y)
#
# timestamp = datetime.datetime.fromtimestamp(timestampvalue)
# plt.xlabel(timestamp.strftime('%Y-%m-%d %H:%M:%S'))
#
# plt.plot(graph_y, graph_x, color='r', linestyle='--', marker='.')
# plt.show()
#
# timestampvalue = time[timeIndexes[1]]
# print(str(nmbOfSamplesBetweenTimestamp[2]))
# print(str(timestampvalue))
# for i in range(nmbOfSamplesBetweenTimestamp[2]):
#     graph_x.append(Ufac*value[i])
#     graph_y.append(timestampvalue)
#     timestampvalue += 1
#
# print(str(graph_x))
# print(graph_y)
#
# plt.plot(graph_y, graph_x, color='r', linestyle='--', marker='.')
# plt.show()
#
#
# timestampvalue = time[timeIndexes[2]]
# print(str(nmbOfSamplesBetweenTimestamp[3]))
# print(str(timestampvalue))
# for i in range(nmbOfSamplesBetweenTimestamp[3]):
#     graph_x.append(Ufac*value[i])
#     graph_y.append(timestampvalue)
#     timestampvalue += 1
#
# print(str(graph_x))
# print(graph_y)
#
# plt.plot(graph_y, graph_x, color='r', linestyle='--', marker='.')
# plt.show()
#
#
# timestampvalue = time[timeIndexes[3]]
# print(str(nmbOfSamplesBetweenTimestamp[4]))
# print(str(timestampvalue))
# for i in range(nmbOfSamplesBetweenTimestamp[4]):
#     graph_x.append(Ufac*value[i])
#     graph_y.append(timestampvalue)
#     timestampvalue += 1
#
# print(str(graph_x))
# print(graph_y)
#
# plt.plot(graph_y, graph_x, color='r', linestyle='--', marker='.')
# plt.show()
#
# timestampvalue = time[timeIndexes[4]]
# print(str(nmbOfSamplesBetweenTimestamp[5]))
# print(str(timestampvalue))
# for i in range(nmbOfSamplesBetweenTimestamp[5]):
#     graph_x.append(Ufac*value[i])
#     graph_y.append(timestampvalue)
#     timestampvalue += 1
#
# print(str(graph_x))
# print(graph_y)
#
# plt.plot(graph_y, graph_x, color='r', linestyle='--', marker='.')
# plt.show()
#
