# ghost.py
import pygame
import random
import time
from ai import a_star, bfs, dfs

class Ghost:
    def __init__(self, start_cell, cell_size, color=(255,0,0), algo="astar"):
        self.cell_size = cell_size
        self.cell = start_cell
        # positions kept as floats for smooth movement
        self.x = float(self.cell[0] * cell_size)
        self.y = float(self.cell[1] * cell_size)
        self.rect = pygame.Rect(int(self.x), int(self.y), cell_size, cell_size)
        self.color = color
        self.mode = "chase"   # "chase" or "frightened"
        self.algo = algo.lower()
        self.path = [self.cell]
        self.repath_interval = 0.35
        self._last_repath = 0.0
        self.speed = 100.0    # pixels / second

        # frightened timer (unix time)
        self.frightened_until = 0.0

        # house/spawn cell
        self.house = start_cell

    def set_target(self, target_cell):
        self.target = target_cell

    def needs_repath(self):
        return (time.time() - self._last_repath) > self.repath_interval

    def compute_path(self, maze):
        start = self.cell
        if self.mode == "frightened":
            # pick a random reachable dot or random nearby path cell
            if maze.dots:
                goal = random.choice(list(maze.dots))
            else:
                goal = start
        else:
            goal = getattr(self, "target", start)

        grid = maze.grid
        path = []
        if self.algo == "astar":
            path = a_star(start, goal, grid)
        elif self.algo == "bfs":
            path = bfs(start, goal, grid)
        elif self.algo == "dfs":
            path = dfs(start, goal, grid)
        else:
            path = bfs(start, goal, grid)

        if path:
            self.path = path
        else:
            self.path = [start]

        self._last_repath = time.time()

    def update(self, dt, maze):
        # expire frightened
        if self.mode == "frightened" and time.time() > self.frightened_until:
            self.mode = "chase"
            self._last_repath = 0.0

        # compute path if needed
        if not self.path or self.needs_repath():
            self.compute_path(maze)

        # follow the path smoothly
        if len(self.path) >= 2:
            next_cell = self.path[1]
            target_x = next_cell[0] * self.cell_size
            target_y = next_cell[1] * self.cell_size
            step = self.speed * dt

            if self.x < target_x:
                self.x = min(self.x + step, target_x)
            elif self.x > target_x:
                self.x = max(self.x - step, target_x)
            if self.y < target_y:
                self.y = min(self.y + step, target_y)
            elif self.y > target_y:
                self.y = max(self.y - step, target_y)

            # reached next cell?
            if int(round(self.x)) == target_x and int(round(self.y)) == target_y:
                self.cell = next_cell
                if len(self.path) > 1:
                    self.path = self.path[1:]
        else:
            # idle jitter so ghosts don't freeze visually
            if random.random() < 0.01:
                x,y = self.cell
                candidates = []
                for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
                    nx,ny = x+dx, y+dy
                    if 0 <= ny < maze.rows and 0 <= nx < maze.cols and maze.is_path((nx,ny)):
                        candidates.append((nx,ny))
                if candidates:
                    self.path = [self.cell, random.choice(candidates)]

        self.rect.topleft = (int(round(self.x)), int(round(self.y)))

    def draw(self, surf):
        pygame.draw.rect(surf, self.color, self.rect)

    def collides(self, pacman):
        """
        Robust rect-based collision with tolerance proportional to cell size.
        Works even if pacman has .rect or only x,y.
        """
        try:
            prect = pacman.rect
        except Exception:
            prect = pygame.Rect(int(pacman.x), int(pacman.y), self.cell_size, self.cell_size)

        tolerance = int(self.cell_size * 0.5)
        return self.rect.inflate(-tolerance, -tolerance).colliderect(prect.inflate(-tolerance, -tolerance))

    def set_frightened(self, seconds):
        self.mode = "frightened"
        self.frightened_until = time.time() + max(0.1, float(seconds))
        self._last_repath = 0.0

    def reset_to_house(self, maze):
        self.cell = self.house
        self.x = float(self.cell[0] * self.cell_size)
        self.y = float(self.cell[1] * self.cell_size)
        self.path = [self.cell]
        self._last_repath = 0.0
        self.mode = "chase"
        self.frightened_until = 0.0
        self.rect.topleft = (int(round(self.x)), int(round(self.y)))
