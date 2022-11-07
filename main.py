# import
import pygame
import sys
import time
import math
import os
import random
from levels import *
 
pygame.init()

# display settings
WIN_WIDTH = 1200
WIN_HEIGHT = 816
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
 
pygame.display.set_caption("Tanks")

pygame.display.set_icon(pygame.image.load(
    os.path.join("graphics", "tank.png")).convert_alpha())

pygame.mouse.set_visible(False)

# colours (255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
PURPLE = (255, 0, 255)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)

# colour (random)
ORANGE = (255, 128, 0)
DARK_GREEN = (0, 128, 0)
BROWN = (140,70,20)

# shades
WHITE_1 = (255, 255, 255)
WHITE_2 = (247, 247, 247)
WHITE_3 = (239, 239, 239)

GRAY_1 = (112, 112, 112)
GRAY_2 = (120, 120, 120)
GRAY_3 = (128, 128, 128)

DARK_GRAY = (64, 64, 64)

BLACK = (0, 0, 0)

# sprite groups
player_group = pygame.sprite.GroupSingle()
barral_group = pygame.sprite.GroupSingle()
enemy_group = pygame.sprite.Group()
player_bullet_group = pygame.sprite.Group()
enemy_bullet_group = pygame.sprite.Group()
collision_tile_group = pygame.sprite.Group()
backgound_tile_group = pygame.sprite.Group()
explosion_effect_group = pygame.sprite.Group()
trail_effect_group = pygame.sprite.Group()

