# coding=utf-8
import re
# import json
import math
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib
from collections import defaultdict
from pylab import *


mpl.rcParams['font.sans-serif'] = ['SimHei']

coordination_source = """
{name:'兰州', geoCoord:[103.73, 36.03]},
{name:'嘉峪关', geoCoord:[98.17, 39.47]},
{name:'西宁', geoCoord:[101.74, 36.56]},
{name:'成都', geoCoord:[104.06, 30.67]},
{name:'石家庄', geoCoord:[114.48, 38.03]},
{name:'拉萨', geoCoord:[102.73, 25.04]},
{name:'贵阳', geoCoord:[106.71, 26.57]},
{name:'武汉', geoCoord:[114.31, 30.52]},
{name:'郑州', geoCoord:[113.65, 34.76]},
{name:'济南', geoCoord:[117, 36.65]},
{name:'南京', geoCoord:[118.78, 32.04]},
{name:'合肥', geoCoord:[117.27, 31.86]},
{name:'杭州', geoCoord:[120.19, 30.26]},
{name:'南昌', geoCoord:[115.89, 28.68]},
{name:'福州', geoCoord:[119.3, 26.08]},
{name:'广州', geoCoord:[113.23, 23.16]},
{name:'长沙', geoCoord:[113, 28.21]},
//{name:'海口', geoCoord:[110.35, 20.02]},
{name:'沈阳', geoCoord:[123.38, 41.8]},
{name:'长春', geoCoord:[125.35, 43.88]},
{name:'哈尔滨', geoCoord:[126.63, 45.75]},
{name:'太原', geoCoord:[112.53, 37.87]},
{name:'西安', geoCoord:[108.95, 34.27]},
//{name:'台湾', geoCoord:[121.30, 25.03]},
{name:'北京', geoCoord:[116.46, 39.92]},
{name:'上海', geoCoord:[121.48, 31.22]},
{name:'重庆', geoCoord:[106.54, 29.59]},
{name:'天津', geoCoord:[117.2, 39.13]},
{name:'呼和浩特', geoCoord:[111.65, 40.82]},
{name:'南宁', geoCoord:[108.33, 22.84]},
//{name:'西藏', geoCoord:[91.11, 29.97]},
{name:'银川', geoCoord:[106.27, 38.47]},
{name:'乌鲁木齐', geoCoord:[87.68, 43.77]},
{name:'香港', geoCoord:[114.17, 22.28]},
{name:'澳门', geoCoord:[113.54, 22.19]}
"""

city_information = {}

for line in coordination_source.split('\n'):
    if not line.strip() or line.startswith('//'): continue

    city = re.findall("name:'(\w+)'", line)
    x_y = re.findall("Coord:\[(\d+.\d+),\s(\d+.\d+)\]", line)[0]
    x_y = tuple(map(float, x_y))
    city_information[city[0]] = x_y
    print('\t', city)  # json.dumps(city, encoding='UTF-8', ensure_ascii=False)
    # print('\t', city)
    print('\t', x_y)
# print json.dumps(city_information, encoding='UTF-8', ensure_ascii=False)


def geo_distance(origin, destination):
    """
    Calculate the Haversine distance.

    Parameters
    ----------
    origin : tuple of float
        (lat, long)
    destination : tuple of float
        (lat, long)

    Returns
    -------
    distance_in_km : float

    Examples
    --------
    > origin = (48.1372, 11.5756)  # Munich
    > destination = (52.5186, 13.4083)  # Berlin
    > round(distance(origin, destination), 1)
    504.2
    """
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371  # km

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) * math.sin(dlat / 2) +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) * math.sin(dlon / 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = radius * c

    return d


def get_city_distance(city1, city2):
    return geo_distance(city_information[city1], city_information[city2])


# print get_city_distance(u"上海", u"杭州")
cities = list(city_information.keys())
# print(type(cities))
# G = nx.Graph(city_information)

# G = nx.Graph()
# G.add_nodes_from(cities)
# nx.draw(G, city_information, with_labels=True, node_size=10)
# plt.show()

d_threshold = 700
city_connections = defaultdict(list)
for c0 in cities:
    for c1 in cities:
        if c1 == c0:
            continue
        if get_city_distance(c0, c1) < d_threshold:
            city_connections[c0].append(c1)
print('city_connections:\n', city_connections)


G = nx.Graph(city_connections)
nx.draw(G, city_information, with_labels=True, node_size=10)
plt.show()


def get_path_distance(path):
    distance = 0
    for num in range(len(path) - 1):
        distance += get_city_distance(path[num], path[num + 1])
    return distance


def min_change_station(pathes):
    pathes0 = sorted(pathes, key=lambda p: len(p))
    pathes_best = []
    for path in pathes0:
        if len(path) == len(pathes0[0]):
            pathes_best.append(path)
        else:
            break
    return pathes_best


def min_distance(pathes):
    pathes0 = sorted(pathes, key=lambda p: get_path_distance(p))
    pathes_best = []
    for path in pathes0:
        if get_path_distance(path) == get_path_distance(pathes0[0]):
            pathes_best.append(path)
        else:
            break
    return pathes_best


def comprehensive_sort(pathes):
    pathes0 = sorted(pathes, key=lambda p: len(p) + get_path_distance(p))
    pathes_best = []
    for path in pathes0:
        if len(path) + get_path_distance(path) == len(pathes0[0]) + get_path_distance(pathes0[0]):
            pathes_best.append(path)
        else:
            break
    return pathes_best


def search_pathes(start, destination, stratigy_func):
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

        for c2 in city_connections[frontier]:
            if c2 in seen:
                continue
            new_path = path + [c2]
            pathes.append(new_path)
            if c2 == destination:
                chosen_pathes.append(new_path)

    return stratigy_func(chosen_pathes)


print('best_path:\n', search_pathes('杭州', '拉萨', min_change_station))

print('best_path:\n', search_pathes('杭州', '拉萨', min_distance))

print('best_path:\n', search_pathes('杭州', '拉萨', comprehensive_sort))
