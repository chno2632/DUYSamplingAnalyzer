# Create time-axis information where all samples belong to a specific time in unixtimeformat
# Each timestamp value is a definition of the time of the specific sample
# The granularity is 1 second and a sampling time less than 1 second is not expected

from matplotlib import pyplot as plt
import datetime
# ADC maximumm value 14 bits == 16383
with open("SMPLOG3_240523.txt") as datasource:
    rawData = datasource.readlines()

print("Length of raw data is : " + str(len(rawData)) + " elements")

# Create timestamp list and value list
# Each timestamp holds the time for the next corresponding sample value
# This means moving the first timestamp to new list at same position index as in the original samplelist
# The next timestamp

index = 0
timeStampInserted = False       # For each timestamp in rawFile a sample value should be inserted
value = []
time = []
timestampRaw = []
totalNumberOfSamples = 0
for i in range(len(rawData)):
    val = int(rawData[i])
    # For all positions sort out values and timestamps
    if val < 16384:
        totalNumberOfSamples += 1
        value.append(val)
        if timeStampInserted is False:
            time.append(int(0))
        else:
            timeStampInserted = False
    else:
        time.append(val)
        timeStampInserted = True
        timestampRaw.append(val)

if len(time) != len(value):
    print("Something wrong. value and time has not equal lengths!!")

timeComp = time # Save values to test with better time information compensation. Se below

print(str(len(time)))
print(str(len(value)))
print("Raw data contains : " + str(len(timestampRaw)) + " timestamp elements")
print("Number of samples is " + str(len(rawData)-len(timestampRaw)) + " elements")
print(timestampRaw)
print("Total number of samples is " + str(totalNumberOfSamples))


# Make a list of index, one index value for all positions not containing zero
timeIndexes = []  # Holds the indexes where timestamps has originally been written in the raw data file
timeSamplesBetweenTimestamps = []
samplesBetweenTimeStamps = -1
for i in range(len(time)):
    unixTime = int(time[i])
    samplesBetweenTimeStamps += 1
    if unixTime != 0:
        if samplesBetweenTimeStamps < 1:
            timeIndexes.append(0) # first index, special case
        else :
            timeIndexes.append(i)
            timeSamplesBetweenTimestamps.append(samplesBetweenTimeStamps)
            samplesBetweenTimeStamps = 0

# For each time interval insert each samples time value

# Sanity check: Lower resolution than 1 sec not allowed

print("Indexes at timestamps are " + str(timeIndexes))

# print(timeSamplesBetweenTimestamps)
# print(sum(timeSamplesBetweenTimestamps))
# print(str(float(timeIndexes[-1])))
# print(str(float(sum(timeSamplesBetweenTimestamps))))
fs = float(timeIndexes[-1])/float(sum(timeSamplesBetweenTimestamps))
print('Sampling frequency is ' +  str(fs))
if (fs < 1.0):
    print('ERROR: Sampling frequency below 1 second could not be handled!')


# Fill the time list with the calculated values
cnt = 0
indexesBetweenTimestamps = []
cntIndexes = 0  # Always start with a zero interval as start value
for i in range(len(time)):
    unixTime = int(time[i])
    if (unixTime > 0):
        unixTimestamp = unixTime
        indexesBetweenTimestamps.append(cntIndexes)
        cntIndexes = 1
    else:
        unixTimestamp += int(fs)
        time[i] = unixTimestamp
        cnt += 1
        cntIndexes += 1


print(cnt)
print(len(time))
print('Number of samples in each interval is ' + str(indexesBetweenTimestamps))

# timestampRawIntervals = []
# for i in range(len(timeIndexes)-1):
#     timestampRawIntervals.append(int(timeIndexes[i+1] - int(timeIndexes[i])))
# print('Raw timestamp interval ' + str(timestampRawIntervals))

timestampRawList = []
for i in range(len(rawData)):
    val = int(rawData[i])
    if val > 16384:
        timestampRawList.append(val)

timestampRawIntervals = []
for i in range(len(timestampRawList)-1):
    timestampRawIntervals.append(int(timeIndexes[i + 1] - int(timeIndexes[i])))
print('Raw timestamp interval ' + str(timestampRawIntervals))


#  disruptsOfInterval = []
timeOfEachInterval = []
samplesDifferenceOfDisruptsInTime = [] # Difference in number of samples
for i in range(len(timeIndexes)-1):
    timeVal = time[timeIndexes[i+1]]-time[timeIndexes[i+1] - 1] # Not consecutive time
#    disruptsOfInterval.append(i + 1) # Interval number, counts from 1
    samplesDifferenceOfDisruptsInTime.append(timeVal-1)


if (len(samplesDifferenceOfDisruptsInTime) != len(timestampRaw)-1):
    print('Debug output: Number of disrupts doesnt match')

#  print('Indexes where time disruptions occur (The index of last consecutive index)' + str(disruptsOfInterval))
print('Length in samples of the disruption ' + str(samplesDifferenceOfDisruptsInTime))


# # Analyze if an interval is consisting of a continuous sampling or if the sampling
# # has been interrupted or restarted.
# # The criteria for this is if the number of samples within an interval compared to the timestamp difference
# # of the same interval does not differs more than +/- 15%.
#

relativeDisruption = []
for i in range(len(timeSamplesBetweenTimestamps)):
    relativeDisruption.append(float(samplesDifferenceOfDisruptsInTime[i]/float(timeSamplesBetweenTimestamps[i])))


# for i in range(len(timeIndexes)-1):
#     rawTimeStampLengthOfInterval = time[timeIndexes[i+1]] - time[timeIndexes[i]]
#     relativeDisruption.append(float(samplesDifferenceOfDisruptsInTime[i]/float(rawTimeStampLengthOfInterval)))
# relativeDisruption < 1 : Actual time value should be added by nominal fs + relativeDisrution
#                    = 1 : No compensation nedded
#                    < 1 : Actual time value should be added by nominal fs + relativeDisrution
print(relativeDisruption)

# Calculate a fs for each interval

f = open("timeStampFileBeforeComp.txt", "w")
for item in time:
    f.write(f"\n{item}")
f.close()

# Time compensation
# for i in range(len(timeComp)):
#     ts = timeComp[i]
fsIntervalUncompensated = 1.0
for i in range(len(timeIndexes)-1):
    fsInterval = relativeDisruption[i]
    timeStamp = timeComp[timeIndexes[i]]
    if abs(fsInterval > 0.15):
        print('The interval ' + str(i) + ' (0, 1, 2...) has been disrupted and no time compensation is done')
        print('Uncompensated fs will be used')
        #  TODO add timestamps
        for j in range(timeIndexes[i] + 1, timeIndexes[i + 1]):
            timeStamp += fsIntervalUncompensated
            timeComp[j] = int(round(timeStamp))
    else:
        # print(fsInterval)
        # timeStamp = timeComp[i]
        # print(timeStamp)
        for j in range(timeIndexes[i] + 1, timeIndexes[i + 1]):
            timeStamp += fsInterval + fsIntervalUncompensated
            timeComp[j] = int(round(timeStamp))


f = open("timeStampFileAfterComp.txt", "w")
for item in time:
    f.write(f"\n{item}")
f.close()
