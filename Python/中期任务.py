import enum
import heapq
import queue
import time
import tkinter as tk
from tkinter import messagebox
import threading 
import random
class MyList(object):
    
    class Node(object):
        def __init__(self,value):
            self.next=None
            self.prev=None
            self.value = value
            pass
         
    def __init__(self):
        self.size=0
        self.head=None
        self.tail=None

    def append(self,data):
        new_node=self.Node(data)
        if self.head is None:
            self.head= new_node
            self.tail= new_node
        else:
            if self.tail is not None:
                self.tail.next= new_node
            new_node.prev= self.tail
            self.tail= new_node
            self.head.prev= self.tail
        self.size+=1

    def pop(self):
        ret=self.tail
        to_del=self.tail
        self.tail=self.tail.prev
        del to_del
        self.size-=1
        return ret.value

    def return_list(self,index:int):
        ret=self.head
        for _ in range(index):
            ret=ret.next
        return ret.value

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
        
        #状态信息
        self.state = state
        self.rectangle = rectangle

class PathFindingAlgorithm(object):
    DIJKSTRA = "Dijkstra"
    ASTAR = 'A*'

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

class DrawingMethod(object):

    def __init__(self,height:int,width:int,size:int):
        #格子尺寸大小
        self.height = height
        self.width = width
        self.size = size

        #起始点，终点
        self.start_point = None
        self.end_point = None
        
        #格子的集合
        self.points_list = MyList()

        #主窗口
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
                random_point=messagebox.askyesno("tips","默认生成迷宫不")
                if random_point:
                    self.generate_maze(self.width, self.height)
                self.canvas.bind("<Button-1>",self.set_barriers)
                self.canvas.bind("<Button-3>",self.choose_method_finding_way)
        
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
            for j in range(self.height):
                if (i,j)==self.start_point:
                    self.points_list.append(PointArray(i, j, 0, 0, PointState.START.value, None,
                              self.canvas.create_rectangle((i * self.size + 3, j * self.size + 3),
                                                           ((i + 1) * self.size + 3, (j + 1) * self.size + 3),
                                                             fill=PointState.START.value)))
                    continue
                elif (i,j)==self.end_point:
                    self.points_list.append(PointArray(i, j, 0, 0, PointState.END.value, None,
                              self.canvas.create_rectangle((i * self.size + 3, j * self.size + 3),
                                                           ((i + 1) * self.size + 3, (j + 1) * self.size + 3),
                                                             fill=PointState.END.value)))
                    continue
                self.points_list.append(PointArray(i, j, 0, 0, PointState.UNUSED.value, None,
                              self.canvas.create_rectangle((i * self.size + 3, j * self.size + 3),
                                                           ((i + 1) * self.size + 3, (j + 1) * self.size + 3),
                                                             fill=PointState.UNUSED.value)))
        

    def draw_lattice(self):
        for i in range(self.height + 1):
            self.canvas.create_line((3, i * self.size + 3), (self.width * self.size + 3, i * self.size + 3))
        for i in range(self.width + 1):
            self.canvas.create_line((i * self.size + 3, 3), (i * self.size + 3, self.height * self.size + 3))
        
    def set_barriers(self,event):
        x = (event.x - 3) // self.size
        y = (event.y - 3) // self.size
        if x < self.width and y < self.height:
            if self.points_list.return_list(x*self.height+y).state == PointState.BARRIER.value:
                self.points_list.return_list(x*self.height+y).state = PointState.UNUSED.value
                self.canvas.itemconfig(self.points_list.return_list(x*self.height+y).rectangle, fill=PointState.UNUSED.value)
            elif self.points_list.return_list(x*self.height+y).state == PointState.UNUSED.value:
                self.points_list.return_list(x*self.height+y).state = PointState.BARRIER.value
                self.canvas.itemconfig(self.points_list.return_list(x*self.height+y).rectangle, fill=PointState.BARRIER.value)
        
    def choose_method_finding_way(self, event):
        messagebox.showinfo("Tips", "Hello world")
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<Button-3>")

        # 创建一个Toplevel窗口作为选择算法的对话框
        algorithm_dialog = tk.Toplevel(self.root)
        algorithm_dialog.title("Choose Path Finding Algorithm")

        var = tk.IntVar()
        var.set(1)
        astar_button = tk.Radiobutton(
            algorithm_dialog, text="A*", variable=var, value=1,
        )
        astar_button.pack(side=tk.LEFT)  # 使用pack布局

        bfs_button = tk.Radiobutton(
            algorithm_dialog, text="BFS",variable=var,value=3,
        )
        bfs_button.pack(side=tk.LEFT)

        dfs_button = tk.Radiobutton(
            algorithm_dialog, text="DFS",variable=var,value=4,
        )
        dfs_button.pack(side=tk.LEFT)

        # 添加“确定”按钮
        def on_confirm():
            selected_algorithm = var.get()
            if selected_algorithm == 1:
                new_thread = threading.Thread(target=self.the_Astar_method)
                new_thread.start()
            elif selected_algorithm == 3:
                new_thread = threading.Thread(target=self.bfs())
                new_thread.start()
            elif selected_algorithm == 4:
                new_thread = threading.Thread(target=self.dfs())
                new_thread.start()
            algorithm_dialog.destroy()

        def on_close():
            self.canvas.bind("<Button-1>", self.set_barriers)
            self.canvas.bind("<Button-3>", self.choose_method_finding_way)
            algorithm_dialog.destroy()
        
        confirm_button = tk.Button(algorithm_dialog, text="Confirm", command=on_confirm)
        confirm_button.pack(side=tk.BOTTOM, pady=5)

        # 为对话框添加关闭按钮
        close_button = tk.Button(algorithm_dialog, text="Close", command=on_close)
        close_button.pack(side=tk.BOTTOM, pady=5)

        # 使对话框居中显示
        algorithm_dialog.update_idletasks()  
        dialog_width = algorithm_dialog.winfo_width()
        dialog_height = algorithm_dialog.winfo_height()
        screen_width = algorithm_dialog.winfo_screenwidth()
        screen_height = algorithm_dialog.winfo_screenheight()
        x = (screen_width - dialog_width) // 2
        y = (screen_height - dialog_height) // 2
        algorithm_dialog.geometry(f'+{x}+{y}')

    def changeState(self, point, state):
        point.state = state
        self.canvas.itemconfig(point.rectangle, fill=state)


    def trace_path(self, current):
        while current.father:
            self.changeState(current, PointState.PATH.value)
            current = current.father
        self.changeState(self.points_list.return_list(((self.start_point[0] - 3) // self.size)*self.height+(self.start_point[1] - 3) // self.size), PointState.START.value)
        self.changeState(self.points_list.return_list(((self.end_point[0] - 3) // self.size)*self.height+(self.end_point[1] - 3) // self.size), PointState.END.value)


    def the_Astar_method(self):
        def find_min_point(li:list)->PointArray:
            f=114514
            ans=-1
            for index,point in enumerate(li):
                if point.f <= f:
                    ans=index
                    f=point.f
            return li[ans]
        messagebox.showinfo("Tips","Astar")
        close_list = set()
        open_list = set()
        open_point_list=[]
        start_x = self.start_point[0]
        start_y = self.start_point[1]
        open_list.add((start_x,start_y))
        open_point_list.append(self.points_list.return_list(start_x*self.height+start_y))
        while True:
            point_of_min_f=find_min_point(open_point_list)
            cur_x=point_of_min_f.x
            cur_y=point_of_min_f.y
            close_list.add((cur_x, cur_y))
            open_list.remove((cur_x,cur_y))
            open_point_list.remove(self.points_list.return_list(cur_x*self.height+cur_y))

            if (cur_x,cur_y) != self.start_point:
                self.changeState(self.points_list.return_list(cur_x*self.height+cur_y),PointState.CLOSED.value)
                
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:  # 包含对角线方向
                next_x, next_y = cur_x + dx, cur_y + dy
                if 0 <= next_x < self.width and 0 <= next_y < self.height and (next_x, next_y) not in close_list:
                    neighbor = self.points_list.return_list(next_x*self.height+next_y)
                    if neighbor.state != PointState.BARRIER.value and (next_x,next_y) not in close_list:
                        cost = 14 if dx != 0 and dy != 0 else 10  # 对角线与直行代价
                        if dx!=0 and dy!=0:
                            if self.points_list.return_list(next_x*self.height+next_y).state==PointState.BARRIER.value or self.points_list.return_list(cur_x*self.height+cur_y).state==PointState.BARRIER.value:
                                continue
                        
                        if (neighbor.x,neighbor.y) not in open_list:
                            neighbor.g=cost+point_of_min_f.g
                            neighbor.f=neighbor.g+10*(abs(neighbor.x-self.end_point[0])+abs(neighbor.y-self.end_point[1]))
                            neighbor.father=point_of_min_f
                            open_list.add((neighbor.x,neighbor.y))
                            self.changeState(neighbor,PointState.OPEN.value)
                            open_point_list.append(self.points_list.return_list(neighbor.x*self.height+neighbor.y))
                        
                        else:
                            if (cost+point_of_min_f.g)<neighbor.g:
                                neighbor.g=cost+point_of_min_f.g
                                neighbor.f=neighbor.g+10*(abs(next_x-self.end_point[0])+abs(self.end_point[1]-next_y))
                                neighbor.father=point_of_min_f
                        
            if self.end_point in open_list:
                next_p=self.points_list.return_list(self.end_point[0]*self.height+self.end_point[1])
                next_p.father=point_of_min_f
                self.changeState(next_p,PointState.END.value)
                while next_p:
                    next_p=next_p.father
                    if next_p is None:
                        break
                    if (next_p.x,next_p.y) != self.start_point:
                        self.changeState(next_p,PointState.PATH.value)
                    else:
                        self.changeState(next_p,PointState.START.value)
                messagebox.showinfo("tips","找到了")
                self.root.after(5000, self.root.destroy)
                break
            if  len(open_list)==0 :
                messagebox.showerror("不可理喻")
                self.root.after(5000, self.root.destroy)
                break
            self.canvas.update() 
            time.sleep(0.1)
    
    def bfs(self):
        messagebox.showinfo("Tips", "BFS")
        visited = [[False for _ in range(self.height + 10)] for _ in range(self.width + 10)]
        que = queue.Queue()
        que.put(self.start_point)
        visited[self.start_point[0]][self.start_point[1]] = True
        ans_list = MyList()
        end = False

        while not que.empty() and not end:
            cur_x, cur_y = que.get()
            ans_list.append((cur_x, cur_y))

            if (cur_x, cur_y) == self.end_point:
                end = True
                break

            for dx, dy in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, 1), (1, 0), (1, -1)]:
                next_px, next_py = cur_x + dx, cur_y + dy
                if 0 <= next_px < self.width and 0 <= next_py < self.height and not visited[next_px][next_py] and self.points_list.return_list(next_px*self.height+next_py).state != PointState.BARRIER.value:
                    if dx != 0 and dy != 0:
                        if self.points_list.return_list(next_px*self.height+cur_y).state == PointState.BARRIER.value or self.points_list.return_list(cur_x*self.height+next_py).state == PointState.BARRIER.value:
                            continue
                    visited[next_px][next_py] = True
                    que.put((next_px, next_py))

                    if (next_px, next_py) != self.start_point and (next_px, next_py) != self.end_point:
                        self.changeState(self.points_list.return_list(next_px*self.height+next_py), PointState.QUEUE.value)
                    if (next_px,next_py)==self.end_point:
                        break
                    self.canvas.update()
                    time.sleep(0.02)
        if end:
            messagebox.showinfo("i","找到了")
        else:
            messagebox.showinfo("i","找个锤子")

    def dfs(self):
        messagebox.showinfo("Tips","DFS")
        path=MyList()
        path.append(self.start_point)
        visited=[[False for _ in range(114)] for _ in range(114)]
        visited[self.start_point[0]][self.start_point[1]]=True
        while path.size!=0:
            cur_x,cur_y=path.pop()
            if (cur_x,cur_y)==self.end_point:
                break
            dx=[0,0,-1,1]
            dy=[-1,1,0,0]
            index=0
            while index<4:
                next_x=dx[index]+cur_x
                next_y=dy[index]+cur_y
                if 0<=next_x<self.width and 0<=next_y<self.height \
                    and self.points_list.return_list(next_x*self.height+next_y).state != PointState.BARRIER.value \
                    and visited[next_x][next_y] == False:
                    visited[next_x][next_y]=True
                    if (next_x,next_y)==self.end_point:
                        messagebox.showinfo("Result","找到了")
                        self.root.after(5000, self.root.destroy)
                        return
                    path.append((next_x,next_y))
                    self.changeState(self.points_list.return_list(next_x*self.height+next_y),PointState.PATH.value)
                else:
                    index+=1
                self.canvas.update()
                time.sleep(0.02)
        messagebox.showinfo("Result","找不到")
        self.root.after(5000, self.root.destroy)  

    def generate_maze(self,width=20, height=30, obstacle_probability=0.5):
        # 确保起始点和终点无障碍
        maze = [[0]*height for _ in range(width)]
        maze[self.start_point[0]][self.start_point[1]] = 0  # 起点
        maze[self.end_point[0]][self.end_point[1]] = 0  # 终点
        
        # 生成随机障碍物
        for i in range(width):
            for j in range(height):
                # 起点、终点及周边格子不生成障碍物，以确保可达性
                if (i,j)==self.start_point or (i,j) == self.end_point :
                    continue
                if random.random() < obstacle_probability:
                    maze[i][j] = 1
                    
        # 确保左右边缘有通路
        for i in range(width):
            if maze[i][0] == 1:  # 左边缘
                maze[i][0] = 0
            if maze[i][-1] == 1:  # 右边缘
                maze[i][-1] = 0

        # 确保上下边缘有通路
        for j in range(height):
            if maze[0][j] == 1:  # 上边缘
                maze[0][j] = 0
            if maze[-1][j] == 1:  # 下边缘
                maze[-1][j] = 0

        for i in range(self.width):
            for j in range(self.height):
                if maze[i][j]==1:
                    self.points_list.return_list(i*self.height+j).state=PointState.BARRIER.value
                    self.changeState(self.points_list.return_list(i*self.height+j),PointState.BARRIER.value)

draw=DrawingMethod(20,30,40)