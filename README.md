<p align='center'><h1> Data analysis </h1></p>

<b> Framework Spark </b> <br>
Apache Spark is a lightning-fast cluster computing technology, designed for fast computation. It is based on Hadoop MapReduce and it extends the MapReduce model to efficiently use it for more types of computations, which includes interactive queries and stream processing. The main feature of Spark is its in-memory cluster computing that increases the processing speed of an application.
Spark is designed to cover a wide range of workloads such as batch applications, iterative algorithms, interactive queries and streaming. Apart from supporting all these workload in a respective system, it reduces the management burden of maintaining separate tools

<p align='center'>
<img src="https://github.com/JiriCagis/Spark/blob/master/images/Sparkimage.png"/>
</p>

<h3> Word counter </h3>
This example show as Spark framework working. Spark divide calculate to two part.
In first part map algorithm go through all lines text and individually word save to map and second part filter algorithm sum occurrence word in  text.
<div>
<b>Example:</b><br>
- <u> Map </u><br> INPUT: ahoj svete ahoj svete <br>OUTPUT: [ahoj,1] [svete,1] [ahoj,1] <br>
- <u> Filter</u><br>INPUT: [ahoj,1,1] <br> OUTPUT: [ahoj,2] <br>
</div>

<h3> Inverted Indexing </h3>
Algorithm is use for find out count occurrence words in many text documents.
It produce list words with information about totally occurrence in all documents and individually occurrence for concrete document. A goal of a this implementation is to optimize the speed of the query: find the documents where word X occurs. You can use for base full-text search engine.
<div>
<b>Example:</b> <br>
<PRE>
INPUT:
1: if you prick us do we not bleed <BR>
2: if you tickle us do we not laugh <BR>
3: if you poison us do we not die and <BR>
4: if you wrong us shall we not revenge <BR>
</PRE>
<PRE>
OUTPUT: 
and     : 1 : (3, 1) 
bleed   : 1 : (1, 1)
die     : 1 : (3, 1)
do      : 3 : (1, 1), (2, 1), (3, 1)
if      : 4 : (1, 1), (2, 1), (3, 1), (4, 1)
laugh   : 1 : (2, 1)
not     : 4 : (1, 1), (2, 1), (3, 1), (4, 1)
poison  : 1 : (3, 1)
prick   : 1 : (1, 1)
revenge : 1 : (4, 1)
shall   : 1 : (4, 1)
tickle  : 1 : (2, 1)
us      : 4 : (1, 1), (2, 1), (3, 1), (4, 1)
we      : 4 : (1, 1), (2, 1), (3, 1), (4, 1)
wrong   : 1 : (4, 1)
you     : 4 : (1, 1), (2, 1), (3, 1), (4, 1)
</PRE>
<div>
<b>Explanation:</b> First number present totally count occurence of all documents. Braces contains two numbers, 
left number mean number document and right number is occurence in this document.
</div>

<h3> K-means </h3>

Often used algorithm for non-hierarchical clusters analyze. It assume, that objects present points in euclide space and count clusters is know in advance. Clusters are define his centroids. Centroid is point in cluster. Objects are add to cluster with nearest centroid. On start take first N clusters and assign objects to him. After it recalculate centroids by mean point in cluster. If are new centroids same algorithm finish, else it iterative work further. This implementation support find clusters in 2d decimal vectors.

<p align='center'><img src='http://3.bp.blogspot.com/-5vr_gg5oUME/VSr9P-mQJnI/AAAAAAAAALY/MNdRgs9bbE8/s1600/plot_mean_shift.png' width='55%' title='Sample graph for explain.'> </p>

<br><b> How it works: </b>
<ol>
  <li>Load first N vectors from input file and denote as previous clusters.</li>
  <li>Divide all vertices to N groups by distance of previous centroids and calculate average vector in groups. Denote this vector as potential centroid. </li>
  <li>For each potential centroid find nearest point from data set and mark as new centroid.</li>
  <li>Verify if previous and new centroids are same. If centroids are same, algorithm finish and show clusters, else
  assign to previous clusters variable new clusters and go back to step 2.</li>
</ol>

<br><b>Example:</b>
<pre>
1. Iteration: centroids {(1,1),(2,1)} # Random choosed
    (1,1) -> {(1,2),(1,3)}
    (2,1) -> {(6,3)(7,3)(6,4)(7,4)(7,5)}

2. Iteration: centroids {(1,2)(6,3)} # New centroids from mean vertices in cluster
    (1,2) -> {(1,1)(2,1)(1,3)}
    (6,3) -> {(7,3)(6,4)(7,4)(7,5)}

3. Iteration: centroids {(1,2)(7,4)} # New centroids from mean vertices in cluster
    (1,2) -> {(1,1)(2,1)(1,3)}
    (7,4) -> {(7,3)(6,4)(6,3)(7,5)}

4. Iteration: centroids {(1,2)(7,4)} # It find same centroid and finish calculate
</pre>


