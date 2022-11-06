# import
import pygame
import sys
import time
import math
import os
import random
from levels import *
 
pygame.init()

# window
WIN_WIDTH = 1200
WIN_HEIGHT = 816
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
 
pygame.display.set_caption("Tanks")

pygame.display.set_icon(pygame.image.load(
    os.path.join("graphics", "tank.png")).convert_alpha())

pygame.mouse.set_visible(False)

# colours
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
PURPLE = (255, 0, 255)

ORANGE = (255, 165, 0)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

GRAY = (32, 32, 32)

# sprite groups
player_group = pygame.sprite.GroupSingle()
barral_group = pygame.sprite.GroupSingle()
enemy_group = pygame.sprite.Group()
player_bullet_group = pygame.sprite.Group()
enemy_bullet_group = pygame.sprite.Group()
tile_group = pygame.sprite.Group()
effect_group = pygame.sprite.Group()

# fonts
font_1 = pygame.font.Font(os.path.join("font", "comic_sans.ttf"), 42)
font_2 = pygame.font.Font(os.path.join("font", "comic_sans.ttf"), 86)

# text
space_to_start_font = font_1.render("Press Space To Start", True, WHITE)
space_to_start_font_rect = space_to_start_font.get_rect(center=(WIN_WIDTH / 2, WIN_WIDTH / 2))

successful_font = font_2.render("Successful", True, GREEN)
successful_font_rect = successful_font.get_rect(center=(WIN_WIDTH / 2, WIN_HEIGHT / 2))

failed_font = font_2.render("Failed", True, RED)
failed_font_rect = failed_font.get_rect(center=(WIN_WIDTH / 2, WIN_HEIGHT / 2))

    
class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.speed = 125
    
        self.width = 48
        self.height = self.width
    
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(BLUE)

        self.rect = self.image.get_rect(topleft=(pos_x, pos_y))
    
        self.vector2 = pygame.math.Vector2(0, 0)

        self.rect_pos = pygame.math.Vector2(self.rect.x, self.rect.y)

        self.player_shoot_delay = 0.2
        self.player_shoot_timer = self.player_shoot_delay

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
        self.rect.x = round(self.rect_pos.x)

    def vertical_movement(self, delta_time):
        self.key = pygame.key.get_pressed()

        if self.key[pygame.K_w]:
            self.vector2.y = -1
        elif self.key[pygame.K_s]:
            self.vector2.y = 1
        else:
            self.vector2.y = 0

        self.rect_pos.y += self.vector2.y * self.speed * delta_time
        self.rect.y = round(self.rect_pos.y)

    def shoot(self, delta_time):
        pressed = pygame.mouse.get_pressed()

        if pressed[0]:
            if self.player_shoot_timer < 0:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                target = player_group.sprite.rect.center
                
                bullet = Bullet(BLUE, CYAN, enemy_group, target, (mouse_x, mouse_y))
                player_bullet_group.add(bullet)

                self.player_shoot_timer = self.player_shoot_delay
        
        self.player_shoot_timer -= delta_time

    def update(self, delta_time):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        self.horizontal_movement(delta_time)
        self.horizontal_collisions()

        self.vertical_movement(delta_time)
        self.vertical_collisions()

        self.shoot(delta_time)

        pygame.draw.line(WIN, BLUE, (self.rect.x + (self.width / 2), self.rect.y + (self.height / 2)), (mouse_x, mouse_y), 10)
        pygame.draw.circle(WIN, BLUE, (mouse_x, mouse_y), 8)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, colour, shoot_delay, pos_x, pos_y):
        super().__init__()
        self.speed = random.randint(50, 150)
 
        self.width = 48
        self.height = self.width
 
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(colour)
 
        self.rect = self.image.get_rect(topleft=(pos_x, pos_y))
 
        self.vector2 = pygame.math.Vector2(0, 0)
        self.rect_pos = pygame.math.Vector2(self.rect.x, self.rect.y)

        self.shoot_delay = shoot_delay
        self.shoot_timer = random.randint(1, 10) / 10
       
        start_direction = [-1, 1]

        self.vector2.x = random.choice(start_direction)
        self.vector2.y = random.choice(start_direction)
 
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
        self.rect.x = round(self.rect_pos.x)
 
    def vertical_movement(self, delta_time):
        self.rect_pos.y += self.vector2.y * self.speed * delta_time
        self.rect.y = round(self.rect_pos.y)

    def shoot(self, delta_time):
        self.shoot_timer -= delta_time

        if self.shoot_timer < 0:
            for sprites in player_group.sprites():
                player_center_x, player_center_y = sprites.rect.center
            
            bullet = Bullet(RED, ORANGE, player_group, self.rect.center, (player_center_x + random.randint(-100, 100), player_center_y + random.randint(-100, 100)))
            enemy_bullet_group.add(bullet)
            
            self.shoot_timer = self.shoot_delay

    def update(self, delta_time):
        self.horizontal_movement(delta_time)
        self.horizontal_collisions()

        self.vertical_movement(delta_time)
        self.vertical_collisions()

        self.shoot(delta_time)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, colour_1, colour_2, kill_group, start_pos, target_pos):
        super().__init__()
        self.group = kill_group

        self.colour_1 = colour_1
        self.colour_2 = colour_2

        self.bullet_speed = 225
 
        self.max_bounces = 1
 
        self.width = 20
        self.height = self.width

        self.image = pygame.Surface((self.width, self.height))
 
        self.rect = self.image.get_rect(center=start_pos)
 
        self.x_center, self.y_center = self.rect.center

        target_x, target_y = target_pos
 
        self.rise = target_x - self.x_center
        self.run = target_y - self.y_center
 
        self.angle = math.atan2(self.run, self.rise)
 
        self.delta_y = math.sin(self.angle) * self.bullet_speed
        self.delta_x = math.cos(self.angle) * self.bullet_speed
 
        self.rect_pos = pygame.math.Vector2(self.rect.x, self.rect.y)
 
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
                effect = Effect(ORANGE, YELLOW, 112, 128, self.rect.x + (self.width / 2), self.rect.y + (self.height / 2))
                effect_group.add(effect)

                sprite.kill()
                Bullet.kill(self)
 
    def movement(self, delta_time):
        self.rect_pos.x += self.delta_x * delta_time
        self.rect_pos.y += self.delta_y * delta_time
 
        self.rect.x = round(self.rect_pos.x)
        self.rect.y = round(self.rect_pos.y)

    def explode_bullet(self):
        if self.bounce_index > self.max_bounces:
            effect = Effect(ORANGE, YELLOW, 32, 64, self.rect.x + (self.width / 2), self.rect.y + (self.height / 2))
            effect_group.add(effect)
            
            self.colour_1 = YELLOW
            self.colour_2 = YELLOW

            Bullet.kill(self)
    
    def fake_bullet(self):
        effect = Effect(self.colour_1, self.colour_2, 16, 64, self.rect.x + (self.width / 2), self.rect.y + (self.height / 2))
        effect_group.add(effect)

    def update(self, delta_time):
        self.collisions()
        self.explode_bullet()
        self.fake_bullet()
        self.movement(delta_time)


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.width = 48
        self.height = self.width
 
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(BLACK)
 
        self.rect = self.image.get_rect(topleft=(pos_x, pos_y))


