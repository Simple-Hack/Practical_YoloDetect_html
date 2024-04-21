import enum
import time
import tkinter as tk
from tkinter import messagebox
import threading as th

class MyList(object):
    
    class Node(object):
        def __init__(self,value):
            self.value = value

            pass
         
    def __init__(self):
        self.next=None
        self.prev=None

        self.size=0

        self.head=None
        self.tail=None

    def search_value(self,index:int):
        
        pass

    def append(self,node:Node):

        pass
        
    def size(self)->int:
        return self.size


class PointArray(object):
    def __init__(self,x:int,y:int,f:int,g:int,state,father,rectangle):
        self.x = x
        self.y = y

        #A*寻路方法
        self.f=f
        self.g=g
        self.father = father
        
        #默认在可以选择格子的情况下，直接对角线走的话，代价小于两个水平垂直的格子的总和    
        #状态信息
        self.state = state
        self.rectangle = rectangle

class PathFindingAlgorithm(object):
    DIJKSTRA = "Dijkstra"
    ASTAR = 'A*'

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
    #起始格子
    START = 'red'
    #终止格子
    END = 'blue'

class DrawingMethod(object):

    def __init__(self,height:int,width:int,size:int):
        self.height = height
        self.width = width
        self.size = size

        self.start_point = None
        self.end_point = None

        self.points_list = []

        self.root = tk.Tk()
        self.root.title('Navigation')
        self.canvas = tk.Canvas(self.root, width=self.width * self.size + 3, height=self.height * self.size + 3)
        self.canvas.pack()

        self.canvas.bind("<Button-1>", self.on_left_click)
        self.canvas.bind("<Button-3>", self.on_right_click)

        self.draw_lattice()
        messagebox.showinfo('提示','左键选择起始点\n右键选择终止点')

        self.root.mainloop()

        

    def on_left_click(self, event):
        x, y = event.x - 3, event.y - 3  # 转换为相对于画布原点的坐标
        cell_x, cell_y = x // self.size, y // self.size

        if self.start_point is None and (cell_x,cell_y)!=self.end_point:
            self.set_start_point(cell_x, cell_y)
        elif (cell_x,cell_y)!=self.end_point and self.start_point==(cell_x,cell_y):
            if self.start_point:
                self.canvas.delete("start_point_rect")
                self.start_point = None
        if (cell_x,cell_y)==self.end_point:
            messagebox.showinfo('???','你在做什么?')
        self.confirm_selection()


    def on_right_click(self, event):
        x, y = event.x - 3, event.y - 3
        cell_x, cell_y = x // self.size, y // self.size

        if self.end_point is None and self.start_point != (cell_x, cell_y):  
            self.set_end_point(cell_x, cell_y)
        elif self.start_point!=(cell_x,cell_y) and self.end_point==(cell_x,cell_y):
            if self.end_point:
                self.canvas.delete("end_point_rect")
                self.end_point = None
        if (cell_x,cell_y)==self.start_point:
            messagebox.showinfo('???','你在做什么?')
        self.confirm_selection()
        
    def set_start_point(self, x: int, y: int):
        if self.start_point:
            self.canvas.delete("start_point_rect")
            self.start_point = None
        self.canvas.create_rectangle(x * self.size + 3, y * self.size + 3,
                                     (x + 1) * self.size + 2, (y + 1) * self.size + 2,
                                     fill="red",
                                     tags=("start_point_rect"))
        self.start_point = (x, y)

    def set_end_point(self, x: int, y: int):
        if self.end_point:
            self.canvas.delete("end_point_rect")
            self.end_point = None
        self.canvas.create_rectangle(x * self.size + 3, y * self.size + 3,
                                     (x + 1) * self.size + 2, (y + 1) * self.size + 2,
                                     fill="blue",
                                     tags=("end_point_rect",))  # 使用标签便于后续清除
        self.end_point = (x, y)

    def confirm_selection(self):
        if self.start_point is not None and self.end_point is not None:
            result=messagebox.askyesno("嗯?", "你确定?????")
            if not result:
                self.clear_points()
            else:
                self.canvas.unbind("<Button-1>")
                self.canvas.unbind("<Button-3>")
                messagebox.showinfo("提示","左键选择障碍物")
                self.generate_points()
                self.canvas.bind("<Button-1>",self.set_barriers)
        
        return False  


    def clear_points(self):
        if self.start_point:
            self.canvas.delete("start_point_rect")
            self.start_point = None
        if self.end_point:
            self.canvas.delete("end_point_rect")
            self.end_point = None

    def generate_points(self):

        for i in range(self.width):
            pre_list= []
            for j in range(self.height):
                if (i,j)==self.start_point:
                    pre_list.append(PointArray(i, j, 0, 0, PointState.START.value, None,
                              self.canvas.create_rectangle((i * self.size + 3, j * self.size + 3),
                                                           ((i + 1) * self.size + 3, (j + 1) * self.size + 3),
                                                             fill=PointState.START.value)))
                    
                    continue
                elif (i,j)==self.end_point:
                    pre_list.append(PointArray(i, j, 0, 0, PointState.END.value, None,
                              self.canvas.create_rectangle((i * self.size + 3, j * self.size + 3),
                                                           ((i + 1) * self.size + 3, (j + 1) * self.size + 3),
                                                             fill=PointState.END.value)))
                    continue
                pre_list.append(PointArray(i, j, 0, 0, PointState.UNUSED.value, None,
                              self.canvas.create_rectangle((i * self.size + 3, j * self.size + 3),
                                                           ((i + 1) * self.size + 3, (j + 1) * self.size + 3),
                                                             fill=PointState.UNUSED.value)))
            self.points_list.append(pre_list)
        

    def draw_lattice(self):
        for i in range(self.height + 1):
            self.canvas.create_line((3, i * self.size + 3), (self.width * self.size + 3, i * self.size + 3))
        for i in range(self.width + 1):
            self.canvas.create_line((i * self.size + 3, 3), (i * self.size + 3, self.height * self.size + 3))
        


    def set_barriers(self,event):
        x = int((event.x + 3) / self.size)
        y = int((event.y + 3) / self.size)
        if x < self.width and y < self.height:
            if self.points_list[x][y].state == PointState.BARRIER.value:
                self.points_list[x][y].state = PointState.UNUSED.value
                self.canvas.itemconfig(self.points_list[x][y].rectangle, fill=PointState.UNUSED.value)
            elif self.points_list[x][y].state == PointState.UNUSED.value:
                self.points_list[x][y].state = PointState.BARRIER.value
                self.canvas.itemconfig(self.points_list[x][y].rectangle, fill=PointState.BARRIER.value)
        

    def the_Astar_method(self):

        pass

    def the_Dijkstar_method(self):

        pass


    def draw_final_way(self):

        pass


draw=DrawingMethod(20,30,40)