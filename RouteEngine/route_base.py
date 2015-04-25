import numpy as np
import copy

class Node:
    def __init__(self, nid, par, dis):
        self.nid = nid  # node id
        self.par = par  # parent reference
        self.dis = dis  # distance up to this node

    def __repr__(self):
        return "%d<-%d:%.3f" % (self.nid, self.par.nid, self.dis)

def readGraph(graph_f):
    edges = np.loadtxt(graph_f)
    G = {}
    for i in range(len(edges)):
        if edges[i,0] not in G:
            G[edges[i,0]] = [(edges[i,1],edges[i,2])]
        else:
            G[edges[i,0]].append((edges[i,1],edges[i,2]))
        if edges[i,1] not in G:
            G[edges[i,1]] = [(edges[i,0],edges[i,2])]
        else:
            G[edges[i,1]].append((edges[i,0],edges[i,2]))
    return G

def traceBack(node):
    path = [node.nid]
    tmp = Node(node.nid, node.par, node.dis)
    while tmp.par is not None:
        path.append(tmp.par.nid)
        tmp = tmp.par
    return path
    

def naiveBFS(G, v, d):
    """Find a set of routes starting at v end at v with distance d"""
    node = Node(v, None, 0)
    Q = [node]

    final_set = []
    while len(Q)>0:
        QQ = []  # candidates in next layer
        for node in Q:
            for neibids,dd in G[node.nid]:
                neinode = Node(neibids, node, node.dis+dd)
                QQ.append(neinode)

        # first remove or collect those already come back
        newQQ = []
        for i in range(len(QQ)):
            node = QQ[i]
            if node.nid == v:
                if abs(node.dis-d) < 0.05*d:
                    route = traceBack(node)[::-1]
                    #print "Add directly", route
                    final_set.append(route)
            else:
                newQQ.append(node)
        QQ = newQQ

        # next remove too far route or collect route by join two path
        newQQ = []
        for i in range(len(QQ)):
            node = QQ[i]
            # test if can be pruned
            if node.nid != v and node.dis > 1.05*d:  # can be continued
                continue
            
            #for j in range(i+1,len(QQ)):
            #    other = QQ[j]
            #    if node.nid == other.nid:  #find a meeting point
            #        if abs((node.dis + other.dis) - d)<0.05*d:
            #            route = traceBack(node)[::-1]+traceBack(other.par)
            #            print "Add by join two path", route
            #            final_set.append(route)
            # if not be pruned and not collected
            newQQ.append(node)
        Q = newQQ
        #print "Final set:",final_set
    return final_set

def rankRoute(route_set):
    nodeCount = []
    for route in route_set:
        nodeCount.append(len(set(route)))
    inds = sorted(range(len(nodeCount)), key=lambda k: nodeCount[k])[::-1]
    return [route_set[i] for i in inds]

def main():
    G = readGraph('test_g.txt')
    route_set = naiveBFS(G,1,6)
    route_set = rankRoute(route_set)
    print route_set
if __name__ == "__main__":
    main()
