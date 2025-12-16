"""
خوارزمية Dijkstra
"""
import heapq
from .base import reconstruct_path

def dijkstra(gamemap, start, goal):
    """
    خوارزمية Dijkstra للبحث عن المسار الأقصر
    
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
    cost = {start: 0}
    
    while open_set:
        current_cost, current = heapq.heappop(open_set)
        
        if current == goal:
            return reconstruct_path(came_from, start, goal)
        
        if current_cost > cost.get(current, float('inf')):
            continue
        
        for neighbor in gamemap.neighbors(current):
            new_cost = cost[current] + 1
            
            if neighbor not in cost or new_cost < cost[neighbor]:
                cost[neighbor] = new_cost
                heapq.heappush(open_set, (new_cost, neighbor))
                came_from[neighbor] = current
    
    return []

