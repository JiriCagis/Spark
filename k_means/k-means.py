import sys
import os
import shutil
from k_means.functions import load_vertices
from k_means.functions import load_first_vertices
from k_means.functions import calculate_potential_centroids
from k_means.functions import calculate_new_centroids

# -----------------------------
# CONFIGURE SPARK ENVIRONMENT
# -----------------------------
try:
    os.environ['SPARK_HOME'] = "/Users/admin/spark-1.6.0/"
    sys.path.append("/Users/admin/spark-1.6.0/python/lib/py4j-0.9-src.zip")  # Append pyspark  to Python Path
    sys.path.append("/Users/admin/spark-1.6.0/python/")
    from pyspark import SparkContext
    from pyspark import SparkConf

    sc = SparkContext('local')  # sc mean spark content
    print ("Successfully imported Spark Modules")

    if os.path.isdir("output"):
        shutil.rmtree("output")
        os.mkdir("output")
        print ("Delete output folder")

except ImportError as e:
    print ("Can not import Spark Modules", e)
    sys.exit(1)


# -----------------
# FUNCTIONS
# -----------------
def k_means(input_file, count_centroids):
    """
    Clustering algorithm for calculate centroids in input vector data set
    :param input_file: file contains vertices, each line is compose N coordinates divide by coma (example line 1,2,3,4...)
    :param count_centroids: how many centroids you wish find
    :return: list of centroids
    """
    vertices = load_vertices(input_file,sc)
    previous_centroids = load_first_vertices(vertices,count_centroids)
    while (True):
        centroids = calculate_potential_centroids(vertices, previous_centroids,sc)
        new_centroids = calculate_new_centroids(vertices, centroids,sc)
        if is_same(previous_centroids, new_centroids):
            return new_centroids
        else:
            previous_centroids = new_centroids


def is_same(vertices1, vertices2):
    if len(vertices1) != len(vertices2):
        return False

    for i in range(len(vertices1)):
        vertex1 = vertices1[i]
        vertex2 = vertices2[i]
        for k in range(len(vertex1)):
            x1 = vertex1[k]
            x2 = vertex2[k]
            if abs(x1 - x2) > 0.5:
                return False

    return True

input_file = "inputs/iris.data.txt"
count_centroids = 3;
file_name = input_file[input_file.index("/")+1:len(input_file)-4]

centroids = k_means(input_file, count_centroids)

file = open("output/SparkResult_"+file_name+"_centroids_"+str(count_centroids)+".txt","w")
centroids.sort()
for centroid in centroids:
    for coordinate in centroid:
        file.write(str(coordinate)+",")
    file.write("\n")
file.close()
