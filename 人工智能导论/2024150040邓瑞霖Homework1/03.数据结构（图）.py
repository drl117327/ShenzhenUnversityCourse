class Graph:
    def __init__(self, n:int):
        self.adjacency_list = [0]*(n+1)

    # 添加顶点
    def add_vertex(self, vertex):
        self.adjacency_list.append(vertex)
        self.adjacency_list[vertex] = []

    # 添加无向边
    def add_edge(self, vertex1, vertex2):
        self.adjacency_list[vertex1].append(vertex2)
        self.adjacency_list[vertex2].append(vertex1)

    # 广度优先搜索
    def bfs(self, start_vertex):
        visited = [0]*len(self.adjacency_list)
        queue = [start_vertex]

        while len(queue) > 0:
            vertex = queue[0]
            queue = queue[1:]
            if visited[vertex] == 1:
                continue
            visited[vertex] = 1
            print(vertex, end=' ')
            for neighbor in self.adjacency_list[vertex]:
                if visited[neighbor] == 0:
                    queue.append(neighbor)

if __name__ == '__main__':
    n, m = (input().split())
    n = int(n)
    m = int(m)
    graph = Graph(n)
    for i in range(1, n+1):
        graph.add_vertex(i)


    for i in range(m):
        u, v = input().split()
        u = int(u)
        v = int(v)
        graph.add_edge(u, v)

    graph.bfs(1)