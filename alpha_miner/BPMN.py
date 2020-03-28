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
        self._board = [[None]]
        self._connections = { "from" : [],
                              "to" : []}
        self.start_bpmn, self.start_bpmn_rect = load_image("start.png")
        self.end_bpmn, self.end_bpmn_rect = load_image("end.png")
        self.exclusive_bpmn, self.exclusive_bpmn_rect = load_image("exclusive.png")
        self.parallel_bpmn, self.parallel_bpmn_rect = load_image("parallel.png")
        self.arrow_right, self.arrow_right_rect = load_image("arrow_right.png")

        self.already_on = []

        self.activities_surfaces = [[],[]] # table where first row are names of activities e.g ["a", "b"], and second row are surfaces and surfaces_rects of this activities e.g [ [a_surf, a_surf_rect], [b_surf, b_surf_rect]]
        self.activities_surfaces[0] = activities[1][:]

        for name in activities[0]:
            self.activities_surfaces[1].append([])
            a_s, a_s_rect = self.create_activity_surf( name )
            self.activities_surfaces[1][ len(self.activities_surfaces [1])-1 ].append( a_s )
            self.activities_surfaces[1][ len(self.activities_surfaces [1])-1 ].append( a_s_rect )

    @property
    def height(self):
        return len(self._board)

    @property
    def width(self):
        return len(self._board[0])

    def run(self, TI, TO, YLa, YLb, YLc):
        #create start
        if len( TI ) == 2: 
            self.add_elem_on_board( "start", [0,0])
            self.add_column()
            self.add_elem_on_board( "exclusive", [0,1])
            self.add_connection([0,0], [0,1])

            self.add_column()
            self.add_row()

            self.add_elem_on_board( TI[0], [0,2])
            self.add_connection([0,1], [0,2])

            self.add_elem_on_board( TI[1], [1,2])
            self.add_connection([0,1], [1,2])
        elif len( TI ) == 1: 
            self.add_elem_on_board( "start", [0,0])
            self.add_column()

            self.add_elem_on_board( TI[0], [0,1])
            self.add_connection([0,0], [0,1])
        else:
            print( "BPMN model isnt ready for more then 2 start activities" )
        
        #create end
        start_width = self.width
        start_height = self.height

        self.add_column()
        for to_elem in TO:
            if to_elem in TI: 
                if self.get_activity( [ TI.index(to_elem), 2 ] ) == None: # If place that we want put elem into is empty
                    self.add_elem_on_board( "end", [ TI.index(to_elem), 2 ])
                else:# If not we have to find free place to move element
                    for row_num in range( 0, self.height ):# go through whole column
                        if self.get_activity( [row_num, start_width] ) == None: # if we find empty place we move element there
                            found = True
                            move_elem( [ TI.index(to_elem), 2 ], [row_num, start_width] )
                            self.add_elem_on_board( "end", [ TI.index(to_elem), 2 ])
                        if found == False:#otherwise we have to add new row and then move elem
                            self.add_row()
                            move_elem([ TI.index(to_elem), 2 ], [self.height - 1, start_width])
                            self.add_elem_on_board( "end", [ TI.index(to_elem), 2 ])
            else:
                if self.width == start_width + 1:
                    self.add_column()
                found = False
                for row_num in range( 0, self.height ):
                    if self.get_activity( [row_num, start_width] ) == None:
                        found = True
                        self.add_elem_on_board( to_elem, [ row_num, start_width ])
                        self.add_elem_on_board( "end", [ row_num, start_width + 1 ])
                        self.add_connection(  [ row_num, start_width ], [ row_num, start_width + 1 ] )
                        break
                    if found == False:
                        self.add_row()
                        self.add_elem_on_board( to_elem, [ self.height - 1, start_width ])
                        self.add_elem_on_board( "end", [ self.height - 1, start_width + 1 ])
                        self.add_connection(  [ self.height - 1, start_width ], [ self.height - 1, start_width + 1 ] )
                        break
        #create pattern a

        #checking how many fields separate the beginning and the end 
        move_about = 0
        for pat_num in range(0, len(YLa[0])):
            if YLa[0][pat_num] in TI and YLa[1][pat_num] in TO:
                pass
            elif (YLa[0][pat_num] not in TI and YLa[1][pat_num] in TO) or (YLa[0][pat_num] in TI and YLa[1][pat_num] not in TO):
                move_about = 1
            else:
                move_about = 2
                break
        #adding columns
        self.add_column(move_about)
        #moving all elements from "move_about" number of columns to the right
        for i in range(0, 2):
            for row_num in range(0, self.height):
                self.move_elem( [row_num, self.width - 1 - i - move_about] , [row_num, self.width - 1 - i])

        #putting pattern a on board
        for pat_num in range(0, len(YLa[0])):
            if YLa[0][pat_num] in TI and YLa[1][pat_num] in TO:# if start activity and end activity is in pattern a
                self.add_connection( find_in_board(YLa[0][pat_num]), find_in_board(YLa[1][pat_num]) )

            elif YLa[0][pat_num] in TI:# if start activity is in pattern a
                coord = self.find_in_board( YLa[0][pat_num] )
                if YLa[1][pat_num] not in self.already_on:
                    if self._board[ coord[0]][ coord[1] + 1] == None:
                        self.add_elem_on_board( YLa[1][pat_num], [coord[0], coord[1] + 1] )
                        self.add_connection( coord, [coord[0], coord[0] + 1] )
                    else:
                        for row_num in range(0, self.height): 
                            if self._board[row_num][coord[1] + 1] == None:
                                found = True
                                self.add_elem_on_board( YLa[1][pat_num], [row_num, coord[1] + 1] )
                                self.add_connection( coord, [row_num, coord[0] + 1] )
                                break
                        if found == False:
                            self.add_row()
                            self.add_elem_on_board( YLa[1][pat_num], [self.height - 1, coord[1] + 1] )
                            self.add_connection( coord, [self.height - 1, coord[0] + 1] )
                else:#if element is already on board
                    self.add_connection( coord, self.find_in_board( YLa[1][pat_num]  ) )
                #Co jezeli wielokrotnie sie tu pokaze cos
                
            elif YLa[1][pat_num] in TO:# if end activity is in pattern a
                coord = self.find_in_board( YLa[1][pat_num] )
                if YLa[0][pat_num] not in self.already_on:
                    self.add_elem_on_board( YLa[0][pat_num], [coord[0], coord[1] - 1] )
                    self.add_connection( [coord[0], coord[1] - 1], coord )
                else:
                    self.add_connection( self.find_in_board( YLa[0][pat_num]  ) , coord)

        for pat_num in range(0, len(YLa[0])):
            found = False
            if YLa[0][pat_num] not in TI and YLa[1][pat_num] not in TO:
                for row_num in range(0, self.height):
                    if self._board[row_num][start_width] == None and self._board[row_num][start_width + 1] == None:
                        found = True
                        if YLa[0][pat_num] not in self.already_on:
                            self.add_elem_on_board( YLa[0][pat_num], [row_num, start_width] )
                        if YLa[1][pat_num] not in self.already_on:
                            self.add_elem_on_board( YLa[1][pat_num], [row_num, start_width + 1] )
                        self.add_connection( self.find_in_board( YLa[0][pat_num]  ), self.find_in_board( YLa[1][pat_num]  ) )
                        break
                if found == False:
                    self.add_row()
                    if YLa[0][pat_num] not in self.already_on:
                        self.add_elem_on_board( YLa[0][pat_num], [self.height - 1, start_width] )
                    if YLa[1][pat_num] not in self.already_on:
                        self.add_elem_on_board( YLa[1][pat_num], [self.height - 1, start_width + 1] )
                    self.add_connection( self.find_in_board( YLa[0][pat_num]  ), self.find_in_board( YLa[1][pat_num]  ) )
        
        #create pattern b
        for pat_num in range(0, len(YLb[0])):
            if YLb[0][pat_num] not in self.already_on:
                pass
            else:#if YLb[0][pat_num] is already on board we just add exclusive
                coord = self.find_in_board( YLb[0][pat_num] )
                if self._board[ coord[0]][ coord[1] + 1 ] == None:
                    self.add_elem_on_board ( "exclusive", [ coord[0], coord[1] + 1 ] )
                    self.add_connection( [ coord[0], coord[1] ], [ coord[0], coord[1] + 1 ] )
                else:
                    self.add_column
                    for i in range(0, self.width - 2 - coord[1] ):
                        for row_num in range(0, self.height):
                            self.move_elem( [row_num, self.width - 1 - i - 1] , [row_num, self.width - 1 - i])
                    self.add_elem_on_board ( "exclusive", [ coord[0], coord[1] + 1 ] )
                    self.add_connection( [ coord[0], coord[1] ], [ coord[0], coord[1] + 1 ] )

    def add_elem_on_board(self, elem_name, pos):
        """
        put elem surface and elem surface_rect into board on pos
        :param elem: name of element that will be added on board e.g "a"
        :param pos: position on the board on which the element is to be placed e.g [0, 5], 0 - row, 5 - col
        """
        if (elem_name not in self.already_on) or (elem_name == "start" or elem_name == "end" or elem_name == "exclusive" or elem_name == "parallel"):
            if self.get_activity(pos) == None:
                self._board[ pos[0] ][ pos[1] ] = elem_name 
                self.already_on.append(elem_name)
            else:
                print("you wanted to place: ", elem_name, " on place: ", pos[0], pos[1], " but there is already some surf")
        else:
            print("you wanted to place ", elem_name, "but it's already on board")

    def move_elem(self, from_pos, where_pos):
        if self.get_activity(where_pos) == None:
            self._board[where_pos[0]][where_pos[1]] = self._board[from_pos[0]][from_pos[1]]
            self._board[from_pos[0]][from_pos[1]] = None
            for start_pos in self._connections["from"]:
                if from_pos == start_pos: 
                    self._connections["from"][ self._connections["from"].index(start_pos)] = where_pos
                
            for end_pos in self._connections["to"]:
                if from_pos == end_pos: 
                    self._connections["to"][ self._connections["to"].index(end_pos)] = where_pos

    def find_in_board(self, name):
        """can find position of activity on the board when you give its name"""
        for row_num in range(0, len(self._board)):
            for col_num in range(0, len(self._board[row_num])):
                if self._board[row_num][col_num] == name:
                    return [row_num, col_num]
           
    def ele_pos(self, surf, pos_board):
        """returns possition on surface of element of given position in board
        
        :param surface: surface on which the BPMN model will be drawn, size is important
        :param pos_board: position of the element on the board whose position on the surface is to be returned, given as two integers [ column, row ]
        :return pos: pos in pixels of element given with pos
        """
        pos = [surf.get_width() * (pos_board[1] + 0.5)/self.width, surf.get_height() * (pos_board[0] + 0.5)/self.height]

        return pos

    def get_activity(self, pos):
        """gives name of activiti on given position on board"""
        if self._board[pos[0]][pos[1]] != None:
            return self._board[pos[0]][pos[1]]
        else:
            return None

    def add_connection(self, start_pos, end_pos):
        self._connections["from"].append([])
        self._connections["to"].append([])
        self._connections["from"][len(self._connections["from"])-1].append( start_pos[0] )
        self._connections["from"][len(self._connections["from"])-1].append( start_pos[1] )
        self._connections["to"][len(self._connections["to"])-1].append( end_pos[0] )
        self._connections["to"][len(self._connections["to"])-1].append( end_pos[1] )

    def create_activity_surf(self, name ):
        # load corners
        top_left_corner, top_left_corner_rect = load_image("top_left_corner.png") 
        top_right_corner, top_right_corner_rect = load_image("top_right_corner.png")
        bottom_right_corner, bottom_right_corner_rect = load_image("bottom_right_corner.png")
        bottom_left_corner, bottom_left_corner_rect = load_image("bottom_left_corner.png")

        #create text
        text, text_rect = make_text( text= name, font_name= 'calibri-font-sv\Calibri Bold.ttf'\
                                    , size= 20, pos= (0,0)\
                                    , text_color= (255, 180, 69), text_background_color= (0, 0, 0))
        
        #create activity surface
        activity_surf = pg.Surface( (text_rect.width + 30, text_rect.height + 40) ).convert()
        activity_surf.fill( (0, 0, 0) )
        activity_surf_rect = activity_surf.get_rect( topleft = (0,0) )

        #set corners position
        top_left_corner_rect.topleft = (0, 0)
        top_right_corner_rect.topright = (activity_surf_rect.width, 0)
        bottom_right_corner_rect.bottomright = (activity_surf_rect.width, activity_surf_rect.height)
        bottom_left_corner_rect.bottomleft = (0, activity_surf_rect.height)
        #set text position
        text_rect.center = activity_surf_rect.center

        activity_surf.blit( top_left_corner, top_left_corner_rect )
        activity_surf.blit( top_right_corner, top_right_corner_rect )
        activity_surf.blit( bottom_right_corner, bottom_right_corner_rect )
        activity_surf.blit( bottom_left_corner, bottom_left_corner_rect )

        self.draw_line(activity_surf, (top_left_corner_rect.right, top_left_corner_rect.top + 2), ( top_right_corner_rect.left, top_right_corner_rect.top + 2), False, 5 )
        self.draw_line(activity_surf, (top_right_corner_rect.right - 3, top_right_corner_rect.bottom), ( bottom_right_corner_rect.right - 3, bottom_right_corner_rect.top), False, 5 )
        self.draw_line(activity_surf, (bottom_right_corner_rect.left, bottom_right_corner_rect.bottom - 3), ( bottom_left_corner_rect.right, bottom_left_corner_rect.bottom - 3), False, 5 )
        self.draw_line(activity_surf, (bottom_left_corner_rect.left + 2, bottom_left_corner_rect.top), ( top_left_corner_rect.left + 2, top_left_corner_rect.bottom), False, 5 )

        activity_surf.blit( text, text_rect )

        return activity_surf, activity_surf_rect
    
    def get_activity_surf(self, name):
        if name != None:
            if name == "start":
                elem_surf, elem_surf_rect = self.start_bpmn, self.start_bpmn_rect
            elif name == "end":
                elem_surf, elem_surf_rect = self.end_bpmn, self.end_bpmn_rect
            elif name == "exclusive":
                elem_surf, elem_surf_rect = self.exclusive_bpmn, self.exclusive_bpmn_rect
            elif name == "parallel":
                elem_surf, elem_surf_rect = self.parallel_bpmn, self.parallel_bpmn_rect
            else:
                index = self.activities_surfaces[0].index( name )
                elem_surf = self.activities_surfaces[1][index][0]
                elem_surf_rect = self.activities_surfaces[1][index][1]

            return elem_surf, elem_surf_rect
        return None

    def add_row(self, how_many = 1):
        for j in range(0, how_many):
            self._board.append( [ None for i in range(0, self.width ) ] )

    def add_column(self, how_many = 1):
        for j in range(0, how_many):
            for i in range(0, self.height):
                self._board[i].append( None )

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
        for connection_num in range(0, len(self._connections["from"]) ):
            start_pos = self.ele_pos( surf, self._connections["from"][connection_num] )
            start_surf, start_surf_rect = self.get_activity_surf(self.get_activity( self._connections["from"][connection_num] ))
            start_pos[0] += start_surf_rect.width/2

            end_pos = self.ele_pos( surf, self._connections["to"][connection_num] )
            end_surf, end_surf_rect = self.get_activity_surf( self.get_activity( self._connections["to"][connection_num] )) #connection must end before activity, not in middle
            end_pos[0] -= end_surf_rect.width/2

            self.draw_line( surf, start_pos, [ start_pos[0] + (end_pos[0] - start_pos[0])/2, start_pos[1] ] )
            self.draw_line( surf, [ start_pos[0] +  (end_pos[0] - start_pos[0])/2, start_pos[1] ], [ start_pos[0] + (end_pos[0] - start_pos[0])/2, end_pos[1] ] )
            self.draw_line( surf, [ start_pos[0] +  (end_pos[0] - start_pos[0])/2, end_pos[1] ], end_pos, True )

        #bliting activities, events ....
        for c in range(0, len(self._board)):
            for r in range(0, len(self._board[c])):
                if self._board[c][r] != None:#If there is name on possition
                    elem_surf, elem_surf_rect = self.get_activity_surf( self._board[c][r] )
                    elem_surf_rect.center = self.ele_pos(surf, [c, r])
                    surf.blit( elem_surf, elem_surf_rect )
