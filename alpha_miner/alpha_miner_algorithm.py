import pygame as pg
from pygame.locals import *

from pm4py.objects.log.importer.xes import factory as xes_import_factory

import sys
import os

from load import make_text, load_image
from button import Button
from file_path import get_file_path


class Alpha_Miner_Algorithm():
    """Alpha Miner Algorithm"""
    def __init__(self, window, path):
        """Alpha Miner Algorithm - constructor"""

        self.window = window
        self.window_rect = self.window.get_rect() 
        self.path = path

        #Create background surface
        self.bg = pg.Surface( self.window.get_size() ).convert()
        self.bg.fill( (0, 0, 0) )
        self.bg_rect = self.bg.get_rect( topleft = (0,0) )

        #Create menu images
        img_folder = "alg_buttons"
        self.buttons = {
                "left" : [None, False, (self.window_rect.width * 4.5/10, self.window_rect.height *11/12)],
                "right" : [None, False, (self.window_rect.width * 5.5/10, self.window_rect.height* 11/12)],
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
        self.text, self.text_rect = make_text( text= "Alpha miner algorithm", font_name= 'calibri-font-sv\Calibri Bold.ttf'\
                                                    , size= 35, pos= (self.bg_rect.centerx, 40)\
                                                    , text_color= (72, 144, 220), text_background_color= (0, 0, 0))
        self.bg.blit( self.text, self.text_rect )#Blit text on background

        self.initialized = -1
        self.current_phase = 0

        self.phase_range = (0, 4)
        #Initialize clock
        self.clock = pg.time.Clock()

        self.click_down = False
        self.click_up = False

    def initialization(self):
        if self.current_phase == 0:
            self.text0, self.text_rect0 = make_text( text= "0", font_name= 'calibri-font-sv\Calibri Bold.ttf'\
                                                    , size= 35, pos= (self.window_rect.centerx,self.window_rect.centery)\
                                                    , text_color= (72, 144, 220), text_background_color= (0, 0, 0))
        
            self.initialized = 0
        elif self.current_phase == 1:
            self.text1, self.text_rect1 = make_text( text= "1", font_name= 'calibri-font-sv\Calibri Bold.ttf'\
                                                    , size= 35, pos= (self.window_rect.centerx,self.window_rect.centery)\
                                                    , text_color= (72, 144, 220), text_background_color= (0, 0, 0))
        
        elif self.current_phase == 2:
            self.text2, self.text_rect2 = make_text( text= "2", font_name= 'calibri-font-sv\Calibri Bold.ttf'\
                                                    , size= 35, pos= (self.window_rect.centerx,self.window_rect.centery)\
                                                    , text_color= (72, 144, 220), text_background_color= (0, 0, 0))
        
         
        elif self.current_phase == 3:
            self.text3, self.text_rect3 = make_text( text= "3", font_name= 'calibri-font-sv\Calibri Bold.ttf'\
                                                    , size= 35, pos= (self.window_rect.centerx,self.window_rect.centery)\
                                                    , text_color= (72, 144, 220), text_background_color= (0, 0, 0))
        
         
        elif self.current_phase == 4:
            self.text4, self.text_rect4 = make_text( text= "4", font_name= 'calibri-font-sv\Calibri Bold.ttf'\
                                                    , size= 35, pos= (self.window_rect.centerx,self.window_rect.centery)\
                                                    , text_color= (72, 144, 220), text_background_color= (0, 0, 0))
        
         
            self.initialized = 1
    
    def display(self, ):
        if self.current_phase == 0:
            self.window.blit( self.text0, self.text_rect0 )
        elif self.current_phase == 1:
            self.window.blit( self.text1, self.text_rect1 )
        elif self.current_phase == 2:
            self.window.blit( self.text2, self.text_rect2 )
        elif self.current_phase == 3:
            self.window.blit( self.text3, self.text_rect3 )
        elif self.current_phase == 4:
            self.window.blit( self.text4, self.text_rect4 )

    def run(self):
        """Main loop"""

        while not self.handle_events():
            mx, my = pg.mouse.get_pos()

            if self.current_phase > self.initialized:
                self.initialization()

            self.window.blit( self.bg, self.bg_rect )

            self.allsprites.update()
            self.allsprites.draw( self.window )
            
            self.display()

            #button images support
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

            #button reaction support
            for i, button_name in enumerate( self.buttons ):
                if self.buttons[button_name][1] == True:
                    if button_name == "right":
                        if self.current_phase < self.phase_range[1]:
                            self.current_phase += 1
                    if button_name == "left":
                        if self.current_phase > self.phase_range[0]:
                            self.current_phase -= 1
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