# maze.py
import pygame

class Maze:
    def __init__(self, path="assets/map.txt", cell_size=24):
        self.cell_size = cell_size
        self.grid = self._load_map(path)
        self.rows = len(self.grid)
        self.cols = len(self.grid[0]) if self.rows>0 else 0
        self.dots = set()
        self._init_dots()

    def _load_map(self, path):
        with open(path,'r') as f:
            lines = [l.rstrip('\n') for l in f.readlines() if l.strip()]
        grid = []
        for line in lines:
            row = []
            for ch in line:
                if ch in ('0','1','P','D'):
                    row.append(ch)
                else:
                    # treat other as wall
                    row.append('0')
            grid.append(row)
        return grid

    def _init_dots(self):
        self.dots.clear()
        for y,row in enumerate(self.grid):
            for x,ch in enumerate(row):
                if ch == '1' or ch == 'P' or ch == 'D':
                    # add a dot on paths (except special markers)
                    if ch != 'P':  # P is start
                        self.dots.add((x,y))

    def is_path(self, cell):
        x,y = cell
        if 0 <= y < self.rows and 0 <= x < self.cols:
            return self.grid[y][x] in ('1','P','D')
        return False

    def find_start(self):
        for y,row in enumerate(self.grid):
            for x,ch in enumerate(row):
                if ch == 'P':
                    return (x,y)
        # fallback
        for y,row in enumerate(self.grid):
            for x,ch in enumerate(row):
                if ch == '1':
                    return (x,y)
        return (1,1)

    def find_near(self, sx, sy):
        # return nearest path cell to suggested coords
        for r in range(0, max(self.rows,self.cols)):
            for dy in range(-r, r+1):
                for dx in range(-r, r+1):
                    x = sx + dx
                    y = sy + dy
                    if 0 <= y < self.rows and 0 <= x < self.cols:
                        if self.is_path((x,y)):
                            return (x,y)
        return self.find_start()

    def draw(self, surf):
        cs = self.cell_size
        for y,row in enumerate(self.grid):
            for x,ch in enumerate(row):
                if ch == '0':
                    pygame.draw.rect(surf, (33,33,120), (x*cs, y*cs, cs, cs))
                else:
                    # path background
                    pygame.draw.rect(surf, (0,0,0), (x*cs, y*cs, cs, cs))
                    # dot
                    if (x,y) in self.dots:
                        pygame.draw.circle(surf, (200,200,50), (x*cs + cs//2, y*cs + cs//2), max(2, cs//8))