class Effect(pygame.sprite.Sprite):
    def __init__(self, colour_1, colour_2, radius, speed, pos_x, pos_y):
        super().__init__()
        self.radius = radius

        self.colour_1 = colour_1
        self.colour_2 = colour_2

        self.speed = speed

        self.width = 0
        self.height = self.width

        self.image = pygame.Surface((self.width, self.height))

        self.rect = self.image.get_rect(center=(pos_x, pos_y))

    def draw(self):
        self.circle = pygame.draw.circle(WIN, self.colour_1, (self.rect.x, self.rect.y), self.radius)
        self.circle = pygame.draw.circle(WIN, self.colour_2, (self.rect.x, self.rect.y), self.radius / 2)

    def scale(self, delta_time):
        if self.radius > 4:
            self.radius -= delta_time * self.speed
        else:
            effect_group.remove(self)
    
    def update(self, delta_time):
        self.scale(delta_time)
        self.draw()


class Game():
    def __init__(self):
        self.current_level = 0

        self.game_active = False
        self.game_just_started = True

    def level_setup(self, level_data):
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
                    enemy = Enemy(RED, 0.5, x, y)
                    enemy_group.add(enemy)

    def level_clear(self):
        player_group.empty()
        enemy_group.empty()
        player_bullet_group.empty()
        enemy_bullet_group.empty()
        tile_group.empty()

    def load_level(self):
        if len(enemy_group) == 0:

            self.current_level += 1

            if self.current_level == 1:
                self.level_clear()
                self.level_setup(level_1)
            
            if self.current_level == 2:
                self.level_clear()
                self.level_setup(level_2)

            if self.current_level == 3:
                self.level_clear()
                self.level_setup(level_3)

        if self.current_level == 4:
            self.game_active = False

    def bullet_bullet_collisions(self):
        for player_bullet_sprite in player_bullet_group.sprites():
            for enemy_bullet_sprite in enemy_bullet_group.sprites():
                if player_bullet_sprite.rect.colliderect(enemy_bullet_sprite.rect):
                    effect = Effect(ORANGE, YELLOW, 32, 64, player_bullet_sprite.rect.x + (player_bullet_sprite.width / 2), player_bullet_sprite.rect.y + (player_bullet_sprite.height / 2))
                    effect_group.add(effect)

                    effect = Effect(ORANGE, YELLOW, 32, 64, enemy_bullet_sprite.rect.x + (enemy_bullet_sprite.width / 2), enemy_bullet_sprite.rect.y + (enemy_bullet_sprite.height / 2))
                    effect_group.add(effect)

                    player_bullet_sprite.kill()
                    enemy_bullet_sprite.kill()
        
        self.game_just_started = False

    def player_bullet_collisions(self):
        try:
            for sprite in enemy_group.sprites():
                if sprite.rect.colliderect(player_group.sprite.rect):
                    self.game_active = False
        except:
            self.game_active = False

    def draw(self):
        WIN.fill(GRAY)

        player_group.draw(WIN)
        enemy_group.draw(WIN)
        tile_group.draw(WIN)
        effect_group.draw(WIN)

    def menu(self):
        WIN.fill(GRAY)

        self.level_clear()

        WIN.blit(space_to_start_font, (space_to_start_font_rect))

        if self.current_level == 4:
            WIN.blit(successful_font, successful_font_rect)
        elif not self.current_level == 4 and not self.game_just_started:
            WIN.blit(failed_font, failed_font_rect)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        pygame.draw.circle(WIN, BLUE, (mouse_x, mouse_y), 8)

    def update(self, delta_time):
        if self.game_active:
            self.draw()
            self.load_level()
            self.bullet_bullet_collisions()
            self.player_bullet_collisions()

            player_group.update(delta_time)
            enemy_group.update(delta_time)
            player_bullet_group.update(delta_time)
            enemy_bullet_group.update(delta_time)
            effect_group.update(delta_time)
        else:
            self.menu()

        pygame.display.update()


def main():
    previous_time = time.time()

    game = Game()

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
                    if not game.game_active:
                        game.current_level = 0
                        game.game_active = True

        game.update(delta_time)

if __name__ == "__main__":
    main()
