# ai.py
from collections import deque
import heapq

def neighbors(cell, grid):
    x,y = cell
    dirs = [(1,0),(-1,0),(0,1),(0,-1)]
    for dx,dy in dirs:
        nx,ny = x+dx, y+dy
        if 0 <= ny < len(grid) and 0 <= nx < len(grid[0]) and grid[ny][nx] in ('1','P','D'):
            yield (nx,ny)

def manhattan(a,b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def a_star(start, goal, grid):
    if start == goal: return [start]
    open_set = []
    heapq.heappush(open_set, (manhattan(start,goal), 0, start))
    came_from = {}
    gscore = {start:0}
    closed = set()
    while open_set:
        f, g, current = heapq.heappop(open_set)
        if current in closed:
            continue
        closed.add(current)
        if current == goal:
            path=[]
            node = current
            while node in came_from:
                path.append(node)
                node = came_from[node]
            path.append(start)
            path.reverse()
            return path
        for n in neighbors(current, grid):
            tentative = g + 1
            if n in gscore and tentative >= gscore[n]:
                continue
            came_from[n] = current
            gscore[n] = tentative
            heapq.heappush(open_set, (tentative + manhattan(n,goal), tentative, n))
    return []

def bfs(start, goal, grid):
    if start == goal: return [start]
    q = deque([start])
    parent = {start: None}
    while q:
        cur = q.popleft()
        if cur == goal:
            path=[]
            node = cur
            while node:
                path.append(node)
                node = parent[node]
            path.reverse()
            return path
        for n in neighbors(cur, grid):
            if n not in parent:
                parent[n] = cur
                q.append(n)
    return []

def dfs(start, goal, grid):
    if start == goal: return [start]
    stack = [start]
    parent = {start: None}
    visited = set([start])
    while stack:
        cur = stack.pop()
        if cur == goal:
            path=[]
            node = cur
            while node:
                path.append(node)
                node = parent[node]
            path.reverse()
            return path
        for n in neighbors(cur, grid):
            if n not in visited:
                visited.add(n)
                parent[n] = cur
                stack.append(n)
    return []
