"""
خوارزمية Greedy Best-First Search
"""
import heapq
from .base import heuristic_manhattan, reconstruct_path

def greedy_best_first(gamemap, start, goal):
    """
    خوارزمية Greedy Best-First Search
    
    Args:
        gamemap: خريطة اللعبة
        start: نقطة البداية (x, y)
        goal: نقطة الهدف (x, y)
    
    Returns:
        قائمة بالمسار من البداية إلى الهدف
    """
    if start == goal:
        return [start]
    
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {start: None}
    
    while open_set:
        _, current = heapq.heappop(open_set)
        
        if current == goal:
            return reconstruct_path(came_from, start, goal)
        
        for neighbor in gamemap.neighbors(current):
            if neighbor not in came_from:
                came_from[neighbor] = current
                priority = heuristic_manhattan(neighbor, goal)
                heapq.heappush(open_set, (priority, neighbor))
    
    return []

