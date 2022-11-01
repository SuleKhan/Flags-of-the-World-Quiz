import pygame
import random

pygame.init()

# Screen Dimensions
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 600

# Screen Setup
WIN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flags of the World")
clock = pygame.time.Clock()
FPS = 60

# Define Colors
BG = pygame.Color("chartreuse4")
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Flag Setup
flags_image = pygame.image.load("Images/Flags.png")
flags_image = pygame.transform.scale(flags_image, (420, 300))
flag_width = 30
flag_height = 20
BLIT_FLAG_WIDTH = 300
BLIT_FLAG_HEIGHT = 200

# Text Setup
text_font = pygame.font.Font(None, 32)
input_str = ""
text_rect = pygame.Rect(100, 400, 200, 32)

score_font = pygame.font.Font(None, 70)


def make_flag_list(flags_image):
    flag_list = []

    for row in range(0, 14):
        for col in range(0, 14):

            image = pygame.Surface((flag_width, flag_height))
            image.blit(flags_image, (0, 0), (col * flag_width, row * flag_height, flag_width, flag_height))
            image = pygame.transform.scale(image, (BLIT_FLAG_WIDTH, BLIT_FLAG_HEIGHT))
            flag_list.append(image)

    # ADD LAST FLAG
    image = pygame.Surface((flag_width, flag_height))
    image.blit(flags_image, (0, 0), (0, 14 * flag_height, flag_width, flag_height))
    image = pygame.transform.scale(image, (300, 200))
    flag_list.append(image)

    return flag_list


flags_list = make_flag_list(flags_image)

# list of country names
with open("Country Names", "r") as file:
    country_list = file.readlines()

# remove /n from list and split with delimiter ,
for index in range(0, 197):
    if index != 196:
        country_list[index] = country_list[index][:-1]
    country_list[index] = country_list[index].split(",")

# make flag - name list
flag_name_list = []
for index, flag in enumerate(flags_list):
    flag_name_list.append((flag, country_list[index]))

# randomize flag order
random.shuffle(flag_name_list)

# arrow buttons
arrow_img = pygame.image.load("Images/arrow button.png")
arrow_img = pygame.transform.scale(arrow_img, (80, 200))

right_arrow_rect = pygame.Rect(410, 100, 80, 200)
right_arrow_img = arrow_img

left_arrow_rect = pygame.Rect(10, 100, 80, 200)
left_arrow_img = pygame.transform.flip(arrow_img, True, False)

# give up button
give_up_font = pygame.font.Font(None, 50)
give_up_str = "Give Up"
give_up_text = give_up_font.render(give_up_str, True, WHITE)

give_up_width = give_up_text.get_width() + 10
give_up_height = give_up_text.get_height() + 10
give_up_rect = pygame.Rect(SCREEN_WIDTH - give_up_width - 20, SCREEN_HEIGHT - give_up_height - 20, give_up_width, give_up_height)

# Timer
timer_font = pygame.font.Font(None, 50)

timer_rect = pygame.rect.Rect(SCREEN_WIDTH - 100, 10, 50, 50)


run = True
backspace_counter = 0
backspace_tick = 8

index = 0

score = 0

gave_up = False

timer = 0
secs = 0
mins = 0

while run:
    clock.tick(FPS)

    # draw onto screen
    WIN.fill(BG)

    if not gave_up:
        timer += 1
        if timer >= FPS:
            secs += 1
            timer = 0
            if secs >= 60:
                mins += 1
                secs = 0

        pygame.draw.rect(WIN, WHITE, text_rect, 2)

        text_surface = text_font.render(input_str, True, WHITE)
        WIN.blit(text_surface, (text_rect.x+5, text_rect.y+5))

        pygame.draw.rect(WIN, RED, give_up_rect)
        WIN.blit(give_up_text, (give_up_rect.x + 5, give_up_rect.y + 5))
    else:
        text_surface = text_font.render(flag_name_list[index][1][0].upper(), True, WHITE)
        text_surface_width = text_surface.get_width()
        text_surface_height = text_surface.get_height()
        text_surface_rect = pygame.rect.Rect(SCREEN_WIDTH/2 - text_surface_width/2, 400, text_surface_width, text_surface_height)
        WIN.blit(text_surface, text_surface_rect)

    timer_str = f"{mins:02}:{secs:02}"
    timer_text = timer_font.render(timer_str, True, WHITE)
    WIN.blit(timer_text, timer_rect)

    score_text = score_font.render(str(score) + " / 197", True, WHITE)
    score_text_width = score_text.get_width()
    WIN.blit(score_text, (SCREEN_WIDTH/2 - score_text_width/2, 50))

    WIN.blit(flag_name_list[index][0], (SCREEN_WIDTH/2 - BLIT_FLAG_WIDTH/2, 100))

    if index > 0:
        WIN.blit(left_arrow_img, left_arrow_rect)
    if index < len(flag_name_list) - 1:
        WIN.blit(right_arrow_img, right_arrow_rect)

    pygame.display.update()

    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN and event.key != pygame.K_BACKSPACE:
            input_str += event.unicode
        if event.type == pygame.MOUSEBUTTONDOWN:
            if right_arrow_rect.collidepoint(event.pos) and index < len(flag_name_list) - 1:
                index += 1
                input_str = ""
            if left_arrow_rect.collidepoint(event.pos) and index > 0:
                index -= 1
                input_str = ""
            if give_up_rect.collidepoint(event.pos):
                gave_up = True

    if keys[pygame.K_BACKSPACE] and backspace_counter > backspace_tick:
        input_str = input_str[:-1]
        backspace_counter = 0

    backspace_counter += 1

    # text box
    text_width = text_surface.get_width()
    text_rect.w = max(300, text_width + 10)
    if text_width + 10 > 300:
        text_rect.x = (SCREEN_WIDTH - text_width) / 2
    else:
        text_rect.x = 100

    # check input string
    if input_str.lower() in flag_name_list[index][1]:
        flag_name_list.remove(flag_name_list[index])
        input_str = ""
        score += 1
        if len(flag_name_list) == 0:
            print("YOU WIN!")
            run = False
        elif index >= len(flag_name_list):
            index = len(flag_name_list) - 1

pygame.quit()

