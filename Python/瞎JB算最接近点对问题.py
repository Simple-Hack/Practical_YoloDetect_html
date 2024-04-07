import math  
import random  

struct_node = lambda: {'x': 0.0, 'y': 0.0}  

def cmp(a, b):  
    return a['x'] < b['x']  

def dis(a, b):  
    return math.sqrt((a['x'] - b['x']) ** 2 + (a['y'] - b['y']) ** 2)  

def calc(nodes, n):  
    global ans  
    for i in range(n):  
        for j in range(i + 1, min(i + 6, n)):  
            ans = min(ans, dis(nodes[i], nodes[j]))  
  
def around(nodes, n, ds):  
    ds = ds * (math.pi / 180.0)  
    for i in range(n):  
        x, y = nodes[i]['x'], nodes[i]['y']  
        xn = x * math.cos(ds) - y * math.sin(ds)  
        yn = x * math.sin(ds) + y * math.cos(ds)  
        nodes[i]['x'], nodes[i]['y'] = xn, yn  
    nodes.sort(key=lambda node: node['x'])  
    calc(nodes, n)  
  
def main():  
    global ans  
    n = int(input())  
    nodes = [struct_node() for _ in range(n)]  
    for i in range(n):  
        nodes[i]['x'], nodes[i]['y'] = map(float, input().split())  
  
    ans = 1145141919  
    nodes.sort(key=lambda node: node['x'])  
    calc(nodes, n)  
    around(nodes, n, random.randint(0, 359))
    around(nodes, n, random.randint(0, 359))
    around(nodes, n, random.randint(0, 359))
    print(f"{ans:.4f}")  
  
if __name__ == '__main__':  
    main()