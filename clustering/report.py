from clustering.kmeans import k_means
import os
import time

head = """
  /\ /\     _ __ ___   ___  __ _ _ __  ___
 / //_/____| '_ ` _ \ / _ \/ _` | '_ \/ __|
/ __ \_____| | | | | |  __/ (_| | | | \__ \\
\/  \/     |_| |_| |_|\___|\__,_|_| |_|___/

 __                  _
/ _\_ __   __ _ _ __| | __
\ \| '_ \ / _` | '__| |/ /
_\ \ |_) | (_| | |  |   <
\__/ .__/ \__,_|_|  |_|\_\\
   |_|                        by Jiri Caga
"""

current_milli_time = lambda: int(round(time.time() * 1000))

def generateSeparator(length):
    result = ""
    for i in range(length):
        result += "-"
    result += "\n"
    return result

startTime = current_milli_time()
result = head
for i in range(1, 6, 1):
    result += generateSeparator(120)
    dataset = "inputs/graph.txt"
    result += "Dataset: " + dataset + "\t\t count centroids: " + str(i) + "\n"
    centroids = k_means(dataset, i)
    centroids.sort()
    for centroid in centroids:
        for coordinate in centroid:
            result += str(coordinate) + "\t"
        result+="\n"
    result += "\n"

for i in range(1, 6, 1):
    result += generateSeparator(120)
    dataset = "inputs/iris.data.txt"
    result += "Dataset: " + dataset + "\t\t count centroids: " + str(i) + "\n"
    centroids = k_means(dataset, i)
    centroids.sort()
    for centroid in centroids:
        for coordinate in centroid:
            result += str(coordinate) + "\t"
        result+="\n"
    result += "\n"
stopTime = current_milli_time()
result+="Algorithm find all centroids in :" + str(stopTime-startTime) + "ms."

file = open("output/report.txt","w")
file.write(result)
