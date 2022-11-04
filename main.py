import pygame
import sys
import time
import math
import os
import random
from levels import *
 
pygame.init()

WIN_WIDTH = 1200
WIN_HEIGHT = 816
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
 
pygame.display.set_caption("Tanks")

pygame.display.set_icon(pygame.image.load(
    os.path.join("graphics", "tank.png")).convert_alpha())

pygame.mouse.set_visible(False)

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
PURPLE = (255, 0, 255)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

GRAY_1 = (128, 128, 128)
GRAY_2 = (64, 64, 64)
GRAY_3 = (32, 32, 32)

player_group = pygame.sprite.GroupSingle()

barral_group = pygame.sprite.GroupSingle()

enemy_group = pygame.sprite.Group()

player_bullet_group = pygame.sprite.Group()

enemy_bullet_group = pygame.sprite.Group()

tile_group = pygame.sprite.Group()

explosion_group = []

font_1 = pygame.font.Font(os.path.join("font", "jersey_M54.ttf"), 42)
font_2 = pygame.font.Font(os.path.join("font", "jersey_M54.ttf"), 86)

space_to_start_font = font_1.render("Press Space To Start", True, WHITE)
space_to_start_font_rect = space_to_start_font.get_rect(center=(WIN_WIDTH / 2, WIN_WIDTH / 2))

successful_font = font_2.render("Successful", True, GREEN)
successful_font_rect = successful_font.get_rect(center=(WIN_WIDTH / 2, WIN_HEIGHT / 2))

failed_font = font_2.render("Failed", True, RED)
failed_font_rect = failed_font.get_rect(center=(WIN_WIDTH / 2, WIN_HEIGHT / 2))

shoot_timer = pygame.USEREVENT + 1
pygame.time.set_timer(shoot_timer, 300)

