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

# colours
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
PURPLE = (255, 0, 255)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)

ORANGE = (255, 128, 0)
DARK_GREEN = (0, 128, 0)

BROWN_1 = (98, 52, 18)
BROWN_2 = (106, 60, 26)

WHITE_1 = (255, 255, 255)
WHITE_2 = (239, 239, 239)

GRAY_1 = (32, 32, 32)
GRAY_2 = (40, 40, 40)

BLACK = (0, 0, 0)

# sprite groups
player_group = pygame.sprite.GroupSingle()
barral_group = pygame.sprite.GroupSingle()
enemy_group = pygame.sprite.Group()
player_bullet_group = pygame.sprite.Group()
enemy_bullet_group = pygame.sprite.Group()
collision_tile_group = pygame.sprite.Group()
backgound_tile_group = pygame.sprite.Group()
partical_list = []

# fonts
FONT_1 = pygame.font.Font(os.path.join("font", "comic_sans.ttf"), 42)
FONT_2 = pygame.font.Font(os.path.join("font", "comic_sans.ttf"), 86)


class Player(pygame.sprite.Sprite):
    def __init__(self, colour, size, speed, shoot_delay, bullet_colour, bullet_speed, bullet_max_bounces, bullet_size, pos_x, pos_y):
        super().__init__()
        self.colour = colour

        self.width = size
        self.height = size

        self.speed = speed

        self.shoot_delay = shoot_delay

        self.bullet_colour = bullet_colour

        self.bullet_speed = bullet_speed

        self.bullet_max_bounces = bullet_max_bounces

        self.bullet_size = bullet_size

        self.image = pygame.Surface((self.width, self.height))

        self.rect = self.image.get_rect(topleft=(pos_x, pos_y))
        
        self.direction = pygame.math.Vector2(0, 0)

        self.rect_pos = pygame.math.Vector2(self.rect.x, self.rect.y)

        self.shoot_timer = self.shoot_delay

    def horizontal_collisions(self):
        for sprite in collision_tile_group.sprites():
            if sprite.rect.colliderect(self):
                if self.direction.x > 0:
                    self.rect.right = sprite.rect.left
                    self.rect_pos.x = sprite.rect.left - self.width

                elif self.direction.x < 0:
                    self.rect.left = sprite.rect.right
                    self.rect_pos.x = sprite.rect.right

    def vertical_collisions(self):
        for sprite in collision_tile_group.sprites():
            if sprite.rect.colliderect(self):
                if self.direction.y > 0:
                    self.rect.bottom = sprite.rect.top
                    self.rect_pos.y = sprite.rect.top - self.height

                elif self.direction.y < 0:
                    self.rect.top = sprite.rect.bottom
                    self.rect_pos.y = sprite.rect.bottom

    def horizontal_movement(self, delta_time):
        self.key = pygame.key.get_pressed()

        if self.key[pygame.K_a]:
            self.direction.x = -1
        elif self.key[pygame.K_d]:
            self.direction.x = 1
        else:
            self.direction.x = 0

        self.rect_pos.x += self.direction.x * self.speed * delta_time
        self.rect.x = round(self.rect_pos.x)

    def vertical_movement(self, delta_time):
        self.key = pygame.key.get_pressed()

        if self.key[pygame.K_w]:
            self.direction.y = -1
        elif self.key[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        self.rect_pos.y += self.direction.y * self.speed * delta_time
        self.rect.y = round(self.rect_pos.y)

    def shoot(self, delta_time):
        if pygame.mouse.get_pressed()[0]:
            if self.shoot_timer < 0:
                target = player_group.sprite.rect.center

                bullet = Bullet(self.bullet_colour, self.bullet_speed, self.bullet_max_bounces,
                                self.bullet_size, enemy_group, target, pygame.mouse.get_pos())
                player_bullet_group.add(bullet)

                self.shoot_timer = self.shoot_delay

        self.shoot_timer -= delta_time
    
    def draw(self):
        pygame.draw.rect(WIN, self.colour, (self.rect.x,self.rect.y, self.width, self.height), 0, 8)

        center_x, center_y = self.rect.center

        mouse_x, mouse_y = pygame.mouse.get_pos()

        self.rise = mouse_x - center_x
        self.run = mouse_y - center_y

        self.angle = math.atan2(self.run, self.rise)
        
        self.delta_y = math.sin(self.angle)    
        self.delta_x = math.cos(self.angle)

        pygame.draw.circle(WIN, BLUE, (mouse_x + self.delta_x - self.rise / 8, mouse_y + self.delta_y - self.run / 8), 8)
        pygame.draw.circle(WIN, BLUE, (mouse_x + self.delta_x - self.rise / 4, mouse_y + self.delta_y - self.run / 4), 8)
        pygame.draw.circle(WIN, BLUE, (mouse_x + self.delta_x - self.rise / 2.66, mouse_y + self.delta_y - self.run / 2.66), 8)
        pygame.draw.circle(WIN, BLUE, (mouse_x + self.delta_x - self.rise / 2, mouse_y + self.delta_y - self.run / 2), 8)
        pygame.draw.circle(WIN, BLUE, (mouse_x + self.delta_x - self.rise / 1.62, mouse_y + self.delta_y - self.run / 1.62), 8)
        pygame.draw.circle(WIN, BLUE, (mouse_x + self.delta_x - self.rise / 1.36, mouse_y + self.delta_y - self.run / 1.36), 8)
        pygame.draw.circle(WIN, BLUE, (mouse_x + self.delta_x - self.rise / 1.16, mouse_y + self.delta_y - self.run / 1.16), 8)

    def update(self, delta_time):
        self.horizontal_movement(delta_time)
        self.horizontal_collisions()

        self.vertical_movement(delta_time)
        self.vertical_collisions()

        self.shoot(delta_time)
        self.draw()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, colour, size, speed, shoot_delay, bullet_colour, bullet_speed, bullet_max_bounces, bullet_size, pos_x, pos_y):
        super().__init__()
        self.colour = colour

        self.width = size
        self.height = size

        self.speed = speed

        self.shoot_delay = shoot_delay

        self.bullet_colour = bullet_colour

        self.bullet_speed = bullet_speed

        self.bullet_max_bounces = bullet_max_bounces

        self.bullet_size = bullet_size

        self.image = pygame.Surface((self.width, self.height))

        self.rect = self.image.get_rect(topleft=(pos_x, pos_y))

        self.vector2 = pygame.math.Vector2(0, 0)
        self.rect_pos = pygame.math.Vector2(self.rect.x, self.rect.y)

        self.shoot_timer = self.shoot_delay

        self.direction_change_timer = random.randint(2, 5)
        
        self.direction_list = [-1, 1]

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

                bullet = Bullet(self.bullet_colour, self.bullet_speed, self.bullet_max_bounces, self.bullet_size, player_group,
                                self.rect.center, (player_center_x + random.randint(-100, 100), player_center_y + random.randint(-100, 100)))
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
        pygame.draw.rect(WIN, self.colour, (self.rect.x,
                         self.rect.y, self.width, self.height), 0, 8)

        self.horizontal_movement(delta_time)
        self.horizontal_collisions()

        self.vertical_movement(delta_time)
        self.vertical_collisions()

        self.direction_change(delta_time)
        self.shoot(delta_time)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, bullet_colour, bullet_speed, bullet_max_bounces, bullet_size, kill_group, start_pos, target_pos):
        super().__init__()
        self.bullet_colour = bullet_colour

        self.bullet_speed = bullet_speed

        self.max_bounces = bullet_max_bounces

        self.width = bullet_size
        self.height = bullet_size

        self.kill_group = kill_group

        self.image = pygame.Surface((self.width, self.height))

        self.rect = self.image.get_rect(center=start_pos)

        center_x, center_y = self.rect.center

        target_x, target_y = target_pos

        self.rise = target_x - center_x
        self.run = target_y - center_y

        self.angle = math.atan2(self.run, self.rise)
        
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

    def kill_sprite(self):
        for sprite in self.kill_group.sprites():
            if self.rect.colliderect(sprite):
                sprite.kill()
                Bullet.kill(self)

                for i in range(50):
                    partical_list.append(Partical(ORANGE, random.randint(self.width, self.width * 2), random.randint(40, 90), random.randint(-500, 500),
                                         random.randint(-500, 500), self.rect.x + self.width / 2 + random.randint(-4, 4), self.rect.y + self.height / 2 + random.randint(-4, 4)))

    def movement(self, delta_time):
        self.rect_pos.x += self.delta_x * delta_time
        self.rect_pos.y += self.delta_y * delta_time

        self.rect.x = round(self.rect_pos.x)
        self.rect.y = round(self.rect_pos.y)

    def explode_bullet(self):
        if self.bounce_index > self.max_bounces:
            Bullet.kill(self)

            for i in range(50):
                partical_list.append(Partical(ORANGE, random.randint(self.width, self.width * 2), random.randint(60, 120), random.randint(-250, 250),
                                     random.randint(-250, 250), self.rect.x + self.width / 2 + random.randint(-4, 4), self.rect.y + self.height / 2 + random.randint(-4, 4)))

    def fake_bullet(self):
        partical_list.append(Partical(self.bullet_colour, self.width / 1.8, random.randint(25, 65), random.randint(-30, 30), random.randint(-30, 30),
                             self.rect_pos.x + self.width / 2 + random.randint(-4, 4), self.rect_pos.y + self.height / 2 + random.randint(-4, 4)))

    def update(self, delta_time):
        self.collisions()
        self.kill_sprite()
        self.explode_bullet()
        self.fake_bullet()
        self.movement(delta_time)


