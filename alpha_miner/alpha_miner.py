import pygame as pg
from pygame.locals import *

import sys
import os

from load import make_text, load_image
from button import Button
from file_path import get_file_path
from alpha_miner_algorithm import Alpha_Miner_Algorithm


class Alpha_Miner():
    """Alpha Miner"""
    def __init__(self):
        """Alpha Miner - constructor"""
        pg.init()

        #Create display window
        infoObject = pg.display.Info() # Gets information about the screen
        if infoObject.current_w > 1366 + 150 and infoObject.current_h > 768 + 150:
            os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % ( 150, 150 ) # The initial position of the window on the screen
        else:
            os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % ( 0, 0 ) # The initial position of the window on the screen
        self.window = pg.display.set_mode(( 1366, 768 )) # Creating a game window
        self.window_rect = self.window.get_rect()
        pg.display.set_caption("Alpha miner") # Name of the game window

        #Create background surface
        self.bg = pg.Surface( self.window.get_size() ).convert()
        self.bg.fill( (0, 0, 0) )
        self.bg_rect = self.bg.get_rect( topleft = (0,0) )

        #Create menu images
        img_folder = "main_buttons"
        self.buttons = {
                "choose_XES" : [None, False, (self.window_rect.width * 10/12, self.window_rect.height/5)],
                "start_am" : [None, False, (self.window_rect.width * 1/2, self.window_rect.height* 5/6)],
                "exit" : [None, False, (self.window_rect.width * 1/12, self.window_rect.height* 12/13)],
                }
            #Buttons possition
        
        #creating buttons
        all_buttons = []

        for i, button_name in enumerate( self.buttons ):
            self.buttons[button_name][0] = ( Button(folder_name = img_folder, \
                                            img_name = button_name, pos = self.buttons[button_name][2] ) )
            all_buttons.append ( self.buttons[button_name][0] )

        self.allsprites = pg.sprite.RenderPlain( all_buttons )

        #Create main menu text
        self.text, self.text_rect = make_text( text= "Alpha miner presentation", font_name= 'calibri-font-sv\Calibri Bold.ttf'\
                                                    , size= 35, pos= (self.bg_rect.centerx, 40)\
                                                    , text_color= (72, 144, 220), text_background_color= (0, 0, 0))
        self.bg.blit( self.text, self.text_rect )#Blit text on background

        self.bg_XES, self.bg_XES_rect = load_image("bg_XES.png", (self.window_rect.width* 4/10, self.window_rect.height/5) )

        self.XES_text, self.XES_text_rect = make_text( text= "PATH:", font_name= 'calibri-font-sv\Calibri Bold.ttf'\
                                                    , size= 35, pos= (self.window_rect.width* 1/13, self.bg_XES_rect.centery)\
                                                    , text_color= (72, 144, 220), text_background_color= (0, 0, 0))

        self.path = "" # path to XLS file
        self.XES_path, self.XES_path_rect = make_text( text= self.path, font_name= 'calibri-font-sv\Calibri Bold.ttf'\
                                                    , size= 35, pos= (self.bg_XES_rect.centerx, self.bg_XES_rect.centery)\
                                                    , text_color= (72, 144, 220), text_background_color= (0, 0, 0))

        self.bg.blit( self.bg_XES, self.bg_XES_rect ) #Blit text on background
        self.bg.blit( self.XES_text, self.XES_text_rect ) #Blit text on background
        self.double_path = False
        self.w_path = False

        self.wrong_path, self.wrong_path_rect = make_text( text= "it's not XLS path :(", font_name= 'calibri-font-sv\Calibri Bold.ttf'\
                                                        , size= 45, pos= (self.window_rect.width* 4/10, self.window_rect.height/5)\
                                                        , text_color= (242, 0, 0), text_background_color= (21,215,152))
        #Initialize clock
        self.clock = pg.time.Clock()

        self.click_down = False
        self.click_up = False

    def run(self):
        """Main loop"""

        while not self.handle_events():
            mx, my = pg.mouse.get_pos()

            self.window.blit( self.bg, self.bg_rect )

            self.allsprites.update()
            self.allsprites.draw( self.window )

            for i, button_name in enumerate( self.buttons ):
                if self.buttons[button_name][0].rect.collidepoint( ( mx, my ) ):
                    if self.click_down == True:
                        self.buttons[button_name][0].push()
                    elif self.click_up == True:
                        self.buttons[button_name][1] = True #option was choosed
                    else:
                        self.buttons[button_name][0].release()
                else:
                    self.buttons[button_name][0].release()

            for i, button_name in enumerate( self.buttons ):
                if self.buttons[button_name][1] == True:
                    if button_name == "choose_XES":
                        self.path = get_file_path()
                        if len(self.path) > 3:
                            if (self.path[-3:-1]+self.path[-1]) == "xes":
                                self.w_path = False
                                self.double_path = False
                                self.XES_path, self.XES_path_rect = make_text( text= self.path, font_name= 'calibri-font-sv\Calibri Bold.ttf'\
                                                            , size= 35, pos= (self.window_rect.width* 4/10, self.window_rect.height/5)\
                                                            , text_color= (72, 144, 220), text_background_color= (21,215,152))
                                if self.XES_path_rect.width > 600:
                                    self.double_path = True
                                    for i in range(round(len(self.path)*1/5), len(self.path) ):
                                        if self.path[i] == '/':
                                            first_half = self.path[0:i]
                                            second_half = self.path[i:len(self.path)]
                                            break
                                    self.XES_path1, self.XES_path1_rect = make_text( text= first_half, font_name= 'calibri-font-sv\Calibri Bold.ttf'\
                                                            , size= 16, pos= (self.window_rect.width* 4/10, self.window_rect.height/5-10)\
                                                            , text_color= (72, 144, 220), text_background_color= (21,215,152))
                                    self.XES_path2, self.XES_path2_rect = make_text( text= second_half, font_name= 'calibri-font-sv\Calibri Bold.ttf'\
                                                            , size= 16, pos= (self.window_rect.width* 4/10, self.window_rect.height/5+10)\
                                                            , text_color= (72, 144, 220), text_background_color= (21,215,152))
                            else:
                                self.w_path = True
                                self.path = ""
                        else:
                            self.w_path = True
                            self.path = ""
                    if button_name == "start_am":
                        alpha_miner_algorithm = Alpha_Miner_Algorithm(self.window)
                        alpha_miner_algorithm.run()
                        del alpha_miner_algorithm
                    if button_name == "exit":
                        return True
                    self.buttons[button_name][1] = False


            if self.w_path == False:
                if self.double_path:
                    self.window.blit( self.XES_path1, self.XES_path1_rect )#Blit "XES path" text on background
                    self.window.blit( self.XES_path2, self.XES_path2_rect )#Blit "XES path" text on background
                else:
                    self.window.blit( self.XES_path, self.XES_path_rect )#Blit "XES path" text on background
            else:
                self.window.blit( self.wrong_path, self.wrong_path_rect )#Blit "XES path" text on background

            pg.display.flip()

            self.clock.tick(60)
        pg.quit()
        sys.exit() 

    def handle_events(self):
        """
        Handling system events

        :return True if pg reported a quit event
        """
        self.click_up = False
        for event in pg.event.get():
            if event.type == pg.locals.QUIT:
                return True
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                return True
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.click_down = True
            elif event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    self.click_up = True
                    self.click_down = False