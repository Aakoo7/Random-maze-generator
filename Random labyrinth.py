import random, sys, time, pygame
from fractions import gcd
from pygame.locals import *
from random import *

#End goal: Make a random labyrinth generator
#Generate random, completable walls

    #Have generate_maze be actually completable (Atm moves before assigning, which creates a lot of problems when moving out of already assigned tiles)

#This is stolen. Credit to John Millikin from stackoverflow.com and john-millikin.com. I'd never come up with a solution this compact
def gcd(a, b):
    while b:
        a, b = b, a%b
    return a

if input('Would you like to enable blind mode (recommended)? y/n >>> ') == 'y':
    blind_mode = True
else: blind_mode = False
tile_amount_multiplier = 1 #!!! NEVER SET ABOVE 2! IF YOU DO, THE RESULTS ARE TOTALLY INTENTIONAL GAME DESIGN THAT I JUST DON'T WANT YOU TO SEE
pygame.init()
window_resolution = 800, 600
window = pygame.display.set_mode((window_resolution[0], window_resolution[1]))
score = 0
stag_line_width = 5
line_width = stag_line_width
tile_width_height = gcd(window_resolution[0], window_resolution[1]) // 4 // tile_amount_multiplier
touched = []
wall_drawn = False
player_posx = 0
player_posy = 0
border = window_resolution[0]//100 *2 * tile_amount_multiplier -1, window_resolution[1]//100 *2 * tile_amount_multiplier -1
goal_posx = randint(0, border[0])
goal_posy = randint(0, border[1])
player_pos = player_posx, player_posy
goal_pos = goal_posx, goal_posy
keys = pygame.key.get_pressed()
tile_amount = window_resolution[0] // tile_width_height * (window_resolution[1] // tile_width_height)

def is_border(coordinates, direction):
    if direction == 'right':
        if coordinates[0] >= border[0]:
            return True
        else:
            return False
    elif direction == 'left':
        if coordinates[0] <= 0:
            return True
        else: 
            return False
    elif direction == 'up':
        if coordinates[1] <= 0:
            return True
        else:
            return False
    elif direction == 'down':
        if coordinates[1] >= border [1]:
            return True
        else: 
            return False
    else:
        print('You are safe from the end of the fucking world')
        return False
    print('Unexpected error in determining border location. You should probably fix that')

def is_wall(dire):
    if is_border(player_pos, dire) == False:
        for pos in no_wall_tiles:
            if (dire == 'right' or 'left') and ((player_pos[1] == pos[0][1]) or (player_pos[1] == pos[1][1])):
                if dire == 'right':
                    if ((player_pos[0] == pos[0][0]) or (player_pos[0] == pos[1][0])) and (((player_pos[0] + 1) == pos[1][0]) or ((player_pos[0] + 1) == pos[0][0])):
                        return False
                elif dire == 'left':
                    if ((player_pos[0] == pos[0][0]) or (player_pos[0] == pos[1][0])) and (((player_pos[0] - 1) == pos[1][0]) or ((player_pos[0] - 1) == pos[0][0])):
                        return False
            if (dire == 'up' or 'down') and ((player_pos[0] == pos[1][0]) or (player_pos[0] == pos[0][0])):
                if dire == 'up':
                    if ((player_pos[1] == pos[0][1]) or (player_pos[1] == pos[1][1])) and (((player_pos[1] - 1) == pos[1][1]) or ((player_pos[1] - 1) == pos[0][1])):
                        return False
                elif dire == 'down':
                    if ((player_pos[1] == pos[0][1]) or (player_pos[1] == pos[1][1])) and (((player_pos[1] + 1) == pos[1][1]) or ((player_pos[1] + 1) == pos[0][1])):
                        return False
        return True
    else:
        return True

def random_direction():
    digit = randint(1, 4)
    if digit == 1:
        return 'right'
    if digit == 2:
        return 'left'
    if digit == 3:
        return 'up'
    return 'down'


def generate_maze():
    wall_generated = False
    generation_visited = []
    global no_wall_tiles
    no_wall_tiles = []
    generation_pos = [randint(0, border[0]), randint(0, border [1])]
    generation_last_pos = []
    first_run = True
    while wall_generated == False:
        if tuple(generation_pos) in generation_visited:
            is_visited = True
        else:
            is_visited = False
        if is_visited == False:
            generation_visited.append(tuple(generation_pos))
            if first_run == False:
                no_wall_tiles.append((tuple(generation_last_pos), tuple(generation_pos)))
        direction = random_direction()
        generation_last_pos = generation_pos.copy()
        if is_border(tuple(generation_pos), direction) == False: #Checks for bounds
            if direction == 'right': #Checks every direction possible
                generation_last_pos = generation_pos.copy()
                generation_pos[0] += 1
            elif direction == 'left': # ^
                generation_last_pos = generation_pos.copy()
                generation_pos[0] -= 1
            elif direction == 'up': # ^
                generation_last_pos = generation_pos.copy()
                generation_pos[1] -= 1
            elif direction == 'down': # ^
                generation_last_pos = generation_pos.copy()
                generation_pos[1] += 1
        first_run = False
        if len(generation_visited) == tile_amount:
            print(no_wall_tiles)
            wall_generated = True

