import numpy as np
import copy


class Node:
    def __init__(self, nid, par, dis):
        self.nid = nid  # node id
        self.par = par  # parent reference
        self.dis = dis  # distance up to this node

    def __repr__(self):
        return "%d<-%d, dis:%.3f" % (self.nid, self.par.nid, self.dis)

def readGraph(graph_f):
    edges = np.loadtxt(graph_f)
    G = {}
    for i in range(len(edges)):
        if edges[i,0] not in G:
            G[edges[i,0]] = [(edges[i,1],edges[i,2])]
        else:
            G[edges[i,0]].append((edges[i,1],edges[i,2]))
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

    final_set = []  # for the final found routes set
    while len(Q)>0:
        # First get all the candidates in next layer
        QQ = []  
        for node in Q:
            for neibids,dd in G[node.nid]:
                neinode = Node(neibids, node, node.dis+dd)
                QQ.append(neinode)

        newQQ = []
        for i in range(len(QQ)):
            node = QQ[i]
            if node.nid == v:
                if abs(node.dis-d) < 0.05*d:
                    route = traceBack(node)[::-1]
                    final_set.append(route)
            else:
                if node.dis < d:  # can be considered
                    newQQ.append(node)
        Q = newQQ
    return final_set


def twowayBFS(G, v, d):
    """Find a set of routes starting at v end at v with distance d"""
    node = Node(v, None, 0)
    Q = [[node]]
    final_set = []  # for the final found routes set

    while len(Q)>0:
        # First get all the candidates in next layer
        QQ = []  
        for oneset in Q:
            for node in oneset:
                tmpQ = []
                for neibid,dd in G[node.nid]:
                    if neibid == v:
                        continue
                    else:
                        neinode = Node(neibid, node, node.dis+dd)
                        tmpQ.append(neinode)
                QQ.append(tmpQ)

        newQQ = [] 
        for i in range(len(QQ)):
            oneset = QQ[i]
            tmpset = []
            for node in oneset:
                if node.dis > d:  # already too long
                    continue
                else:
                    tmpset.append(node)
                for j in range(i+1,len(QQ)):
                    otherset = QQ[j]
                    for other in otherset:
                        if node.nid == other.nid:
                            if abs(node.dis+other.dis-d)<0.05*d:
                                # found a join point
                                part1 = traceBack(node)[::-1]
                                part2 = traceBack(other)
                                route = part1+part2[1:]
                                final_set.append(route)
            newQQ.append(tmpset)
        Q = newQQ        
    return final_set

def rankRoute(route_set):
    nodeCount = []
    for route in route_set:
        nodeCount.append(len(set(route)))
    inds = sorted(range(len(nodeCount)), key=lambda k: nodeCount[k])[::-1]
    return [route_set[i] for i in inds]

def main():
    #G = readGraph('test_g.txt')
    #route_set = twowayBFS(G, 1, 6)
    
    G = readGraph('../mapAndNode/result/map_info.txt')
    route_set = naiveBFS(G, 73819, 5000)
    route_set = rankRoute(route_set)
    print route_set


if __name__ == "__main__":
    main()
