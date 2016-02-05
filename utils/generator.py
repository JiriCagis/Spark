import sys
import os
import math
import random

vertices = []
# ------------------
# Cluster 1
# -------------------
# Neighborhood
for i in range(0, 30, 1):
    x = random.randint(3000, 4000) / float(100)
    y = random.randint(3000, 4000) / float(100)
    vertices.append((x, y))
# Center
for i in range(0, 70, 1):
    x = random.randint(3500, 4200) / float(100)
    y = random.randint(3500, 4200) / float(100)
    vertices.append((x, y))

# ------------------
# Cluster 2
# -------------------
# Neighborhood
for i in range(0, 30, 1):
    x = random.randint(3000, 3400) / float(100)
    y = random.randint(4000, 6000) / float(100)
    vertices.append((x, y))
# Center
for i in range(0, 70, 1):
    x = random.randint(3200, 3300) / float(100)
    y = random.randint(4500, 5500) / float(100)
    vertices.append((x, y))

# ------------------
# Cluster 3
# -------------------
# Neighborhood
for i in range(0, 30, 1):
    x = random.randint(6000, 9000) / float(100)
    y = random.randint(5000, 7000) / float(100)
    vertices.append((x, y))
# Center
for i in range(0, 70, 1):
    x = random.randint(7000, 8000) / float(100)
    y = random.randint(5700, 6500) / float(100)
    vertices.append((x, y))

output = open("inputs/graph2.txt","w")
for vertex in vertices:
    output.write(str(vertex[0]) + "," + str(vertex[1]) + "\n")
output.close()