# fonts
font_1 = pygame.font.Font(os.path.join("font", "comic_sans.ttf"), 42)
font_2 = pygame.font.Font(os.path.join("font", "comic_sans.ttf"), 86)

    
class Player(pygame.sprite.Sprite):
    def __init__(self, colour, size, speed, shoot_delay, bullet_colour_1, bullet_colour_2, bullet_speed, bullet_max_bounces, bullet_size, pos_x, pos_y):
        super().__init__()
        self.colour = colour

        self.width = size
        self.height = size
        
        self.speed = speed

        self.shoot_delay = shoot_delay

        self.bullet_colour_1 = bullet_colour_1
        self.bullet_colour_2 = bullet_colour_2

        self.bullet_speed = bullet_speed

        self.bullet_max_bounces = bullet_max_bounces

        self.bullet_size = bullet_size

        self.image = pygame.Surface((self.width, self.height))

        self.rect = self.image.get_rect(topleft=(pos_x, pos_y))
    
        self.vector2 = pygame.math.Vector2(0, 0)

        self.rect_pos = pygame.math.Vector2(self.rect.x, self.rect.y)

        self.shoot_timer = self.shoot_delay

    def horizontal_collisions(self):
        for sprite in collision_tile_group.sprites():
            if sprite.rect.colliderect(self):
                if self.vector2.x > 0:
                    self.rect.right = sprite.rect.left
                    self.rect_pos.x = sprite.rect.left - self.width
    
                elif self.vector2.x < 0:
                    self.rect.left = sprite.rect.right
                    self.rect_pos.x = sprite.rect.right
    
    def vertical_collisions(self):
        for sprite in collision_tile_group.sprites():
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
        if pygame.mouse.get_pressed()[0]:
            if self.shoot_timer < 0:
                target = player_group.sprite.rect.center
                
                bullet = Bullet(self.bullet_colour_1, self.bullet_colour_2, self.bullet_speed, self.bullet_max_bounces, self.bullet_size, enemy_group, target, pygame.mouse.get_pos())
                player_bullet_group.add(bullet)

                self.shoot_timer = self.shoot_delay
        
        self.shoot_timer -= delta_time

    def update(self, delta_time):
        pygame.draw.rect(WIN, self.colour, (self.rect.x, self.rect.y, self.width, self.height), 0, 8)

        self.horizontal_movement(delta_time)
        self.horizontal_collisions()

        self.vertical_movement(delta_time)
        self.vertical_collisions()

        self.shoot(delta_time)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, colour, size, speed, shoot_delay, bullet_colour_1, bullet_colour_2, bullet_speed, bullet_max_bounces, bullet_size, pos_x, pos_y):
        super().__init__()
        self.colour = colour

        self.width = size
        self.height = size
        
        self.speed = speed

        self.shoot_delay = shoot_delay

        self.bullet_colour_1 = bullet_colour_1
        self.bullet_colour_2 = bullet_colour_2

        self.bullet_speed = bullet_speed

        self.bullet_max_bounces = bullet_max_bounces

        self.bullet_size = bullet_size
 
        self.image = pygame.Surface((self.width, self.height))
 
        self.rect = self.image.get_rect(topleft=(pos_x, pos_y))
 
        self.vector2 = pygame.math.Vector2(0, 0)
        self.rect_pos = pygame.math.Vector2(self.rect.x, self.rect.y)

        self.shoot_timer = self.shoot_delay
       
        self.direction_list = [-1, 1]

        self.direction_change_timer = random.randint(2, 5)

        self.vector2.x = random.choice(self.direction_list)
        self.vector2.y = random.choice(self.direction_list)
 
    def horizontal_collisions(self):
        for sprite in collision_tile_group.sprites():
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
        for sprite in collision_tile_group.sprites():
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
            
            bullet = Bullet(self.bullet_colour_1, self.bullet_colour_2, self.bullet_speed, self.bullet_max_bounces, self.bullet_size , player_group, self.rect.center, (player_center_x + random.randint(-100, 100), player_center_y + random.randint(-100, 100)))
            enemy_bullet_group.add(bullet)
            
            self.shoot_timer = self.shoot_delay

    def direction_change(self, delta_time):
        self.direction_change_timer -= delta_time

        if self.direction_change_timer < 0:
            self.vector2.x = random.choice(self.direction_list)
            self.vector2.y = random.choice(self.direction_list)

            self.direction = random.choice(self.direction_list)
            self.direction_change_timer = random.randint(2, 5)

    def update(self, delta_time):
        pygame.draw.rect(WIN, self.colour, (self.rect.x, self.rect.y, self.width, self.height), 0, 8)

        self.horizontal_movement(delta_time)
        self.horizontal_collisions()

        self.vertical_movement(delta_time)
        self.vertical_collisions()

        self.direction_change(delta_time)
        self.shoot(delta_time)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, bullet_colour_1, bullet_colour_2, bullet_speed, bullet_max_bounces, bullet_size, kill_group, start_pos, target_pos):
        super().__init__()
        self.bullet_colour_1 = bullet_colour_1
        self.bullet_colour_2 = bullet_colour_2

        self.bullet_speed = bullet_speed

        self.max_bounces = bullet_max_bounces

        self.width = bullet_size
        self.height = bullet_size

        self.kill_group = kill_group

        self.image = pygame.Surface((self.width, self.height))
 
        self.rect = self.image.get_rect(center=start_pos)
 
        center_x, center_y = self.rect.center

        target_x, target_y = target_pos
 
        rise = target_x - center_x
        run = target_y - center_y

        self.angle = math.atan2(run, rise)
 
        self.delta_y = math.sin(self.angle) * self.bullet_speed
        self.delta_x = math.cos(self.angle) * self.bullet_speed

        self.rect_pos = pygame.math.Vector2(self.rect.x, self.rect.y)
 
        self.bounce_index = 0

    def collisions(self):
        for sprite in collision_tile_group.sprites():
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

        for sprite in self.kill_group.sprites():
            if self.rect.colliderect(sprite):
                trail_effect = Trail_Effect(ORANGE, YELLOW, 88, 148, self.rect.x + self.width / 2, self.rect.y + self.height / 2)
                trail_effect_group.add(trail_effect)

                sprite.kill()
                Bullet.kill(self)
 
    def movement(self, delta_time):
        self.rect_pos.x += self.delta_x * delta_time
        self.rect_pos.y += self.delta_y * delta_time
 
        self.rect.x = round(self.rect_pos.x)
        self.rect.y = round(self.rect_pos.y)

    def explode_bullet(self):
        if self.bounce_index > self.max_bounces:
            trail_effect = Trail_Effect(ORANGE, YELLOW, 32, 64, self.rect.x + self.width / 2, self.rect.y + self.height / 2)
            trail_effect_group.add(trail_effect)
            
            self.colour_1 = YELLOW
            self.colour_2 = YELLOW

            Bullet.kill(self)
    
    def fake_bullet(self):
        trail_effect = Trail_Effect(self.bullet_colour_1, self.bullet_colour_2, self.width, 64, self.rect_pos.x + self.width / 2, self.rect_pos.y + self.height / 2)
        trail_effect_group.add(trail_effect)

    def update(self, delta_time):
        self.collisions()
        self.explode_bullet()
        self.fake_bullet()
        self.movement(delta_time)


