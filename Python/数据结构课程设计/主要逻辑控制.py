import time
import tkinter as tk
from tkinter import messagebox
import threading 
import random
from my_queue import MyQueue 
from my_list import MyList
from init import PointArray,PointState

class DrawingMethod(object):
    def __init__(self,height:int,width:int,size:int):
        self.height = height #画布长几个格子
        self.width = width #画布宽几个格子
        self.size = size #画布每个正方向格子的尺寸

        self.start_point = None #起始点坐标,(x,y)形式
        self.end_point = None #终止点坐标

        self.start_image = None #画布上显示的起始点的标号
        self.end_image = None   #画布上显示的终止点的标号
        self.image_end = None   #终止点的图像数据
        self.image_start = None #起始点的图像数据

        self.points_list = MyList() #每个格子对象的列表

        self.root = tk.Tk() #主界面
        self.root.title('Navigation')
        self.canvas = tk.Canvas(self.root, width=self.width * self.size + 3, height=self.height * self.size + 3)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_left_click)
        self.canvas.bind("<Button-3>", self.on_right_click)
        self.draw_lattice()
        messagebox.showinfo('提示','左键选择起始点\n右键选择终止点')
        self.root.mainloop()

    def on_left_click(self, event):
        x, y = event.x - 3, event.y - 3  
        cell_x, cell_y = x // self.size, y // self.size
        if self.start_point is None and (cell_x,cell_y)!=self.end_point:
            self.set_start_point(cell_x, cell_y)
        elif (cell_x,cell_y)!=self.end_point and self.start_point==(cell_x,cell_y):
            if self.start_point:
                self.canvas.delete(self.start_image)
                self.start_point = None
        if (cell_x,cell_y)==self.end_point:
            messagebox.showinfo('提示','不能设置起点终点为同一个点')
        self.confirm_selection()

    def on_right_click(self, event):
        x, y = event.x - 3, event.y - 3
        cell_x, cell_y = x // self.size, y // self.size
        if self.end_point is None and self.start_point != (cell_x, cell_y):  
            self.set_end_point(cell_x, cell_y)
        elif self.start_point!=(cell_x,cell_y) and self.end_point==(cell_x,cell_y):
            if self.end_point:
                self.canvas.delete(self.end_image)
                self.end_point = None
        if (cell_x,cell_y)==self.start_point:
            messagebox.showinfo('提示','不允许起点终点一样')
        self.confirm_selection()
        
    def set_start_point(self, x: int, y: int):
        if self.start_point:
            self.canvas.delete(self.start_image)
            self.start_point = None
        self.image_start=tk.PhotoImage(file="1.gif",width=self.size,height=self.size)
        self.start_image=self.canvas.create_image(x*self.size+3+self.size//2+1,y*self.size+3+self.size//2+1,image=self.image_start)
        self.canvas.pack()
        self.canvas.update()
        self.start_point = (x, y)

    def set_end_point(self, x: int, y: int):
        if self.end_point:
            self.canvas.delete(self.end_image)
            self.end_point=None
        self.image_end=tk.PhotoImage(file="2.gif",width=self.size,height=self.size)
        self.end_image=self.canvas.create_image(x*self.size+3+self.size//2+1,y*self.size+3+self.size//2+1,image=self.image_end)
        self.canvas.pack()
        self.canvas.update()
        self.end_point = (x, y)

    def confirm_selection(self):
        if self.start_point is not None and self.end_point is not None:
            result=messagebox.askyesno("嗯?", "你确定?????")
            if not result:
                self.clear_points()
            else:
                self.canvas.unbind("<Button-1>")
                self.canvas.unbind("<Button-3>")
                messagebox.showinfo("提示","左键选择障碍物\n右键开始")
                self.generate_points()
                random_point=messagebox.askyesno("提示","默认生成迷宫不")
                if random_point:
                    self.generate_maze(self.width, self.height)
                self.canvas.bind("<Button-1>",self.set_barriers)
                self.canvas.bind("<Button-3>",self.choose_method_finding_way)
        return False

    def clear_points(self):
        if self.start_point:
            self.canvas.delete(self.start_image)
            self.canvas.update()
            self.start_point = None
        if self.end_point:
            self.canvas.delete(self.end_image)
            self.canvas.update()
            self.end_point = None

    def generate_points(self):
        for i in range(self.width):
            for j in range(self.height):
                if (i,j)==self.start_point:
                    self.points_list.append(PointArray(i, j, 0, 0, PointState.START.value, None,
                            None))
                    continue
                elif (i,j)==self.end_point:
                    self.points_list.append(PointArray(i, j, 0, 0, PointState.END.value, None,
                            None))
                    continue
                self.points_list.append(PointArray(i, j, 0, 0, PointState.UNUSED.value, None,
                              self.canvas.create_rectangle((i * self.size + 3, j * self.size + 3),
                                                           ((i + 1) * self.size + 3, (j + 1) * self.size + 3),
                                                             fill=PointState.UNUSED.value)))
        self.canvas.update()
        
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
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<Button-3>")

        algorithm_dialog = tk.Toplevel(self.root)
        algorithm_dialog.title("选择寻路算法")

        var = tk.IntVar()
        var.set(1)
        astar_button = tk.Radiobutton(
            algorithm_dialog, text="A*", variable=var, value=1,
        )
        astar_button.pack(side=tk.LEFT)  

        bfs_button = tk.Radiobutton(
            algorithm_dialog, text="BFS",variable=var,value=3,
        )
        bfs_button.pack(side=tk.LEFT)

        dfs_button = tk.Radiobutton(
            algorithm_dialog, text="DFS",variable=var,value=4,
        )
        dfs_button.pack(side=tk.LEFT)

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
        
        confirm_button = tk.Button(algorithm_dialog, text="确认", command=on_confirm)
        confirm_button.pack(side=tk.BOTTOM, pady=5)

        close_button = tk.Button(algorithm_dialog, text="取消", command=on_close)
        close_button.pack(side=tk.BOTTOM, pady=5)

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

    def the_Astar_method(self):
        def find_min_point(li:list)->PointArray:
            f=114514
            ans=-1
            for index,point in enumerate(li):
                if point.f <= f:
                    ans=index
                    f=point.f
            return li[ans]
        messagebox.showinfo("提示","这是Astar算法")
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
                        cost = 14 if dx != 0 and dy != 0 else 10 
                        if dx!=0 and dy!=0:
                            if self.points_list.return_list(next_x*self.height+cur_y).state==PointState.BARRIER.value or self.points_list.return_list(cur_x*self.height+next_y).state==PointState.BARRIER.value:
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

                while next_p:
                    next_p=next_p.father
                    if next_p is None:
                        break
                    if (next_p.x,next_p.y) != self.start_point :
                        self.changeState(next_p,PointState.PATH.value)

                messagebox.showinfo("提示","找到了")
                self.root.after(5000, self.root.destroy)
                break
            if  len(open_list)==0 :
                messagebox.showerror("找不到欸")
                self.root.after(5000, self.root.destroy)
                break
            self.canvas.update() 
            time.sleep(0.1)
    
    def bfs(self):
        messagebox.showinfo("提示", "这是BFS")
        visited = [[False for _ in range(self.height + 10)] \
                   for _ in range(self.width + 10)]
        que = MyQueue()
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
                    self.points_list.return_list(next_px*self.height+next_py).father=self.points_list.return_list(cur_x*self.height+cur_y)
                    visited[next_px][next_py] = True
                    que.put((next_px, next_py))

                    if (next_px, next_py) != self.start_point and (next_px, next_py) != self.end_point:
                        self.changeState(self.points_list.return_list(next_px*self.height+next_py), PointState.OPEN.value)
                    if (next_px,next_py)==self.end_point:
                        fat=self.points_list.return_list(next_px*self.height+next_py)
                        while fat.father is not None and (fat.father.x,fat.father.y) != self.start_point:
                            self.changeState(fat.father,PointState.PATH.value)
                            fat=fat.father
                        break
                    self.canvas.update()
                    time.sleep(0.02)
        if end:
            messagebox.showinfo("结果","找到了")
        else:
            messagebox.showinfo("结果","找不到")

    def dfs(self):
        messagebox.showinfo("提示","这是DFS")
        path=MyList()
        path.append(self.start_point)
        visited=[[False for _ in range(114)] for _ in range(114)]
        visited[self.start_point[0]][self.start_point[1]]=True
        while path.size()!=0:
            cur_x,cur_y=path.pop()
            self.changeState(self.points_list.return_list(cur_x*self.height+cur_y),PointState.UNUSED.value)
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
                    self.points_list.return_list(next_x*self.height+next_y).father=self.points_list.return_list(cur_x*self.height+cur_y)
                    if (next_x,next_y)==self.end_point:
                        fat=self.points_list.return_list(next_x*self.height+next_y)
                        while fat.father is not None and (fat.father.x,fat.father.y) != self.start_point:
                            self.changeState(fat.father,PointState.PATH.value)
                            fat=fat.father
                        messagebox.showinfo("结果","找到了")
                        self.root.after(5000, self.root.destroy)
                        return
                    path.append((next_x,next_y))
                    self.changeState(self.points_list.return_list(next_x*self.height+next_y),PointState.OPEN.value)
                else:
                    index+=1
                self.canvas.update()
                time.sleep(0.02)
        messagebox.showinfo("结果","找不到")
        self.root.after(5000, self.root.destroy)  

    def generate_maze(self,width=20, height=30, obstacle_probability=0.5):

        maze = [[0]*height for _ in range(width)]
        maze[self.start_point[0]][self.start_point[1]] = 0 
        maze[self.end_point[0]][self.end_point[1]] = 0  
        
        for i in range(width):
            for j in range(height):
                if (i,j)==self.start_point or (i,j) == self.end_point :
                    continue
                if random.random() < obstacle_probability:
                    maze[i][j] = 1
        for i in range(width):
            if maze[i][0] == 1:  
                maze[i][0] = 0
            if maze[i][-1] == 1:  
                maze[i][-1] = 0

        for j in range(height):
            if maze[0][j] == 1:  
                maze[0][j] = 0
            if maze[-1][j] == 1:  
                maze[-1][j] = 0

        for i in range(self.width):
            for j in range(self.height):
                if maze[i][j]==1:
                    self.points_list.return_list(i*self.height+j).state=PointState.BARRIER.value
                    self.changeState(self.points_list.return_list(i*self.height+j),PointState.BARRIER.value)