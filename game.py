import subprocess

import pygame
from pygame.locals import (
        K_1,
        K_2,
        K_3,
        K_4,
        K_ESCAPE,
        KEYDOWN,
        K_SPACE,
    )
import sys


player1_nick = sys.argv[1]
player2_nick = sys.argv[2]
player3_nick = sys.argv[3]
player4_nick = sys.argv[4]


def main():

    screen_width = 720
    screen_height = 1280
    start_position = 30
    start_time = 0

    class Fonts:
        def __init__(self):
            super(Fonts, self).__init__()
            # Fonts settings
            self.ubuntu_bold = pygame.font.Font('fonts/Ubuntu-B.ttf', 30)
            self.bit_font = pygame.font.Font('fonts/8-BIT WONDER.TTF', 30)
            self.candy_beans = pygame.font.Font('fonts/Candy Beans.otf', 70)
            self.candy_beans2 = pygame.font.Font('fonts/Candy Beans.otf', 40)
            self.tasty_donuts = pygame.font.Font('fonts/TASTY DONUTS.otf', 30)

    class Player1(pygame.sprite.Sprite):
        def __init__(self, pos, group):
            super().__init__(group)
            self.image = pygame.image.load('media/bolid_red_1.png').convert_alpha()
            self.rect = self.image.get_rect(topleft=pos)
            self.direction = pygame.math.Vector2()
            self.name = player1_nick
            self.name_surf = Fonts().ubuntu_bold.render(self.name, False, (255, 255, 255))
            self.speed = 5

        def input(self):
            keys = pygame.key.get_pressed()
            if keys[K_1]:
                self.direction.x = 1
            else:
                self.direction.x = 0

        def update(self):
            self.input()
            self.rect.center += self.direction * self.speed

    class Player2(pygame.sprite.Sprite):
        def __init__(self, pos, group):
            super().__init__(group)
            image1 = pygame.image.load('media/bolid_yellow_1.png').convert_alpha()
            image2 = pygame.image.load('media/bolid_yellow_2.png').convert_alpha()
            self.player_image = [image1, image2]
            self.image_index = 0
            self.image = image1
            self.rect = self.image.get_rect(topleft=pos)
            self.direction = pygame.math.Vector2()
            self.speed = 5
            self.name = player2_nick
            self.name_surf = Fonts().ubuntu_bold.render(self.name, False, (255, 255, 255))

        def input(self):
            keys = pygame.key.get_pressed()
            if keys[K_2]:
                self.direction.x = 1
            else:
                self.direction.x = 0

        def update(self):
            self.input()
            self.rect.center += self.direction * self.speed
            self.image_index += 0.08
            if self.image_index >= len(self.player_image):
                self.image_index = 0

            self.image = self.player_image[int(self.image_index)]

    class Player3(pygame.sprite.Sprite):
        def __init__(self, pos, group):
            super().__init__(group)
            self.image = pygame.image.load('media/bolid_blue_1.png').convert_alpha()
            self.rect = self.image.get_rect(topleft=pos)
            self.direction = pygame.math.Vector2()
            self.speed = 5
            self.name = player3_nick
            self.name_surf = Fonts().ubuntu_bold.render(self.name, False, (255, 255, 255))

        def input(self):
            keys = pygame.key.get_pressed()
            if keys[K_3]:
                self.direction.x = 1
            else:
                self.direction.x = 0

        def update(self):
            self.input()
            self.rect.center += self.direction * self.speed

    class Player4(pygame.sprite.Sprite):
        def __init__(self, pos, group):
            super().__init__(group)
            self.image = pygame.image.load('media/bolid_pink_1.png').convert_alpha()
            self.rect = self.image.get_rect(topleft=pos)
            self.direction = pygame.math.Vector2()
            self.speed = 5
            self.name = player4_nick
            self.name_surf = Fonts().ubuntu_bold.render(self.name, False, (255, 255, 255))

        def input(self):
            keys = pygame.key.get_pressed()
            if keys[K_4]:
                self.direction.x = 1
            else:
                self.direction.x = 0

        def update(self):
            self.input()
            self.rect.center += self.direction * self.speed

    class Houses(pygame.sprite.Sprite):
        def __init__(self, group):
            super(Houses, self).__init__(group)
            self.image = pygame.image.load('media/houses.png').convert_alpha()
            self.rect = self.image.get_rect(topleft=(0, 0))

    class HousesBack(pygame.sprite.Sprite):
        def __init__(self, group):
            super().__init__(group)
            self.image = pygame.image.load('media/houses_2.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (720, 400))
            self.rect = self.image.get_rect(topleft=(0, 0))

    class Road(pygame.sprite.Sprite):
        def __init__(self, group):
            super().__init__(group)
            self.image = pygame.image.load('media/road.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (720, 290))
            self.rect = self.image.get_rect(topleft=(0, 0))

    class CameraGroup(pygame.sprite.Group):
        def __init__(self):
            super().__init__()
            self.current_time = 0
            self.time = 0
            self.display_surface = pygame.display.get_surface()
            self.offset = pygame.math.Vector2()
            self.half_w = self.display_surface.get_size()[0] // 2
            self.half_h = self.display_surface.get_size()[1] // 2

            # Camera box
            self.camera_borders = {'left': 100, 'right': 100, 'top': 100, 'bottom': 100}
            l = self.camera_borders['left']
            t = self.camera_borders['top']
            w = screen_width - (self.camera_borders['left'] + self.camera_borders['right'])
            h = screen_height - (self.camera_borders['top'] + self.camera_borders['bottom'])
            self.camera_rect = pygame.Rect(l, t, w, h)

            self.sky_surf = pygame.surface.Surface((720, 600))
            self.sky_rect = pygame.Surface.fill(self.sky_surf, (201, 248, 253))

            self.info_board_image = pygame.image.load('media/rule1.png').convert_alpha()
            self.info_board_image = pygame.transform.scale(self.info_board_image, (300, 300))

        def display_score(self):
            self.current_time = int((pygame.time.get_ticks() - start_time) / 1000)
            if self.current_time < 60:
                self.time = str(self.current_time) + ' s'
            if 60 <= self.current_time < 3600:
                seconds = self.current_time % 60
                minutes = int((self.current_time - seconds) / 60)
                self.time = str(minutes) + 'min ' + str(seconds) + ' s'

            score_surf = Fonts().ubuntu_bold.render(self.time, False, (64, 64, 64))
            score_rect = score_surf.get_rect(topleft=(350, 20))
            time_text = Fonts().ubuntu_bold.render('Time: ', False, (0, 0, 0))
            self.display_surface.blit(score_surf, score_rect)
            self.display_surface.blit(time_text, (270, 20))

        def box_camera(self, target):
            if target.rect.right > self.camera_rect.right:
                self.camera_rect.right = target.rect.right

            self.offset.x = self.camera_rect.left - self.camera_borders['left']
            self.offset.y = self.camera_rect.top - self.camera_borders['top']

        def custom_draw(self, player):
            # Camera mode
            self.box_camera(player)
            # Background color
            self.display_surface.blit(self.sky_surf, (0, 0))

            # House in second plane display and movement settings. Change multiplier value to change speed.
            relative_x_back = ((self.camera_rect.x - 100) * -0.6) % houses_back.image.get_rect().width
            self.display_surface.blit(houses_back.image, (relative_x_back - houses_back.image.get_rect().width, 100))
            if relative_x_back < screen_width:
                self.display_surface.blit(houses_back.image, (relative_x_back, 100))

            # House in first plane display and movement settings. Change multiplier value to change speed.
            relative_x_road = ((self.camera_rect.x - 100) * -1) % houses.image.get_rect().width
            self.display_surface.blit(houses.image, (relative_x_road - houses.image.get_rect().width, 200))
            if relative_x_road < screen_width:
                self.display_surface.blit(houses.image, (relative_x_road, 200))

            # Road display and movement settings. Change multiplier value to change speed.
            relative_x_road = ((self.camera_rect.x - 100) * -1) % road.image.get_rect().width
            self.display_surface.blit(road.image, (relative_x_road - road.image.get_rect().width, 500))
            if relative_x_road < screen_width:
                self.display_surface.blit(road.image, (relative_x_road, 500))

            # Game title
            game_title = Fonts().candy_beans2.render('Tiktok live game', False, (64, 64, 64))
            game_title_rect = game_title.get_rect(center=(screen_width / 2, 63))
            self.display_surface.blit(game_title, game_title_rect)
            game_name = Fonts().candy_beans2.render('BET YOUR FAVOURITE', False, (64, 64, 64))
            game_name_rect = game_name.get_rect(center=(screen_width/2, 130))
            self.display_surface.blit(game_name, game_name_rect)
            # Time counter
            self.display_score()
            # Game info - floating board
            self.display_surface.blit(self.info_board_image, (400, 800))

            # Players sprites blit.
            for sprite in [player1, player2, player3, player4]:
                offset_pos = sprite.rect.topleft - self.offset
                name_offset = sprite.rect.topleft - self.offset - (30, 0)
                self.display_surface.blit(sprite.image, offset_pos)
                self.display_surface.blit(sprite.name_surf, name_offset)

    class FinishLine(pygame.sprite.Sprite):

        def __init__(self):
            super(FinishLine, self).__init__()
            self.surf = pygame.Surface((8, 400))
            self.surf.fill((255, 255, 255))
            self.rect = self.surf.get_rect(topleft=(5000, 340))

    # GAME Initialization ---------------------------------------------------------------------------------------------
    pygame.init()
    pygame.event.set_grab(True)
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()

    # ----------------------------------  SETUP  ----------------------------------------------------------------------
    camera_group = CameraGroup()
    houses_back = HousesBack(camera_group)
    houses = Houses(camera_group)
    road = Road(camera_group)
    player1 = Player1((start_position, 485), camera_group)
    player2 = Player2((start_position, 555), camera_group)
    player3 = Player3((start_position, 625), camera_group)
    player4 = Player4((start_position, 705), camera_group)
    finish_line = FinishLine()
    game_active = True
    running = True

    while running:

        # Quiting events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if game_active is True:
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        game_active = False
            else:
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        pygame.quit()
                        subprocess.run('python ./gra.py', shell=True)


                        """game_active = True
                        camera_group.camera_rect.x = 100
                        player1.rect.x = start_position
                        player2.rect.x = start_position
                        player3.rect.x = start_position
                        player4.rect.x = start_position
                        start_time = pygame.time.get_ticks()"""

        if game_active:
            screen.fill((0, 176, 0))

            # Collision with finnish line
            if finish_line.rect.colliderect(player1):
                game_active = False
            if finish_line.rect.colliderect(player2):
                game_active = False
            if finish_line.rect.colliderect(player3):
                game_active = False
            if finish_line.rect.colliderect(player4):
                game_active = False

            # Assigning which player is currently 1st for camera movement.
            first_player = player1
            if player2.rect.x > first_player.rect.x:
                first_player = player2
            if player3.rect.x > first_player.rect.x:
                first_player = player3
            if player4.rect.x > first_player.rect.x:
                first_player = player4
            if player1.rect.x > first_player.rect.x:
                first_player = player1

            camera_group.update()
            camera_group.custom_draw(first_player)

        else:
            # Game finished
            screen.fill((0, 176, 0))

            # Time/score text settings
            finish_time_render = Fonts().ubuntu_bold.render(str(camera_group.time), False, (0, 0, 0))
            camera_group.display_surface.blit(finish_time_render, (350, 20))
            time_text = Fonts().ubuntu_bold.render('Total time: ', False, (0, 0, 0))
            camera_group.display_surface.blit(time_text, (195, 20))

            # Play again text settings
            play_again_surface = pygame.font.Font.render(
                Fonts().ubuntu_bold,
                'Type "RESTART" in chat to play again.',
                False,
                (0, 0, 0)
            )
            camera_group.display_surface.blit(play_again_surface, (100, 500))

            # Winner text settings
            winner = Fonts().ubuntu_bold.render(f'The Winner is!!   {str(first_player.name)} !!', False, (255, 255, 0))
            winner_rect = winner.get_rect(center=(screen_width/2, 200))
            camera_group.display_surface.blit(winner, winner_rect)

            text2 = Fonts().candy_beans.render('!! CONGRATULATIONS !!', False, (255, 255, 0))
            text2_rect = text2.get_rect(center=(screen_width / 2, 350))
            camera_group.display_surface.blit(text2, text2_rect)

            # Moving text on end screen
            text3 = Fonts().ubuntu_bold.render('If you enjoyed - please like, share', False, (0, 0, 204))
            text4 = Fonts().ubuntu_bold.render('or send gift to help run this project. ', False, (0, 0, 204))

            camera_group.display_surface.blit(text3, (110, 700))
            camera_group.display_surface.blit(text4, (110, 750))

        pygame.display.update()
        clock.tick(60)


if __name__ == '__main__':
    main()

