import sys
import confSpark

# DYNAMIC IMPORT SPARK MODULES
try:
    confSpark.registerPath()
    from pyspark import SparkContext
    from pyspark import SparkConf

    print ("Successfully imported Spark Modules")
except ImportError as e:
    print ("Can not import Spark Modules", e)
    sys.exit(1)

# YOUR PROGRAM
sc = SparkContext('local')
words = sc.parallelize(["scala","java","hadoop","spark","akka"])
print words.count()
