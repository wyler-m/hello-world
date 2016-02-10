# 
# In the shortest-path oracle described in Andrew Goldberg's
# interview, each node has a label, which is a list of some other
# nodes in the network and their distance to these nodes.  These lists
# have the property that
#
#  (1) for any pair of nodes (x,y) in the network, their lists will
#  have at least one node z in common
#
#  (2) the shortest path from x to y will go through z.
# 
# Given a graph G that is a balanced binary tree, preprocess the graph to
# create such labels for each node.  Note that the size of the list in
# each label should not be larger than log n for a graph of size n.
#

#
# create_labels takes in a balanced binary tree and the root element
# and returns a dictionary, mapping each node to its label
#
# a label is a dictionary mapping another node and the distance to
# that node
#

from math import log

# ===========================================================================================================

def min_node(dist_so_far):
    best_node = None
    best_cost = 1000000

    for v in dist_so_far:
      if dist_so_far[v] < best_cost:
        (best_node, best_cost ) = (v, dist_so_far[v] )

    return best_node


def dijkstra(graph, v):
    
    dist_so_far = {}
    dist_so_far[v] = 0
    final_dist = {}

    path_dict = {v:"start"}

    while dist_so_far:

        # get current min node
        w = min_node(dist_so_far)
        
        # found min value, add to final
        final_dist[w] = dist_so_far[w]  
        del dist_so_far[w]

        for neighbor in graph[w].keys():

            if neighbor not in final_dist:
                 
               # check if this node needs to be added to the cost so far
                if neighbor not in dist_so_far: 
                    # make dicitonary for new flight
                    dist_so_far[neighbor] = {}

                    # for finding the cost of the flight
                    dist_so_far[neighbor] = final_dist[w] + graph[w][neighbor]
                    
                    # to keep track of the shortest paths
                    path_dict[neighbor] = w

                # check to see if the new path is better
                elif final_dist[w] + graph[w][neighbor] <= dist_so_far[neighbor]:
                      
                    # for finding the cost of the flight (added whether the time is better or not)
                    dist_so_far[neighbor] = final_dist[w] + graph[w][neighbor]
                      
                    # to keep track of the shortest paths
                    path_dict[neighbor] = w
                   
    return final_dist, path_dict

def get_path(path_dict, i, j):
    path = [j]
    current = j
    while  current != i:
        current = path_dict[current]
        path.append(current)
    path.reverse()
    return path

def get_children(tree, node, parent): 

    return set(tree[node].keys()) - set([parent])

def mark_parents(tree, parent_dict, labels, node, root):
    parent = parent_dict[node]
    while parent != "start":
        labels[node][parent] = labels[node][root] - labels[parent][root]
        parent = parent_dict[parent]

def mark_children(tree, parent_dict, labels, node, parent, root):
    children = set(tree[node].keys()) - set([parent])
    for child in children:
        for lable in labels[node]:
            labels[child] = {lable: labels[node][lable] + tree[node][child] }
        mark_children(tree, parent_dict, labels, child, node, root)
     
    if children == set([]):
        mark_parents(tree, parent_dict, labels, node, root)

    return labels

def create_labels(binarytreeG, root):
    labels = {root:{root:0}}

    (final_dist, parent_dict) = dijkstra(binarytreeG, root)
    mark_children(binarytreeG, parent_dict, labels, root, root, root)

    return labels



#######
# Testing
#

def get_distances(G, labels):
    # labels = {a:{b: distance from a to b,
    #              c: distance from a to c}}
    # create a mapping of all distances for
    # all nodes
    distances = {}
    for start in G:
        # get all the labels for my starting node
        label_node = labels[start]
        s_distances = {}
        for destination in G:
            shortest = float('inf')
            # get all the labels for the destination node
            label_dest = labels[destination]
            # and then merge them together, saving the
            # shortest distance
            for intermediate_node, dist in label_node.iteritems():
                # see if intermediate_node is our destination
                # if it is we can stop - we know that is
                # the shortest path
                if intermediate_node == destination:
                    shortest = dist
                    break
                other_dist = label_dest.get(intermediate_node)
                if other_dist is None:
                    continue
                if other_dist + dist < shortest:
                    shortest = other_dist + dist
            s_distances[destination] = shortest
        distances[start] = s_distances
    return distances

def make_link(G, node1, node2, weight=1):
    if node1 not in G:
        G[node1] = {}
    (G[node1])[node2] = weight
    if node2 not in G:
        G[node2] = {}
    (G[node2])[node1] = weight
    return G

def test():
    edges = [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7),
             (4, 8), (4, 9), (5, 10), (5, 11), (6, 12), (6, 13)]
    tree = {}
    for n1, n2 in edges:
        make_link(tree, n1, n2)
    print "tree",tree
    labels = create_labels(tree, 1)
    print "labels",labels
    distances = get_distances(tree, labels)

    assert distances[1][2] == 1
    assert distances[1][4] == 2


test()
