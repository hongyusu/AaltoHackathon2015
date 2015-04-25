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
    distances = []
    final_set = []  # for the final found routes set
    while len(Q)>0 and len(final_set)<100:
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
                    if node.dis in distances:
                        continue
                    distances.append(node.dis)
                    print "found route with lenght",node.dis
                    route = traceBack(node)[::-1]
                    final_set.append(route)
            else:
                if node.dis < d:  # can be considered
                    newQQ.append(node)
        Q = newQQ
    return final_set, distances


def twowayBFS(G, v, d):
    """Find a set of routes starting at v end at v with distance d"""
    node = Node(v, None, 0)
    Q = [[node]]
    final_set = []  # for the final found routes set
    distances = []
    while len(Q) > 0 or len(final_set)<100:
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
                            if abs(node.dis+other.dis-d)<0.01*d:
                                if node.dis+other.dis in distances:
                                    continue
                                # found a join point
                                print "Found",node.dis+other.dis
                                part1 = traceBack(node)[::-1]
                                part2 = traceBack(other)
                                route = part1+part2[1:]
                                final_set.append(route)

            newQQ.append(tmpset)
        Q = newQQ        
    return final_set

def rankRoute(route_set,dis):
    nodeCount = []
    for route in route_set:
        nodeCount.append(len(set(route)))
    inds = sorted(range(len(nodeCount)), key=lambda k: nodeCount[k])[::-1]
    return [route_set[i] for i in inds],[dis[i] for i in inds]

def main(uid, dis):
    #G = readGraph('test_g.txt')
    #route_set = twowayBFS(G, 1, 6)
    fname = "%d_%d_all_routes.txt" % (uid, dis)
    G = readGraph('../mapAndNode/result/map_info.txt')
    route_set, distances = naiveBFS(G, uid, dis)
    #route_set = twowayBFS(G, 134, 5000)
    route_set, distances = rankRoute(route_set, distances)
    n_candis = len(route_set)
    
    if len(route_set) > 10:
        inds = np.random.randint(0,n_candis,10)
        final_set = [route_set[i] for i in inds]
        final_dis = [distances[i] for i in inds]
    else:
        final_set = route_set
        final_dis = distances
        
    w = open(fname,'w')
    n_path = len(final_set)    
    for i in range(n_path):
        route = final_set[i]
        d = final_dis[i]
        w.write(str(d)+" "+" ".join(map(str,route))+"\n")
    w.close()

def test():
    G = readGraph('../mapAndNode/result/map_info.txt')
    routes = open('134_3000_all_routes.txt').read().split("\n")
    route = routes[0]
    route = route.split(' ')
    print route[0]
    route = map(int,map(float,route[1:]))
    start = route[0]
    
    dis = 0
    for i in range(1,len(route)):
        cur = route[i]
        for n,d in G[start]:
            if n == cur:
                dis = dis + d
                print start,cur,dis
        start = cur
    print dis

if __name__ == "__main__":
    #main(134, 3000)
    #main(134, 5000)
    test()
