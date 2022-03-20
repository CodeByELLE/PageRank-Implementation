#!/usr/bin/env python
# coding: utf-8

# ### Brief description of the algorithm:
# The article propose an algorithm called "Hierarchical clustering" for detecting compact communities  based on a another graph traversal algorithm "LexDFS".In fact the "Hierarchical clustering"  algorithm applies "LexDFS" first on the graph for a  certain number l of iterations(starting by a differnt node of the graph in each iteretion).bellow is a breif description of LexDFS . <br>
# LexDFS:
#  * input : graph,starting node
#  * output : affect  a number node.visited to each node (it corresponds to the iteretation in which the node has             been visited) <br>
#  
# The application of LexDFS gives a "rank"  to each node (node.visited) based on which we can affect scores  to the  edges of the graph. Hierarchical clustering then  ordred the set of edges decreaingly .while set isn't empty the algorithm takes the edge with the smallest score and merge the clusters containing the two nodes composing this edge.<br>
# **NB**: we don't have any condition on the score to take into consideration while clustering the nodes ,consequently the algorithm put all the nodes that have a commun edge in the same cluster .we then end up by a set of cluster such that each cluster is composed by a connexe component of the graph.<br>
# We tested the algorithm on lage datasets ,but for the demonstration bellow we use a graph with two connexe comppnenets to make it more visible.

# ###### We define a class called node each node is characterized by the following attributes
# * Node's id (`string`)
# * Node's visited value (`int`)
# * Node's lex value (`list that takes the two last elements of lex value`)
# * Node's neighbors (`list of nodes`)
# * A method that fills the neighbors' list

# In[1]:


class node:
    def __init__(self,id):
        self.id = id
        self.lex = [0,0]
        self.visited = 0
        self.neighbors = []
    def add_neighbor(self,v):
        if v not in self.neighbors :
            self.neighbors.append(v)


# ###### LexDFS algorithm : given a graph and a starting point, the algorithm computes the lexicographical DFS & returns a list of the visited nodes

# In[2]:


def Lexdfs(graph,start):
    stack = []
    stack.append(start)
    i = 1
    listvisited =[]
    while (stack != []):
        node = stack.pop()
        node.visited = i
        print('current node :',node.id," visited :",node.visited," lex :",node.lex)
        listvisited.append(node.id)
        array = []
        for v in node.neighbors:
            if v.visited == 0:
                #print('non-visited neihbors : ',v.id)
                if(v in stack):
                    stack.remove(v)
                x = v.lex[0]
                v.lex[1] = x
                v.lex[0] = i
                array.append(v)
        sortedArray = sorted(array, key=lambda v: sum(v.lex))
        for j in range(len(sortedArray)):
            stack.append(sortedArray[j])
        i = i+1
    print("List of visited nodes :",listvisited)


# ##### Reading graph from a text file(note that the graph is composed by two connected components)

# In[3]:


import operator
import random

f = open("C:/Users/Emily/Desktop/DNA courses/Algo/lexdfs_graph_test.txt", "r").read().splitlines()
graph = {}
outlinks=[]
for x in f:
    outlinks = x[2:].split(" ")
    graph.update({x[0]:outlinks})
print("Graph : ",graph)


# ###### Generating graph with node object & filling the neighbors list

# In[4]:


graphlist = [node(v) for v in graph.keys()]
# def set_node_neighbors(graph)
for mynode in graphlist:
    for i in graph:
        l = []
        if mynode.id == i:
            l = graph[i]
        for node in graphlist:
            if node.id == i:
                for elt in l:
                    for k in graphlist:
                        if k.id == elt:
                            node.add_neighbor(k)
#print (graphlist)


# ###### `LexDFS example :` run over graphlist and the node '1' and node '7' since we have two connected components.

# In[5]:


Lexdfs(graphlist,graphlist[0])


# In[6]:


Lexdfs(graphlist,graphlist[6])


# ##### This method gives the set of edges (u,v) of a given graph and initialize the score of all edges to 0

# In[7]:


def edges_set(graph):
    edges ={}
    for i in graph:
        for j in i.neighbors:
            edges.update({(i,j):0})
            if (j,i) in edges.keys():
                edges.pop((j,i))
                #print("(",i.id,",",j.id,")")
    return(edges)


# In[8]:


edges = edges_set(graphlist)
for i in range(1, 11): #10 iteration
   ######### Re-initialize values of the graph before every lexDFS#########
    for node in graphlist:
        node.visited=0
        node.lex=[0,0]
   #######################################################################    
    start = graphlist[random.randrange(len(graphlist))] # takes a random node from the graph
    print('Starting point :', start.id)
    Lexdfs(graphlist, start)
    print("***end iter lexDFS***")
    for key in edges:
        s = 1 - abs((key[0].visited - key[1].visited) / len(edges))
        edges[key] = (edges[key] * (i - 1) + s) / i


#we sort the set of edges by score value
ordered_edg_set = [ x[0]for x in sorted(edges.items(), key=operator.itemgetter(1))]

#fill cluster by sub-clusters containing the singleton [node]
cluster=[]
for node in graphlist:
    cluster.append([node])

while len(ordered_edg_set)>1:
    edg = ordered_edg_set .pop()
    #print('edge:(',edg[0].id,",",edg[1].id,")")
    V = cluster
    y = []
    for c in cluster:
        if edg[0] in c:
            if edg[1] not in c:
                y=c
                V.remove(c)
    for c in cluster:
         if edg[1] in c:
                c.extend(y)
#print('Final clusters :',V)
print ("The total number of clusters is :",len(V))
print('list of clusters : ', V)


# ## Team members:
# * Safae Elamrani
# * Imane Elabid
# * Meryem Janati Idrissi
