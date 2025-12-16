"""
خوارزمية BFS (Breadth-First Search)
"""
from collections import deque
from .base import reconstruct_path

def bfs(gamemap, start, goal):
    """
    خوارزمية BFS للبحث عن المسار
    
    Args:
        gamemap: خريطة اللعبة
        start: نقطة البداية (x, y)
        goal: نقطة الهدف (x, y)
    
    Returns:
        قائمة بالمسار من البداية إلى الهدف
    """
    if start == goal:
        return [start]
    
    queue = deque([start])
    came_from = {start: None}
    
    while queue:
        current = queue.popleft()
        
        if current == goal:
            return reconstruct_path(came_from, start, goal)
        
        for neighbor in gamemap.neighbors(current):
            if neighbor not in came_from:
                came_from[neighbor] = current
                queue.append(neighbor)
    
    return []

