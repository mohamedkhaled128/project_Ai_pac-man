# game.py
import pygame
import sys
import time

from maze import Maze
from pacman import Pacman
from ghost import Ghost
from gui import GUI
from utils import load_sprite

CELL = 28
AI_TICK = 0.25
FPS = 60
SPAWN_INVUL_SECONDS = 2.0

def _draw_overlay_nonblocking(screen, gui, title_text, subtitle_text=None):
    overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))

    title_surf = gui.big_font.render(title_text, True, (255, 255, 255))
    screen.blit(title_surf, (screen.get_width()//2 - title_surf.get_width()//2, screen.get_height()//2 - 80))

    if subtitle_text:
        sub_surf = gui.title_font.render(subtitle_text, True, (200, 200, 200))
        screen.blit(sub_surf, (screen.get_width()//2 - sub_surf.get_width()//2, screen.get_height()//2))

    hint = gui.small_font.render("Press R to Restart or ESC to Quit", True, (180,180,180))
    screen.blit(hint, (screen.get_width()//2 - hint.get_width()//2, screen.get_height()//2 + 60))

def run():
    pygame.init()

    maze = Maze("assets/map.txt", cell_size=CELL)
    rows, cols = maze.rows, maze.cols
    SCREEN_W = cols * CELL
    SCREEN_H = rows * CELL
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption("Pac‑Man AI")
    clock = pygame.time.Clock()

    gui = GUI(screen, CELL)

    pacman_sprite = None
    try:
        pacman_sprite = load_sprite("assets/pacman.png", (CELL, CELL))
    except Exception:
        pacman_sprite = None

    pacman = Pacman(maze.find_start(), CELL, sprite=pacman_sprite)
    pacman.invulnerable_until = time.time() + SPAWN_INVUL_SECONDS

    ghosts = [
        Ghost(maze.find_near(5, 5), CELL, (255,0,0), algo="bfs"),
        Ghost(maze.find_near(6, 5), CELL, (0,255,0), algo="astar"),
        Ghost(maze.find_near(7, 5), CELL, (255,182,193), algo="dfs"),
        Ghost(maze.find_near(8, 5), CELL, (255,165,0), algo="random"),
    ]
    for g in ghosts:
        g.path = [g.cell]
        g._last_repath = 0.0

    game_state = "menu"   # menu / playing / game_over / win
    running = True
    last_ai_tick = 0.0
    power_dot_active = False
    power_dot_timer = 0.0

    # helper: call whichever input API pacman exposes
    def set_player_held_dir(p, d):
        if hasattr(p, "set_held_direction"):
            p.set_held_direction(d)
        elif hasattr(p, "request_dir"):
            # request_dir used to buffer; here we pass (0,0) to indicate stop
            p.request_dir(d if d is not None else (0,0))
        else:
            # fallback: try to set next_dir attribute
            setattr(p, "next_dir", d if d is not None else (0,0))

    while running:
        dt = clock.tick(FPS) / 1000.0
        now = time.time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game_state == "menu":
                    game_state = "playing"
                    pacman.invulnerable_until = time.time() + SPAWN_INVUL_SECONDS
                    for g in ghosts:
                        g.path = [g.cell]
                        g._last_repath = 0.0

                if event.key == pygame.K_r and game_state in ("game_over", "win"):
                    maze = Maze("assets/map.txt", cell_size=CELL)
                    pacman = Pacman(maze.find_start(), CELL, sprite=pacman_sprite)
                    pacman.invulnerable_until = time.time() + SPAWN_INVUL_SECONDS
                    ghosts = [
                        Ghost(maze.find_near(5, 5), CELL, (255,0,0), algo="bfs"),
                        Ghost(maze.find_near(6, 5), CELL, (0,255,0), algo="astar"),
                        Ghost(maze.find_near(7, 5), CELL, (255,182,193), algo="dfs"),
                        Ghost(maze.find_near(8, 5), CELL, (255,165,0), algo="random"),
                    ]
                    for g in ghosts:
                        g.path = [g.cell]
                        g._last_repath = 0.0
                    game_state = "playing"

                if event.key == pygame.K_ESCAPE:
                    running = False

        # stop updates when game over / win (still allow keys)
        if game_state in ("game_over", "win"):
            screen.fill((0,0,0))
            maze.draw(screen)
            pacman.draw(screen)
            for g in ghosts:
                g.draw(screen)
            gui.draw_hud(pacman.score, max(0, pacman.lives), power_dot_active)
            if game_state == "game_over":
                _draw_overlay_nonblocking(screen, gui, "GAME OVER", f"Score: {pacman.score}")
            else:
                _draw_overlay_nonblocking(screen, gui, "YOU WIN!", f"Score: {pacman.score}")
            pygame.display.flip()
            continue

        # read input: get held direction or None
        keys = pygame.key.get_pressed()
        held = None
        if keys[pygame.K_LEFT]:
            held = (-1, 0)
        elif keys[pygame.K_RIGHT]:
            held = (1, 0)
        elif keys[pygame.K_UP]:
            held = (0, -1)
        elif keys[pygame.K_DOWN]:
            held = (0, 1)

        set_player_held_dir(pacman, held)

        # update pacman
        pacman.update(dt, maze)

        # power pellet eaten?
        if getattr(pacman, "power_eaten", False):
            power_dot_active = True
            power_dot_timer = 8.0
            for g in ghosts:
                g.set_frightened(power_dot_timer)
            pacman.power_eaten = False

        # AI tick
        if now - last_ai_tick > AI_TICK:
            for g in ghosts:
                g.set_target(pacman.cell)
                g.compute_path(maze)
            last_ai_tick = now

        # update ghosts
        for g in ghosts:
            g.update(dt, maze)

        # collisions (respect invulnerability and ensure single-hit)
        for g in ghosts:
            if getattr(pacman, "invulnerable_until", 0.0) > time.time():
                continue
            if g.collides(pacman):
                if g.mode == "frightened":
                    g.reset_to_house(maze)
                    pacman.score += 100
                    pacman.invulnerable_until = time.time() + 0.7
                else:
                    pacman.lose_life()
                    if pacman.lives < 0:
                        pacman.lives = 0
                    pacman.reset_to_start(maze)
                    pacman.invulnerable_until = time.time() + SPAWN_INVUL_SECONDS
                    # reset ghosts to avoid repeated immediate collisions
                    for gg in ghosts:
                        gg.path = [gg.cell]
                        gg._last_repath = 0.0
                        gg.mode = "chase"
                        gg.frightened_until = 0.0
                    if pacman.lives <= 0:
                        game_state = "game_over"
                    break

        # power-dot timer
        if power_dot_active:
            power_dot_timer -= dt
            if power_dot_timer <= 0:
                power_dot_active = False
                for g in ghosts:
                    g.mode = "chase"
                    g.frightened_until = 0.0

        # win condition
        if len(maze.dots) == 0:
            game_state = "win"

        # draw everything
        screen.fill((0,0,0))
        maze.draw(screen)
        pacman.draw(screen)
        for g in ghosts:
            g.draw(screen)
        gui.draw_hud(pacman.score, max(0, pacman.lives), power_dot_active)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    run()
