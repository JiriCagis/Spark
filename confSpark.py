import os
import sys


# Method add need paths into work with Spark framework
# before import Spark module
def registerPath():
    # Path for spark source folder
    os.environ['SPARK_HOME'] = "/Users/admin/spark-1.6.0/"

    # Append pyspark  to Python Path
    sys.path.append("/Users/admin/spark-1.6.0/python/lib/py4j-0.9-src.zip")
    sys.path.append("/Users/admin/spark-1.6.0/python/")


""" #THIS PART YOU MUST COPY AND UNCOMMENT WHERE USE SPARK, BECAUSE STATIC IMPORT NOT WORK IN PYCHARM

try:
    confSpark.registerPath()
    from pyspark import SparkContext
    from pyspark import SparkConf

    print ("Successfully imported Spark Modules")
except ImportError as e:
    print ("Can not import Spark Modules", e)
    sys.exit(1)
sc = SparkContext('local')

"""
