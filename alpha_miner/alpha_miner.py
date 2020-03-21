import pygame as pg
from pygame.locals import *

import sys
import os

from load import make_text
import button


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
        pg.display.set_caption("Alpha miner") # Name of the game window

        #Create background surface
        self.bg = pg.Surface( self.window.get_size() ).convert()
        self.bg.fill( (0, 0, 0) )
        self.bg_rect = self.bg.get_rect( topleft = (0,0) )

        #Create main menu text
        self.text, self.text_rect = make_text( text= "Alpha miner presentation", font_name= 'calibri-font-sv\Calibri Bold.ttf'\
                                                    , size= 25, pos= (self.bg_rect.centerx, 40)\
                                                    , text_color= (255, 255, 255), text_background_color= (0, 0, 0))

        self.clock = pg.time.Clock()
    
    def run(self):
        """Main loop"""

        while not self.handle_events():

            self.window.blit( self.bg, self.bg_rect )
            self.window.blit( self.text, self.text_rect )

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