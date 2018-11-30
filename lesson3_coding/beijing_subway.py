# -*- coding: UTF-8 -*-

import re
from bs4 import BeautifulSoup
import urllib.request
import bs4
import requests
import csv
import networkx as nx
import matplotlib.pyplot as plt
from pylab import *


mpl.rcParams['font.sans-serif'] = ['SimHei']


url = 'https://www.bjsubway.com/e/action/ListInfo/?classid=39&ph=1'
response = urllib.request.urlopen(url)
page = response.read()
soup = BeautifulSoup(page, 'html.parser')
tables = soup.find_all('table')
print(len(tables))
subway_stations = {}
for table in tables:
    subway_name = re.findall('\s*(.*?线.*?)首末车时刻表', table.text)
    stations = []
    if subway_name:
        trs = table.find_all('tr')
        print(trs)
    else:
        break
    for tr in trs:
        print('tr.text:\n', tr.text)

        station_tuple = re.findall('(\w+)[\n|\s]+(\d+:\d+|――)[\n|\s]+(\d+:\d+|――)', tr.text)
        if station_tuple:
            print('station:\n', type(station_tuple[0]), station_tuple[0])
            station = list(station_tuple[0])[0]
            print('station:\n', station)
            stations.append(station)
    # print('station:\n', stations)
    # print(type(subway_name[0]), subway_name[0])
    # print(type(subway_name), stations)
    subway_stations[subway_name[0]] = stations
    print(subway_stations)
subway_net = nx.Graph()
for subway_name in subway_stations:
    subway_net.add_nodes_from(subway_stations[subway_name])
    for i in range(len(subway_stations[subway_name]) - 1):
        subway_net.add_edge(subway_stations[subway_name][i], subway_stations[subway_name][i + 1])
nx.draw(subway_net, with_labels=True, node_size=10)
plt.show()


def min_station(pathes):
    pathes0 = sorted(pathes, key=lambda p: len(p))
    pathes_best = []
    for path in pathes0:
        if len(path) == len(pathes0[0]):
            pathes_best.append(path)
        else:
            break
    return pathes_best


# def min_change_station(pathes):
#     pathes0 = sorted(pathes, key=lambda p: len(p))
#     pathes_best = []
#     for path in pathes0:
#         if len(path) == len(pathes0[0]):
#             pathes_best.append(path)
#         else:
#             break
#     return pathes_best

def search_pathes(graph,start, destination, stratigy_func):
    pathes = [[start]]
    seen = []
    chosen_pathes = []
    while pathes:
        path = pathes.pop(0)
        frontier = path[-1]
        if frontier in seen:
            continue
        else:
            seen.append(frontier)

        for c2 in graph[frontier]:
            if c2 in seen:
                continue
            new_path = path + [c2]
            pathes.append(new_path)
            if c2 == destination:
                chosen_pathes.append(new_path)

    return stratigy_func(chosen_pathes)


start,destination = input('please input [start] [destination]:').split()
print('best_path:\n', search_pathes(subway_net, start, destination, min_station))
