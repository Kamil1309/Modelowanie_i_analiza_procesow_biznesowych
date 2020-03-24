import pygame as pg
from pygame.locals import *

# from pm4py.objects.log.importer.xes import factory as xes_import_factory

# import sys
# import os

from load import make_text, load_image

class BPMN():
    def __init__(self, activities):
        """
        :param activities: table [[],[]] first table are real names of activities, second are new names
        """
        self._board = [[[]]]
        self._connections = { "from" : [],
                              "to" : []}
        self.start_bpmn, self.start_bpmn_rect = load_image("start.png")
        self.end_bpmn, self.end_bpmn_rect = load_image("end.png")
        self.exclusive_bpmn, self.exclusive_bpmn_rect = load_image("exclusive.png")
        self.parallel_bpmn, self.parallel_bpmn_rect = load_image("parallel.png")
        self.arrow_right, self.arrow_right_rect = load_image("arrow_right.png")

        self.activities_surfaces = [[],[]]
        self.activities_surfaces[0] = activities[1][:]

        for name in activities[0]:
            activities_surfaces[1].append([])
            a_s, a_s_rect = create_activity_surf( name )
            activities_surfaces[1][ len(activities_surfaces[1])-1 ].append( a_s )
            activities_surfaces[1][ len(activities_surfaces[1])-1 ].append( a_s_rect )

    @property
    def height(self):
        return len(self._board)

    @property
    def width(self):
        return len(self._board[0])

    def add_row(self):
        self._board.append( [ [] for i in range(0, self.width ) ] )

    def add_column(self):
        for i in range(0, self.height):
            self._board[i].append([])
    
    def ele_pos(self, surf, pos_board):
        """returns possition on surface of element of given position in board
        
        :param surface: surface on which the BPMN model will be drawn, size is important
        :param pos_board: position of the element on the board whose position on the surface is to be returned, given as two integers [ column, row ]
        :return pos: pos in pixels of element given with pos
        """
        pos = [surf.get_width() * (pos_board[1] + 0.5)/self.width, surf.get_height() * (pos_board[0] + 0.5)/self.height]

        return pos

    def draw_line(self, surf, start_pos, end_pos, arrow = False, size = 3 ):
        if arrow:
            pg.draw.line( surf, (72, 144, 220), start_pos, end_pos, size )
            self.arrow_right_rect.right = end_pos[0]
            self.arrow_right_rect.top = end_pos[1] - self.arrow_right_rect.height/2 + 1
            surf.blit( self.arrow_right, self.arrow_right_rect )
        else:
            pg.draw.line(surf, (72, 144, 220), start_pos, end_pos, size)

    def draw_on(self, surf):
        """drawing BPMN model on given surface
        
        :param surface: surface on which the BPMN model will be drawn"""
        #bliting connections
        for i in range(0, len(self._connections["from"]) ):
            if self.BPMN_connections["from"][i][1] != -1:# if it is connection from no where into start event
                start_pos = self.ele_pos( surf, [ self._connections["from"][i][1], 0 ])
            else:
                start_pos = self.ele_pos( surf, self._connections["from"][i] )
                
            if self.BPMN_connections[1][i][1] != 1000:
                end_pos = self.ele_pos( surf, [ self._connections["to"][i][1], self.width - 1 ])
            else:
                end_pos = self.ele_pos( surf, self._connections["to"][i] )

            self.draw_line( surf, start_pos, end_pos, True )

        #bliting activities, events ....
        for c in range(0, len(self._board)):
            for r in range(0, len(self._board[c])):
                if len(self.BPMN[c][r]) == 2:#If there is surface on possition
                    self.BPMN[classmethod][r][1].center = ele_pos(surf, [c, r])
                    self.bg3.blit( self.BPMN[c][r][0], self.BPMN[c][r][1] )