player_shoot_timer = pygame.USEREVENT + 2
pygame.time.set_timer(player_shoot_timer, 150)

    
class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.speed = 160
    
        self.width = 48
        self.height = self.width
    
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(BLUE)
    
        self.rect = self.image.get_rect(topleft=(pos_x, pos_y))
    
        self.vector2 = pygame.math.Vector2(0, 0)
        self.rect_pos = pygame.math.Vector2(self.rect.x, self.rect.y)

    def horizontal_collisions(self):
        for sprite in tile_group.sprites():
            if sprite.rect.colliderect(self):
                if self.vector2.x > 0:
                    self.rect.right = sprite.rect.left
                    self.rect_pos.x = sprite.rect.left - self.width
    
                elif self.vector2.x < 0:
                    self.rect.left = sprite.rect.right
                    self.rect_pos.x = sprite.rect.right
    
    def vertical_collisions(self):
        for sprite in tile_group.sprites():
            if sprite.rect.colliderect(self):
                if self.vector2.y > 0:
                    self.rect.bottom = sprite.rect.top
                    self.rect_pos.y = sprite.rect.top - self.height
    
                elif self.vector2.y < 0:
                    self.rect.top = sprite.rect.bottom
                    self.rect_pos.y = sprite.rect.bottom
    
    def horizontal_movement(self, delta_time):
        self.key = pygame.key.get_pressed()

        if self.key[pygame.K_a]:
            self.vector2.x = -1
        elif self.key[pygame.K_d]:
            self.vector2.x = 1
        else:
            self.vector2.x = 0

        self.rect_pos.x += self.vector2.x * self.speed * delta_time
        self.rect.x = self.rect_pos.x

    def vertical_movement(self, delta_time):
        self.key = pygame.key.get_pressed()

        if self.key[pygame.K_w]:
            self.vector2.y = -1
        elif self.key[pygame.K_s]:
            self.vector2.y = 1
        else:
            self.vector2.y = 0

        self.rect_pos.y += self.vector2.y * self.speed * delta_time
        self.rect.y = self.rect_pos.y

    def update(self, delta_time):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        self.horizontal_movement(delta_time)
        self.horizontal_collisions()

        self.vertical_movement(delta_time)
        self.vertical_collisions()

        pygame.draw.line(WIN, BLUE, (self.rect.x + (self.width / 2), self.rect.y + (self.height / 2)), (mouse_x, mouse_y), 10)
        pygame.draw.circle(WIN, BLUE, (mouse_x, mouse_y), 8)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.speed = random.randint(50, 150)
 
        self.width = 48
        self.height = self.width
 
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(RED)
 
        self.rect = self.image.get_rect(topleft=(pos_x, pos_y))
 
        self.vector2 = pygame.math.Vector2(0, 0)
        self.rect_pos = pygame.math.Vector2(self.rect.x, self.rect.y)

        list = [-1, 1]

        self.vector2.x = random.choice(list)
        self.vector2.y = random.choice(list)
 
    def horizontal_collisions(self):
        for sprite in tile_group.sprites():
            if sprite.rect.colliderect(self):
                if self.vector2.x > 0:
                    self.rect.right = sprite.rect.left
                    self.rect_pos.x = sprite.rect.left - self.width
                    self.vector2.x *= -1
 
                elif self.vector2.x < 0:
                    self.rect.left = sprite.rect.right
                    self.rect_pos.x = sprite.rect.right
                    self.vector2.x *= -1
 
    def vertical_collisions(self):
        for sprite in tile_group.sprites():
            if sprite.rect.colliderect(self):
                if self.vector2.y > 0:
                    self.rect.bottom = sprite.rect.top
                    self.rect_pos.y = sprite.rect.top - self.height
                    self.vector2.y *= -1
 
                elif self.vector2.y < 0:
                    self.rect.top = sprite.rect.bottom
                    self.rect_pos.y = sprite.rect.bottom
                    self.vector2.y *= -1
 
    def horizontal_movement(self, delta_time):
        self.rect_pos.x += self.vector2.x * self.speed * delta_time
        self.rect.x = self.rect_pos.x
 
    def vertical_movement(self, delta_time):
        self.rect_pos.y += self.vector2.y * self.speed * delta_time
        self.rect.y = self.rect_pos.y

    def update(self, delta_time):
        self.horizontal_movement(delta_time)
        self.horizontal_collisions()

        self.vertical_movement(delta_time)
        self.vertical_collisions()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, group, colour_1, colour_2, start, target_x, target_y):
        super().__init__()
        self.group = group

        self.bullet_speed = 225
 
        self.max_bounces = 1
 
        self.width = 18
        self.height = self.width

        self.image = pygame.Surface((self.width, self.height))
 
        self.rect = self.image.get_rect(center=(start))
 
        self.x_center, self.y_center = self.rect.center
 
        self.rise = target_x - self.x_center
        self.run = target_y - self.y_center
 
        self.angle = math.atan2(self.run, self.rise)
 
        self.delta_y = math.sin(self.angle) * self.bullet_speed
        self.delta_x = math.cos(self.angle) * self.bullet_speed
 
        self.rect_pos = pygame.math.Vector2(self.rect.x, self.rect.y)

        self.colour_1 = colour_1
        self.colour_2 = colour_2
 
        self.bounce_index = 0

    def collisions(self):
        for sprite in tile_group.sprites():
            if self.rect.colliderect(sprite):
                left = abs(self.rect.right - sprite.rect.left)
                right = abs(self.rect.left - sprite.rect.right)
                top = abs(self.rect.bottom - sprite.rect.top)
                bottom = abs(self.rect.top - sprite.rect.bottom)

                if left < right and left < top and left < bottom and self.delta_x > 0:
                    self.delta_x *= -1
                    self.bounce_index += 1
            
                elif right < left and right < top and right < bottom and self.delta_x < 0:
                    self.delta_x *= -1
                    self.bounce_index += 1
            
                elif top < left and top < right and top < bottom and self.delta_y > 0:
                    self.delta_y *= -1
                    self.bounce_index += 1
            
                elif bottom < left and bottom < right and bottom < top and self.delta_y < 0:
                    self.delta_y *= -1
                    self.bounce_index += 1

        for sprite in self.group.sprites():
            if self.rect.colliderect(sprite):
                sprite.kill()
                Bullet.kill(self)

        if self.bounce_index > self.max_bounces:
            Bullet.kill(self)
            explosion = Explosion(self.colour_1, self.colour_2, 24, self.rect_pos.x + self.width / 2, self.rect_pos.y + self.height / 2)
            explosion_group.append(explosion)
 
    def movement(self, delta_time):
        self.rect_pos.x += self.delta_x * delta_time
        self.rect_pos.y += self.delta_y * delta_time
 
        self.rect.x = round(self.rect_pos.x)
        self.rect.y = round(self.rect_pos.y)

    def update(self, delta_time):
        self.collisions()
        self.movement(delta_time)

        explosion = Explosion(self.colour_1, self.colour_2, 16, self.rect_pos.x + self.width / 2, self.rect_pos.y + self.height / 2)
        explosion_group.append(explosion)


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.width = 48
        self.height = self.width
 
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(BLACK)
 
        self.rect = self.image.get_rect(topleft=(pos_x, pos_y))


