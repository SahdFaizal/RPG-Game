import pygame 
from pygame.locals import *
import math
import random
import sys
import os
import pickle
from game_tiles import image_list

WIDTH = 1370
HEIGHT = 710
FPS = 60

# Colors (R.G.B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RPG Game")
clock = pygame.time.Clock()

class game:
    def __init__(self, image_tiles):
        self.running = True
        self.idle = [pygame.transform.scale2x(pygame.image.load(os.path.join("player", "idle0.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("player", 'idle90.png'))), pygame.transform.scale2x(pygame.image.load(os.path.join("player",'idle-90.png'))), 
        pygame.transform.scale2x(pygame.image.load(os.path.join("player",'idle180.png')))]
        self.idle = [pygame.transform.scale2x(pygame.image.load(os.path.join("player", "idle0.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("player", 'idle90.png'))), pygame.transform.scale2x(pygame.image.load(os.path.join("player",'idle-90.png'))), 
        pygame.transform.scale2x(pygame.image.load(os.path.join("player",'idle180.png')))]
        self.walk_up = [pygame.transform.scale2x(pygame.image.load(os.path.join("player", "walk0.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("player", 'walk0.1.png'))), pygame.transform.scale2x(pygame.image.load(os.path.join("player",'walk0.2.png'))), 
        pygame.transform.scale2x(pygame.image.load(os.path.join("player",'walk0.3.png'))), pygame.transform.scale2x(pygame.image.load(os.path.join("player",'walk0.4.png'))), pygame.transform.scale2x(pygame.image.load(os.path.join("player",'walk0.5.png')))]
        self.walk_down = [pygame.transform.scale2x(pygame.image.load(os.path.join("player", "walk180.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("player", 'walk180.1.png'))), pygame.transform.scale2x(pygame.image.load(os.path.join("player",'walk180.2.png'))), 
        pygame.transform.scale2x(pygame.image.load(os.path.join("player",'walk180.3.png'))), pygame.transform.scale2x(pygame.image.load(os.path.join("player",'walk180.4.png'))), pygame.transform.scale2x(pygame.image.load(os.path.join("player",'walk180.5.png')))]
        self.walk_right = [pygame.transform.scale2x(pygame.image.load(os.path.join("player", "walk90.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("player", 'walk90.1.png'))), pygame.transform.scale2x(pygame.image.load(os.path.join("player",'walk90.2.png'))), 
        pygame.transform.scale2x(pygame.image.load(os.path.join("player",'walk90.3.png'))), pygame.transform.scale2x(pygame.image.load(os.path.join("player",'walk90.4.png'))), pygame.transform.scale2x(pygame.image.load(os.path.join("player",'walk90.5.png')))]
        self.walk_left = [pygame.transform.scale2x(pygame.image.load(os.path.join("player", "walk-90.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("player", 'walk-90.1.png'))), pygame.transform.scale2x(pygame.image.load(os.path.join("player",'walk-90.2.png'))), 
        pygame.transform.scale2x(pygame.image.load(os.path.join("player",'walk-90.3.png'))), pygame.transform.scale2x(pygame.image.load(os.path.join("player",'walk-90.4.png'))), pygame.transform.scale2x(pygame.image.load(os.path.join("player",'walk-90.5.png')))]
        self.grass = pygame.image.load("grass.png")
        self.grass = pygame.transform.scale(self.grass, (math.floor(1.25 * WIDTH),math.floor(1.25 * HEIGHT)))
        self.player_x = 65
        self.player_y = 625
        self.joy_x = 0
        self.joy_y = 0
        self.joy_dist = 0
        self.key_buttons = []
        self.costume = self.idle[3]
        self.player_dir = 0 
        self.frame = 0
        self.base_costume = 1
        self.tiles = []

        for tile in image_list: 
            self.tiles.append(pygame.transform.scale2x(pygame.image.load(tile)))

        self.camera_x = WIDTH/2
        self.camera_y = HEIGHT/2
        self.tile_costume = self.tiles[20]
        self.grid = []
        if os.path.isfile("grid"):
            self.grid = pickle.load(open("grid", "rb"))
        
        self.gidx = 0
        self.Gmax = 100
        self.gx = 0 
        self.gy = 0

    def background(self, surf): 
        surf.blit(self.grass, (WIDTH - ((self.camera_x - WIDTH/2)%32) - WIDTH, HEIGHT - ((self.camera_y - HEIGHT/2)%32) - HEIGHT))
        pass
    
    def paint_tiles(self, surf): 
        self.gx = (self.camera_x)
        self.gy = (self.camera_y)
        self.gidx = math.floor((self.gx-WIDTH/2)/32)
        self.gidx += 0 - self.Gmax * math.floor((self.gy-HEIGHT/2)/32)
        y_pos = (HEIGHT) - ((self.gy - HEIGHT/2) %32)

        for m in range(15):

            x_pos = (WIDTH) - ((self.gx - WIDTH/2) %32) - WIDTH
            for i in range(23): 
                if not self.gidx >= len(self.grid):
                    costume = self.grid[self.gidx]
                    self.tile_costume = self.tiles[costume]
                surf.blit(self.tile_costume, (x_pos, y_pos))      
                x_pos += 64
                self.gidx += 1

            self.gidx += self.Gmax - 23
            y_pos -= 64

    def paint_player(self, surf): 
        self.base_costume = (math.floor(self.base_costume) + (math.floor(self.frame)))%5
        surf.blit(self.costume, ((self.player_x - self.camera_x + WIDTH/2,(self.player_y - 10) - self.camera_y + HEIGHT/2)))
    
    def player_controls(self): 
        if "RIGHT" in self.key_buttons:
            self.joy_x = 1

        if "LEFT" in self.key_buttons:
            self.joy_x = -1

        if "DOWN" in self.key_buttons:
            self.joy_y = 1

        if "UP" in self.key_buttons:
            self.joy_y = -1

        if not "RIGHT" in self.key_buttons and not "LEFT" in self.key_buttons:
            self.joy_x = 0

        if not "UP" in self.key_buttons and not "DOWN" in self.key_buttons:
            self.joy_y = 0
        
        self.joy_dist = math.sqrt((self.joy_x*self.joy_x) + (self.joy_y * self.joy_y))

    def try_move(self, dx, dy): 
        self.player_x += dx 
        self.player_y += dy

    def player_movement(self): 
        if self.joy_dist > 1:
            self.joy_dist = 1.25
        self.joy_x = self.joy_x/self.joy_dist
        self.joy_y = self.joy_y/self.joy_dist
        self.try_move(self.joy_x*15, self.joy_y*15) 
        if self.joy_x < 0: 
            self.player_dir = -90 

        elif self.joy_x > 0: 
            self.player_dir = 90 

        elif self.joy_y < 0: 
            self.player_dir = 180 

        else: 
            self.player_dir = 0
        
        if self.player_dir == -90: 
            self.costume = self.walk_left[self.base_costume]

        if self.player_dir == 90: 
            self.costume = self.walk_right[self.base_costume]

        if self.player_dir == 180: 
            self.costume = self.walk_up[self.base_costume]

        if self.player_dir == 0: 
            self.costume = self.walk_down[self.base_costume]

        self.frame += 0.25

    def tick_player(self):
        self.player_controls() 
        if self.joy_dist > 0: 
            self.player_movement()
        else: 

            if self.player_dir == 0: 
                self.costume = self.walk_down[self.base_costume]
                
            if self.player_dir == -90: 
                self.base_costume = 2

            if self.player_dir == 90: 
                self.base_costume = 1

            if self.player_dir == 180: 
                self.base_costume = 0
        
            if self.player_dir == 0: 
                self.base_costume = 3
                self.frame = 0
                
            self.costume = self.idle[self.base_costume]

        self.camera_x = self.player_x
        self.camera_y = self.player_y
        if self.camera_x < WIDTH/2 :
            self.camera_x = WIDTH/2 
        if self.camera_y > HEIGHT/2 + 40: 
            self.camera_y = HEIGHT/2 + 40
        if self.camera_x > (self.Gmax * 32) + 10: 
            self.camera_x = self.Gmax * 32 + 10
        if self.camera_y < 0 - ((self.Gmax * 32) - 750): 
            self.camera_y = 0 - ((self.Gmax * 32) - 750)

    def keyboard(self): 
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.KEYDOWN:#Track down key presses here

                if event.key==pygame.K_DOWN:
                    self.key_buttons.append('DOWN')

                if event.key==pygame.K_RIGHT:
                    self.key_buttons.append('RIGHT')

                if event.key==pygame.K_UP:
                    self.key_buttons.append('UP')        

                if event.key==pygame.K_LEFT:
                    self.key_buttons.append('LEFT')
                
            elif event.type== pygame.KEYUP:#Track down key releases here

                if event.key == pygame.K_DOWN:
                    self.key_buttons.remove('DOWN')

                if event.key == pygame.K_UP:
                    self.key_buttons.remove('UP')

                if event.key==pygame.K_RIGHT:
                    self.key_buttons.remove('RIGHT')
        
                if event.key==pygame.K_LEFT:
                    self.key_buttons.remove('LEFT')
                
    def add_to_grid(self, count, tile):
        for i in range(count):
            if tile == 62:
                if random.randint(1, 10) == 1: 
                    self.grid.append(121)
                else: 
                    self.grid.append(tile)
            else: 
                self.grid.append(tile)

    def map(self): 
        if not os.path.isfile("grid"):
            self.add_to_grid(self.Gmax, 121)
            for i in range(self.Gmax-2):
                self.grid.append(121)
                self.add_to_grid(self.Gmax-2, 62)
                self.grid.append(121)

            self.add_to_grid(self.Gmax, 121)

            pickle.dump(self.grid, open("grid", "wb"))

        
Game = game(image_list)
Game.map()
while Game.running:
    # keep the loop runing at the right speed
    clock.tick(FPS)
    
    # events
    Game.keyboard()
    # update
    Game.background(screen)
    Game.paint_tiles(screen)
    Game.tick_player()
    # draw
    Game.paint_player(screen)

    # Double Buffering. After drawing everything flip the display
    pygame.display.flip()
    
pygame.quit()
sys.exit()