def is_touched(x):
    return x in touched

def draw_walls():
    opposite_cord = 0
    line_color = 100, 0 , 100
    if blind_mode == True:
        line_color = 0,0,0
    for z in range(window_resolution[0] // tile_width_height):
        global line_width
        coordinatex = window_resolution[0] // 10
        coordinatey = window_resolution[1] // 10
        posx = 0
        for x in range(coordinatex // 10 * 4 * tile_amount_multiplier):
            for i in range(1, 4):
                if i == 1:
                    for coord in no_wall_tiles:
                        if (x, z) in coord and (x, z+1) in coord:
                            should_draw = False
                            break
                        should_draw = True
                    if should_draw == True:
                        pygame.draw.line(window,(line_color),(posx, opposite_cord + tile_width_height), (tile_width_height + posx, opposite_cord + tile_width_height), line_width)
                elif i == 2:
                    for coord in no_wall_tiles:
                        if (x, z) in coord and (x+1, z) in coord:
                            should_draw = False
                            break
                        should_draw = True
                    if should_draw == True:
                        pygame.draw.line(window,(line_color),(posx + tile_width_height, opposite_cord), (posx + tile_width_height, opposite_cord + tile_width_height), line_width)
            posx += tile_width_height
            line_width = stag_line_width
        for y in range(coordinatey // 10 * 4 * tile_amount_multiplier):
            posx += tile_width_height
            line_width = stag_line_width
        opposite_cord += tile_width_height
        posx = 0

def is_victory ():
    if player_pos == goal_pos:
        return True
    return False

def draw_tileset():
    opposite_cord = 0
    for z in range(window_resolution[0] // tile_width_height):
        global line_width
        rect_color = 0,0,0
        rect_coror_perma = rect_color
        coordinatex = window_resolution[0] // 10
        coordinatey = window_resolution[1] // 10
        posx = 0
        for x in range(coordinatex // 10 * 4 * tile_amount_multiplier):
            if goal_posx == x and goal_posy == z:
                line_width = 0
                rect_color = (255, 0, 0)
            elif player_posx == x and player_posy == z:
                rect_color = (0, 0, 255)
                line_width = 0
            elif is_touched((x, z)):
                rect_color = 50,200,200
                line_width = 0
            pygame.draw.rect(window, rect_color, (posx, opposite_cord, tile_width_height, tile_width_height), line_width)
            rect_color = rect_coror_perma
            posx += tile_width_height
            line_width = stag_line_width
        for y in range(coordinatey // 10 * 4 * tile_amount_multiplier):
            if player_posy == z and player_posy == y:
                line_width = 1
            pygame.draw.rect(window,(rect_color),(opposite_cord, posx, tile_width_height, tile_width_height), line_width)
            posx += tile_width_height
            line_width = stag_line_width
        opposite_cord += tile_width_height
        posx = 0

#Dumb ass system to coordinates conversion guide: coord main_coordinate = main_coordinate, secondary coordinate = z

generate_maze()
draw_tileset()
draw_walls()
pygame.display.update()

while True:
    player_pos = player_posx, player_posy
    if is_victory() == True:
        score += 1
        print('Your score is now', score)
        player_posx = 0
        player_posy = 0
        goal_posx = randint(0, border[0])
        goal_posy = randint(0, border[1])
        goal_pos = goal_posx, goal_posy
        touched = []
        generate_maze()
        window.fill((0, 0, 0))
        draw_tileset()
        draw_walls()
        pygame.display.update()
    for event in pygame.event.get():
        if event.type == QUIT:
            print('You got a score of', score)
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == K_a and is_wall('left') == False:
                if player_pos not in touched:
                    touched.append(player_pos)
                player_posx -= 1
                window.fill((0, 0, 0))
                draw_tileset()
                draw_walls()
                pygame.display.update()
            elif event.key == K_d and is_wall('right') == False:
                if player_pos not in touched:
                    touched.append(player_pos)
                player_posx += 1 
                window.fill((0, 0, 0))
                draw_tileset()
                draw_walls()
                pygame.display.update()
            elif event.key == K_s and is_wall('down') == False:
                if player_pos not in touched:
                    touched.append(player_pos)
                player_posy += 1
                window.fill((0, 0, 0))
                draw_tileset()
                draw_walls()
                pygame.display.update()
            elif event.key == K_w and is_wall('up') == False:
                if player_pos not in touched:
                    touched.append(player_pos)
                player_posy -= 1
                window.fill((0, 0, 0))
                draw_tileset()
                draw_walls()
                pygame.display.update()