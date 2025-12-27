import heapq  # 用于实现优先队列
import time
class Node:
    def __init__(self, parent, state, g, h):
        self.parent = parent    # 父节点（用于回溯路径）
        self.state = state      # 当前状态（一维列表）
        self.g = g              # 从起点到当前节点的实际代价（步数）
        self.h = h              # 启发式估计代价（到目标的预估距离）
        self.f = g + h          # 估价函数 f(n) = g(n) + h(n)
    
    # 定义比较运算符（用于优先队列排序）
    def __lt__(self, other):
        return self.f < other.f

class AStar:
    def __init__(self, originalNode, targetNode, length):
        self.originalNode = originalNode  # 初始状态节点
        self.targetNode = targetNode      # 目标状态节点
        self.open = []                    # 优先队列（最小堆）
        heapq.heappush(self.open, originalNode)
        self.close = set()                # 关闭列表（用集合去重）
        self.spce = [-3, 3, -1, 1]        # 上下左右移动方向
        self.length = length              # 棋盘边长（八数码为3）

    # 计算曼哈顿距离（启发式函数）
    def manhattan_distance(self, state):
        distance = 0
        for num in range(1, 9):  # 忽略空白格（0）
            # 当前状态中数字的位置
            x1, y1 = divmod(state.index(num), self.length)
            # 目标状态中数字的位置
            x2, y2 = divmod(self.targetNode.state.index(num), self.length)
            distance += abs(x1 - x2) + abs(y1 - y2)
        return distance

    # 检查节点是否在开放或关闭列表中
    def is_in_table(self, state):
        return tuple(state) in self.close

    # 复制状态（避免修改原状态）
    def copy_array(self, state):
        return state.copy()

    def showLine(self):
        endState = self.open[-1]  # 获取最终状态
        road = [endState]  # 存储路径的列表

        # 回溯父节点直到根节点
        while(True):
            if(endState.parent):
                endState = endState.parent
                road.append(endState)
            else:
                break
        road.reverse()  # 反转列表得到从初始到目标的顺序

        # 打印路径中的每个状态
        for j in road:
            for i in range(0, 3):
                print(j.state[i*3: i*3+3])

            print('->')

    # A*搜索算法
    def search(self):
        while self.open:
            current_node = heapq.heappop(self.open)  # 取出f值最小的节点
            blank_pos = current_node.state.index(0)  # 空白格位置

            if current_node.state == self.targetNode.state:
                return True  # 找到解

            self.close.add(tuple(current_node.state))  # 加入关闭列表

            # 尝试四个移动方向
            for move in self.spce:
                # 检查移动是否合法
                if (move == -3 and blank_pos + move >= 0) or \
                   (move == 3 and blank_pos + move < len(current_node.state)) or \
                   (move == -1 and blank_pos % self.length != 0) or \
                   (move == 1 and (blank_pos + 1) % self.length != 0):
                    
                    new_state = self.copy_array(current_node.state)
                    # 交换空白格和相邻数字
                    new_state[blank_pos], new_state[blank_pos + move] = new_state[blank_pos + move], new_state[blank_pos]
                    
                    if tuple(new_state) not in self.close:
                        # 计算新节点的g和h值
                        new_g = current_node.g + 1  # 每步代价为1
                        new_h = self.manhattan_distance(new_state)
                        new_node = Node(current_node, new_state, new_g, new_h)
                        
                        # 检查是否在开放列表中（需更新更优路径）
                        in_open = False
                        for node in self.open:
                            if node.state == new_state and node.g > new_g:
                                node.g = new_g
                                node.f = new_g + node.h
                                heapq.heapify(self.open)  # 更新堆结构
                                in_open = True
                                break
                        
                        if not in_open:
                            heapq.heappush(self.open, new_node)

        return False  # 无解

def calculate_manhattan_distance(state, target_state, length):
    """计算曼哈顿距离启发式值"""
    distance = 0
    for num in range(1, 9):  # 对数字1-8进行计算（忽略空白格0）
        # 获取数字在当前状态和目标状态中的位置
        current_pos = state.index(num)
        target_pos = target_state.index(num)
        
        # 计算行和列的差值
        row_diff = abs(current_pos // length - target_pos // length)
        col_diff = abs(current_pos % length - target_pos % length)
        
        distance += row_diff + col_diff
    
    return distance

if __name__=='__main__':
    #A*算法
    originate=[2,8,3,1,6,4,7,0,5]
    target=[1,2,3,7,8,4,0,6,5]
    h_start = calculate_manhattan_distance(originate, target, 3)  # 结果为5    
    node1 = Node(None, originate, 0, h_start)
    node2 = Node(None, target, 0, 0)
    astar=AStar(node1,node2,3)
    Now_d=time.time()
    flag_d=astar.search()
    end_d=time.time()
    Now_b=time.time()
    end_b=time.time()
    cost_d=end_d-Now_d
    cost_b=end_b-Now_b
    if(flag_d):
        print('A*算法:已经找到路径')
        astar.showLine()
        print('A*算法共用时%f秒\n\n' %(cost_d))
    else:
        print('未找到路径')