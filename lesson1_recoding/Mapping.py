# -*- coding: UTF-8 -*-
import networkx
import matplotlib.pyplot as plt


BJ = 'Beijing'
SZ = 'Shenzhen'
GZ = 'Guangzhou'
WH = 'Wuhan'
HLG = 'Heilongjiang'
NY = 'New York City'
CM = 'Chiangmai'
SG = 'Singapore'
air_route = {BJ: {SZ, GZ, WH, HLG, NY}, GZ: {WH, BJ, CM, SG}, SZ: {BJ, SG}, WH: {BJ, GZ}, HLG: {BJ}, CM: {GZ}, NY: {BJ}}

air_route = networkx.Graph(air_route)  # type: Graph
# matplotlib inline
networkx.draw(air_route, with_labels=True)
#plt.show()


def search_desitination(graph, start, destination):
    pathes = [[start]]
    seen = set(start)  # type: Set[Any]
    choosen_pathes = []
    pathes_steps = 100
    while pathes:
        path = pathes.pop(0)
        froniter = path[-1]
        # get new lines

        for city in graph[froniter]:
            if city in path:
                continue
            new_path = path + [city]
            pathes.append(new_path)
            if city == destination:
                if len(new_path) < pathes_steps:
                    pathes_steps = len(new_path)
                    choosen_pathes = [new_path]
                else:
                    if len(new_path) == pathes_steps:
                        choosen_pathes.append(new_path)
    return choosen_pathes


def draw_route(pathes):
    while pathes:
        path = pathes.pop(0)
        print ' ✈️ -> '.join(path)

draw_route(search_desitination(air_route, SG, HLG))  #NY, SG))
