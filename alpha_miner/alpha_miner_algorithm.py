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
        # self.bg = pg.Surface( self.window.get_size() ).convert()
        # self.bg.fill( (0, 0, 0) )
        # self.bg_rect = self.bg.get_rect( topleft = (0,0) )

        #Create menu images
        img_folder = "alg_buttons"
        self.buttons = {
                "left" : [None, False, (self.window_rect.width * 4.5/10, self.window_rect.height *11/12)],
                "right" : [None, False, (self.window_rect.width * 5.5/10, self.window_rect.height* 11/12)],
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
        self.text, self.text_rect = make_text( text= "Alpha miner algorithm", font_name= 'calibri-font-sv\Calibri Bold.ttf'\
                                                    , size= 35, pos= (self.window_rect.centerx, 40)\
                                                    , text_color= (72, 144, 220), text_background_color= (0, 0, 0))
        #self.bg.blit( self.text, self.text_rect )#Blit text on background

        self.initialized = -1
        self.current_phase = 0

        self.phase_range = (0, 4)
        #Initialize clock
        self.clock = pg.time.Clock()

        self.click_down = False
        self.click_up = False

    def initialization(self):
        if self.current_phase == 0:
            log = xes_import_factory.apply(self.path)
            self.L = []
            self.diff_names = [[],[]]
            for trace_num, trace in enumerate(log):
                self.L.append([])
                for event_num, event in enumerate(trace):
                    self.L[trace_num].append(event["concept:name"])
                    if event["concept:name"] not in self.diff_names[0]:
                        self.diff_names[0].append(event["concept:name"])
                        self.diff_names[1].append(str(chr(97 + len(self.diff_names[0])-1 )))

            for name_num in range(0, len(self.diff_names[0])):
                org_name, org_name_rect = make_text( text= self.diff_names[0][name_num], font_name= 'calibri-font-sv\Calibri Bold.ttf'\
                                                        , size= 25, pos= (self.window_rect.width*3/8, self.window_rect.height*(6+name_num)/25)\
                                                        , text_color= (72, 144, 220), text_background_color= (0, 0, 0))
                new_name, new_name_rect = make_text( text= self.diff_names[1][name_num], font_name= 'calibri-font-sv\Calibri Bold.ttf'\
                                                        , size= 25, pos= (self.window_rect.width*6/8, self.window_rect.height*(6+name_num)/25)\
                                                        , text_color= (72, 144, 220), text_background_color= (0, 0, 0))
                self.diff_names[0][name_num] = [org_name, org_name_rect]
                self.diff_names[1][name_num] = [new_name, new_name_rect]

            org_name_text, org_name_text_rect = make_text( text= "Original name", font_name= 'calibri-font-sv\Calibri Bold.ttf'\
                                                        , size= 25, pos= (self.window_rect.width*3/8, self.window_rect.height*4/25)\
                                                        , text_color= (255, 180, 69), text_background_color= (0, 0, 0))
            new_name_text, new_name_text_rect = make_text( text= "New name", font_name= 'calibri-font-sv\Calibri Bold.ttf'\
                                                        , size= 25, pos= (self.window_rect.width*6/8, self.window_rect.height*4/25)\
                                                        , text_color= (255, 180, 69), text_background_color= (0, 0, 0))
            #Create picture
            self.bg0 = pg.Surface( self.window.get_size() ).convert()
            self.bg0.fill( (0, 0, 0) )
            self.bg0_rect = self.bg0.get_rect( topleft = (0,0) )

            pg.draw.line(self.bg0, (255,134,69), (self.window_rect.width*5/8, self.window_rect.height*5/25),\
                        (self.window_rect.width*5/8, self.window_rect.height*(6 + len(self.diff_names[0]))/25),2)

            self.bg0.blit( self.text, self.text_rect )
            self.bg0.blit( org_name_text, org_name_text_rect )
            self.bg0.blit( new_name_text, new_name_text_rect )
            for i in range(0, len(self.diff_names[0])):
                self.bg0.blit( self.diff_names[0][i][0], self.diff_names[0][i][1] )
                self.bg0.blit( self.diff_names[1][i][0], self.diff_names[1][i][1] )
                pg.draw.line(self.bg0, (255,199,115), (self.window_rect.width*2/8, self.window_rect.height*(13+2*i)/50),\
                        (self.window_rect.width*7/8, self.window_rect.height*(13+2*i)/50 ),1)
            self.initialized = 0

        elif self.current_phase == 1:
            self.L
            new_name_text, new_name_text_rect = make_text( text= "New name", font_name= 'calibri-font-sv\Calibri Bold.ttf'\
                                                        , size= 25, pos= (self.window_rect.width*6/8, self.window_rect.height*4/25)\
                                                        , text_color= (255, 180, 69), text_background_color= (0, 0, 0))
            
            #Create picture
            self.bg1 = pg.Surface( self.window.get_size() ).convert()
            self.bg1.fill( (0, 0, 0) )
            self.bg1_rect = self.bg1.get_rect( topleft = (0,0) )

            self.text1, self.text_rect1 = make_text( text= "1", font_name= 'calibri-font-sv\Calibri Bold.ttf'\
                                                    , size= 35, pos= (self.window_rect.centerx,self.window_rect.centery)\
                                                    , text_color= (72, 144, 220), text_background_color= (0, 0, 0))

            self.bg1.blit( self.text1, self.text_rect1 )
        elif self.current_phase == 2:
            #Create picture
            self.bg2 = pg.Surface( self.window.get_size() ).convert()
            self.bg2.fill( (0, 0, 0) )
            self.bg2_rect = self.bg2.get_rect( topleft = (0,0) )

            self.text2, self.text_rect2 = make_text( text= "2", font_name= 'calibri-font-sv\Calibri Bold.ttf'\
                                                    , size= 35, pos= (self.window_rect.centerx,self.window_rect.centery)\
                                                    , text_color= (72, 144, 220), text_background_color= (0, 0, 0))
        
            self.bg2.blit( self.text2, self.text_rect2 )
        elif self.current_phase == 3:
            #Create picture
            self.bg3 = pg.Surface( self.window.get_size() ).convert()
            self.bg3.fill( (0, 0, 0) )
            self.bg3_rect = self.bg3.get_rect( topleft = (0,0) )

            self.text3, self.text_rect3 = make_text( text= "3", font_name= 'calibri-font-sv\Calibri Bold.ttf'\
                                                    , size= 35, pos= (self.window_rect.centerx,self.window_rect.centery)\
                                                    , text_color= (72, 144, 220), text_background_color= (0, 0, 0))
        
            self.bg3.blit( self.text3, self.text_rect3 )
        elif self.current_phase == 4:
            #Create picture
            self.bg4 = pg.Surface( self.window.get_size() ).convert()
            self.bg4.fill( (0, 0, 0) )
            self.bg4_rect = self.bg4.get_rect( topleft = (0,0) )

            self.text4, self.text_rect4 = make_text( text= "4", font_name= 'calibri-font-sv\Calibri Bold.ttf'\
                                                    , size= 35, pos= (self.window_rect.centerx,self.window_rect.centery)\
                                                    , text_color= (72, 144, 220), text_background_color= (0, 0, 0))
            self.bg4.blit( self.text4, self.text_rect4 )

            self.initialized = 1
    
    def display(self, ):
        if self.current_phase == 0:
            self.window.blit( self.bg0, self.bg0_rect )

        elif self.current_phase == 1:
            self.window.blit( self.bg1, self.bg1_rect )
        elif self.current_phase == 2:
            self.window.blit( self.bg2, self.bg2_rect )
        elif self.current_phase == 3:
            self.window.blit( self.bg3, self.bg3_rect )
        elif self.current_phase == 4:
            self.window.blit( self.bg4, self.bg4_rect )

    def run(self):
        """Main loop"""

        while not self.handle_events():
            mx, my = pg.mouse.get_pos()

            if self.current_phase > self.initialized:
                self.initialization()

            self.display()

            self.allsprites.update()
            self.allsprites.draw( self.window )

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
                    if button_name == "exit":
                        return True
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