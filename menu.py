# menu.py
import pygame

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 48)

    def draw_start(self):
        self.screen.fill((0,0,0))
        title = self.font.render("Pac-Man AI (Press SPACE to Start)", True, (255,255,0))
        self.screen.blit(title, (40, self.screen.get_height()//2 - 30))

    def draw_game_over(self, score):
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0,0,0,180))
        self.screen.blit(overlay, (0,0))
        f = pygame.font.SysFont(None, 64)
        self.screen.blit(f.render("GAME OVER", True, (255,50,50)), (self.screen.get_width()//2 - 160, 200))
        self.screen.blit(f.render(f"Score: {score}", True, (255,255,255)), (self.screen.get_width()//2 - 100, 280))
        self.screen.blit(pygame.font.SysFont(None,28).render("Press R to Restart", True, (200,200,200)), (self.screen.get_width()//2 - 90, 360))
        pygame.display.flip()
        # pause until key
        self._wait_key()

    def draw_win(self, score):
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0,0,0,180))
        self.screen.blit(overlay, (0,0))
        f = pygame.font.SysFont(None, 64)
        self.screen.blit(f.render("YOU WIN!", True, (50,255,50)), (self.screen.get_width()//2 - 120, 200))
        self.screen.blit(f.render(f"Score: {score}", True, (255,255,255)), (self.screen.get_width()//2 - 100, 280))
        self.screen.blit(pygame.font.SysFont(None,28).render("Press R to Restart", True, (200,200,200)), (self.screen.get_width()//2 - 90, 360))
        pygame.display.flip()
        self._wait_key()

    def _wait_key(self):
        import pygame, sys
        waiting = True
        while waiting:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_r:
                        waiting = False
                    if e.key == pygame.K_ESCAPE:
                        pygame.quit(); sys.exit()
