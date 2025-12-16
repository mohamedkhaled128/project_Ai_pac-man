"""
خوارزمية A* (A-Star)
"""
import heapq
from .base import heuristic_manhattan, reconstruct_path

def astar(gamemap, start, goal):
    """
    خوارزمية A* للبحث عن المسار الأقصر
    
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
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic_manhattan(start, goal)}
    
    while open_set:
        _, current = heapq.heappop(open_set)
        
        if current == goal:
            return reconstruct_path(came_from, start, goal)
        
        for neighbor in gamemap.neighbors(current):
            tentative_g_score = g_score[current] + 1
            
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic_manhattan(neighbor, goal)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))
    
    return []

