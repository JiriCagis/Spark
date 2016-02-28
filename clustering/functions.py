import math
import sys


def load_vertices(input_file, sc):
    """
    Function load all vertices from input path and place to RDD Spark collection.
    :param input_file: file with vertices
    :param sc: spark content
    :return: RDD collection
    """
    lines = sc.textFile(input_file)
    return lines.map(lambda line: line_to_vertex(line))


def line_to_vertex(line):
    """
    Support function for lambda term, it take line and split line
    to float list of coordinates one vector
    :param line: text line formatted as "number,number,....."
    :return: list of coordinates meaning vector
    """
    vertex = []
    coordinates = line.split(",")
    for coordinate in coordinates:
        vertex.append(float(coordinate))
    return tuple(vertex)


def load_first_vertices(vertices, count):
    """
    From RDD collection with vertices take first N vector and
    return as broad cast variable shared between computer node.
    :param vertices: RDD collections
    :param count: how many first vertices you wish get
    :return: first N vertices as broad cast variable
    """
    return tuple(vertices.take(count))


def calculate_potential_centroids(vertices, previous_centroids, sc):
    """
    Function divide vertices to N clusters by previous centroids and
    calculate potential centroids as sum vertices in cluster divided
    count vertices in cluster.
    :param vertices: all vertices in data set (RDD collection)
    :param previous_centroids: broad cast variable
    :param sc: spark content
    :return: tuole of potential centroids
    """
    previous_centroids = sc.broadcast(previous_centroids)  # variable for share between computer node
    centroids_with_vertices = vertices.map(lambda vertex: assign_centroid(vertex, previous_centroids.value))
    count_vertices_to_centroids = centroids_with_vertices.countByKey()
    sum_vertices_to_centroids = centroids_with_vertices.reduceByKey(
            lambda vertex1, vertex2: sum_vertex(vertex1, vertex2)).collect()

    potential_centroids = []
    for sum_vertices in sum_vertices_to_centroids:
        previous_centroid = sum_vertices[0]
        new_centroid = list(sum_vertices[1])
        count = count_vertices_to_centroids[previous_centroid]
        for k in range(len(new_centroid)):
            new_centroid[k] /= float(count)
        potential_centroids.append(tuple(new_centroid))
    return potential_centroids


def assign_centroid(vertex, previous_centroids):
    """
    Support function for lambda term, method read vertex and assign it
    near centroid by euclide distance.
    :param vertex: tuple mean coordinates in vertex
    :param previous_centroids: list of previous centroids
    :return: couple <choose centroid,vertex>
    """
    min_distance = sys.maxint
    choose_centroid = None
    for centroid in previous_centroids:
        intermediate = 0
        for k in range(len(centroid)):
            intermediate += math.pow(vertex[k] - centroid[k], 2)
        distance = math.sqrt(intermediate)
        if distance < min_distance:
            min_distance = distance
            choose_centroid = centroid
    return (choose_centroid, vertex)


def sum_vertex(vertex1, vertex2):
    """
    Support function for lambda term, method sum two vertices.
    :param vertex1:
    :param vertex2:
    :return: sum vertex1 and vertex2
    """
    result = []
    for k in range(len(vertex1)):
        result.append(vertex1[k] + vertex2[k])
    return result


def calculate_new_centroids(vertices, potential_centroids, sc):
    """
    Function assign nearest vertex from vertices for each potential centroid and
    return it as new centroid.
    :param vertices:
    :param potential_centroids:
    :param sc:
    :return:
    """
    sc.broadcast(potential_centroids)  # variable for share between computer node
    centroids_with_distance = vertices.flatMap(lambda vertex: assign_distance(vertex, potential_centroids))

    new_centroids = centroids_with_distance.reduceByKey(
            lambda vertex_with_dis1, vertex_with_dis2: minimum(vertex_with_dis1, vertex_with_dis2)).map(
            lambda result: format_result(result)).collect()
    return new_centroids


def assign_distance(vertex, potential_centroids):
    result = []
    for centroid in potential_centroids:
        intermediate = 0
        for k in range(len(centroid)):
            intermediate += math.pow(vertex[k] - centroid[k], 2)
        distance = math.sqrt(intermediate)
        result.append([tuple(centroid), (vertex, distance)])
    return result


def minimum(vertex_with_distance1, vertex_with_distance2):
    distance1 = vertex_with_distance1[1]
    distance2 = vertex_with_distance2[1]
    if distance1 < distance2:
        return vertex_with_distance1
    else:
        return vertex_with_distance2


def format_result(result):
    previous_centroid = result[0]
    vertex_with_distance = result[1]
    new_centroid = vertex_with_distance[0]
    return new_centroid
