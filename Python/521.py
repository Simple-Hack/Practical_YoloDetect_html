import os
from time import sleep
import psutil
import matplotlib.pyplot as plt
import re
import tkinter as tk
from tkinter import ttk


def read_process_stats(pid):
    """
    读取指定PID的进程状态信息。
    :param pid: 进程ID
    :return: 包含进程名、CPU占用和内存占用的字典，如果无法读取则返回None
    """
    stat_file_path = f"/proc/{pid}/stat"
    try:
        with open(stat_file_path, 'r') as stat_file:
            content = stat_file.readline().split()
            
            # 解析内容：
            # content[1] 是进程名（在括号内，可能包含其他信息，需要清理）
            # content[13] 是用户CPU时间，与sysconf(_SC_CLK_TCK)结合可计算CPU占用率
            # content[22] 是RSS（常驻集大小），单位是页，通常一页为4KB，转换为MB需要除以4*1024
            
            # 提取进程名，移除括号及括号内内容
            process_name = content[1].split('(')[1].split(')')[0]
            
            # 计算CPU时间（这里简化处理，未考虑所有CPU时间字段的累加）
            # 注意：实际应用中可能需要根据_SC_CLK_TCK计算用户和系统CPU时间总和
            cpu_time = float(content[13]) / os.sysconf('SC_CLK_TCK')
            
            # 转换内存占用为MB
            mem_usage = float(content[22]) / (4 * 1024)
            
            return {
                'pid': pid,
                'pname': process_name,
                'cpu': cpu_time,
                'mem': mem_usage
            }
    except FileNotFoundError:
        print(f"PID {pid} not found.")
        return None
    except Exception as e:
        print(f"Error reading stats for PID {pid}: {e}")
        return None


def plot_memory_usage():
    pids = [int(folder) for folder in os.listdir("/proc") if folder.isdigit()]
    #不同状态的进程pid统计如下：
    pid_info=[read_process_stats(pid) for pid in pids]
    sorted_cpu_pid=sorted(pid_info,key=lambda x:x['cpu'],reverse=True)
    sorted_mem_pid=sorted(pid_info,key=lambda x:x['mem'],reverse=True)
    create_table(pid_info,sorted_cpu_pid,sorted_mem_pid)



def create_table(pid_info,sorted_cpu_pid,sorted_mem_pid):
    root = tk.Tk()
    root.title("my资源管理器")
    rows=len(pid_info)
    style = ttk.Style()
    style.configure("Treeview", rowheight=30)
    tree = ttk.Treeview(root, columns=("col1", "col2", "col3", "col4"), show="headings",height=20)
    tree.column("col1", width=100, anchor="center")
    tree.column("col2", width=300, anchor="center")
    tree.column("col3", width=100, anchor="center")
    tree.column("col4", width=100, anchor="center")

    tree.heading("col1", text="pid")
    tree.heading("col2", text="进程名")
    tree.heading("col3", text="cpu占用")
    tree.heading("col4", text="内存占用")

    for proc in pid_info:
        tree.insert("", "end", values=(f"{proc['pid']}", f"{proc['pname']}", f"{proc['cpu']}", f"{proc['mem']}"))

    scrollbar = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    tree.pack(side="left", fill="both", expand=True)

    root.mainloop()



if __name__ == "__main__":
    plot_memory_usage()

    