<p align='center'><h1> Data analysis </h1></p>

<b> Framework Spark </b> <br>
Apache Spark is a lightning-fast cluster computing technology, designed for fast computation. It is based on Hadoop MapReduce and it extends the MapReduce model to efficiently use it for more types of computations, which includes interactive queries and stream processing. The main feature of Spark is its in-memory cluster computing that increases the processing speed of an application.
Spark is designed to cover a wide range of workloads such as batch applications, iterative algorithms, interactive queries and streaming. Apart from supporting all these workload in a respective system, it reduces the management burden of maintaining separate tools

<p align='center'>
<img src="https://github.com/JiriCagis/Spark/blob/master/images/Sparkimage.png"/>
</p>


<h3> Word counter </h3>
This example shows as the hadoop framework works. Hadoop uses the mapreduce algorithm that divide a task to two pats. First part map algorithm go through all lines text and individually word save to map and second part run reduce sum occurence a word in text.
<div>
<b>Example:</b><br>
- <u> Mapper </u><br> INPUT: ahoj svete ahoj svete <br>OUTPUT: [ahoj,1] [svete,1] [ahoj,1] <br>
- <u> Reducer</u><br>INPUT: [ahoj,1,1] <br> OUTPUT: [ahoj,2] <br>
</div>

<h3> Inverted Indexing </h3>
Algorith is uses for find out count occurence words in many text documents. It producess list words with information about totally occurrence in all documents and individually occurence for concrete document. A goal of the implementation is to optimize the speed of the query: find the documents where word X orrurs. You can use as base implementation a full-text seach engine.
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
<u>Explanation:</u> First number presents totally count occurence of all documents. Braces contains two numbers, left number mean a document number and right number is occurence in the doument.
</div>

<h3> K-means </h3>
Algorithm often uses in a non-hierarchical cluster analysis. It assume, that objects present points in euclide space and count clusters is know. Clusters are define his centroids. Centroid is point in cluster. Objects are add to cluster with nearest centroid. On start before compare the algorithm take first N points and mark as centroids and it assign objects to him. After it recalculate centroids by mean point in cluster again. The algorithm finish when new centroids are same with previous centroids, else it iterative works further. This implementation supports find clusters in 2d decimal vectors.

<p align='center'><img src='http://3.bp.blogspot.com/-5vr_gg5oUME/VSr9P-mQJnI/AAAAAAAAALY/MNdRgs9bbE8/s1600/plot_mean_shift.png' width='55%' title='Sample graph for explain.'> </p>

<br><b> How does it works? </b>
<ol>
  <li>Load first N vectors from input file and denote as previous clusters.</li>
  <li>Divide all vertices to N groups by distance of previous centroids and calculate average vector in groups and it denote this vectors as potential centroids. </li>
  <li>It finds neares points from poit from data set for each potencial centroid and mark as new centroid.</li>
  <li>It verifies if previous and new centroids are same. If centrois are same, algorithm finish and show clusters, else it assign to previous clusters variable new clusters and go back to the step second.</li>
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


