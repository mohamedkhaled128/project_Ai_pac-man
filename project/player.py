import pygame
class Player:
    def __init__(self,pos,tile):
        self.pos = list(pos)
        self.tile = tile
        self.rect = pygame.Rect(self.pos[0]*tile,self.pos[1]*tile,tile,tile)
        self._req = None
    def request_move(self,delta):
        self._req = delta
    def update(self,game_map):
        if self._req:
            nx = self.pos[0] + self._req[0]
            ny = self.pos[1] + self._req[1]
            if game_map.in_bounds((nx,ny)) and game_map.passable((nx,ny)):
                self.pos = [nx,ny]
                self.rect.topleft = (nx*self.tile, ny*self.tile)
        self._req = None
    def draw(self,surface):
        cx = self.pos[0]*self.tile + self.tile//2
        cy = self.pos[1]*self.tile + self.tile//2
        pygame.draw.circle(surface,(255,255,0),(cx,cy),self.tile//2-2)
    def reset(self,start):
        self.pos = list(start)
        self.rect.topleft = (self.pos[0]*self.tile,self.pos[1]*self.tile)
