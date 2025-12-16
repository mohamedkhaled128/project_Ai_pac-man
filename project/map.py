from pathlib import Path
class GameMap:
    def __init__(self,path):
        self.tile_size = 32
        self.grid = []
        self.pellets = set()
        self.power_pellets = set()
        self.ghost_positions = []
        self.start = (1,1)
        for y,line in enumerate(Path(path).read_text().splitlines()):
            row = list(line.rstrip("\n"))
            self.grid.append(row)
            for x,ch in enumerate(row):
                if ch == '.':
                    self.pellets.add((x,y))
                if ch == 'o':
                    self.power_pellets.add((x,y))
                if ch == 'P':
                    self.start = (x,y)
                    self.grid[y][x] = ' '
                if ch == 'G':
                    self.ghost_positions.append((x,y))
                    self.grid[y][x] = ' '
    def in_bounds(self,pos):
        x,y = pos
        return 0 <= y < len(self.grid) and 0 <= x < len(self.grid[0])
    def passable(self,pos):
        x,y = pos
        if not self.in_bounds(pos):
            return False
        if y >= len(self.grid) or x >= len(self.grid[y]):
            return False
        return self.grid[y][x] != '#'
    def neighbors(self,pos):
        x,y = pos
        for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
            n = (x+dx,y+dy)
            if self.in_bounds(n) and self.passable(n):
                yield n
