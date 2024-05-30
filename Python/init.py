import enum
class PointArray(object):
    def __init__(self,x:int,y:int,f:int,g:int,state,father,rectangle):
        self.x = x
        self.y = y

        #A*寻路方法
        self.f=f
        self.g=g
        self.father = father
        
        #状态信息
        self.state = state
        self.rectangle = rectangle


class PointState(enum.Enum):
    #Astar
    # 障碍物
    BARRIER = 'black'
    # 未使用
    UNUSED = 'white'
    # 在open list的方格
    OPEN = 'gold'
    # 在close list的方格
    CLOSED='yellow'
    # 路径
    PATH = 'orangered'
    #起始格子
    START = 'green'
    #终止格子
    END = 'blue'

    #BFS
    QUEUE='darkgray'
