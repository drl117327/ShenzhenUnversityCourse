import time

class Node:
    def __init__(self, parent, state, degree):
        self.parent = parent  # 父节点，用于回溯路径
        self.state = state  # 当前状态，用一维列表表示3x3的八数码棋盘
        self.degree = degree  # 当前节点的深度（移动步数）

# 深度优先搜索算法
class dfs:
    def __init__(self, originalNode, targetNode, MaxDegree, length):
        """
        originalNode:初始节点状态
        targetNode:目标节点状态
        MaxDegree:最大深度
        length:棋盘长度（八数码难题为3）
        """
        self.originalNode = originalNode
        self.targetNode = targetNode
        self.open = [self.originalNode]
        self.close = [self.originalNode]
        self.spce = [-3, 3, -1, 1]  # 上下左右四个移动方向
        self.MaxDegree = MaxDegree  # 深度限制，到达此深度未找到解便返回
        self.length = length

    # 判断是否有解
    def hasSolve(self):
        targetVer=self.getreVersNum(self.target.state)  # 目标状态的逆序数
        orinateVer=self.getreVersNum(self.origate.state)  # 初始状态的逆序数
        if(targetVer%2!=orinateVer%2):
            return False
        else:
            return True
        
    # 获取逆序数
    def getreVersNum(self, state):
        sum = 0
        for i in range(len(state)):
            if(state[i] == 0):
                continue
            else:
                for j in range(i):
                    if(state[j] > state[i]):
                        sum += 1
        
        return sum
    
    def copyArray(self, data):
        arr = []
        return arr + data
    
    # 检查节点是否在表中（开放或关闭列表）
    def isInTable(self, node, table):
        for i in table:
            if i.state == node.state and i.degree == node.degree:
                return True
        
        return False
    
    # 显示解决方案路径
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

    # 执行深度优先搜索
    def search(self):
        while(True):
            if(len(self.open)):  # 如果开放列表不为空
                extandState=self.open[-1]   # 获取栈顶节点（DFS特点）
                spacIndex=extandState.state.index(0)    # 找到空白格位置
                flag=False

                # 检查深度限制
                if(extandState.degree>=self.MaxDegree):
                    node=self.open.pop()
                    self.close.append(node)
                    continue
                else:
                     # 尝试四个移动方向
                    for i in range(len(self.spce)):
                        # 检查移动是否合法
                        if((i==0 and (spacIndex+self.spce[i])>=0) or
                        (i==1 and (spacIndex+self.spce[i])<len(extandState.state)-1)
                        or(i==2 and (spacIndex%self.length!=0 )) or
                        (i==3 and ((spacIndex+1)%self.length)!=0)):
                            state=self.copyArray(extandState.state)
                            #扩展状态
                            # 执行移动：交换空白格和目标位置
                            temp=state[spacIndex+self.spce[i]]
                            state[spacIndex+self.spce[i]]=0
                            state[spacIndex]=temp

                            # 创建新节点
                            nodeState=Node(extandState,state,extandState.degree+1)

                            # 检查是否达到目标状态
                            if(state==self.targetNode.state):
                                self.open.append(nodeState)
                                return True
                            elif( not self.isInTable(nodeState,self.close) and not self.isInTable(nodeState,self.open)):
                                self.open.append(nodeState)
                                flag=True
                            else:
                                continue
                    # 处理未成功扩展的情况        
                    if(not flag):
                        self.open.pop()
                    else:
                        self.close.append(extandState)
                        self.open.remove(extandState)
            else:
                return False

if __name__=='__main__':
    #深度优先算法
    originate=[2,8,3,1,6,4,7,0,5]
    target=[1,2,3,7,8,4,0,6,5]
    node1=Node(None,originate,0)
    node2=Node(None,target,0)
    depth=dfs(node1,node2,10,3)
    Now_d=time.time()
    flag_d=depth.search()
    end_d=time.time()
    Now_b=time.time()
    end_b=time.time()
    cost_d=end_d-Now_d
    cost_b=end_b-Now_b
    if(flag_d):
        print('深度优先算法:已经找到路径')
        depth.showLine()
        print('深度优先算法共用时%f秒\n\n' %(cost_d))
    else:
        print('未找到路径')