class Tile(pygame.sprite.Sprite):
    def __init__(self, colour_list, pos_x, pos_y):
        super().__init__()
        self.width = 48
        self.height = self.width

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(random.choice(colour_list))

        self.rect = self.image.get_rect(topleft=(pos_x, pos_y))


class Partical():
    def __init__(self, colour, radius, srink_speed, x_vel, y_vel, x_pos, y_pos):
        self.colour = colour

        self.radius = radius

        self.srink_speed = srink_speed

        self.x_vel = x_vel
        self.y_vel = y_vel

        self.x_pos = x_pos
        self.y_pos = y_pos

    def draw(self):
        pygame.draw.circle(
            WIN, self.colour, (self.x_pos, self.y_pos), self.radius)

    def move(self, delta_time):
        self.x_pos += self.x_vel * delta_time
        self.y_pos += self.y_vel * delta_time

    def scale(self, delta_time):
        self.radius -= delta_time * self.srink_speed

    def remove(self):
        if self.radius < 0:
            partical_list.remove(self)

    def update(self, delta_time):
        self.draw()
        self.move(delta_time)
        self.scale(delta_time)
        self.remove()


class Game():
    def __init__(self):
        self.current_level = 0

        self.current_time = 0
        self.fastest_time = math.inf

        self.game_active = False

        self.game_just_started = True
        self.game_finished = False

        self.white_colour_list = [WHITE_1, WHITE_2]
        self.gray_colour_list = [GRAY_1, GRAY_2]

        self.space_to_start_text = FONT_1.render(
            "Press Space To Start", True, BLACK)
        self.space_to_start_text_rect = self.space_to_start_text.get_rect(
            center=(WIN_WIDTH / 2, WIN_WIDTH / 2))

        self.space_to_start_text_rect_pos = pygame.math.Vector2(
            self.space_to_start_text_rect.x, self.space_to_start_text_rect.y)
        self.space_to_start_text_delta_y = 1

        self.successful_text = FONT_2.render("Successful", True, GREEN)
        self.successful_text_rect = self.successful_text.get_rect(
            center=(WIN_WIDTH / 2, WIN_HEIGHT / 2))

        self.failed_text = FONT_2.render("Failed", True, RED)
        self.failed_text_rect = self.failed_text.get_rect(
            center=(WIN_WIDTH / 2, WIN_HEIGHT / 2))

        self.current_level_text = FONT_1.render(
            f"| Level: {self.current_level}", True, BLACK)
        self.current_level_text_rect = self.current_level_text.get_rect(
            topleft=(0 + 48, 0))

        self.current_time_text = FONT_1.render(
            f" | Time: {round(self.current_time, 1)}", True, BLACK)
        self.current_time_text_rect = self.current_time_text.get_rect(
            topleft=(self.current_level_text_rect.topright))

        self.fastest_time_text = FONT_1.render(
            f"Fastest Time: {round(self.fastest_time, 1)} |", True, BLACK)
        self.fastest_time_text_rect = self.fastest_time_text.get_rect(
            topright=(WIN_WIDTH - 48, 0))

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
                    player = Player(BLUE, 48, 120, 0.2, BLUE, 260, 1, 17, x, y)
                    player_group.add(player)

                if cell == "A":
                    enemy = Enemy(RED, 48, 60, 1, RED, 260, 1, 17, x, y)
                    enemy_group.add(enemy)

    def level_clear(self):
        player_group.empty()
        enemy_group.empty()
        player_bullet_group.empty()
        enemy_bullet_group.empty()
        collision_tile_group.empty()
        backgound_tile_group.empty()

    def load_level(self):
        if len(enemy_group) == 0:
            if self.current_level == 3:
                self.game_finished = True
                self.game_active = False
            else:
                self.level_clear()
                self.current_level += 1

                self.game_just_started = False

                if self.current_level == 1:
                    self.level_setup(level_1)

                if self.current_level == 2:
                    self.level_setup(level_2)

                if self.current_level == 3:
                    self.level_setup(level_3)

    def timer(self, delta_time):
        self.current_time += delta_time

        self.current_time_text = FONT_1.render(
            f" | Time: {round(self.current_time, 1)}", True, BLACK)
        self.current_time_text_rect = self.current_time_text.get_rect(
            topleft=(self.current_level_text_rect.topright))

        self.current_level_text = FONT_1.render(
            f"| Level: {self.current_level}", True, BLACK)
        self.current_level_text_rect = self.current_level_text.get_rect(
            topleft=(0 + 48, 0))

    def bullet_bullet_collisions(self):
        for player_bullet_sprite in player_bullet_group.sprites():
            for enemy_bullet_sprite in enemy_bullet_group.sprites():
                if player_bullet_sprite.rect.colliderect(enemy_bullet_sprite.rect):
                    player_bullet_sprite.kill()
                    enemy_bullet_sprite.kill()

                    for i in range(50):
                        partical_list.append(Partical(ORANGE, random.randint(round(player_bullet_sprite.width / 2), round(player_bullet_sprite.width * 2)), random.randint(90, 180), random.randint(-180, 180), random.randint(
                            -180, 180), player_bullet_sprite.rect.x + player_bullet_sprite.width / 2 + random.randint(-4, 4), player_bullet_sprite.rect.y + player_bullet_sprite.height / 2 + random.randint(-4, 4)))

                    for i in range(50):
                        partical_list.append(Partical(ORANGE, random.randint(round(enemy_bullet_sprite.width / 2), round(enemy_bullet_sprite.width * 2)), random.randint(90, 180), random.randint(-180, 180),
                                             random.randint(-180, 180), enemy_bullet_sprite.rect.x + enemy_bullet_sprite.width / 2 + random.randint(-4, 4), enemy_bullet_sprite.rect.y + enemy_bullet_sprite.height / 2 + random.randint(-4, 4)))

    def player_bullet_collisions(self,):
        if len(player_group) == 0:
            self.game_active = False

    def update(self, delta_time):
        if self.game_active:
            WIN.fill(WHITE_1)

            collision_tile_group.draw(WIN)
            backgound_tile_group.draw(WIN)

            player_group.update(delta_time)
            enemy_group.update(delta_time)
            player_bullet_group.update(delta_time)
            enemy_bullet_group.update(delta_time)

            for partical in partical_list:
                partical.update(delta_time)

            self.timer(delta_time)
            self.load_level()

            self.bullet_bullet_collisions()
            self.player_bullet_collisions()
        else:
            WIN.fill(WHITE_1)

            if self.space_to_start_text_rect_pos.y < 0 + 48 * 12:
                self.space_to_start_text_delta_y *= -1
            elif self.space_to_start_text_rect_pos.y > WIN_HEIGHT - 48 * 4:
                self.space_to_start_text_delta_y *= -1

            self.space_to_start_text_rect_pos.y += self.space_to_start_text_delta_y * 40 * delta_time
            self.space_to_start_text_rect.y = round(
                self.space_to_start_text_rect_pos.y)

            WIN.blit(self.space_to_start_text, self.space_to_start_text_rect)

            if self.current_level == 3 and self.game_finished:
                WIN.blit(self.successful_text, self.successful_text_rect)

                if self.current_time < self.fastest_time:
                    self.fastest_time = self.current_time

                    self.fastest_time_text = FONT_1.render(
                        f"Fastest Time: {round(self.fastest_time, 1)} |", True, BLACK)
                    self.fastest_time_text_rect = self.fastest_time_text.get_rect(
                        topright=(WIN_WIDTH - 48, 0))

            elif not self.game_finished and not self.game_just_started:
                WIN.blit(self.failed_text, self.failed_text_rect)

        WIN.blit(self.current_time_text, self.current_time_text_rect)
        WIN.blit(self.fastest_time_text, self.fastest_time_text_rect)
        WIN.blit(self.current_level_text, self.current_level_text_rect)


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
                        partical_list.clear()

                        game.current_time = 0
                        game.current_level = 0

                        game.game_finished = False

                        game.game_active = True

        game.update(delta_time)

        pygame.draw.circle(WIN, BLUE, pygame.mouse.get_pos(), 8)

        
        pygame.display.update()


if __name__ == "__main__":
    main()