class Level():
    def __init__(self):
        self.current_level = 0
        self.game_active = True

    def level_loader(self):
        if len(enemy_group) == 0:
            self.current_level += 1

            if self.current_level == 1:
                self.clear()
                self.setup(Level_6)
            
            if self.current_level == 2:
                self.clear()
                self.setup(Level_2)

            if self.current_level == 3:
                self.clear()
                self.setup(Level_3)

            if self.current_level == 4:
                self.game_active = False
    
    def clear(self):
        player_group.empty()

        enemy_group.empty()

        player_bullet_group.empty()

        enemy_bullet_group.empty()

        tile_group.empty()

    def setup(self, level_data):
        for row_index, row in enumerate(level_data):
            for col_index, cell in enumerate(row):
                x = col_index * 48
                y = row_index * 48

                if cell == "T":
                    tile = Tile(x, y)
                    tile_group.add(tile)

                if cell == "P":
                    player = Player(x, y)
                    player_group.add(player)

                if cell == "E":
                    enemy = Enemy(x, y)
                    enemy_group.add(enemy)


class Explosion():
    def __init__(self, colour_1, colour_2, radius, pos_x, pos_y):
        self.radius = radius

        self.pos_x = pos_x
        self.pos_y = pos_y

        self.colour_1 = colour_1
        self.colour_2 = colour_2

    def draw(self):
        self.circle_1 = pygame.draw.circle(WIN, self.colour_1, (self.pos_x, self.pos_y), self.radius)
        self.circle_2 = pygame.draw.circle(WIN, self.colour_2, (self.pos_x, self.pos_y), self.radius - (self.radius / 2))

    def scale(self, delta_time):
        if self.radius > 4:
            self.radius -= delta_time * 64
        else:
            explosion_group.remove(explosion_group[0])
    
    def update(self, delta_time):
        self.scale(delta_time)
        self.draw()


def update(delta_time):
    player_group.update(delta_time)
    enemy_group.update(delta_time)
    player_bullet_group.update(delta_time)
    enemy_bullet_group.update(delta_time)

    player_bullet_group.draw(WIN)
    enemy_bullet_group.draw(WIN)
    player_group.draw(WIN)
    enemy_group.draw(WIN)
    tile_group.draw(WIN)

    for explosion in explosion_group:
        explosion.update(delta_time)


def main():
    previous_time = time.time()
    level = Level()

    game_active = False
    can_shoot = False
    just_dided = False
    just_started = True

    while True:
        delta_time = time.time() - previous_time
        previous_time = time.time()

        for event in pygame.event.get():
 
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
 
            if event.type == pygame.KEYDOWN:
 
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                if event.key == pygame.K_SPACE:
                    game_active = True
 
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_button = pygame.mouse.get_pressed()
                
                if mouse_button[0]:
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    explosion = Explosion(BLUE, BLUE, 12, mouse_x, mouse_y)
                    explosion_group.append(explosion)
 
                    if game_active:
                        if can_shoot:
                            target = player_group.sprite.rect.center
                            
                            bullet = Bullet(enemy_group, BLUE, CYAN, target, mouse_x, mouse_y)
                            player_bullet_group.add(bullet)

                            can_shoot = False

            if game_active:
                if event.type == shoot_timer:
                    for sprites in player_group.sprites():
                        player_center_x, player_center_y = sprites.rect.center
                    
                    for sprites in enemy_group.sprites():
                        target = sprites.rect.center
                    
                        bullet = Bullet(player_group, RED, YELLOW, target, player_center_x + random.randint(-200, 200), player_center_y + random.randint(-200, 200))
                        enemy_bullet_group.add(bullet)
                        
                if not can_shoot:
                    if event.type == player_shoot_timer:
                        can_shoot = True

        if game_active:
            level.level_loader()

            WIN.fill(GRAY_3)

            update(delta_time)

            try:
                for sprite in enemy_group.sprites():
                    if sprite.rect.colliderect(player_group.sprite.rect):
                        game_active = False
                        just_dided = True

            except:
                game_active = False
                just_dided = True
            
            if not level.game_active:
                game_active = False
                just_dided = False

            for player_bullet_sprite in player_bullet_group.sprites():
                for enemy_bullet_sprite in enemy_bullet_group.sprites():
                    if player_bullet_sprite.rect.colliderect(enemy_bullet_sprite.rect):
                        player_bullet_sprite.kill()
                        enemy_bullet_sprite.kill()

            just_started = False

        else:
            WIN.fill(GRAY_3)

            for explosion in explosion_group:
                explosion.update(delta_time)

            level.clear()

            level.current_level = 0
            level.game_active = True

            WIN.blit(space_to_start_font, (space_to_start_font_rect))

            if just_dided:
                WIN.blit(failed_font, (failed_font_rect))
            elif not just_dided and not just_started:
                WIN.blit(successful_font, (successful_font_rect))

            mouse_x, mouse_y = pygame.mouse.get_pos()

            pygame.draw.circle(WIN, BLUE, (mouse_x, mouse_y), 8)
                
        pygame.display.update()

if __name__ == "__main__":
    main()
