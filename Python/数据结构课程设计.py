# -*- coding: utf-8 -*-
from tkinter import *
import enum
import heapq
import time
import _thread
#添加修改起点，终点的功能，以及默认图形地点等功能

class PointState(enum.Enum):
    # 障碍物
    BARRIER = 'black'
    # 未使用
    UNUSED = 'white'
    # 在open list的方格
    OPEN = 'gold'
    # 在close list的方格
    CLOSED = 'darkgray'
    # 路径
    PATH = 'orangered'


class MiniMap:
    class Point:
        def __init__(self, x, y, f, g, father, state, rectangle):
            # x坐标
            self.x = x
            # y坐标
            self.y = y
            # f = g + h, h为预估代价，这里使用曼哈顿距离
            self.f = f
            # 从寻路起点到这个点的代价
            self.g = g
            # 父节点
            self.father = father
            # 当前点状态
            self.state = state
            # 当前点对应画布上的矩形
            self.rectangle = rectangle

        # 重写比较，方便堆排序
        def __lt__(self, other):
            if self.f < other.f:
                return True
            else:
                return False

    def __init__(self, *args):
        # 高
        self.height = args[0]
        # 宽
        self.width = args[1]
        # 方格尺寸
        self.size = args[2]
        # 起点
        self.start = args[3]
        # 终点
        self.end = args[4]
        # 每次绘制的延迟时间
        self.delay = args[5]

        self.root = Tk()
        self.root.title('navigation')
        self.canvas = Canvas(self.root, width=self.width * self.size + 3, height=self.height * self.size + 3)
        # 生成方格集合
        self.points = self.generatePoints()
        # 生成网格
        self.generateMesh()

        self.canvas.bind('<Button-1>', self.createBarrier)
        self.canvas.bind('<Button-2>', self.cleanMap)
        self.canvas.bind('<Button-3>', self.navigation)

        self.canvas.pack(side=TOP, expand=YES, fill=BOTH)
        self.root.resizable(False, False)
        self.root.mainloop()

    def generatePoints(self):
        """
        初始化绘制用的方格集合
        设置每个方格的状态和对应的矩形
        """
        points = [[self.Point(x, y, 0, 0, None, PointState.UNUSED.value,
                              self.canvas.create_rectangle((x * self.size + 3, y * self.size + 3),
                                                           ((x + 1) * self.size + 3, (y + 1) * self.size + 3),
                                                           fill=PointState.UNUSED.value)) for y in range(self.height)]
                  for x in range(self.width)]
        return points

    def generateMesh(self):
        """
        绘制网格
        """
        for i in range(self.height + 1):
            self.canvas.create_line((3, i * self.size + 3), (self.width * self.size + 3, i * self.size + 3))
        for i in range(self.width + 1):
            self.canvas.create_line((i * self.size + 3, 3), (i * self.size + 3, self.height * self.size + 3))

    def createBarrier(self, event):
        """
        设置障碍/移除障碍
        通过鼠标点击位置更改对应方格的状态
        """
        x = int((event.x + 3) / self.size)
        y = int((event.y + 3) / self.size)
        if x < self.width and y < self.height:
            if self.points[x][y].state == PointState.BARRIER.value:
                self.changeState(self.points[x][y], PointState.UNUSED.value)
            else:
                self.changeState(self.points[x][y], PointState.BARRIER.value)

    def cleanMap(self, event):
        """
        清空画布
        """
        for i in range(self.width):
            for j in range(self.height):
                # 不清空障碍物（因为太难点了），不需要此功能则去掉判断
                if self.points[i][j].state != PointState.BARRIER.value:
                    self.changeState(self.points[i][j], PointState.UNUSED.value)

    def navigation(self, event):
        """
        新开一个线程调用寻路函数
        """
        _thread.start_new_thread(self.generatePath, (self.start, self.end))

    def changeState(self, point, state):
        """
        修改某一point的状态
        """
        point.state = state
        self.canvas.itemconfig(point.rectangle, fill=state)

    def generatePath(self, start, end):
        """
        开始寻路
        """
        xStart = start[0]
        yStart = start[1]
        xEnd = end[0]
        yEnd = end[1]

        # 用最小堆存点，使每次取出的点都预估代价最小
        heap = []
        # 两个set用于查找，存储坐标的二元组
        close_list = set()
        open_list = set()
        # 将起点加入open list,每格距离设置为10，是为了使斜着走时距离设置为14，方便计算
        heapq.heappush(heap, self.points[xStart][yStart])
        open_list.add((xStart, yStart))
        # 寻路循环
        while 1:
            # 从open list中取出代价最小点
            pMin = heapq.heappop(heap)
            open_list.remove((pMin.x, pMin.y))
            # 将这个点放入close list中
            close_list.add((pMin.x, pMin.y))
            self.changeState(self.points[pMin.x][pMin.y], PointState.CLOSED.value)
            # 遍历八个方向
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if i == 0 and j == 0:
                        continue
                    # 当前要判断的点的坐标
                    xCur = pMin.x + i
                    yCur = pMin.y + j
                    # 如果这个点越界则跳过
                    if xCur >= self.width or xCur < 0 or yCur >= self.height or yCur < 0:
                        continue
                    pCur = self.points[xCur][yCur]
                    # 这个点是否在pMin的非正方向（即四个角落）
                    isCorner = i != 0 and j != 0
                    if isCorner:
                        # 如果将要判断的斜角方向被阻挡则跳过（如将要判断东南方向，若东方或南方被阻挡，则跳过）
                        if self.points[xCur][pMin.y].state == PointState.BARRIER.value or \
                                self.points[pMin.x][yCur].state == PointState.BARRIER.value:
                            continue
                    # 如果在close list中出现或该点为障碍物则跳过判断
                    if (xCur, yCur) not in close_list and self.points[xCur][yCur].state != PointState.BARRIER.value:
                        # 如果在open list中
                        if (xCur, yCur) in open_list:
                            # 如果通过起点到pMin再到pCur的代价比起点到pCur的代价小，则更新pCur的代价，将pMin设置为pCur的父节点
                            if ((14 if isCorner else 10) + pMin.g) < pCur.g:
                                # 如果在角落，则pMin到pCur的代价为14，否则为10
                                pCur.g = pMin.g + (14 if isCorner else 10)
                                pCur.f = pCur.g + 10 * (abs(xEnd - xCur) + abs(yEnd - yCur))
                                pCur.father = pMin
                        # 如果不在open list中，则代表这个点第一次被访问，直接将pMin设置为pCur的父节点
                        else:
                            # 如果在角落，则pMin到pCur的代价为14，否则为10
                            pCur.g = pMin.g + (14 if isCorner else 10)
                            pCur.f = pCur.g + 10 * (abs(xEnd - xCur) + abs(yEnd - yCur))
                            pCur.father = pMin
                            self.changeState(pCur, PointState.OPEN.value)
                            # 将这个点加入open list
                            open_list.add((xCur, yCur))
                            heapq.heappush(heap, pCur)
            # 检测是否寻路完成
            if (xEnd, yEnd) in open_list:
                pNext = self.points[xEnd][yEnd]
                self.changeState(pNext, PointState.PATH.value)
                while pNext.father:
                    pNext = pNext.father
                    self.changeState(self.points[pNext.x][pNext.y], PointState.PATH.value)
                break
            # 如果寻路不完成但open list长度为0，则没有可达路径
            if len(open_list) == 0:
                print('Unreachable!')
                break
            # 等待绘制
            time.sleep(self.delay)


# 参数为地图高、宽、方格尺寸、起点坐标（0开始）、终点坐标（0开始）、延迟时间
demo = MiniMap(20, 30, 30, (0, 0), (29, 19), 0.05)
