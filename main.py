import pygame
import os
from option import OptionButton
from button import Button
import script

# create game window
WIDTH, HEIGHT = 1920, 1080  # <-- change this to your screen resolution
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Story Game")
pygame.font.init()
pygame.mixer.init(44100, -16, 2, 2048)

# load assets
START_BT = pygame.transform.scale(pygame.image.load(os.path.join("assets/images", "start.png")), (250, 250))
QUIT_BT = pygame.transform.scale(pygame.image.load(os.path.join("assets/images", "quit.png")), (225, 90))
MAIN_MENU_BG = pygame.transform.scale(pygame.image.load(os.path.join("assets/backgrounds", "main_menu.png")),
                                      (WIDTH, HEIGHT))
MAIN_MENU_MUSIC = pygame.mixer.Sound(os.path.join("assets/audios", "main_menu.mp3"))
MAIN_MENU_MUSIC.set_volume(0.5)
GAMEPLAY_MUSIC = pygame.mixer.Sound(os.path.join("assets/audios", "game_audio.mp3"))
GAMEPLAY_MUSIC.set_volume(0.5)

# button
start_button = Button(START_BT, (WIDTH / 2, HEIGHT / 2))
quit_button = Button(QUIT_BT, (WIDTH - 112.5, 45))

parts = [script.part_1, script.part_2]

current_part = 0
current_scene = 0
OPTIONS = []
run = True


def display_footer(text, font):
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
                    window.blit(font.render(new_line, True, (255, 255, 255)), (40, (HEIGHT - 120) + 30 * i))
                    i += 1
                    new_line = word
                # if the line is not too long, add the word to the line
                else:
                    new_line += " " + word
        # display the last line
        window.blit(font.render(new_line, True, (255, 255, 255)), (40, (HEIGHT - 120) + 30 * i))
    # if the text is not too long, display it
    else:
        window.blit(font.render(text, True, (255, 255, 255)), (40, (HEIGHT - 120) + 30 * i))


# display options in the middle of the screen
def display_options(options, font):
    OPTIONS.clear()
    # loop through each option
    for i in range(len(options)):
        # create an option button
        if len(options) > 2:
            option = OptionButton(options[i], 100 * i + 175 - 125, WIDTH, font, pygame, window)
        else:
            option = OptionButton(options[i], 100 * i + 175, WIDTH, font, pygame, window)
        # add the option to the list of options
        OPTIONS.append(option)
        # draw the option
        option.draw(window)
        # save the chosen option
        if option.is_clicked():
            parts[current_part][current_scene].chosen = i


def decide():
    global current_scene, run, current_part
    # if the current part is the last part, end the game
    if len(parts[current_part]) - 1 == current_scene:
        if current_part < len(parts) - 1:
            current_part += 1
            current_scene = -1
    # if the current part is not the last part, go to the next scene
    if current_part == 0:
        if parts[current_part][current_scene].chosen != -1:
            if parts[current_part][current_scene].chosen == 0:
                parts[current_part].extend(script.part_1_question_1_option_1)
            else:
                parts[current_part].extend(script.part_1_question_1_option_2)
            current_scene += 1
        else:
            if current_scene < len(parts[current_part]) - 1:
                current_scene += 1
    if current_part == 1:
        if current_scene < len(parts[current_part]) - 1:
            current_scene += 1


# main loop
def main():
    FPS = 60
    TIMER = pygame.time.get_ticks() / 1000
    started = False

    # redraw/refresh the screen
    def refresh_display():

        font = pygame.font.SysFont("comicsans", 30)

        if started:
            # draw the background
            window.blit(parts[current_part][current_scene].background, (0, 0))

            # draw the quit button
            quit_button.update(window)

            # draw a rectangle in the bottom section of the screen to display text
            pygame.draw.rect(window, (0, 0, 0, 128), (0, HEIGHT - 120, WIDTH, 120), 0, 10)

            # display the parts[current_part] text in the bottom section of the screen in a specific width
            display_footer(parts[current_part][current_scene].text, font)

            # display options
            display_options(parts[current_part][current_scene].options, font)
        else:
            # draw the background
            window.blit(MAIN_MENU_BG, (0, 0))
            # draw the start button
            start_button.update(window)

        pygame.display.update()

    global run
    while run:
        global current_scene
        TIMER = pygame.time.get_ticks() / 1000
        if started:
            GAMEPLAY_MUSIC.play()
            MAIN_MENU_MUSIC.stop()
        else:
            MAIN_MENU_MUSIC.play()
            GAMEPLAY_MUSIC.stop()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            # if the user clicks the mouse, go to the next scene
            if event.type == pygame.MOUSEBUTTONDOWN and started:
                decide()
            # if the user clicks the mouse, start the game
            if event.type == pygame.MOUSEBUTTONDOWN and not started:
                if start_button.checkForInput(pygame.mouse.get_pos()):
                    started = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if quit_button.checkForInput(pygame.mouse.get_pos()):
                    run = False

        refresh_display()

    pygame.quit()


if __name__ == "__main__":
    main()
