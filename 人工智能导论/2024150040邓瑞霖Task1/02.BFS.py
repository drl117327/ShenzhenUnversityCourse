import time

class Node:
    def __init__(self, parent, state, degree):
        self.parent = parent
        self.state = state
        self.degree = degree

# 广度优先算法
class bfs:
    def __init__(self,originaNode,targetNode,MaxDegree,length):
        """
        originalNode:初始节点状态
        targetNode:目标节点状态
        MaxDegree:最大深度
        length:棋盘长度（八数码难题为3）
        """
        self.originNode=originaNode
        self.targetNode=targetNode
        self.open=[self.originNode]
        self.close=[self.originNode]
        self.spce=[-3,3,-1,1] #上下左右四个移动方向
        self.MaxDegree=MaxDegree  #深度限制，到达此深度未找到解便返回
        self.length=length

    #判断是否有解
    def hasSolve(self):
        targetVer=self.getreVersNum(self.target.state)
        orinateVer=self.getreVersNum(self.origate.state)
        if(targetVer%2!=orinateVer%2):
            return False
        else:
            return True
    #获取逆序数
    def getreVersNum(self,state):
        sum=0
        for i in range(0,len(state)):
            if(state[i]==0):
                continue
            else:
                for j in range(0,i):
                    if(state[j]>state[i]):
                        sum+=1
        return sum

    def copyArray(self,state):
        arr=[]
        return arr+state

    def isInTable(self,node,table):
        for i in table:
            if i.state==node.state and i.degree==node.degree:
                return True
        return False

    def showLine(self):
        endState=self.open[-1]
        road=[endState]
        while(True):
            if(endState.parent):
                endState=endState.parent
                road.append(endState)
            else:
                break
        road.reverse()
        for j in road:
            for i in range(0,3):
                print(j.state[i*3:i*3+3])

            print('->')


    def search(self):
        """
        执行广度优先搜索(BFS)来求解八数码问题
        使用队列实现BFS（先进先出）
        """
        while len(self.open) > 0:  # 开放列表不为空时继续搜索
            # 从队列头部取出节点（FIFO）
            current_node = self.open.pop(0)
            # 找到空白格（0）的位置
            blank_pos = current_node.state.index(0)
            
            # 检查是否达到目标状态
            if current_node.state == self.targetNode.state:
                self.open.append(current_node)  # 将解节点加入队列（便于后续路径回溯）
                return True  # 找到解
            
            # 尝试四个移动方向（上、下、左、右）
            for move in self.spce:  # self.spce = [-3, 3, -1, 1]（上下左右）
                # 检查移动是否合法
                if (move == -3 and blank_pos + move >= 0) or \
                (move == 3 and blank_pos + move < len(current_node.state)) or \
                (move == -1 and blank_pos % self.length != 0) or \
                (move == 1 and (blank_pos + 1) % self.length != 0):
                    
                    # 复制当前状态，避免修改原状态
                    new_state = self.copyArray(current_node.state)
                    # 交换空白格和目标位置
                    new_state[blank_pos], new_state[blank_pos + move] = new_state[blank_pos + move], new_state[blank_pos]
                    
                    # 创建新节点
                    new_node = Node(current_node, new_state, current_node.degree + 1)
                    
                    # 检查新状态是否未被探索
                    if not self.isInTable(new_node, self.close) and not self.isInTable(new_node, self.open):
                        self.open.append(new_node)  # 新节点加入队列尾部（BFS关键）
            
            # 将当前节点标记为已探索
            self.close.append(current_node)
        
        return False  # 开放列表为空，无解
    
if __name__=='__main__':
    #广度优先算法
    originate=[2,8,3,1,6,4,7,0,5]
    target=[1,2,3,7,8,4,0,6,5]
    node1=Node(None,originate,0)
    node2=Node(None,target,0)
    breadth=bfs(node1,node2,10,3)
    Now_d=time.time()
    flag_d=breadth.search()
    end_d=time.time()
    Now_b=time.time()
    end_b=time.time()
    cost_d=end_d-Now_d
    cost_b=end_b-Now_b
    if(flag_d):
        print('广度优先算法:已经找到路径')
        breadth.showLine()
        print('广度优先算法共用时%f秒\n\n' %(cost_d))
    else:
        print('未找到路径')