import pygame
import sys
from enum import Enum
from dataclasses import dataclass

# ---------- Constants and Enums ----------
class GameState(Enum):
    TITLE = 0
    PLAYING = 1
    PAUSED = 2
    GAME_OVER = 3
    LEVEL_COMPLETE = 4
    GAME_WON = 5

class Direction(Enum):
    LEFT = 0
    RIGHT = 1

@dataclass
class Tile:
    x: int
    y: int
    type: str

# ---------- Game Configuration ----------
WIDTH, HEIGHT = 600, 400
FPS = 60
TILE_SIZE = 16
GRAVITY = 0.5
JUMP_FORCE = -11
PLAYER_SPEED = 5

# ---------- Initialize Pygame ----------
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# ---------- Asset Classes ----------
class MarioAssets:
    GROUND = pygame.Color('#6B8C42')
    SKY = pygame.Color('#6BE0F7')
    BRICK = pygame.Color('#C56B31')
    COIN_ANIM = [pygame.Color('#F7D308'), pygame.Color('#F7B508')]
    
    @staticmethod
    def draw_block(surface, rect, color):
        pygame.draw.rect(surface, color, rect)
        pygame.draw.rect(surface, pygame.Color('black'), rect, 1)

# ---------- Game Entities ----------
class Mario(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((16, 32))
        self.image.fill(pygame.Color('red'))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.velocity = pygame.Vector2(0, 0)
        self.state = 'small'
        self.direction = Direction.RIGHT

    def update(self, tiles):
        self.velocity.y += GRAVITY
        self.rect.x += self.velocity.x
        self.collide('x', tiles)
        self.rect.y += self.velocity.y
        self.collide('y', tiles)

    def collide(self, axis, tiles):
        for tile in tiles:
            if self.rect.colliderect(tile.rect):
                if axis == 'x':
                    if self.velocity.x > 0:
                        self.rect.right = tile.rect.left
                    elif self.velocity.x < 0:
                        self.rect.left = tile.rect.right
                if axis == 'y':
                    if self.velocity.y > 0:
                        self.rect.bottom = tile.rect.top
                        self.velocity.y = 0
                    elif self.velocity.y < 0:
                        self.rect.top = tile.rect.bottom
                        self.velocity.y = 0

class Goomba(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((16, 16))
        self.image.fill(pygame.Color('brown'))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.direction = Direction.LEFT
        self.speed = 2

    def update(self, tiles):
        self.rect.x += -self.speed if self.direction == Direction.LEFT else self.speed
        if not any(t.rect.collidepoint(self.rect.midbottom) for t in tiles):
            self.direction = Direction.RIGHT if self.direction == Direction.LEFT else Direction.LEFT

# ---------- Level Data ----------
LEVEL_1_1 = [
    # Ground
    *[Tile(x*TILE_SIZE, 13*TILE_SIZE, 'ground') for x in range(0, 60)],
    # Pipes
    Tile(10*TILE_SIZE, 10*TILE_SIZE, 'pipe'),
    Tile(20*TILE_SIZE, 8*TILE_SIZE, 'pipe'),
    # Bricks
    Tile(15*TILE_SIZE, 9*TILE_SIZE, 'brick'),
    Tile(16*TILE_SIZE, 9*TILE_SIZE, 'brick'),
    # Enemies
    Tile(18*TILE_SIZE, 12*TILE_SIZE, 'goomba'),
]

# ---------- Game Manager ----------
class MarioGame:
    def __init__(self):
        self.state = GameState.TITLE
        self.level = 1
        self.player = Mario(100, 100)
        self.tiles = []
        self.enemies = pygame.sprite.Group()
        self.load_level(LEVEL_1_1)
        self.camera_x = 0

    def load_level(self, level_data):
        self.tiles.clear()
        self.enemies.empty()
        
        for tile in level_data:
            if tile.type == 'ground':
                self.tiles.append(pygame.Rect(tile.x, tile.y, TILE_SIZE, TILE_SIZE))
            elif tile.type == 'goomba':
                self.enemies.add(Goomba(tile.x, tile.y))

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player.velocity.x = -PLAYER_SPEED
            self.player.direction = Direction.LEFT
        elif keys[pygame.K_RIGHT]:
            self.player.velocity.x = PLAYER_SPEED
            self.player.direction = Direction.RIGHT
        else:
            self.player.velocity.x = 0
            
        if keys[pygame.K_SPACE]:
            if self.player.velocity.y == 0:
                self.player.velocity.y = JUMP_FORCE

    def update_camera(self):
        self.camera_x = max(0, self.player.rect.centerx - WIDTH//2)

    def draw(self):
        screen.fill(MarioAssets.SKY)
        
        # Draw ground
        for tile in self.tiles:
            adjusted_rect = tile.move(-self.camera_x, 0)
            MarioAssets.draw_block(screen, adjusted_rect, MarioAssets.GROUND)
        
        # Draw player
        player_pos = self.player.rect.move(-self.camera_x, 0)
        screen.blit(self.player.image, player_pos)
        
        # Draw enemies
        for enemy in self.enemies:
            enemy_pos = enemy.rect.move(-self.camera_x, 0)
            screen.blit(enemy.image, enemy_pos)
        
        pygame.display.flip()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if self.state == GameState.PLAYING:
                self.handle_input()
                self.player.update(self.tiles)
                self.enemies.update(self.tiles)
                self.update_camera()

            self.draw()
            clock.tick(FPS)

if __name__ == "__main__":
    game = MarioGame()
    game.run()
