import sys
import time

import pygame
import ipaddress


def get_ip_and_port():
    pygame.init()

    # Set up the screen
    screen_width = 1200
    screen_height = 800
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("snake")

    # Define some colors
    black = (0, 0, 0)
    white = (255, 255, 255)

    # Initialize the text input string
    text_input = ""

    # Create a font for rendering text
    font = pygame.font.Font(None, 50)
    text_color = white

    clock = pygame.time.Clock()

    flag = False
    invalid_input_flag = False
    running = True
    while running:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if invalid_input_flag:
                time.sleep(0.2)
                invalid_input_flag = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return -1 # return to menu
                if event.key == pygame.K_RETURN:
                    # User pressed Enter, you can process the input here
                    if text_input == "local":
                        return "local", 5000
                    flag = is_valid_ip_and_port(text_input)
                    print("User Input:", text_input)
                    print(flag)
                    if flag is True:
                        split_strings = text_input.split(":")
                        ip_string = split_strings[0]
                        port_string = split_strings[1]
                        return ip_string, port_string
                    text_input = ""
                    invalid_input_flag = True
                elif event.key == pygame.K_BACKSPACE:
                    # User pressed Backspace, remove the last character
                    text_input = text_input[:-1]
                else:
                    # Append the typed character to the text input string
                    text_input += event.unicode

        # Clear the screen
        screen.fill(black)

        # Render the text input
        write_text(screen, 50, "For your local ip enter 'local'", (0, 255, 0), (250, 250))
        write_text(screen, 50, "Enter ip and port (for ex': 192.168.37.1:1234)", (0, 255, 0), (250, 300))
        write_text(screen, 50, text_input, white, (500, 400))
        if invalid_input_flag:
            write_text(screen, 50, "Invalid input", white, (500, 400))

        # Update the screen
        pygame.display.update()

        # Cap the frame rate
        clock.tick(60)

    pygame.quit()
    sys.exit()


def is_valid_ip(ip_string):
    try:
        ipaddress.ip_address(ip_string)
        return True
    except ValueError:
        return False


def is_valid_port(port_string):
    if len(port_string) == 0:
        return False
    if port_string.isdigit() is False:
        return False
    if 0 < int(port_string) < 65535:
        return True
    return False


def is_valid_ip_and_port(input_string):
    if ':' not in input_string:
        print(" ':' not in str ")
        return False

    split_strings = input_string.split(":")
    ip_string = split_strings[0]
    port_string = split_strings[1]

    print("String 1:", ip_string)
    print("String 2:", port_string)
    if is_valid_ip(ip_string) is False:
        return False
    if is_valid_port(port_string) is False:
        return False
    return True


def write_text(window, font_num, text, color, pos):
    font = pygame.font.Font(None, font_num)
    text_surface = font.render(text, True, color)
    window.blit(text_surface, pos)


if __name__ == '__main__':
    get_ip_and_port()