class Tile(pygame.sprite.Sprite):
    def __init__(self,colour_list, pos_x, pos_y):
        super().__init__()
        self.width = 48
        self.height = self.width
 
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(random.choice(colour_list))
 
        self.rect = self.image.get_rect(topleft=(pos_x, pos_y))


class Trail_Effect(pygame.sprite.Sprite):
    def __init__(self, colour_1, colour_2, radius, srink_speed, pos_x, pos_y):
        super().__init__()
        self.radius = radius

        self.srink_speed = srink_speed

        self.colour_1 = colour_1
        self.colour_2 = colour_2

        self.width = 0
        self.height = self.width

        self.image = pygame.Surface((self.width, self.height))

        self.rect = self.image.get_rect(center=(pos_x, pos_y))

    def draw_effect(self):
        self.circle = pygame.draw.circle(WIN, self.colour_1, (self.rect.x, self.rect.y), self.radius)
        self.circle = pygame.draw.circle(WIN, self.colour_2, (self.rect.x, self.rect.y), self.radius / 2)

    def scale_down(self, delta_time):
        if self.radius > 4:
            self.radius -= delta_time * self.srink_speed
        else:
            trail_effect_group.remove(self)
    
    def update(self, delta_time):
        self.scale_down(delta_time)
        self.draw_effect()


