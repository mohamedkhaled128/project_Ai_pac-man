"""
خوارزمية DFS (Depth-First Search)
"""
from .base import reconstruct_path

def dfs(gamemap, start, goal):
    """
    خوارزمية DFS للبحث عن المسار
    
    Args:
        gamemap: خريطة اللعبة
        start: نقطة البداية (x, y)
        goal: نقطة الهدف (x, y)
    
    Returns:
        قائمة بالمسار من البداية إلى الهدف
    """
    if start == goal:
        return [start]
    
    stack = [start]
    came_from = {start: None}
    
    while stack:
        current = stack.pop()
        
        if current == goal:
            return reconstruct_path(came_from, start, goal)
        
        for neighbor in gamemap.neighbors(current):
            if neighbor not in came_from:
                came_from[neighbor] = current
                stack.append(neighbor)
    
    return []

