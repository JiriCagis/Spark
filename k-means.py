import sys
import os
import math
import shutil

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

def k_means(input_file, count):
    """
    Function read text file with vertices and divide to N clusters by input parameter count_cluster.
    :param input_file: file contains vertices, each line contains string "x,y" featuring vertex
    :param count: how many clusters you wish divide vertices
    :return: list of clusters (cluster is collection of vertices)
    """

    """
    Read lines from text file and convert each line to vertex.
    Each vertex is save to RDD collection vertices by function map.
    Last step is create broadcast collection, which is not mutable and
    it is same on all nodes for centroids.
    """
    lines = sc.textFile(input_file)
    vertices = lines.map(lambda line: line_to_vertex(line))
    centroids = sc.broadcast(vertices.take(count))

    """
    Main loop calculate clusters for centroids. After finish calculate
    decide new centroids by mean vertex in cluster. Loop finish after
    previous centroids and new centroids are equally.
    """
    while True:
        map_centroid_vertex = vertices.map(lambda vertex: assign_centroid(vertex, centroids.value))
        count_vertices_in_clusters = map_centroid_vertex.countByKey()
        sum_vertices_in_clusters = map_centroid_vertex \
            .reduceByKey(lambda vertex1, vertex2: (vertex1[0] + vertex2[0], vertex1[1] + vertex2[1])) \
            .collect()

        potential_centroids = calculate_potential_centroids(sum_vertices_in_clusters, count_vertices_in_clusters)
        potential_centroids = sc.broadcast(potential_centroids)

        centroids_distances = vertices.map(
                lambda vertex: assign_centroid_with_distance(vertex, potential_centroids.value)) \
            .groupByKey().map(lambda item: (item[0], list(item[1])))

        new_centroids = []
        for centroid_distances in centroids_distances.take(count):
            distances = sc.parallelize(centroid_distances[1])
            vertex_with_distance = distances.reduce(lambda item1, item2: reduce(item1, item2))
            new_centroids.append(vertex_with_distance[0])

        if is_same_centroids(centroids.value, new_centroids):
            centroids = sc.broadcast(new_centroids)
            break
        else:
            centroids = sc.broadcast(new_centroids)

    clusters = vertices.map(lambda vertex: assign_centroid(vertex, centroids.value)) \
        .groupByKey() \
        .map(lambda x: list(x[1])) \
        .collect()

    print("Centroids:" + str(centroids.value))

    return clusters


def reduce(vertex_with_distance1, vertex_with_distance2):
    """
    Find vertex with minimum distance of centroid
    :param vertex_with_distance1: ((x,y),distance1)
    :param vertex_with_distance2: ((x,y),distance2)
    :return: min vertex with distance
    """
    distance1 = vertex_with_distance1[1]
    distance2 = vertex_with_distance2[1]
    if distance1 < distance2:
        return vertex_with_distance1
    else:
        return vertex_with_distance2


def line_to_vertex(line):
    """
    Convert function, take line and split to vertex
    :param line: line contains string "x,y"
    :return: (x,y)
    """
    item = line.split(",")
    return (float(item[0]), float(item[1]))


def assign_centroid(vertex, centroids):
    """
    Function calculate near centroid for vertex
    :param vertex: (x,y)
    :param centroids:[(x,y),(x,y),..]
    :return: (centroid,vertex)
    """
    minDistance = sys.maxint
    chooseCentroid = None
    for centroid in centroids:
        distance = math.sqrt(math.pow(vertex[0] - centroid[0], 2) + math.pow(vertex[1] - centroid[1], 2))
        if distance < minDistance:
            minDistance = distance
            chooseCentroid = centroid
    return (chooseCentroid, (vertex))


def assign_centroid_with_distance(vertex, centroids):
    """
    Function calculate near centroid for vertex
    :param vertex: (x,y)
    :param centroids:[(x,y),(x,y),..]
    :return: (centroid,vertex)
    """
    minDistance = sys.maxint
    chooseCentroid = None
    for centroid in centroids:
        distance = math.sqrt(math.pow(vertex[0] - centroid[0], 2) + math.pow(vertex[1] - centroid[1], 2))
        if distance < minDistance:
            minDistance = distance
            chooseCentroid = centroid
    return (chooseCentroid, (vertex, minDistance))


def calculate_potential_centroids(sum_vertices_in_clusters, count_vertices_in_clusters):
    """
    Function calculate new list of centroids from total sum vertices in cluster divide count vertices in cluster.
    Float numbers are round on two decimal place.
    :param sum_vertices_in_clusters: list sums vertices for each cluster
    :param count_vertices_in_clusters: list count vertices for each cluster
    :return: list new centroids
    """
    new_clusters = []
    for sum_vertices_in_cluster in sum_vertices_in_clusters:
        centroid = sum_vertices_in_cluster[0]
        sum_vertices = sum_vertices_in_cluster[1]
        count_vertices = count_vertices_in_clusters[centroid]
        cluster = (sum_vertices[0] / float(count_vertices),sum_vertices[1] / float(count_vertices))
        new_clusters.append(cluster)
    return new_clusters


def is_same_centroids(centroids1, centroids2):
    """
    Function compare two list of centroids whether contains same vertices
    :param centroids1: list of centroids
    :param centroids2: list of centroids
    :return: True if are lists equally else return False
    """
    for i in range(0, len(centroids1), 1):
        x1 = centroids1[i][0]
        x2 = centroids2[i][0]
        if abs(x1 - x2) > 0.5:
            return False
        y1 = centroids1[i][1]
        y2 = centroids2[i][1]
        if abs(y1 - y2) > 0.5:
            return False
        return True


# ---------------
# LAUNCHER
# ---------------


# Run k - means for calculate clusters
clusters = k_means("inputs/graph3.txt", 5)

# Save result to output folder
for i in range(0, len(clusters), 1):
    file = open("output/cluster" + str(i) + ".txt", "w")
    for vertex in clusters[i]:
        file.write(str(vertex[0]) + "," + str(vertex[1]) + "\n")
    file.close()

print("SPARK WORK SUCCESSFUL :)")