class Game():
    def __init__(self):
        self.current_level = 0

        self.current_time = 0
        self.fastest_time = math.inf

        self.game_active = False
        self.game_just_started = True
        self.player_just_died = True

        self.level_swich_timer = 1

        self.gray_colour_list = [GRAY_1, GRAY_2, GRAY_3]
        self.white_colour_list = [WHITE_1, WHITE_2, WHITE_3]

        self.space_to_start_text = font_1.render("Press Space To Start", True, BLACK)
        self.space_to_start_text_rect = self.space_to_start_text.get_rect(center=(WIN_WIDTH / 2, WIN_WIDTH / 2))
   
        self.successful_text = font_2.render("Successful", True, GREEN)
        self.successful_text_rect = self.successful_text.get_rect(center=(WIN_WIDTH / 2, WIN_HEIGHT / 2))

        self.failed_text = font_2.render("Failed", True, RED)
        self.failed_text_rect = self.failed_text.get_rect(center=(WIN_WIDTH / 2, WIN_HEIGHT / 2))

        self.current_time_text = font_1.render(f"| Time: {round(self.current_time, 1)}", True, BLACK)
        self.current_time_text_rect = self.current_time_text.get_rect(topleft=(0 + 48, 0))

        self.fastest_time_text = font_1.render(f"Fastest Time: {round(self.fastest_time, 1)} |", True, BLACK)
        self.fastest_time_text_rect = self.fastest_time_text.get_rect(topright=(WIN_WIDTH - 48, 0))

    def level_setup(self, level_data):
        for row_index, row in enumerate(level_data):
            for col_index, cell in enumerate(row):
                x = col_index * 48
                y = row_index * 48

                if cell == " ":
                    tile = Tile(self.white_colour_list, x, y)
                    backgound_tile_group.add(tile)

                if cell == "T":
                    tile = Tile(self.gray_colour_list, x, y)
                    collision_tile_group.add(tile)

                if cell == "P":
                    player = Player(BLUE, 48, 120, 0.28, BLUE, CYAN, 260, 1, 16, x, y)
                    player_group.add(player)

                if cell == "A":
                    enemy = Enemy(RED, 48, 60, 1, RED, YELLOW, 260, 1, 16, x, y)
                    enemy_group.add(enemy)

    def level_clear(self):
        player_group.empty()
        enemy_group.empty()
        player_bullet_group.empty()
        enemy_bullet_group.empty()
        collision_tile_group.empty()
        backgound_tile_group.empty()
        trail_effect_group.empty()
        explosion_effect_group.empty()

    def load_level(self):
        if len(enemy_group) == 0:
            if self.current_level == 3:
                self.game_active = False
                self.player_just_died = False
            else:
                self.level_clear()
                self.current_level += 1

            if self.current_level == 1:
                self.level_setup(level_1)
            
            if self.current_level == 2:
                self.level_setup(level_2)

            if self.current_level == 3:
                self.level_setup(level_3)

    def timer(self, delta_time):
        self.current_time += delta_time

        self.current_time_text = font_1.render(f"| Time: {round(self.current_time, 1)}", True, BLACK)
        self.current_time_text_rect = self.current_time_text.get_rect(topleft=(48, 0))

    def bullet_bullet_collisions(self):
        for player_bullet_sprite in player_bullet_group.sprites():
            for enemy_bullet_sprite in enemy_bullet_group.sprites():
                if player_bullet_sprite.rect.colliderect(enemy_bullet_sprite.rect):
                    trail_effect = Trail_Effect(ORANGE, YELLOW, 32, 64, player_bullet_sprite.rect.x + (player_bullet_sprite.width / 2), player_bullet_sprite.rect.y + (player_bullet_sprite.height / 2))
                    trail_effect_group.add(trail_effect)

                    trail_effect = Trail_Effect(ORANGE, YELLOW, 32, 64, enemy_bullet_sprite.rect.x + (enemy_bullet_sprite.width / 2), enemy_bullet_sprite.rect.y + (enemy_bullet_sprite.height / 2))
                    trail_effect_group.add(trail_effect)

                    player_bullet_sprite.kill()
                    enemy_bullet_sprite.kill()

    def player_bullet_collisions(self):
        if len(player_group) == 0:
            self.player_just_died = True
            self.game_active = False
    
    def menu_text(self):
        WIN.blit(self.space_to_start_text, self.space_to_start_text_rect)

        if self.current_level == 3 and not self.player_just_died:
            WIN.blit(self.successful_text, self.successful_text_rect)

            if self.current_time < self.fastest_time:
                self.fastest_time = self.current_time

                self.fastest_time_text = font_1.render(f"Fastest Time: {round(self.fastest_time, 1)} |", True, BLACK)
                self.fastest_time_text_rect = self.fastest_time_text.get_rect(topright=(WIN_WIDTH - 48, 0))

        elif not self.game_just_started:
            WIN.blit(self.failed_text, self.failed_text_rect)

    def game_update(self, delta_time):
        WIN.fill(WHITE_1)

        collision_tile_group.draw(WIN)
        backgound_tile_group.draw(WIN)

        player_group.update(delta_time)
        enemy_group.update(delta_time)
        player_bullet_group.update(delta_time) 
        enemy_bullet_group.update(delta_time)
        trail_effect_group.update(delta_time)
        explosion_effect_group.update(delta_time)

        self.timer(delta_time)

        self.load_level()

        self.bullet_bullet_collisions()
        self.player_bullet_collisions()

        self.game_just_started = False

    def menu_update(self):
        WIN.fill(WHITE_1)
    
        self.menu_text()

    def update(self, delta_time):
        if self.game_active:
            self.game_update(delta_time)
        else:
            self.menu_update()

        WIN.blit(self.current_time_text, self.current_time_text_rect)
        WIN.blit(self.fastest_time_text, self.fastest_time_text_rect)


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
                        game.level_clear()
                        
                        game.current_time = 0
                        game.current_level = 0
                        game.game_active = True

        game.update(delta_time)

        pygame.draw.circle(WIN, BLUE, pygame.mouse.get_pos(), 8)

        pygame.display.update()

if __name__ == "__main__":
    main()
