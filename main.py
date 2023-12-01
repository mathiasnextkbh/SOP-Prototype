import matplotlib.pyplot as plt
import numpy as np

peak_detection_accuracy = 2
s_0 = 1.05
s_1 = 1.25
k = 1

class Signal:    
    def __init__ (self, interval, peakType, parentData):
        self.x_start = interval[0]
        self.x_end = interval[1]
        self.type = peakType
        self.strength = self.defineSignalStrength(parentData)
    
    def getSmallestValues(self, data):
        values = []
        for i in range(self.x_start, self.x_end):
            values.append(data[i])
        return sorted(values)[:k]

    def defineSignalStrength(self, data):
        smallestValue = self.getSmallestValues(data)
        return sum(smallestValue)/k


class Data:
    def __init__(self, y):
        self.x = []
        for i in range (1, 101):
            self.x.append(i)
        self.y = y

    def definePeaks(self):
        inPeak = False
        peakType = "none"
        peakList = []

        temp_x_start_value = 0

        for i in range(101 - 2 * peak_detection_accuracy):
            Data_sum_1 = 0
            Data_sum_2 = 0
            for j in range(peak_detection_accuracy):
                Data_sum_1 += self.y[i + j]
                Data_sum_2 += self.y[i + j + peak_detection_accuracy]
            Avg_1 = Data_sum_1/peak_detection_accuracy
            Avg_2 = Data_sum_2/peak_detection_accuracy
            
            if (Avg_1 == 0): Avg_1 += 0.0001
            if (Avg_2 == 0): Avg_2 += 0.0001

            DeltaAVG = Avg_1/Avg_2

            if (DeltaAVG >= s_0 and DeltaAVG < s_1 and not inPeak):
                inPeak = True
                peakType = "WIDE"
                temp_x_start_value = i

            elif (DeltaAVG > 1/s_1 and DeltaAVG <= 1/s_0 and inPeak and peakType == "WIDE"):
                inPeak = False
                peakType = "none"
                peakList.append(Signal([temp_x_start_value, i], "WIDE", self.y))

            elif (DeltaAVG >= s_1 and not inPeak):
                inPeak = True
                peakType = "SHARP"
                temp_x_start_value = i

            elif (DeltaAVG <= s_1 and inPeak and peakType == "SHARP"):
                inPeak = False
                peakType = "none"
                peakList.append(Signal([temp_x_start_value, i], "SHARP", self.y))

        return peakList

data = Data([
    0.99, 0.96, 0.92, 0.97, 0.98, 0.94, 0.94, 0.99, 0.77, 0.45,
    0.25, 0.57, 0.78, 0.98, 0.97, 0.97, 0.96, 0.75, 0.48, 0.58,
    0.79, 0.97, 0.95, 0.84, 0.89, 0.93, 0.97, 0.97, 0.96, 0.92,
    0.82, 0.97, 0.98, 0.97, 0.97, 0.99, 0.97, 0.94, 0.99, 0.99,
    0.95, 0.98, 0.97, 0.97, 0.95, 0.92, 0.97, 0.98, 0.95, 0.97,
    0.95, 0.98, 0.97, 0.97, 0.95, 0.96, 0.92, 0.98, 0.97, 0.96,
    0.95, 0.94, 0.99, 0.82, 0.47, 0.10, 0.04, 0.23, 0.57, 0.78,
    0.98, 0.97, 0.97, 0.96, 0.92, 0.98, 0.98, 0.98, 0.97, 0.94,
    0.97, 0.95, 0.98, 0.97, 0.97, 0.97, 0.98, 0.97, 0.98, 0.97,
    0.75, 0.20, 0.67, 0.92, 0.97, 0.79, 0.57, 0.86, 0.97, 0.98,
])

peakdata = data.definePeaks()

for i in peakdata:
    print("(", i.x_start, " - ", i.x_end, "), type = ", i.type, ", strength = ", i.strength)

xpoints = np.array(data.x)
ypoints = np.array(data.y)

plt.plot(xpoints, ypoints)
plt.show()
