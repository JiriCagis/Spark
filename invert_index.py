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
def inverted_index(files):
    pass


# ---------------
# LAUNCHER
# ---------------

files = ("inputs/book1.txt","inputs/book2.txt")
mapFile = {}
for i in range(0,len(files),1):
    mapFile[files[i]] = i

