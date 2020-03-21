import pygame as pg
from pygame.locals import *

import sys
import os

from load import make_text, load_image
from button import Button
from file_path import get_file_path


class Alpha_Miner_Algorithm():
    """Alpha Miner"""
    def __init__(self, window):
        """Alpha Miner - constructor"""
        pg.init()

        self.window = window

        #Create background surface
        self.bg = pg.Surface( self.window.get_size() ).convert()
        self.bg.fill( (0, 0, 0) )
        self.bg_rect = self.bg.get_rect( topleft = (0,0) )

        #Create menu images
        img_folder = "main_buttons"
        self.buttons = {
                
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
                    

                    self.buttons[button_name][1] = False


            

            pg.display.flip()

            self.clock.tick(60)

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