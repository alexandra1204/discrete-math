import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

# Исходные данные
edges = [(4, 6), (2, 14), (5, 14), (7, 14), (10, 14), (7, 16), (6, 9),
         (3, 16), (6, 7), (3, 14), (12, 14), (9, 14), (2, 6), (6, 12),
         (6, 15), (10, 16), (13, 14), (2, 16), (13, 16), (3, 6),
         (9, 16), (6, 10), (11, 14), (6, 13), (6, 8), (4, 16),
         (6, 11), (5, 6), (11, 16), (14, 15), (12, 16), (8, 16),
         (5, 16), (8, 14), (15, 16)]

##
from collections import deque


def is_bipartite(graph, n):
    color = [-1] * (n + 1)
    queue = deque()
    color[2] = 0  # Начинаем с вершины 2 (можно любую)
    queue.append(2)

    while queue:
        u = queue.popleft()
        for v in graph[u]:
            if color[v] == -1:
                color[v] = color[u] ^ 1
                queue.append(v)
            elif color[v] == color[u]:
                return False, color
    return True, color


def max_flow_ford_fulkerson(graph, source, sink, n):
    parent = [-1] * (n + 1)
    max_flow = 0

    def bfs(residual_graph):
        visited = [False] * (n + 1)
        queue = deque()
        queue.append(source)
        visited[source] = True

        while queue:
            u = queue.popleft()
            for v, capacity in enumerate(residual_graph[u]):
                if not visited[v] and capacity > 0:
                    parent[v] = u
                    if v == sink:
                        return True
                    queue.append(v)
                    visited[v] = True
        return False

    residual_graph = [row[:] for row in graph]

    while bfs(residual_graph):
        path_flow = float('inf')
        v = sink
        while v != source:
            u = parent[v]
            path_flow = min(path_flow, residual_graph[u][v])
            v = u

        v = sink
        while v != source:
            u = parent[v]
            residual_graph[u][v] -= path_flow
            residual_graph[v][u] += path_flow
            v = u

        max_flow += path_flow

    return max_flow


# Пример использования:


n = max(max(u, v) for u, v in edges)  # Максимальный номер вершины
graph = [[] for _ in range(n + 1)]
for u, v in edges:
    graph[u].append(v)
    graph[v].append(u)

is_bip, color = is_bipartite(graph, n)
# if is_bip:
#     #print("Граф двудольный")
# else:
#     print("Граф не двудольный. Нужно удалить рёбра между вершинами одного цвета.")

# Если граф двудольный, строим максимальное паросочетание
if is_bip:
    # Создаём матрицу смежности для Форда-Фалкерсона
    size = n + 2
    flow_graph = [[0] * size for _ in range(size)]
    source, sink = 0, size - 1

    # Связываем source с U, V с sink
    U = [u for u in range(1, n + 1) if color[u] == 0]
    V = [v for v in range(1, n + 1) if color[v] == 1]

    for u in U:
        flow_graph[source][u] = 1
    for v in V:
        flow_graph[v][sink] = 1

    # Добавляем рёбра графа
    for u, v in edges:
        if color[u] == 0 and color[v] == 1:
            flow_graph[u][v] = 1

    max_matching = max_flow_ford_fulkerson(flow_graph, source, sink, size - 1)
    print(f"Максимальное паросочетание (Форд-Фалкерсон): {max_matching}")
##
# 1. Проверка двудольности графа
def is_bipartite(edges):
    # Создаем граф
    G = nx.Graph()
    G.add_edges_from(edges)

    # Проверяем двудольность
    try:
        color = nx.bipartite.color(G)
        return True, color
    except nx.NetworkXError:
        return False, None


#2.1

# 2.2 Поиск максимального паросочетания (алгоритм Куна)
def kuhn_matching(edges):
    G = nx.Graph()
    G.add_edges_from(edges)

    # Проверяем двудольность
    is_bip, color = is_bipartite(edges)
    if not is_bip:
        return None

    # Разделяем вершины на две доли
    left = [node for node in G.nodes() if color[node] == 0]
    right = [node for node in G.nodes() if color[node] == 1]

    # Создаем направленный граф для алгоритма Куна
    D = nx.DiGraph()
    for u, v in edges:
        if color[u] == 0 and color[v] == 1:
            D.add_edge(u, v)
        elif color[u] == 1 and color[v] == 0:
            D.add_edge(v, u)

    # Применяем алгоритм Куна
    matching = nx.bipartite.maximum_matching(G, left)

    # Форматируем результат
    matching_edges = []
    for u in left:
        if u in matching:
            matching_edges.append((u, matching[u]))

    return matching_edges


# 3. Визуализация графа с паросочетанием
def visualize_graph(edges, matching_edges=None, color=None):
    G = nx.Graph()
    G.add_edges_from(edges)

    # Позиционирование вершин
    if color:
        # Для двудольного графа
        left = [node for node in G.nodes() if color[node] == 0]
        pos = nx.bipartite_layout(G, left)
    else:
        # Для произвольного графа
        pos = nx.spring_layout(G)

    # Цвета вершин
    node_colors = []
    if color:
        node_colors = ['lightblue' if color[node] == 0 else 'lightgreen' for node in G.nodes()]
    else:
        node_colors = 'lightgray'

    # Цвета ребер
    edge_colors = []
    if matching_edges:
        edge_colors = ['red' if (u, v) in matching_edges or (v, u) in matching_edges
                       else 'gray' for u, v in G.edges()]
    else:
        edge_colors = 'gray'

    # Рисуем граф
    plt.figure(figsize=(10, 8))
    nx.draw(G, pos,
            with_labels=True,
            node_color=node_colors,
            edge_color=edge_colors,
            node_size=800,
            font_size=12,
            width=2)

    if matching_edges:
        plt.title("Максимальное паросочетание (красные ребра)")
    elif color:
        plt.title("Двудольный граф")
    else:
        plt.title("Исходный граф")

    plt.show()


# Основная программа
if __name__ == "__main__":
    # Проверяем двудольность
    is_bip, color = is_bipartite(edges)

    if is_bip:
        print("Граф двудольный")

        # Находим максимальное паросочетание
        matching = kuhn_matching(edges)
        print(f"Максимальное паросочетание (алгоритм Куна) ({len(matching)} ребер):")
        for edge in matching:
            print(edge)


        # Визуализируем
        visualize_graph(edges, matching, color)
    else:
        print("Граф не двудольный")

        # Визуализируем без паросочетания
        visualize_graph(edges)

        # Находим конфликтные ребра
        G = nx.Graph()
        G.add_edges_from(edges)
        try:
            # Эта попытка раскраски поможет найти конфликтные ребра
            color = nx.bipartite.color(G)
        except nx.NetworkXError as e:
            print("Конфликтные ребра (которые нужно удалить):")
            # Простая проверка - находим все ребра между вершинами одного цвета
            # (это не оптимальное решение, но дает представление)
            temp_color = {}
            queue = deque([next(iter(G.nodes()))])
            temp_color[queue[0]] = 0
            conflict_edges = []

            while queue:
                u = queue.popleft()
                for v in G.neighbors(u):
                    if v not in temp_color:
                        temp_color[v] = 1 - temp_color[u]
                        queue.append(v)
                    elif temp_color[v] == temp_color[u]:
                        if (u, v) not in conflict_edges and (v, u) not in conflict_edges:
                            conflict_edges.append((u, v))

            for edge in conflict_edges:
                print(edge)

