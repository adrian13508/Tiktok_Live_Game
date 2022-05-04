import pygame
import random
from pygame.locals import (
        K_1,
        K_2,
        K_3,
        K_4,
        K_ESCAPE,
        KEYDOWN,
        K_SPACE,
    )


def main():

    screen_width = 720
    screen_height = 1280
    start_position = -50

    class Player1(pygame.sprite.Sprite):
        def __init__(self, group):
            super(Player1, self).__init__()
            self.surf = pygame.image.load('media/bolid_red_1.png').convert_alpha()
            self.rect = self.surf.get_rect(topleft=(start_position, 350))

        def update(self, pressed_keys):
            if pressed_keys[K_1]:
                self.rect.move_ip(1, 0)
            # if player_one_input == 'gracz 1':
            #    self.rect.move_ip(1, 0)

    class Player2(pygame.sprite.Sprite):
        def __init__(self):
            super(Player2, self).__init__()
            self.surf = pygame.image.load('media/bolid_yellow_1.png').convert_alpha()
            self.rect = self.surf.get_rect(topleft=(start_position, 450))

        def update(self, pressed_keys):
            if pressed_keys[K_2]:
                self.rect.move_ip(1, 0)

    class Player3(pygame.sprite.Sprite):
        def __init__(self):
            super(Player3, self).__init__()
            self.surf = pygame.image.load('media/bolid_blue_1.png').convert_alpha()
            self.rect = self.surf.get_rect(topleft=(start_position, 550))

        def update(self, pressed_keys):
            if pressed_keys[K_3]:
                self.rect.move_ip(1, 0)

    class Player4(pygame.sprite.Sprite):

        def __init__(self):
            super(Player4, self).__init__()
            self.surf = pygame.image.load('media/bolid_pink_1.png').convert_alpha()
            self.rect = self.surf.get_rect(topleft=(start_position, 650))

        def update(self, pressed_keys):
            if pressed_keys[K_4]:
                self.rect.move_ip(1, 0)

    class CameraGroup(pygame.sprite.Group):
        def __init__(self):
            super().__init__()
            self.display_surface = pygame.display.get_surface()
            self.offset = pygame.math.Vector2()

            # Camera box
            self.camera_borders = {'left': 100, 'right': 100, 'top': 100, 'bottom': 100}
            l = self.camera_borders['left']
            t = self.camera_borders['top']
            w = screen_width - (self.camera_borders['left'] + self.camera_borders['right'])
            h = screen_height - (self.camera_borders['top'] + self.camera_borders['bottom'])
            self.camera_rect = pygame.Rect(l, t, w, h)

        def box_camera(self, target):
            if target.rect.right > self.camera_rect.right:
                self.camera_rect.right = target.rect.right

            self.offset.x = self.camera_rect.left - self.camera_borders['left']
            self.offset.y = self.camera_rect.top - self.camera_borders['top']

        def custom_draw(self, player):

            self.box_camera(player)

            for sprite in self.sprites():
                offset_pos = sprite.rect.topleft + self.offset
                self.display_surface.blit(sprite.image, offset_pos)

            pygame.draw.rect(self.display_surface, 'red', self.camera_rect, 5)

    class FinishLine(pygame.sprite.Sprite):

        def __init__(self):
            super(FinishLine, self).__init__()
            self.surf = pygame.Surface((8, 400))
            self.surf.fill((255, 255, 255))
            self.rect = self.surf.get_rect(topleft=(1000, 340))

    # GAME Initialization !!---------------------------------------------------------------------
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))

    # Sky settings
    sky_surface = pygame.surface.Surface((720, 600))
    sky_rect = pygame.Surface.fill(sky_surface, (201, 248, 253))

    # Houses settings first plane
    house_moving = pygame.image.load('media/houses.png').convert_alpha()
    house_moving = pygame.transform.scale(house_moving, (720, 400))
    house_x_position = 0
    house_2_x_position = screen_width

    # Houses settings second plane
    house2_moving = pygame.image.load('media/houses_2.png').convert_alpha()
    house2_moving = pygame.transform.scale(house2_moving, (720, 400))

    # Street settings
    road_moving = pygame.image.load('media/road.png').convert_alpha()
    road_moving = pygame.transform.scale(road_moving, (720, 400))

    # Grass under road settings
    grass_surface = pygame.surface.Surface((720, 600))
    grass_rect = pygame.Surface.fill(grass_surface, (108, 170, 0))

    # Text settings
    ubuntu_bold = pygame.font.Font('/usr/share/fonts/truetype/ubuntu/Ubuntu-B.ttf', 30)
    play_again_surface = pygame.font.Font.render(ubuntu_bold, 'Comment to play again.', True, (0, 0, 0))

    # ------------------------------------------------------------------------------------------------------------------
    camera_group = CameraGroup()
    player1 = Player1(camera_group)
    player2 = Player2()
    player3 = Player3()
    player4 = Player4()
    clock = pygame.time.Clock()
    finish_line = FinishLine()
    game_active = True
    running = True

    while running:
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
                        game_active = True
                        player1.rect.x = start_position
                        player2.rect.x = start_position
                        player3.rect.x = start_position
                        player4.rect.x = start_position

        if game_active:
            pressed_keys = pygame.key.get_pressed()
            player1.update(pressed_keys)
            player2.update(pressed_keys)
            player3.update(pressed_keys)
            player4.update(pressed_keys)

            # Base background
            screen.blit(sky_surface, (0, 0))
            house_speed = 1
            # Moving houses second plane
            screen.blit(house2_moving, (house_x_position, 10))
            house_x_position -= house_speed
            if house_x_position == -screen_width:
                house_x_position = screen_width
            screen.blit(house2_moving, (house_2_x_position, 10))
            house_2_x_position -= house_speed
            if house_2_x_position == -screen_width:
                house_2_x_position = screen_width

            # Moving houses first plane
            screen.blit(house_moving, (house_x_position, 50))
            house_x_position -= house_speed
            if house_x_position == -screen_width:
                house_x_position = screen_width
            screen.blit(house_moving, (house_2_x_position, 50))
            house_2_x_position -= house_speed
            if house_2_x_position == -screen_width:
                house_2_x_position = screen_width

            # Moving street
            screen.blit(road_moving, (house_x_position, 340))
            house_x_position -= house_speed
            if house_x_position == -screen_width:
                house_x_position = screen_width
            screen.blit(road_moving, (house_2_x_position, 340))
            house_2_x_position -= house_speed
            if house_2_x_position == -screen_width:
                house_2_x_position = screen_width

            screen.blit(player1.surf, player1.rect)
            screen.blit(player2.surf, player2.rect)
            screen.blit(player3.surf, player3.rect)
            screen.blit(player4.surf, player4.rect)
            screen.blit(finish_line.surf, finish_line.rect)
            # player4.rect.x -= random.random()

            if finish_line.rect.colliderect(player1):
                game_active = False
            if finish_line.rect.colliderect(player2):
                game_active = False
            if finish_line.rect.colliderect(player3):
                game_active = False
            if finish_line.rect.colliderect(player4):
                game_active = False

            screen.blit(grass_surface, (0, 740))
            camera_group.update()
            camera_group.custom_draw(player1)

        else:
            screen.blit(sky_surface, (0, 0))
            screen.blit(grass_surface, (0, 540))
            screen.blit(play_again_surface, (screen_width/4, 50))

        pygame.display.update()
        clock.tick(60)


if __name__ == '__main__':
    main()

