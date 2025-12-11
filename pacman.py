# pacman.py
import pygame

class Pacman:
    def __init__(self, start_cell, cell_size, sprite=None):
        self.cell_size = cell_size
        self.cell = start_cell
        self.x = self.cell[0] * cell_size
        self.y = self.cell[1] * cell_size
        self.rect = pygame.Rect(self.x, self.y, cell_size, cell_size)
        self.speed = 120  # pixels per second
        self.dir = (0,0)
        self.next_dir = (0,0)
        self.sprite = sprite
        self.score = 0
        self.lives = 3

    def request_dir(self, d):
        self.next_dir = d

    def _can_move(self, cell, maze):
        return maze.is_path(cell)

    def update(self, dt, maze):
        # try to change direction if possible
        if self.next_dir != self.dir and self.next_dir != (0,0):
            nx = (self.cell[0] + self.next_dir[0], self.cell[1] + self.next_dir[1])
            if self._can_move(nx, maze):
                self.dir = self.next_dir

        if self.dir != (0,0):
            target_cell = (self.cell[0] + self.dir[0], self.cell[1] + self.dir[1])
            if self._can_move(target_cell, maze):
                # move smoothly towards target cell
                target_x = target_cell[0] * self.cell_size
                target_y = target_cell[1] * self.cell_size
                # step
                step = self.speed * dt
                if self.x < target_x:
                    self.x = min(self.x + step, target_x)
                elif self.x > target_x:
                    self.x = max(self.x - step, target_x)
                if self.y < target_y:
                    self.y = min(self.y + step, target_y)
                elif self.y > target_y:
                    self.y = max(self.y - step, target_y)
                if int(self.x) == target_x and int(self.y) == target_y:
                    self.cell = target_cell
                    # eat dot
                    if self.cell in maze.dots:
                        maze.dots.remove(self.cell)
                        self.score += 10
            else:
                # blocked
                self.dir = (0,0)

        self.rect.topleft = (int(self.x), int(self.y))

    def draw(self, surf):
        if self.sprite:
            surf.blit(self.sprite, (int(self.x), int(self.y)))
        else:
            pygame.draw.rect(surf, (255,255,0), self.rect)

    def lose_life(self):
        self.lives -= 1

    def reset_to_start(self, maze):
        self.cell = maze.find_start()
        self.x = self.cell[0]*self.cell_size
        self.y = self.cell[1]*self.cell_size
        self.rect.topleft = (self.x, self.y)
        self.dir = (0,0)
        self.next_dir = (0,0)
