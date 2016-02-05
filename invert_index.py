import os
import shutil
import sys

from utils.porterStemming import PorterStemmer

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
        print ("Delete output folder")

except ImportError as e:
    print ("Can not import Spark Modules", e)
    sys.exit(1)


# -----------------
# FUNCTIONS
# -----------------
def inverted_index(files, output_path):
    """
    Algorithm for indexing documents, output algorithm are key present word
    and list values present occurrence in documents.
    For example: <"word",(total_occurrence,{(document_number,occurrence_by_document),...})>
    :param files: list text files for indexing
    :param output_path: folder for save output, IMPORTANT: folder be exist before run algorithm
    :return: nothing
    """

    """
    Mapping each file to number for better and faster process indexing
    """
    map_file = {}
    for i in range(0, len(files), 1):
        print(files[0] + "is map on number:" + str(i))
        map_file[files[i]] = i + 1

    total_indexing = sc.parallelize([])
    for file in files:
        """
        Read all line in file and get all words from line.
        """
        doc_number = sc.broadcast(map_file[file])
        words = sc.textFile(file).flatMap(lambda line: split_word_from(line))

        """
        Use Porter stemming for convert word to base form. For example:
        <fishes,fishing,fished> -> <fish>
        """
        words = words.map(lambda word: convert_to_base(word))

        """
        Output map function are <key,(doc_number,doc_occurrence)> from words and
        calculate occurrence by word in document.
        """
        indexing = words.map(lambda word: (word, (doc_number.value, 1))) \
            .reduceByKey(lambda value1, value2: (doc_number.value, value1[1] + value2[1]))

        total_indexing = total_indexing.union(indexing)

    """
    Group item in collection by keys(words) and add optional parameter total count occurrence word
    """
    total_indexing = total_indexing.groupByKey() \
        .map(lambda item: (item[0], list(item[1]))) \
        .map(decide_total_count) \
        .saveAsTextFile(output_path)


def split_word_from(line):
    """
    Function drag up all english word from line.
    :param line: some text
    :return: list of words
    """
    words = []
    start = 0
    for i in range(0, len(line), 1):
        character = line[i]

        # Last word on line
        if i == len(line) - 1 and start != i:
            words.append(line[start:len(line)])
            break

        if character.isalpha():
            continue

        if start != i:
            words.append(line[start: i])
        start = i + 1

    return words


def convert_to_base(word):
    """
    Function use Porter Stemmer for convert word to base shape.
    :param word: text concept word for convert
    :return: base shape word
    """
    p = PorterStemmer()
    return p.stem(word, 0, len(word) - 1)


def decide_total_count(item):
    """
    Function calculate optional information, total count per all document occurrence.
    :param item: list <word,{(doc_num,doc_occurrence),..}>,..
    :return: list <word,{total_occurrence,[(doc_num,doc_occurrence),..]}
    """
    key = item[0]
    values = item[1]
    total_count = 0
    for value in values:
        total_count += value[1]
    return (key, (total_count, values))


# ---------------
# LAUNCHER
# ---------------
files = ("inputs/book1.txt", "inputs/book2.txt", "inputs/book2.txt")
inverted_index(files, "output")
print("SPARK WORK SUCCESSFUL :)")
