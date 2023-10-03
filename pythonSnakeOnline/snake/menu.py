import pygame


def write_text(window, font_num, text, color, pos):
    font = pygame.font.Font(None, font_num)
    text_surface = font.render(text, True, color)
    window.blit(text_surface, pos)


def menu():
    WIDTH, HEIGHT = 1200, 800
    FPS = 60
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('snake')
    background_surface = pygame.Surface((WIDTH, HEIGHT))
    background_surface.fill((0, 0, 0))
    pygame.init()
    clock = pygame.time.Clock()
    WIN.blit(background_surface, (0, 0))
    run = True

    while run:
        WIN.fill((0, 0, 0))
        write_text(WIN, 50, "press 'Esc' to return to menu at any moment", (0, 255, 0), (0, 0))
        write_text(WIN, 50, "press '1' to play offline game", (0, 255, 0), (WIDTH // 2 - 200, HEIGHT // 2 - 50))
        write_text(WIN, 50, "press '2' to join online game", (0, 255, 0), (WIDTH // 2 - 200, HEIGHT // 2))
        write_text(WIN, 50, "press '3' to create server", (0, 255, 0), (WIDTH // 2 - 200, HEIGHT // 2 + 50))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 1
                if event.key == pygame.K_2:
                    return 2
                if event.key == pygame.K_3:
                    return 3

        clock.tick(FPS)
        pygame.display.update()

    pygame.quit()
    return 0
