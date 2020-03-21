import pygame as pg
import os

from load import load_image

class Button(pg.sprite.Sprite):
    """
    Class for all buttons. Inherits from sprite class
    """
    def __init__(self, *, folder_name, img_name, pos = ( 0, 0 ) ):
        """
        Button constructor. The button must have graphics in both positions, up and down.

        :param folder_name: name of folder where button image is stored
        :param img_name: name of image
        """

        pg.sprite.Sprite.__init__(self) #call Sprite initializer

        self.img_dir = os.path.join(folder_name, img_name )
        self.image_down = load_image( self.img_dir + "_down.png" )[0]
        self.image_up = load_image( self.img_dir + "_up.png" )[0]

        self.image = self.image_up
        self.rect = self.image.get_rect( center = pos )

        self.pushed = 0

    def update( self ):
        "update button image"
        if self.pushed == 0:
            self.image = self.image_up
        elif self.pushed == 1:
            self.image = self.image_down

    def push( self ):
        self.pushed = 1

    def release( self ):
        self.pushed = 0


