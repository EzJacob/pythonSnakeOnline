import time
import pygame
from snake.food import Food
from snake.player import Player


def write_text(window, font_num, text, color, pos):
    font = pygame.font.Font(None, font_num)
    text_surface = font.render(text, True, color)
    window.blit(text_surface, pos)


class Game:
    def __init__(self, network, client, mode, game_num):
        self.width = 1200
        self.height = 800
        self.mode = mode
        self.network = network
        self.player = client
        self.food = Food()
        self.game_num = game_num

    def redrawWindow(self, win, player, player2):
        if player:
            player.draw(win)
        if player2:
            player2.draw(win)
        pygame.display.update()

    def game(self):
        WIDTH, HEIGHT = self.width, self.height
        FPS = 60
        WIN = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('snake')
        background_surface = pygame.Surface((WIDTH, HEIGHT))
        background_surface.fill((0, 0, 0))

        pygame.init()

        client2 = None

        clock = pygame.time.Clock()
        WIN.blit(background_surface, (0, 0))
        player = self.player
        if player is None:
            player = Player()
        food = self.food
        start_flag = True
        waiting_for_the_other_flag = False
        both_players_ready_flag = False
        direction = ''
        players_connected_flag = False
        if self.game_num > 1 and (self.mode == 2 or self.mode == 3):
            players_connected_flag = True

        if self.mode == 3:
            player.pos[0] = 300
        if self.mode == 2:
            player.pos[0] = 900

        run = True

        while run:

            if self.mode == 2 or self.mode == 3:
                client2 = self.network.send(self.player)
                if client2 is None:
                    print("client2 is none")

            WIN.fill((0, 0, 0))
            if self.mode == 3 and client2 is not None and client2.connected is False and players_connected_flag is False:
                write_text(WIN, 50, "Waiting for another player to connect...", (0, 255, 0),
                           (WIDTH // 2 - 350, HEIGHT // 2 - 50))
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        return -1
                continue
            elif self.mode == 3 and client2 is None and players_connected_flag is False:
                write_text(WIN, 50, "Failed to create server", (255, 0, 0),
                           (WIDTH // 2 - 200, HEIGHT // 2 - 50))
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        return -1
                continue
            elif self.mode == 2 and client2 is None and players_connected_flag is True:
                write_text(WIN, 50, "Lost connection to Host / can't connect to Host", (255, 0, 0),
                           (WIDTH // 2 - 350, HEIGHT // 2 - 50))
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        return -1
                continue
            elif (self.mode == 3 and client2 is not None and client2.connected is False and players_connected_flag is True) or (self.mode == 3 and client2 is None):
                write_text(WIN, 50, "Other player lost connection", (255, 0, 0),
                           (WIDTH // 2 - 200, HEIGHT // 2 - 50))
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        return -1
                continue
            elif (self.mode == 3 or self.mode == 2) and players_connected_flag is False:
                players_connected_flag = True

            if (self.mode == 3 or self.mode == 2) and client2 and client2.lost is True and player.ready is False:
                write_text(WIN, 50, "waiting for the other player to reset the game", (0, 255, 0),
                           (WIDTH // 2 - 250, HEIGHT // 2 - 50))
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        return -1
                continue
            if start_flag:
                write_text(WIN, 50, "When ready press 'r'", (0, 255, 0),
                           (WIDTH // 2 - 150, HEIGHT // 2 - 50))
            if (self.mode == 3 or self.mode == 2) and waiting_for_the_other_flag:
                write_text(WIN, 50, "waiting for the other player to be ready", (0, 255, 0),
                           (WIDTH // 2 - 250, HEIGHT // 2 - 50))
                player.draw(WIN)
                client2.draw(WIN)

            if food.spawned is False:
                food.set_pos_list_taken(player)
                food.set_spawn_food_pos(WIDTH, HEIGHT)
            food_rect = pygame.Rect(*food.pos, 50, 50)
            pygame.draw.rect(WIN, (0, 0, 255), food_rect)

            if (self.mode == 2 or self.mode == 3) and client2 and client2.ready is False and player.ready is True:
                waiting_for_the_other_flag = True
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            return -1
                continue
            if ((self.mode == 2 or self.mode == 3) and client2 and client2.ready is True and
                    player.ready is True and both_players_ready_flag is False):
                both_players_ready_flag = True
                waiting_for_the_other_flag = False
                player.movement['up'] = True
                direction = 'up'

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return -1
                    if event.key == pygame.K_r and player.ready is False:
                        player.ready = True
                        start_flag = False
                        if self.mode == 1:
                            player.movement['up'] = True
                            direction = 'up'
                            continue
                if player.ready is False:
                    continue

                if event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_w or event.key == pygame.K_UP) and player.movement['down'] is False:
                        player.movement['up'] = True
                        direction = 'up'
                    if (event.key == pygame.K_s or event.key == pygame.K_DOWN) and player.movement['up'] is False:
                        player.movement['down'] = True
                        direction = 'down'
                    if (event.key == pygame.K_d or event.key == pygame.K_RIGHT) and player.movement['left'] is False:
                        player.movement['right'] = True
                        direction = 'right'
                    if (event.key == pygame.K_a or event.key == pygame.K_LEFT) and player.movement['right'] is False:
                        player.movement['left'] = True
                        direction = 'left'

            player.move(direction)
            time.sleep(0.12)

            player.draw(WIN)

            if player.check_collision(WIDTH, HEIGHT, other=client2) or (client2 and client2.lost):

                if (client2 and client2.lost is False) or self.mode == 1:
                    write_text(WIN, 50, "You Lost", (255, 0, 0),
                               (WIDTH // 2 - 100, HEIGHT // 2 - 50))
                    player.lost = True
                    if client2:
                        client2 = self.network.send(self.player)
                else:
                    write_text(WIN, 50, "You Won", (0, 255, 0),
                               (WIDTH // 2 - 100, HEIGHT // 2 - 50))
                    player.ready = False
                    if self.mode == 3:
                        player.pos[0] = 300
                    if self.mode == 2:
                        player.pos[0] = 900
                    if client2:
                        client2 = self.network.send(self.player)

                write_text(WIN, 50, "press 'r' to reset game", (255, 0, 0),
                           (WIDTH // 2 - 180, HEIGHT // 2))
                write_text(WIN, 50, "snake's length: " + str(player.len), (0, 255, 0),
                           (WIDTH // 2 - 150, HEIGHT // 2 + 50))

                pygame.display.update()
                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                            return -1
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            return False
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_r:
                                player.reset_player()
                                return True

            # check if eat food
            if player.pos == food.pos:
                player.add_node()
                food.spawned = False

            if self.mode == 2 or self.mode == 3:
                self.redrawWindow(WIN, self.player, client2)

            clock.tick(FPS)
            pygame.display.update()

        pygame.quit()
        return False


if __name__ == '__main__':
    pass
