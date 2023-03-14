from time import sleep

import pygame
import os
from button import OptionButton

# create game window
WIDTH, HEIGHT = 1280, 720
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Story Game")
pygame.font.init()

# load images
BACKGROUND1 = pygame.transform.scale(pygame.image.load(os.path.join("backgrounds", "battlefield.jpg")), (WIDTH, HEIGHT))

script = [
    {
        "text": "Germany has crossed into Poland with armed forces! They are quickly advancing into WARSAW!",
        "options": []
    },
    {
        "text": "France is on standby, waiting for the British' official call. We need your decision Commander!!",
        "options": [
            "Send troops to Poland , breaking out a war against Germany",
            "Stay neutral, let Poland handle the situation",
        ]
    },

]

OPTIONS = []


def display_footer(text, font, ):
    i = 0
    text_width, text_height = font.size(text)
    # if the text is too long, split it into multiple lines
    if text_width > 1200:
        # split the text into words
        words = text.split(" ")
        # create a new line
        new_line = ""
        # loop through each word
        for word in words:
            # if the new line is empty, add the word to it
            if new_line == "":
                new_line = word
            # if the new line is not empty, add the word to it and check if the line is too long
            else:
                # if the line is too long, display the line and start a new line
                if font.size(new_line + " " + word)[0] > 1200:
                    window.blit(font.render(new_line, True, (255, 255, 255)), (40, 600 + 30 * i))
                    i += 1
                    new_line = word
                # if the line is not too long, add the word to the line
                else:
                    new_line += " " + word
        # display the last line
        window.blit(font.render(new_line, True, (255, 255, 255)), (40, 600 + 30 * i))


# display options in the middle of the screen
def display_options(options, font):
    OPTIONS.clear()
    # loop through each option
    for i in range(len(options)):
        # create an option button
        option = OptionButton(options[i], 100 * i, WIDTH, font, pygame, window)
        # add the option to the list of options
        OPTIONS.append(option)
        # draw the option
        option.draw(window)


# main loop
def main():
    FPS = 60
    TIMER = pygame.time.get_ticks() / 1000
    current_scene = 0

    # redraw/refresh the screen
    def refresh_display():

        window.blit(BACKGROUND1, (0, 0))
        # draw a rectangle in the bottom section of the screen to display text
        pygame.draw.rect(window, (0, 0, 0, 128), (0, 600, 1280, 120), 0, 10)

        # display text
        font = pygame.font.SysFont("comicsans", 30)

        # display the script text in the bottom section of the screen in a specific width
        display_footer(script[current_scene]["text"], font)

        # display options
        display_options(script[current_scene]["options"], font, )

        pygame.display.update()

    run = True
    while run:
        TIMER = pygame.time.get_ticks() / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if current_scene < len(script) - 1:
                    current_scene += 1
                else:
                    run = False

        refresh_display()

    pygame.quit()


if __name__ == "__main__":
    main()
