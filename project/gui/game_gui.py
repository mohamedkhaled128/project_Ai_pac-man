"""
واجهة المستخدم الرسومية للعبة Pac-Man
"""
import pygame
import json
import sys
import math
from pathlib import Path

# إضافة المجلد الرئيسي إلى المسار للاستيراد الصحيح
sys.path.insert(0, str(Path(__file__).parent.parent))

from map import GameMap
from player import Player
from ghost import Ghost
from algorithms import (
    astar, dijkstra, bfs, dfs,
    greedy_best_first, bidirectional_search,
    ida_star, theta_star
)

# Load best algorithm from results file
def load_best_algorithm():
    """Load the best algorithm from results file"""
    results_file = Path(__file__).parent.parent / "best_algorithm.json"
    
    algorithm_map = {
        'A*': astar,
        'Dijkstra': dijkstra,
        'BFS': bfs,
        'DFS': dfs,
        'Greedy Best-First': greedy_best_first,
        'Bidirectional': bidirectional_search,
        'IDA*': ida_star,
        'Theta*': theta_star
    }
    
    try:
        if results_file.exists():
            with open(results_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                best_name = data.get('best_algorithm', 'A*')
                return algorithm_map.get(best_name, astar), best_name
    except:
        pass
    
    # Default: A*
    return astar, 'A*'

class GameGUI:
    """Graphical User Interface class"""
    
    def __init__(self, map_path):
        pygame.init()
        
        # Load map first to determine size
        self.game_map = GameMap(map_path)
        self.tile = self.game_map.tile_size
        self.map_path = map_path
        
        # Calculate screen size based on map size
        map_width = len(self.game_map.grid[0]) if self.game_map.grid else 40
        map_height = len(self.game_map.grid) if self.game_map.grid else 25
        
        self.SCREEN_W = map_width * self.tile
        self.SCREEN_H = map_height * self.tile + 50  # Extra space for info
        
        self.screen = pygame.display.set_mode((self.SCREEN_W, self.SCREEN_H))
        pygame.display.set_caption("Pac-Man - AI Algorithms")
        self.clock = pygame.time.Clock()
        
        # Fonts
        self.font = pygame.font.SysFont(None, 24)
        self.big_font = pygame.font.SysFont(None, 48)
        self.game_over_font = pygame.font.SysFont(None, 96)

        # Game control flags
        self.running = True
        self.game_over = False

        # Initialize entities/state
        self._init_game_entities()

    def _init_game_entities(self):
        """Initialize or reset player, ghosts, map, score."""
        # Reload map to reset pellets/positions
        self.game_map = GameMap(self.map_path)
        self.tile = self.game_map.tile_size

        # Load best algorithm
        best_algorithm, alg_name = load_best_algorithm()
        self.algorithm_name = alg_name
        
        # Create player and ghosts
        self.player = Player(self.game_map.start, self.tile)
        self.ghosts = []
        
        # Ghost colors (more colors)
        ghost_colors = [
            (255, 0, 0),      # Red
            (255, 128, 0),    # Orange
            (255, 0, 255),    # Magenta
            (0, 255, 255),    # Cyan
            (255, 255, 0),    # Yellow
            (0, 255, 0),      # Green
            (128, 0, 255),    # Purple
            (255, 192, 203)   # Pink
        ]
        
        # Create ghosts based on number in map
        for i, ghost_pos in enumerate(self.game_map.ghost_positions):
            color = ghost_colors[i % len(ghost_colors)]
            self.ghosts.append(
                Ghost(ghost_pos, self.tile, color, self.game_map, best_algorithm)
            )
        
        # If no ghosts, add one at default position
        if not self.ghosts:
            default_pos = (5, 3) if self.game_map.passable((5, 3)) else (1, 1)
            self.ghosts.append(
                Ghost(default_pos, self.tile, (255, 0, 0), self.game_map, best_algorithm)
            )
        
        # Game state
        self.score = 0
        self.lives = 3
        self.game_over = False
        self.game_over_timer = 0
    
    def handle_events(self):
        """Handle events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if self.game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self._init_game_entities()
        
        keys = pygame.key.get_pressed()
        if self.game_over:
            return
        if keys[pygame.K_UP]:
            self.player.request_move((0, -1))
        if keys[pygame.K_DOWN]:
            self.player.request_move((0, 1))
        if keys[pygame.K_LEFT]:
            self.player.request_move((-1, 0))
        if keys[pygame.K_RIGHT]:
            self.player.request_move((1, 0))
    
    def update(self):
        """Update game state"""
        if self.game_over:
            return
        dt = self.clock.tick(30)
        
        # تحديث اللاعب
        self.player.update(self.game_map)
        
        # تحديث الأشباح
        for g in self.ghosts:
            g.update(self.player.pos)
        
        # Collect points
        if tuple(self.player.pos) in self.game_map.pellets:
            self.game_map.pellets.remove(tuple(self.player.pos))
            self.score += 10
        
        if tuple(self.player.pos) in self.game_map.power_pellets:
            self.game_map.power_pellets.remove(tuple(self.player.pos))
            for g in self.ghosts:
                g.frighten(300)
            self.score += 50
        
        # Collision with ghosts
        for g in self.ghosts:
            if g.rect.colliderect(self.player.rect):
                if g.state == "FRIGHTENED":
                    g.respawn()
                    self.score += 200
                else:
                    self.lives -= 1
                    self.player.reset(self.game_map.start)
                    for g2 in self.ghosts:
                        g2.reset()
                    if self.lives <= 0:
                        self.game_over = True
    
    def draw(self):
        """Draw the game"""
        self.screen.fill((0, 0, 0))
        
        # Draw walls
        for y, row in enumerate(self.game_map.grid):
            for x, ch in enumerate(row):
                rx, ry = x * self.tile, y * self.tile
                if ch == '#':
                    pygame.draw.rect(self.screen, (33, 33, 255), 
                                    (rx, ry, self.tile, self.tile))
        
        # Draw pellets
        for p in list(self.game_map.pellets):
            pygame.draw.circle(self.screen, (255, 255, 255),
                             (p[0]*self.tile + self.tile//2,
                              p[1]*self.tile + self.tile//2), 3)
        
        # Draw power pellets
        for p in list(self.game_map.power_pellets):
            pygame.draw.circle(self.screen, (255, 255, 0),
                             (p[0]*self.tile + self.tile//2,
                              p[1]*self.tile + self.tile//2), 6)
        
        # Draw player
        self.player.draw(self.screen)
        
        # Draw ghosts
        for g in self.ghosts:
            g.draw(self.screen)
        
        # Draw info
        info_text = f"Score: {self.score}   Lives: {self.lives}   Algorithm: {self.algorithm_name}"
        txt = self.font.render(info_text, True, (255, 255, 255))
        self.screen.blit(txt, (10, 10))
        
        # Win message
        if not self.game_map.pellets and not self.game_map.power_pellets:
            win = self.big_font.render("YOU WIN!", True, (0, 255, 0))
            win_rect = win.get_rect(center=(self.SCREEN_W//2, self.SCREEN_H//2))
            self.screen.blit(win, win_rect)
        
        # Game over message
        if self.game_over:
            # Animate scale up
            self.game_over_timer += 1
            scale = 1.0 + min(0.6, self.game_over_timer * 0.02)

            base_surface = self.game_over_font.render("GAME OVER", True, (255, 0, 0))
            w, h = base_surface.get_size()
            scaled_surface = pygame.transform.smoothscale(base_surface, (int(w * scale), int(h * scale)))
            lose_rect = scaled_surface.get_rect(center=(self.SCREEN_W//2, self.SCREEN_H//2 - 20))
            self.screen.blit(scaled_surface, lose_rect)

            restart = self.font.render("Press R to Restart", True, (255, 255, 255))
            restart_rect = restart.get_rect(center=(self.SCREEN_W//2, self.SCREEN_H//2 + 30))
            self.screen.blit(restart, restart_rect)
        
        pygame.display.flip()
    
    def run(self):
        """Run the game"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
        
        pygame.quit()

def main():
    """Main function"""
    map_path = Path(__file__).parent.parent / "maps" / "map1.txt"
    game = GameGUI(map_path)
    game.run()

if __name__ == "__main__":
    main()

