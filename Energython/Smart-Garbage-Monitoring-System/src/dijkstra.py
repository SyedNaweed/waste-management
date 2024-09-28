import heapq

def dijkstra(graph, start, end):
    node_data = {}
    for node in graph:
        node_data[node] = {'cost': float('inf'), 'pred': []}

    node_data[start]['cost'] = 0
    visited = set()
    pq = [(0, start)]

    while pq:
        current_cost, current_vertex = heapq.heappop(pq)

        if current_vertex not in visited: 
            visited.add(current_vertex)     

        for neighbor in graph[current_vertex]['neighbors']:
            if neighbor not in visited: 
                cost = current_cost + graph[current_vertex]['neighbors'][neighbor]

                if cost < node_data[neighbor]['cost']:
                    node_data[neighbor]['cost'] = cost
                    node_data[neighbor]['pred'] = node_data[current_vertex]['pred'] + [current_vertex]

                    if neighbor == end:
                        return cost, node_data[current_vertex]['pred'] + [current_vertex]

                heapq.heappush(pq, (cost, neighbor))

    return None
