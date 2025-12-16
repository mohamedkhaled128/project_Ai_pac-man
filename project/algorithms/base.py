"""
الدوال الأساسية المشتركة بين جميع الخوارزميات
"""

def heuristic_manhattan(a, b):
    """Heuristic: Manhattan distance"""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def heuristic_euclidean(a, b):
    """Heuristic: Euclidean distance"""
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5

def reconstruct_path(came_from, start, goal):
    """إعادة بناء المسار من قاموس came_from"""
    path = []
    current = goal
    while current is not None:
        path.append(current)
        current = came_from.get(current)
    path.reverse()
    return path

