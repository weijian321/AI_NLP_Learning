# -*- coding: UTF-8 -*-
from functools import partial

graph_long = {
    '1': '2 7',
    '2': '3',
    '3': '4',
    '4': '5',
    '5': '6 10',
    '7': '8',
    '6': '5',
    '8': '9',
    '9': '10',
    '10': '5 11',
    '11': '12',
    '12': '11',
}
for n in graph_long:
    graph_long[n] = graph_long[n].split()

#print graph_long

def search(graph, concat_func):
    seen = set()
    need_visited = ['1']

    while need_visited:
        node = need_visited.pop(0)
        if node in seen:
            continue
        print('   I am looking at : {}'.format(node))
        seen.add(node)
        new_discoveried = graph[node]
        need_visited = concat_func(new_discoveried, need_visited)


def treat_new_discover_more_important(new_discoveried, need_visited):
    return new_discoveried + need_visited


def treat_already_discoveried_more_important(new_discoveried, need_visited):
    return need_visited + new_discoveried


#print 'BFS:\n'
#search(graph_long, treat_already_discoveried_more_important)
#print 'DFS:\n'
#search(graph_long, treat_new_discover_more_important)
dfs = partial(search, concat_func=treat_new_discover_more_important)
print 'dfs:\n'
dfs(graph_long)
bfs = partial(search, concat_func=treat_already_discoveried_more_important)
print 'dfs:\n'
bfs(graph_long)
