"""
خوارزمية Bidirectional Search
"""
from collections import deque
from .base import reconstruct_path

def bidirectional_search(gamemap, start, goal):
    """
    خوارزمية البحث ثنائي الاتجاه
    
    Args:
        gamemap: خريطة اللعبة
        start: نقطة البداية (x, y)
        goal: نقطة الهدف (x, y)
    
    Returns:
        قائمة بالمسار من البداية إلى الهدف
    """
    if start == goal:
        return [start]
    
    # البحث من البداية
    queue_start = deque([start])
    came_from_start = {start: None}
    
    # البحث من الهدف
    queue_goal = deque([goal])
    came_from_goal = {goal: None}
    
    visited_start = {start}
    visited_goal = {goal}
    
    while queue_start or queue_goal:
        # خطوة من البداية
        if queue_start:
            current_start = queue_start.popleft()
            
            if current_start in visited_goal:
                # تم العثور على التقاطع
                path1 = []
                node = current_start
                while node is not None:
                    path1.append(node)
                    node = came_from_start[node]
                path1.reverse()
                
                path2 = []
                node = came_from_goal[current_start]
                while node is not None:
                    path2.append(node)
                    node = came_from_goal[node]
                
                return path1 + path2
            
            for neighbor in gamemap.neighbors(current_start):
                if neighbor not in visited_start:
                    visited_start.add(neighbor)
                    came_from_start[neighbor] = current_start
                    queue_start.append(neighbor)
        
        # خطوة من الهدف
        if queue_goal:
            current_goal = queue_goal.popleft()
            
            if current_goal in visited_start:
                # تم العثور على التقاطع
                path1 = []
                node = current_goal
                while node is not None:
                    path1.append(node)
                    node = came_from_start[node]
                path1.reverse()
                
                path2 = []
                node = came_from_goal[current_goal]
                while node is not None:
                    path2.append(node)
                    node = came_from_goal[node]
                
                return path1 + path2
            
            for neighbor in gamemap.neighbors(current_goal):
                if neighbor not in visited_goal:
                    visited_goal.add(neighbor)
                    came_from_goal[neighbor] = current_goal
                    queue_goal.append(neighbor)
    
    return []

