import pygame
import random
import time
import math

# Game constants
WIDTH, HEIGHT = 800, 600
TARGET_RADIUS = 30
NUM_TARGETS = 30
TARGET_COLOR = (136, 6, 206)
BG_COLOR = (30, 30, 30)
FONT_COLOR = (255, 255, 255)
FPS = 60

pygame.init()
font = pygame.font.SysFont("Times New Roman", 24)

# Utility functions
def distance(p1, p2):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

class Target:
    def __init__(self, radius=TARGET_RADIUS, color=TARGET_COLOR):
        self.radius = radius
        self.color = color
        self.position = self.random_position()

    def random_position(self):
        x = random.randint(self.radius, WIDTH - self.radius)
        y = random.randint(self.radius, HEIGHT - self.radius)
        return (x, y)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.position, self.radius)

    def is_hit(self, pos):
        return distance(self.position, pos) <= self.radius

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Aim Trainer - Like Aim Lab")

        self.clock = pygame.time.Clock()
        self.running = True

        self.targets_hit = 0
        self.total_clicks = 0
        self.target = Target()
        self.reaction_times = []
        self.last_target_time = time.time()

    def reset_target(self):
        self.target = Target()
        self.last_target_time = time.time()

    def draw_text(self, text, x, y):
        label = font.render(text, True, FONT_COLOR)
        self.screen.blit(label, (x, y))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.total_clicks += 1
                if self.target.is_hit(pygame.mouse.get_pos()):
                    reaction_time = time.time() - self.last_target_time
                    self.reaction_times.append(reaction_time)
                    self.targets_hit += 1
                    if self.targets_hit < NUM_TARGETS:
                        self.reset_target()
                    else:
                        self.running = False

    def game_loop(self):
        self.reset_target()
        while self.running:
            self.screen.fill(BG_COLOR)
            self.target.draw(self.screen)

            # Accuracy calculation
            accuracy = (self.targets_hit / self.total_clicks * 100) if self.total_clicks > 0 else 100

            # Draw HUD
            self.draw_text(f"Targets Hit: {self.targets_hit}/{NUM_TARGETS}", 10, 10)
            self.draw_text(f"Accuracy: {accuracy:.1f}%", 10, 40)

            self.handle_events()
            pygame.display.flip()
            self.clock.tick(FPS)

        self.end_screen()

    def end_screen(self):
        self.screen.fill(BG_COLOR)
        avg_time = sum(self.reaction_times) / len(self.reaction_times) if self.reaction_times else 0
        accuracy = (self.targets_hit / self.total_clicks * 100) if self.total_clicks > 0 else 100
        misses = self.total_clicks - self.targets_hit

        # Display results
        self.draw_text("Game Over!", WIDTH // 2 - 80, HEIGHT // 2 - 70)
        self.draw_text(f"Average Reaction Time: {avg_time:.3f} sec", WIDTH // 2 - 170, HEIGHT // 2 - 30)
        self.draw_text(f"Accuracy: {accuracy:.1f}% ({self.targets_hit} hits / {self.total_clicks} clicks)", WIDTH // 2 - 200, HEIGHT // 2 + 10)
        self.draw_text(f"Misses: {misses}", WIDTH // 2 - 50, HEIGHT // 2 + 50)
        self.draw_text("Press any key to quit...", WIDTH // 2 - 130, HEIGHT // 2 + 90)
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN or event.type == pygame.QUIT:
                    waiting = False

        pygame.quit()

if __name__ == "__main__":
    Game().game_loop()
