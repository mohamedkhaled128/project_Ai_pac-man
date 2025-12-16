"""
كلاس الأشباح - يستخدم الخوارزميات من مجلد algorithms
"""
import pygame
from algorithms import astar  # افتراضي: A*

class Ghost:
    """كلاس الشبح في اللعبة"""
    
    def __init__(self, pos, tile, color, gamemap, algorithm=astar):
        """
        تهيئة الشبح
        
        Args:
            pos: موضع البداية
            tile: حجم البلاطة
            color: لون الشبح
            gamemap: خريطة اللعبة
            algorithm: الخوارزمية المستخدمة (افتراضي: A*)
        """
        self.start = pos
        self.pos = list(pos)
        self.tile = tile
        self.color = color
        self.gamemap = gamemap
        self.algorithm = algorithm
        self.rect = pygame.Rect(self.pos[0]*tile, self.pos[1]*tile, tile, tile)
        self.path = []
        self.state = "CHASE"
        self.fright_timer = 0
        self.move_timer = 0
        self.move_speed = 3  # يتحرك كل 3 إطارات (أبطأ)
    
    def update(self, target):
        """تحديث موضع الشبح"""
        if self.fright_timer > 0:
            self.fright_timer -= 1
            if self.fright_timer <= 0:
                self.state = "CHASE"
        
        # زيادة عداد الحركة
        self.move_timer += 1
        
        if self.state == "FRIGHTENED":
            # في حالة الخوف، يتحرك أبطأ
            if self.move_timer >= self.move_speed * 2:
                self.step_away()
                self.move_timer = 0
            return
        
        # إعادة حساب المسار إذا تغير الهدف
        if not self.path or tuple(target) != self.path[-1]:
            start = tuple(self.pos)
            goal = tuple(target)
            self.path = self.algorithm(self.gamemap, start, goal)
            if self.path and len(self.path) > 1:
                self.path = self.path[1:]  # إزالة الموضع الحالي
        
        # التحرك على المسار (كل عدة إطارات)
        if self.path and self.move_timer >= self.move_speed:
            nxt = self.path.pop(0)
            self.pos = list(nxt)
            self.rect.topleft = (self.pos[0]*self.tile, self.pos[1]*self.tile)
            self.move_timer = 0
    
    def step_away(self):
        """التحرك عشوائياً عند الخوف"""
        import random
        nlist = list(self.gamemap.neighbors(tuple(self.pos)))
        if nlist:
            choice = random.choice(nlist)
            self.pos = [choice[0], choice[1]]
            self.rect.topleft = (self.pos[0]*self.tile, self.pos[1]*self.tile)
    
    def draw(self, surface):
        """رسم الشبح"""
        col = (100, 100, 255) if self.state == "FRIGHTENED" else self.color
        pygame.draw.rect(surface, col, 
                        (self.pos[0]*self.tile, self.pos[1]*self.tile, 
                         self.tile, self.tile))
    
    def frighten(self, frames):
        """جعل الشبح خائفاً"""
        self.state = "FRIGHTENED"
        self.fright_timer = frames
    
    def respawn(self):
        """إعادة إحياء الشبح"""
        self.pos = list(self.start)
        self.rect.topleft = (self.pos[0]*self.tile, self.pos[1]*self.tile)
        self.state = "CHASE"
    
    def reset(self):
        """إعادة تعيين الشبح"""
        self.respawn()
