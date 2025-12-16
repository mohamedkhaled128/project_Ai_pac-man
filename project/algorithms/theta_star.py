"""
خوارزمية Theta* (Any-Angle Pathfinding)
"""
import heapq
from .base import heuristic_manhattan, reconstruct_path

def line_of_sight(gamemap, a, b):
    """
    التحقق من وجود خط رؤية مباشر بين نقطتين
    """
    x0, y0 = a
    x1, y1 = b
    
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy
    
    x, y = x0, y0
    
    while True:
        if not gamemap.passable((x, y)):
            return False
        
        if x == x1 and y == y1:
            return True
        
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x += sx
        if e2 < dx:
            err += dx
            y += sy

def theta_star(gamemap, start, goal):
    """
    خوارزمية Theta* للبحث عن المسار بأي زاوية
    
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
        
        # محاولة الاتصال المباشر مع الهدف
        if current in came_from:
            parent = came_from[current]
            if line_of_sight(gamemap, parent, goal):
                came_from[goal] = parent
                g_score[goal] = g_score[parent] + heuristic_manhattan(parent, goal)
                f_score[goal] = g_score[goal]
                return reconstruct_path(came_from, start, goal)
        
        for neighbor in gamemap.neighbors(current):
            # محاولة الاتصال المباشر مع الوالد
            if current in came_from:
                parent = came_from[current]
                if line_of_sight(gamemap, parent, neighbor):
                    tentative_g_score = g_score[parent] + heuristic_manhattan(parent, neighbor)
                    if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                        came_from[neighbor] = parent
                        g_score[neighbor] = tentative_g_score
                        f_score[neighbor] = tentative_g_score + heuristic_manhattan(neighbor, goal)
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))
                        continue
            
            # المسار العادي
            tentative_g_score = g_score[current] + 1
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic_manhattan(neighbor, goal)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))
    
    return []

