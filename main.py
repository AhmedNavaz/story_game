from time import sleep

import pygame
import os
from option import OptionButton
from button import Button
import script
from user import User

from gtts import gTTS

# create game window
WIDTH, HEIGHT = 1280, 720  # <-- change this to your screen resolution
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Story Game")
pygame.font.init()
pygame.mixer.init(44100, -16, 2, 2048)

# load assets
START_BT = pygame.transform.scale(pygame.image.load(os.path.join("assets/images", "start.png")), (250, 250))
QUIT_BT = pygame.transform.scale(pygame.image.load(os.path.join("assets/images", "quit.png")), (225, 90))
MAIN_MENU_BG = pygame.transform.scale(pygame.image.load(os.path.join("assets/backgrounds", "main_menu.png")),
                                      (WIDTH, HEIGHT))
SPEECH_ON_BT = pygame.transform.scale(pygame.image.load(os.path.join("assets/images", "sound.png")), (64, 64))
SPEECH_OFF_BT = pygame.transform.scale(pygame.image.load(os.path.join("assets/images", "no-sound.png")), (64, 64))
MAIN_MENU_MUSIC = pygame.mixer.Sound(os.path.join("assets/audios", "main_menu.mp3"))
MAIN_MENU_MUSIC.set_volume(0.1)
GAMEPLAY_MUSIC = pygame.mixer.Sound(os.path.join("assets/audios", "game_audio.mp3"))
GAMEPLAY_MUSIC.set_volume(0.1)

# button
start_button = Button(START_BT, (WIDTH / 2, HEIGHT / 2))
quit_button = Button(QUIT_BT, (WIDTH - 112.5, 45))
speech_on_button = Button(SPEECH_ON_BT, (40, 45))
speech_off_button = Button(SPEECH_OFF_BT, (40, 45))

parts = [script.part_1, script.part_2]

current_part = 0
current_scene = 0
run = True
current_footer_text = ""
speech_on = True
answers = set()

user = User("", "", "")


def play_audio(text):
    tts = gTTS(text=text, lang='en')
    file_name = "assets/audios/speech/" + text + ".mp3"
    tts.save(file_name)
    pygame.mixer.music.load(file_name)
    pygame.mixer.music.play()


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
    # loop through each option
    for i in range(len(options)):
        # create an option button
        if len(options) > 2:
            option = OptionButton(options[i], 100 * i + 175 - 125, WIDTH, font, pygame, window)
        else:
            option = OptionButton(options[i], 100 * i + 175, WIDTH, font, pygame, window)
        # draw the option
        option.draw(window)
        # if the option is clicked, set the chosen option to the current option
        if option.is_clicked():
            parts[current_part][current_scene].chosen = i
            answers.add(options[i])
            decide()


def decide():
    global current_scene, run, current_part, current_footer_text
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

    current_footer_text = parts[current_part][current_scene].text
    if speech_on:
        play_audio(current_footer_text)

# main loop
def main():
    FPS = 60
    TIMER = pygame.time.get_ticks() / 1000
    started = False

    print(user)

    # redraw/refresh the screen
    def refresh_display():
        font = pygame.font.SysFont("comicsans", 30)

        if started:
            # draw the background
            window.blit(parts[current_part][current_scene].background, (0, 0))

            # draw the quit button
            quit_button.update(window)

            # draw the speech button
            if speech_on:
                speech_on_button.update(window)
            else:
                speech_off_button.update(window)

            # draw a rectangle in the bottom section of the screen to display text
            pygame.draw.rect(window, (0, 0, 0, 128), (0, HEIGHT - 120, WIDTH, 120), 0, 10)

            # display the parts[current_part] text in the bottom section of the screen in a specific width
            display_footer(current_footer_text, font)

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
        global current_scene, speech_on
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
            if event.type == pygame.MOUSEBUTTONDOWN:
                if speech_on_button.checkForInput(pygame.mouse.get_pos()) and not speech_on:
                    speech_on = True
                    break
                elif speech_off_button.checkForInput(pygame.mouse.get_pos()) and speech_on:
                    speech_on = False
                    break
                if quit_button.checkForInput(pygame.mouse.get_pos()):
                    print(answers)
                    run = False
                    break
                # if the user clicks the mouse, go to the next scene
                if started and parts[current_part][current_scene].options == []:
                    decide()
                # if the user clicks the mouse, start the game
                if not started:
                    if start_button.checkForInput(pygame.mouse.get_pos()):
                        started = True

        refresh_display()

    pygame.quit()


def user_input():
    true = True
    name = ""
    age = ""
    gender = ""

    current_input = "name"

    font = pygame.font.SysFont("comicsans", 30)
    while true:
        window.blit(MAIN_MENU_BG, (0, 0))

        # User Details header
        draw_text("User Details", font, (255, 255, 255), 200, 20)

        # Name
        draw_text("Name: ", font, (255, 255, 255), 20, 100)
        draw_text(name, font, (255, 255, 255), 150, 100)

        # Age
        draw_text("Age: ", font, (255, 255, 255), 20, 200)
        draw_text(age, font, (255, 255, 255), 150, 200)

        # Gender
        draw_text("Gender: ", font, (255, 255, 255), 20, 300)
        draw_text(gender, font, (255, 255, 255), 150, 300)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                true = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    if current_input == "name":
                        name = name[:-1]
                    elif current_input == "age":
                        age = age[:-1]
                    elif current_input == "gender":
                        gender = gender[:-1]
                elif event.key == pygame.K_RETURN:
                    if current_input == "name":
                        user.set_name(name)
                        current_input = "age"
                    elif current_input == "age":
                        user.set_age(age)
                        current_input = "gender"
                    else:
                        user.set_gender(gender)
                        true = False
                        main()
                else:
                    if current_input == "name":
                        name += event.unicode
                    elif current_input == "age":
                        age += event.unicode
                    elif current_input == "gender":
                        gender += event.unicode

        if name != "":
            # instructions to the user at bottom left
            f = pygame.font.SysFont("comicsans", 20)
            draw_text("Press enter to save and move to the next step", f, (255, 255, 255), 20, HEIGHT - 50)

        pygame.display.update()


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    window.blit(img, (x, y))


if __name__ == "__main__":
    user_input()
