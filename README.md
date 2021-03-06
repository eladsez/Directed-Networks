# Weighted directed graphs (directed networks)

> Made by Elad Seznayev and Nerya Bigon.

## Goal:
The goal of this project is to design and implement two key interfaces:
* Weighted directed graph interface.
* Weighted directed graphs algorithms interface.  

And also to represent the graph in an interactive graphical interface (matplotlib/drawGraph) that will introduce the algorithms.  
In addition we've compared the performance between our implementation in java and our implementation in python for some algorithm, it can be found in the wiki pages of this repository.  


## Algorithms:
* `kruskal_MST` - return the minimum spaninig tree in the graph (list of edges).
This method is an implementation of the kruskal minimum spanning tree algorithm by using the union find data structure.
There is also GUI that illustrate the algorithm - still in development.

* `convex_hull` - given set of vertices the algorithm will return a list of edges representing the Convex Hull for this set.
The algorithm in this method is an implementation of Graham scan algorithm for finding Convex Hull.
There is also GUI that illustrate the algorithm - still in development.

* `isConnected` - return whether the graph is strongly connected or not.  
We've implemented the algorithm in the following way:    
  1. Run BFS algorithms from a specific node to all of the other nodes
  2. Run BFS again, this time on the graph transposed.
  3. Check if the BFS's results are equals to each othe and to the nuber of nodes in the graph.
  4. If so - the graph is strongly connected.  

* `shortestPathDist` - return the distance of the shortest path between two nodes.  
We've implemented the algorithm in the following way:    
  1. Run DIJKSTRA algorithm on the source node - in order to get in each node the shortest path from the source, and the distance. 
  2. The answer is contained in the destination node's weight parameter.
  3. So we return it.  

* `shortestPath` - return the shortest path between two nodes.  
We've implemented the algorithm in the following way:    
  1. Run DIJKSTRA algorithm on the source node - in order to get in each node the shortest path from the source, and the distance. 
  2. Because each node tag "carry" the node that came before it in the path, all there is to do is to loop from the destination node and ask who came before until we get to the source node.
  3. The results are then inserted into a list and returned.  

* `center` - return the node that is the closest to every other node.   
**Approach:** we are searching for the node with the shortest path, but from the longest result this node got from `shortestPathDist`.
We've implemented the algorithm in the following way:    
  1. Loop through all of the nodes in the graph.
  2. For each node check with `shortestPathDist` what is the **longest** path
  3. Return the node with the shortest one.  

* `tsp` - return the shrotest path between a list of nodes.   
**Approach:** we are using swaping algorithm, in order to get an acceptble path at reasonble time.
We've implemented the algorithm in the following way:    
  1. Start with a random route that start in the source node.
  2. Perform a swap between nodes (except the source).
  3. Keep new route if it is shorter.
  4. Repeat (2-3) for all possible swaps.
since in this assignment we are not required to return to the source node it's simplify the solution a bit.  
This algorithm is both faster, O(M*N^2) and produces better solutions then greedy algorithm.  
The intuition behind the algorithm is that swapping untangles routes that cross over itself (gets rid of circel's when posible).  
This swap algorithm performed much better than greedy; the path it drew looks similar to something a human might draw.

## Structure:  

Class/file | Description
----- | -----------
`main` | The main file, used to test the program in addition to UnitTests.
`DiGraph` | This class represent the graph -> implements the `GraphInterface` interface.
`GraphAlgo` | this class holds all of the algorithms -> implements the `GraphAlgoInterface` interface.
`Node` | This class represent a node.

## How To Run:
To run the algorithms, do the following:
1. Download this repository and open it in an IDE.
2. In the GraphAlgo.py (in the src folder) go to the bottom of the file and choose a graph (json graph files can be found in the Data folder).
3. Next, choose an algorithm to run on the graph, and finaly run the main function in the GraphAlgo.py file.
4. if you wish to see the graph graphicly, you can use the function `plot_graph()` that show the graph in matplotlib.  
(if you're using PyCharm and you have scientific mode enabled, turn it off for the best results)  

## More Information
- About Directed, Weighted, and Directed + Weighted graphs: http://math.oxford.emory.edu/site/cs171/directedAndEdgeWeightedGraphs/
- Shortest Path: https://en.wikipedia.org/wiki/Shortest_path_problem#Algorithms
- Dijkstra: https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
- Graph Center: https://en.wikipedia.org/wiki/Graph_center
- Travelling Salesman Problem (TSP): https://en.wikipedia.org/wiki/Travelling_salesman_problem
- Kruskal MST algorithm: https://en.wikipedia.org/wiki/Kruskal%27s_algorithm
- Graham Convex Hull - https://en.wikipedia.org/wiki/Graham_scan


