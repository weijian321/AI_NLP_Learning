# -*- coding: UTF-8 -*-

graph = {
    'A': 'B B B C',
    'B': 'A C',
    'C': 'A B D E',
    'D': 'C',
    'E': 'C F',
    'F': 'E'
}
for k in graph:
    graph[k] = set(graph[k].split())
#for element in set('1 2 3 4 5 6 7 8 9 10 100000 元素'.split()):
#    print(element)
#print graph
need_visited = ['A']
seen = set()
while need_visited:
    node = need_visited.pop(0)
    if node in seen:
        continue
    print('   I am looking at : {}'.format(node))
    need_visited += graph[node]

    seen.add(node)
