"""
IDA* (Iterative Deepening A*) Algorithm
"""
import time
from .base import heuristic_manhattan

def ida_star(gamemap, start, goal, time_limit=1.0, max_nodes=5000):
    """
    IDA* algorithm for pathfinding
    
    Args:
        gamemap: Game map
        start: Start point (x, y)
        goal: Goal point (x, y)
    
    Returns:
        List of path from start to goal
    """
    if start == goal:
        return [start]
    
    start_time = time.time()
    explored = 0

    def search(path, g, threshold):
        nonlocal explored

        # زمن التشغيل
        if time.time() - start_time > time_limit:
            return float("inf")

        # حد أقصى لعدد العقد
        explored += 1
        if explored > max_nodes:
            return float("inf")

        node = path[-1]
        f = g + heuristic_manhattan(node, goal)
        
        if f > threshold:
            return f
        
        if node == goal:
            return path
        
        min_cost = float('inf')
        visited = set(path)  # Use set for faster lookup
        
        for neighbor in gamemap.neighbors(node):
            if neighbor not in visited:
                path.append(neighbor)
                result = search(path, g + 1, threshold)
                if isinstance(result, list):
                    return result
                if isinstance(result, (int, float)):
                    min_cost = min(min_cost, result)
                path.pop()
        
        return min_cost
    
    threshold = heuristic_manhattan(start, goal)
    max_iterations = 200  # Prevent infinite loops
    iteration = 0
    
    while iteration < max_iterations:
        result = search([start], 0, threshold)
        if isinstance(result, list):
            return result
        if result == float('inf'):
            return []
        threshold = result
        iteration += 1
    
    return []
