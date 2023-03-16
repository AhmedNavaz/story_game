import pygame
import os

WIDTH, HEIGHT = 1280, 720

# load images
BLACK_BG = pygame.transform.scale(pygame.image.load(os.path.join("assets/backgrounds", "black.jpg")), (WIDTH, HEIGHT))
COUNCIL_ROOM_BG = pygame.transform.scale(pygame.image.load(os.path.join("assets/backgrounds", "council_room.jpg")),
                                         (WIDTH, HEIGHT))
BATTLEFIELD_BG = pygame.transform.scale(pygame.image.load(os.path.join("assets/backgrounds", "battlefield.jpg")),
                                        (WIDTH, HEIGHT))
BATTLEFIELD_2_BG = pygame.transform.scale(pygame.image.load(os.path.join("assets/backgrounds", "battlefield_2.jpg")),
                                          (WIDTH, HEIGHT))
BATTLEFIELD_3_BG = pygame.transform.scale(pygame.image.load(os.path.join("assets/backgrounds", "battlefield3.jpg")),
                                          (WIDTH, HEIGHT))
GERMAN_ROOM_BG = pygame.transform.scale(pygame.image.load(os.path.join("assets/backgrounds", "german_room.jpg")),
                                        (WIDTH, HEIGHT))
WARPLAN_BG = pygame.transform.scale(pygame.image.load(os.path.join("assets/backgrounds", "warplan.jpg")),
                                    (WIDTH, HEIGHT))


class Dialogue:
    def __init__(self, text, background=BLACK_BG, options=None):
        if options is None:
            options = []
        self.text = text
        self.background = background
        self.options = options
        self.chosen = -1


# script
part_1 = [
    Dialogue("B.A.S.S presents"),
    Dialogue("1 September,1939, Britain..."),
    Dialogue("Germany has crossed into Poland with armed forces! They are quickly advancing into WARSAW!",
             COUNCIL_ROOM_BG),
    Dialogue("France is on standby, waiting for the British' official call. We need your decision Commander!!",
             COUNCIL_ROOM_BG, ["Send troops to Poland , breaking out a war against Germany",
                               "Stay neutral, let Poland handle the situation"]),
    Dialogue("Wise choice commander!", COUNCIL_ROOM_BG),
]

part_1_question_1_option_1 = [
    Dialogue("Soldiers have been dispatched to Poland , war ensues against German forces...", BATTLEFIELD_2_BG),
    Dialogue("Weeks pass by.. German forces overwhelm the Allies. Troops are retreating", BATTLEFIELD_2_BG),
    Dialogue("Chief! The battle is not looking good, we have to regroup and retaliate after further planning",
             BATTLEFIELD_BG),
    Dialogue(
        'Taking casualties back home wont be easy. Will burn resources and time. But I need official orders "Sir!"',
        BATTLEFIELD_BG, ["Carry casualties back to Britain, risk losing more lives",
                         "Retreat immediately, leave injured behind"]),
]

part_1_question_1_option_2 = [
    Dialogue("British troops kept on standby , Poland is fighting German forces with France", BATTLEFIELD_BG),
    Dialogue("Weeks pass by.. German forces overwhelm the Allies. Troops are retreating", BATTLEFIELD_BG),
    Dialogue("Helping casualties wont be easy. Will burn resources and time. But I need official orders SIR!",
             BATTLEFIELD_BG, ["Carry casualties back to Britain, risk losing more lives",
                              "Save resources , dont get involved"]),
]

part_2 = [
    Dialogue("Meanwhile IN GERMANY...", GERMAN_ROOM_BG),
    Dialogue("Marshal , I come bearing both good and bad news.", GERMAN_ROOM_BG),
    Dialogue("We have total control over WARSAW.. Ally troops have retreated!! We won ground.", GERMAN_ROOM_BG),
    Dialogue("Now the bad.. France and Britain are planning to retaliate soon. We need to plan our defense , "
             "no time should be wasted!", GERMAN_ROOM_BG),
    Dialogue("France and Britain have their troops surrounding the south and east. Attacking from the WEST IS "
             "POSSIBLE but the terrain puts us at a DISADVANTAGE! Attack from the NORTH would give us a tactical "
             "advantage.", WARPLAN_BG),
    Dialogue("NORTH is the best attack strategy , but we have to overrun BELGIUM. They are neutral. What should we "
             "do Marshal!?", WARPLAN_BG, ["ATTACK FROM WEST", "INVADE BELGIUM"]),
    Dialogue("Just what I was thinking. Troops will be mobilized right away.", WARPLAN_BG),
    Dialogue("10th MAY , 1940...OPERATION FALL GELB"),
    Dialogue("Germany has infiltrated BELGIUM. But Belgian defense is resilient.. German troops are slowed down!!",
             BATTLEFIELD_3_BG, ["Deploy HEINKEL H11 AIR BOMBING FLEET (WILL CAUSE CIVILIAN DEATHS)",
                                "Deploy PANZER IV TANKS UNIT (LOW CASUALTIES BUT MIGHT LOSE BATTLE)"]),
]
