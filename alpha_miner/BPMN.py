import pygame as pg
from pygame.locals import *

# from pm4py.objects.log.importer.xes import factory as xes_import_factory

# import sys
# import os
import math
from load import make_text, load_image

def draw_arc( surf, start_pos, end_pos, *, arc_color= (72, 144, 220)):
    arrow_right, arrow_right_rect = load_image("arrow_right.png")
    arrow_left, arrow_left_rect = load_image("arrow_left.png")
    arrow_down, arrow_down_rect = load_image("arrow_down.png")
    arrow_up, arrow_up_rect = load_image("arrow_up.png")

    size = 3
    #arc_color = (72, 144, 220)
    
    arrow_img = arrow_right
    arrow_rect = arrow_right.get_rect()
    mid_point_rect = arrow_right.get_rect()

    empty_surface = pg.Surface((30,30))
    empty_surface.fill( (0, 0, 0) )
    empty_surface_rect = empty_surface.get_rect()

    elipse_x = 0
    elipse_y = 0

    dist_x = end_pos[0] - start_pos[0]
    dist_y = end_pos[1] - start_pos[1]
    # the comments assume that the starting point is in the center of the coordinate system
    if start_pos[1] == end_pos[1]: # when start and end are in same plane x
        mid_point_rect.topleft = ( dist_x/2 + start_pos[0], start_pos[1])
        elipse_w = abs(dist_x)
        elipse_h = 80
        elipse_y = start_pos[1] - elipse_h/2
        if dist_x > 0:# right side of 0,0
            elipse_x = start_pos[0]
            elipse_start_angle = 0
            elipse_end_angle = math.pi

            arrow_img = arrow_down
            rotate = elipse_w/elipse_h * 10
            if rotate > 30:
                rotate = 30
            arrow_img = pg.transform.rotate(arrow_img, rotate)
            arrow_down_rect.centerx = end_pos[0]
            arrow_down_rect.bottom = end_pos[1]
            arrow_down_rect.move_ip( -rotate * 2/8, -2)
            arrow_rect = arrow_down_rect
        elif dist_x < 0:# left side of 0,0
            elipse_x = end_pos[0]
            elipse_start_angle = math.pi
            elipse_end_angle = 0

            arrow_img = arrow_up
            rotate = elipse_w/elipse_h * 10
            if rotate > 30:
                rotate = 30
            arrow_img = pg.transform.rotate(arrow_img, rotate)
            arrow_up_rect.centerx = end_pos[0]
            arrow_up_rect.top = end_pos[1]
            arrow_up_rect.move_ip( rotate /5, -rotate/4)
            arrow_rect = arrow_up_rect

    elif start_pos[0] == end_pos[0]:# when start and end are in same plane y
        mid_point_rect.topleft = ( start_pos[0], dist_y/2 + start_pos[1])
        elipse_w = 80
        elipse_h = abs(dist_y)
        elipse_x = start_pos[0] - elipse_w/2
        if dist_y > 0:# bottom side of 0,0
            elipse_y = start_pos[1]
            elipse_start_angle = -math.pi * 1/2
            elipse_end_angle = math.pi * 1/2

            arrow_img = arrow_left
            rotate = elipse_h/elipse_w * 10
            if rotate > 30:
                rotate = 30
            arrow_img = pg.transform.rotate(arrow_img, rotate)
            arrow_left_rect.left = end_pos[0]
            arrow_left_rect.centery = end_pos[1]
            arrow_left_rect.move_ip( -rotate /5, -rotate * 3/8)
            arrow_rect = arrow_left_rect
        elif dist_y < 0:# top side of 0,0
            elipse_y = start_pos[1] - elipse_h
            elipse_start_angle = math.pi * 1/2
            elipse_end_angle = math.pi * 3/2

            arrow_img = arrow_right
            rotate = elipse_h/elipse_w * 10
            if rotate > 30:
                rotate = 30
            arrow_img = pg.transform.rotate(arrow_img, rotate)
            arrow_right_rect.right = end_pos[0]
            arrow_right_rect.centery = end_pos[1]
            arrow_right_rect.move_ip( -rotate /4, rotate /7)
            arrow_rect = arrow_right_rect
    else:
        if abs(dist_y/dist_x) <=1 and abs(dist_y/dist_x) > 0:# when dist_y is less then dist_x
            if (dist_x > 0 and dist_y < 0 ) or (dist_x < 0 and dist_y > 0 ):# when the end point is in the first half of the first quarter or third quarter
                mid_point_rect.topleft = ( (1 + abs(dist_y/dist_x)) * (dist_x/2) + start_pos[0], start_pos[1])
                elipse_w, elipse_h = get_elipse_dimensions(start_pos, end_pos, mid_point_rect)
                if elipse_w < 40:
                    elipse_w = 40
                if elipse_h < 40:
                    elipse_h = 40
                if dist_y < 0: # first quater
                    elipse_x = start_pos[0]
                    if (end_pos[0] - mid_point_rect.x) == 0:
                        elipse_start_angle = math.atan(abs(end_pos[1]-mid_point_rect.y)/(end_pos[0]-mid_point_rect.x + 1))
                    else: 
                        elipse_start_angle = math.atan(abs(end_pos[1]-mid_point_rect.y)/(end_pos[0]-mid_point_rect.x))
                        
                        if elipse_w/elipse_h < 1.2:
                            elipse_start_angle += 0.05 * elipse_w/elipse_h
                        elif elipse_w/elipse_h < 1.35:
                            elipse_start_angle += 0.075 * elipse_w/elipse_h
                        elif elipse_w/elipse_h < 1.45:
                            elipse_start_angle += 0.1 * elipse_w/elipse_h
                        elif elipse_w/elipse_h < 1.6:
                            elipse_start_angle += 0.13 * elipse_w/elipse_h
                        elif elipse_w/elipse_h < 1.8:
                            elipse_start_angle += 0.16 * elipse_w/elipse_h
                        elif elipse_w/elipse_h < 2.5:
                            elipse_start_angle += 0.19 * elipse_w/elipse_h
                        elif elipse_w/elipse_h < 2.7:
                            elipse_start_angle += 0.18 * elipse_w/elipse_h
                        elif elipse_w/elipse_h < 3.2:
                            elipse_start_angle += 0.15 * elipse_w/elipse_h
                        elif elipse_w/elipse_h < 4:
                            elipse_start_angle += 0.12 * elipse_w/elipse_h
                        elif elipse_w/elipse_h < 5.1:
                            elipse_start_angle += 0.09 * elipse_w/elipse_h
                        elif elipse_w/elipse_h < 6.2:
                            elipse_start_angle += 0.07 * elipse_w/elipse_h
                        elif elipse_w/elipse_h < 9:
                            elipse_start_angle += 0.04 * elipse_w/elipse_h
                        elif elipse_w/elipse_h < 12:
                            elipse_start_angle += 0.03 * elipse_w/elipse_h
                     
                        #empty_surface_rect.topleft = (end_pos[0], end_pos[1])
                        
                    elipse_end_angle = math.pi

                    arrow_img = arrow_right
                    rotate = elipse_w/elipse_h * 15 - 10
                    if rotate > 25:
                        rotate = 25

                    arrow_img = pg.transform.rotate(arrow_img, -rotate)
                    arrow_right_rect.right = end_pos[0]
                    arrow_right_rect.centery = end_pos[1]
                    if start_pos[1] - end_pos[1] < 10:
                        arrow_right_rect.move_ip( -rotate * 2/8, -rotate * 5/16 - (10 - (start_pos[1] - end_pos[1])) *0.5 )
                    else:
                        arrow_right_rect.move_ip( -rotate * 2/8, -rotate * 5/16)
                    arrow_rect = arrow_right_rect
                elif dist_y > 0: # third quater
                    elipse_x = start_pos[0] - elipse_w
                    if (end_pos[0] - mid_point_rect.x) == 0:
                        elipse_start_angle = math.pi + abs(math.atan(abs(end_pos[1]-mid_point_rect.y)/(end_pos[0]-mid_point_rect.x + 1)))
                    else:
                        elipse_start_angle = math.pi + abs(math.atan(abs(end_pos[1]-mid_point_rect.y)/(end_pos[0]-mid_point_rect.x)))
    
                        if elipse_w/elipse_h < 1.2:
                            elipse_start_angle += 0.05 * elipse_w/elipse_h
                        elif elipse_w/elipse_h < 1.35:
                            elipse_start_angle += 0.075 * elipse_w/elipse_h
                        elif elipse_w/elipse_h < 1.45:
                            elipse_start_angle += 0.1 * elipse_w/elipse_h
                        elif elipse_w/elipse_h < 1.6:
                            elipse_start_angle += 0.13 * elipse_w/elipse_h
                        elif elipse_w/elipse_h < 1.8:
                            elipse_start_angle += 0.16 * elipse_w/elipse_h
                        elif elipse_w/elipse_h < 2.5:
                            elipse_start_angle += 0.19 * elipse_w/elipse_h
                        elif elipse_w/elipse_h < 2.7:
                            elipse_start_angle += 0.18 * elipse_w/elipse_h
                        elif elipse_w/elipse_h < 3.2:
                            elipse_start_angle += 0.15 * elipse_w/elipse_h
                        elif elipse_w/elipse_h < 4:
                            elipse_start_angle += 0.12 * elipse_w/elipse_h
                        elif elipse_w/elipse_h < 5.1:
                            elipse_start_angle += 0.09 * elipse_w/elipse_h
                        elif elipse_w/elipse_h < 6.2:
                            elipse_start_angle += 0.07 * elipse_w/elipse_h
                        elif elipse_w/elipse_h < 9:
                            elipse_start_angle += 0.04 * elipse_w/elipse_h

                    elipse_end_angle = 0

                    arrow_img = arrow_left
                    rotate = elipse_w/elipse_h * 20 - 20
                    if rotate > 30:
                        rotate = 30
                    arrow_img = pg.transform.rotate(arrow_img, -rotate)
                    arrow_left_rect.left = end_pos[0]
                    arrow_left_rect.centery = end_pos[1]
                    arrow_left_rect.move_ip( -rotate * 2/8, -2)
                    arrow_rect = arrow_left_rect
                elipse_y = start_pos[1] - elipse_h/2        
            elif (dist_x > 0 and dist_y > 0 ) or (dist_x < 0 and dist_y < 0 ):# when the end point is in the second half of the second quarter or fourth quarter

                if dist_y < 0: # second quarter
                    mid_point_rect.topleft = ( start_pos[0], (1 + abs(dist_x/dist_y)) * (dist_y/2) + start_pos[1])
                    elipse_w, elipse_h = get_elipse_dimensions(start_pos, end_pos, mid_point_rect)
                    if elipse_w < 60:
                        elipse_w = 60
                    if elipse_h < 60:
                        elipse_h = 60

                    elipse_x = start_pos[0] - elipse_w/2
                    elipse_y = start_pos[1] - elipse_h
                    if (end_pos[0] - mid_point_rect.x) == 0:
                        elipse_start_angle = math.pi - abs(math.atan(abs(end_pos[1]-mid_point_rect.y)/(end_pos[0]-mid_point_rect.x+1)))
                    else:
                        elipse_start_angle = math.pi - abs(math.atan(abs(end_pos[1]-mid_point_rect.y)/(end_pos[0]-mid_point_rect.x)))
                        
                        for i in range(0, 20):# 1 - 0.8
                            if elipse_h/elipse_w >0.99 - i*0.01:
                                elipse_start_angle += (0.04 + 0.02*i) * (elipse_h/elipse_w)**(1/5)
                                break
                        for i in range(0, 20):# 0.8 - 0.6
                            if elipse_h/elipse_w > 0.79 - i*0.01 and elipse_h/elipse_w <= 0.8:
                                elipse_start_angle += (0.45 + 0.023*i) * (elipse_h/elipse_w)**(1/5)
                                break
                        for i in range(0, 39):# 0.6 - 0.4
                            if elipse_h/elipse_w > 0.595 - i*0.005 and elipse_h/elipse_w <= 0.6:
                                elipse_start_angle += (0.9 + 0.014*i) * (elipse_h/elipse_w)**(1/5)
                                break
                        # for i in range(0, 17):# 0.42 - 0.26
                        #     if elipse_h/elipse_w > 0.42 - i*0.01 and elipse_h/elipse_w <= 0.42:
                        #         elipse_start_angle += (1.4 + 0.034*i) * (elipse_h/elipse_w)**(1/5)
                        #         break
                        # for i in range(0, 11):# 0.26 - 0.16
                        #     if elipse_h/elipse_w > 0.26 - i*0.01 and elipse_h/elipse_w <= 0.26:
                        #         elipse_start_angle += (1.95 + 0.047*i) * (elipse_h/elipse_w)**(1/5)
                        #         break
                    elipse_end_angle = math.pi * 3/2

                    arrow_img = arrow_up
                    
                    if  elipse_w/elipse_h < 1.2:
                        rotate =  elipse_w/elipse_h * 10
                    elif  elipse_w/elipse_h <1.5:
                        rotate =  elipse_w/elipse_h * 15
                    else:
                        rotate =  elipse_w/elipse_h * 25
                    if rotate > 80:
                        rotate = 80
                    arrow_img = pg.transform.rotate(arrow_img, rotate)
                    arrow_up_rect.centerx = end_pos[0]
                    arrow_up_rect.top = end_pos[1]
                    if  elipse_w/elipse_h <3:
                        arrow_up_rect.move_ip( rotate * 1/7, -rotate * 2/7)
                    else:
                        arrow_up_rect.move_ip( rotate * 1/7, -rotate * 3/14)
                    arrow_rect = arrow_up_rect
                elif dist_y > 0: # fourth quater
                    mid_point_rect.topleft = ( start_pos[0] + 7/16* (end_pos[0] - start_pos[0]), end_pos[1])
                    elipse_w, elipse_h = get_elipse_dimensions(start_pos, end_pos, mid_point_rect)
                    if elipse_w < 30:
                        elipse_w = 30
                    if elipse_h < 30:
                        elipse_h = 30

                    elipse_x = mid_point_rect.x - elipse_w/2
                    elipse_y = mid_point_rect.y - elipse_h/2
                    if (end_pos[0] - mid_point_rect.x) == 0:
                        elipse_end_angle = math.pi - abs(math.atan(abs(start_pos[1]-mid_point_rect.y)/abs(start_pos[0]-mid_point_rect.x+1)))
                    else:
                        elipse_end_angle = math.pi - abs(math.atan(abs(start_pos[1]-mid_point_rect.y)/abs(start_pos[0]-mid_point_rect.x)))
                    
                        if elipse_h/elipse_w < 0.06:
                            elipse_end_angle -= 200 * elipse_h/elipse_w * elipse_h/elipse_w
                        elif elipse_h/elipse_w < 0.065:
                            elipse_end_angle -= 150 * elipse_h/elipse_w * elipse_h/elipse_w
                        elif elipse_h/elipse_w < 0.075:
                            elipse_end_angle -= 120 * elipse_h/elipse_w * elipse_h/elipse_w
                        elif elipse_h/elipse_w < 0.09:
                            elipse_end_angle -= 80 * elipse_h/elipse_w * elipse_h/elipse_w
                        elif elipse_h/elipse_w < 0.1:
                            elipse_end_angle -= 70 * elipse_h/elipse_w * elipse_h/elipse_w
                        elif elipse_h/elipse_w < 0.11:
                            elipse_end_angle -= 54 * elipse_h/elipse_w * elipse_h/elipse_w
                        elif elipse_h/elipse_w < 0.12:
                            elipse_end_angle -= 40 * elipse_h/elipse_w * elipse_h/elipse_w
                        elif elipse_h/elipse_w < 0.13:
                            elipse_end_angle -= 35 * elipse_h/elipse_w * elipse_h/elipse_w
                        elif elipse_h/elipse_w < 0.15:
                            elipse_end_angle -= 28 * elipse_h/elipse_w * elipse_h/elipse_w
                        elif elipse_h/elipse_w < 0.17:
                            elipse_end_angle -= 20 * elipse_h/elipse_w * elipse_h/elipse_w
                        elif elipse_h/elipse_w < 0.2:
                            elipse_end_angle -= 14 * elipse_h/elipse_w * elipse_h/elipse_w
                        elif elipse_h/elipse_w < 0.22:
                            elipse_end_angle -= 2.4 * elipse_h/elipse_w
                        elif elipse_h/elipse_w < 0.25:
                            elipse_end_angle -= 2 * elipse_h/elipse_w
                        elif elipse_h/elipse_w < 0.27:
                            elipse_end_angle -= 1.8 * elipse_h/elipse_w
                        elif elipse_h/elipse_w < 0.33:
                            elipse_end_angle -= 1.4 * elipse_h/elipse_w
                        elif elipse_h/elipse_w < 0.4:
                            elipse_end_angle -=  elipse_h/elipse_w
                        elif elipse_h/elipse_w < 0.5:
                            elipse_end_angle -=  0.7 * elipse_h/elipse_w
                        elif elipse_h/elipse_w < 0.62:
                            elipse_end_angle -=  0.4 * elipse_h/elipse_w
                        elif elipse_h/elipse_w < 0.7:
                            elipse_end_angle -=  0.2 * elipse_h/elipse_w
                        elif elipse_h/elipse_w < 0.8:
                            elipse_end_angle -=  0.1 * elipse_h/elipse_w
                        elif elipse_h/elipse_w < 0.9:
                            elipse_end_angle -=  0.06 * elipse_h/elipse_w
                        elif elipse_h/elipse_w < 1.05:
                            elipse_end_angle -=  0
                        elif elipse_h/elipse_w < 1.2:
                            elipse_end_angle +=  0.1 * elipse_h/elipse_w
                        elif elipse_h/elipse_w < 1.4:
                            elipse_end_angle +=  0.14 * elipse_h/elipse_w
                        elif elipse_h/elipse_w < 1.6:
                            elipse_end_angle +=  0.17 * elipse_h/elipse_w
                        elif elipse_h/elipse_w < 1.8:
                            elipse_end_angle +=  0.175 * elipse_h/elipse_w
                        elif elipse_h/elipse_w < 2:
                            elipse_end_angle +=  0.18 * elipse_h/elipse_w
                        elif elipse_h/elipse_w < 2.3:
                            elipse_end_angle +=  0.19 * elipse_h/elipse_w
                        elif elipse_h/elipse_w < 2.5:
                            elipse_end_angle +=  0.185 * elipse_h/elipse_w
                        elif elipse_h/elipse_w < 3:
                            elipse_end_angle +=  0.19 * elipse_h/elipse_w

                    elipse_start_angle = 0
                    
                    arrow_img = arrow_down
                    rotate = elipse_w/elipse_h * 10
                    if rotate > 80:
                        rotate = 80
                    arrow_img = pg.transform.rotate(arrow_img, rotate)
                    arrow_down_rect.centerx = end_pos[0]
                    arrow_down_rect.bottom = end_pos[1]
                    
                    if elipse_h < 80:
                        arrow_down_rect.move_ip( -rotate * 4/14 if -rotate * 3/14 > -10 else -10, -rotate * 1/7 if -rotate * 1/7 > -7 else -7)
                    else:
                        arrow_down_rect.move_ip( -rotate * 2/7 if -rotate * 2/7 > -10 else -10, -rotate * 2/7 if -rotate * 2/7 > -7 else -7)
                    arrow_rect = arrow_down_rect

        elif abs(dist_x/dist_y) <=1 and abs(dist_x/dist_y) > 0:# when dist_y is greater then dist_x
            if (dist_x > 0 and dist_y < 0 ) or (dist_x < 0 and dist_y > 0 ):# when the end point is in the second half of the first quarter or third quarter
                mid_point_rect.topleft = ( end_pos[0], start_pos[1])
                elipse_w, elipse_h = get_elipse_dimensions(start_pos, end_pos, mid_point_rect)
                if elipse_w < 60:
                    elipse_w = 60
                if elipse_h < 60:
                    elipse_h = 60
                elipse_y = start_pos[1] - elipse_h/2
                if dist_y < 0: # first quater
                    elipse_x = start_pos[0]
                    elipse_end_angle = math.pi + math.pi/180 * 2
                    elipse_start_angle = math.pi/2

                    arrow_img = arrow_right
                    rotate = elipse_h/elipse_w * 7
                    if rotate > 80:
                        rotate = 80
                    arrow_img = pg.transform.rotate(arrow_img, rotate)
                    arrow_right_rect.right = end_pos[0]
                    arrow_right_rect.centery = end_pos[1]
                    arrow_right_rect.move_ip( -rotate * 3/14 if -rotate * 3/14 > -10 else -10, 0)
                    arrow_rect = arrow_right_rect
                elif dist_y > 0: # third quater
                    elipse_x = start_pos[0] - elipse_w
                    elipse_end_angle = 0
                    elipse_start_angle = math.pi *3/2

                    arrow_img = arrow_left
                    rotate = elipse_h/elipse_w * 14
                    if rotate > 80:
                        rotate = 80
                    arrow_img = pg.transform.rotate(arrow_img, rotate)
                    arrow_left_rect.left = end_pos[0]
                    arrow_left_rect.centery = end_pos[1]
                    arrow_left_rect.move_ip( -rotate * 1/7 if -rotate * 1/7 > -10 else -10, -rotate * 3/7 if -rotate * 3/7 > -9 else -9)
                    arrow_rect = arrow_left_rect
                
            elif (dist_x > 0 and dist_y > 0 ) or (dist_x < 0 and dist_y < 0 ):# when the end point is in the first half of the second quarter or fourth qyarter
                mid_point_rect.topleft = ( start_pos[0], (1 + abs(dist_x/dist_y)) * (dist_y/2) + start_pos[1])
                elipse_w, elipse_h = get_elipse_dimensions(start_pos, end_pos, mid_point_rect)
                if elipse_w < 60:
                    elipse_w = 60
                if elipse_h < 60:
                    elipse_h = 60
                if dist_y < 0: # second quarter
                    elipse_x = start_pos[0] - 1/2 * elipse_w
                    elipse_y = start_pos[1] - elipse_h
                    if (end_pos[1]-mid_point_rect.y) == 0:
                        elipse_start_angle = math.pi*1/2 +  abs(math.atan(abs(end_pos[0]-mid_point_rect.x)/(end_pos[1]-mid_point_rect.y + 1)))
                    else:
                        elipse_start_angle = math.pi*1/2 +  abs(math.atan(abs(end_pos[0]-mid_point_rect.x)/(end_pos[1]-mid_point_rect.y)))
                    elipse_end_angle = math.pi * 3/2

                    arrow_img = arrow_up
                    rotate = elipse_h/elipse_w * 7
                    if rotate > 80:
                        rotate = 80
                    arrow_img = pg.transform.rotate(arrow_img, -rotate)
                    arrow_up_rect.centerx = end_pos[0]
                    arrow_up_rect.top = end_pos[1]
                    arrow_up_rect.move_ip( -rotate * 2/7 if -rotate * 2/7 > -10 else -10, -rotate * 2/7 if -rotate * 2/7 > -9 else -9)
                    arrow_rect = arrow_up_rect
                elif dist_y > 0: # fourth quater
                    elipse_x = start_pos[0] - elipse_w/2
                    elipse_y = start_pos[1]
                    if (end_pos[1]-mid_point_rect.y) == 0:
                        elipse_start_angle = math.pi*3/2 +  abs(math.atan(abs(end_pos[0]-mid_point_rect.x)/(end_pos[1]-mid_point_rect.y + 1)))
                    else:
                        elipse_start_angle = math.pi*3/2 +  abs(math.atan(abs(end_pos[0]-mid_point_rect.x)/(end_pos[1]-mid_point_rect.y)))
                    
                    if elipse_h/elipse_w < 1.1:
                        elipse_start_angle += 0.05 * elipse_h/elipse_w
                    elif elipse_h/elipse_w < 1.25:
                        elipse_start_angle += 0.06 * elipse_h/elipse_w
                    elif elipse_h/elipse_w < 1.4:
                        elipse_start_angle += 0.08 * elipse_h/elipse_w
                    elif elipse_h/elipse_w < 1.6:
                        elipse_start_angle += 0.13 * elipse_h/elipse_w
                    elif elipse_h/elipse_w < 2:
                        elipse_start_angle += 0.16 * elipse_h/elipse_w
                    elif elipse_h/elipse_w < 2.7:
                        elipse_start_angle += 0.18 * elipse_h/elipse_w
                    elif elipse_h/elipse_w < 3.2:
                        elipse_start_angle += 0.16 * elipse_h/elipse_w
                    elif elipse_h/elipse_w < 4:
                        elipse_start_angle += 0.12 * elipse_h/elipse_w


                    elipse_end_angle = math.pi * 1/2

                    arrow_img = arrow_down
                    rotate = elipse_h/elipse_w * 7
                    if rotate > 80:
                        rotate = 80
                    arrow_img = pg.transform.rotate(arrow_img, -rotate)
                    arrow_down_rect.centerx = end_pos[0]
                    arrow_down_rect.bottom = end_pos[1]
                    if end_pos[0] - start_pos[0] <20:
                        arrow_down_rect.move_ip( -rotate * 5/14 if -rotate * 5/14 > -3 else -3 + (20 - (end_pos[0] - start_pos[0]))*0.5, -rotate * 1/7 if -rotate * 1/7 > -10 else -10)
                    else:
                        arrow_down_rect.move_ip( -rotate * 6/14 if -rotate * 6/14 > -3 else -3, -rotate * 1/7 if -rotate * 1/7 > -10 else -10)
                    arrow_rect = arrow_down_rect

    if end_pos[0] != start_pos[0] or end_pos[1] != start_pos[1]:
        pg.draw.arc(surf, arc_color, ( elipse_x, elipse_y, elipse_w, elipse_h), elipse_start_angle, elipse_end_angle, size if size < min(elipse_w, elipse_h) else 1)
        surf.blit(empty_surface, empty_surface_rect)
    pg.display.flip()
    surf.blit(arrow_img, arrow_rect)

def get_elipse_dimensions(start_pos, end_pos, mid_point_rect):
    #calculation of ellipse parameter
    elipse_a = 5
    elipse_b = 5
    counter = -((end_pos[0] - mid_point_rect.x)*(start_pos[1] - mid_point_rect.y))**2 + ((start_pos[0] - mid_point_rect.x)*(end_pos[1] - mid_point_rect.y))**2
    denominator_a = (end_pos[1] - mid_point_rect.y)**2 - (start_pos[1] - mid_point_rect.y)**2
    denominator_b = (start_pos[0] - mid_point_rect.x)**2 - (end_pos[0] - mid_point_rect.x)**2

    if denominator_a != 0:
        elipse_a = math.sqrt(counter/denominator_a)
    # else:
    #     elipse_a = math.sqrt(counter/(denominator_a+1))
    if denominator_b != 0:
        elipse_b = math.sqrt(counter/denominator_b)
    # else:
    #     elipse_b = math.sqrt(counter/(denominator_a+1))

    elipse_w = 2*elipse_a
    elipse_h = 2*elipse_b

    return elipse_w, elipse_h


class BPMN():
    def __init__(self, activities):
        """
        :param activities: table [[],[]] first table are real names of activities, second are new names
        """
        self._board = [[None]]
        self._connections = { "from" : [],
                              "to" : []}
        self.start_bpmn, self.start_bpmn_rect = load_image("start.png")
        self.start_text, self.start_text_rect = make_text( text= "START", font_name= 'calibri-font-sv\Calibri Bold.ttf'\
                                                    , size= 15, pos= (self.start_bpmn_rect.width/2, 60)\
                                                    , text_color= (72, 144, 220), text_background_color= (0, 0, 0))
        self.start_bpmn.blit( self.start_text, self.start_text_rect )

        self.end_bpmn, self.end_bpmn_rect = load_image("end.png")
        self.end_text, self.end_text_rect = make_text( text= "END", font_name= 'calibri-font-sv\Calibri Bold.ttf'\
                                                    , size= 15, pos= (self.end_bpmn_rect.width/2, 60)\
                                                    , text_color= (72, 144, 220), text_background_color= (0, 0, 0))
        self.end_bpmn.blit( self.end_text, self.end_text_rect )

        self.exclusive_bpmn, self.exclusive_bpmn_rect = load_image("exclusive.png")
        self.parallel_bpmn, self.parallel_bpmn_rect = load_image("parallel.png")
        self.arrow_right, self.arrow_right_rect = load_image("arrow_right.png")
        self.arrow_left, self.arrow_left_rect = load_image("arrow_left.png")

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

    def create_start(self, TI):
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

    def create_end(self, TI, TO):
        #create end
        self.start_width = self.width

        self.add_column()
        for to_elem in TO:
            if to_elem in TI: 
                if self.get_activity( [ TI.index(to_elem), 2 ] ) == None: # If place that we want put elem into is empty
                    self.add_elem_on_board( "end", [ TI.index(to_elem), 2 ])
                else:# If not we have to find free place to move element
                    for row_num in range( 0, self.height ):# go through whole column
                        if self.get_activity( [row_num, self.start_width] ) == None: # if we find empty place we move element there
                            found = True
                            move_elem( [ TI.index(to_elem), 2 ], [row_num, self.start_width] )
                            self.add_elem_on_board( "end", [ TI.index(to_elem), 2 ])
                        if found == False:#otherwise we have to add new row and then move elem
                            self.add_row(d)
                            move_elem([ TI.index(to_elem), 2 ], [self.height - 1, self.start_width])
                            self.add_elem_on_board( "end", [ TI.index(to_elem), 2 ])
            else:
                if self.width == self.start_width + 1:
                    self.add_column()
                found = False
                for row_num in range( 0, self.height ):
                    if self.get_activity( [row_num, self.start_width] ) == None:
                        found = True
                        self.add_elem_on_board( to_elem, [ row_num, self.start_width ])
                        self.add_elem_on_board( "end", [ row_num, self.start_width + 1 ])
                        self.add_connection(  [ row_num, self.start_width ], [ row_num, self.start_width + 1 ] )
                        break
                    if found == False:
                        self.add_row()
                        self.add_elem_on_board( to_elem, [ self.height - 1, self.start_width ])
                        self.add_elem_on_board( "end", [ self.height - 1, self.start_width + 1 ])
                        self.add_connection(  [ self.height - 1, self.start_width ], [ self.height - 1, self.start_width + 1 ] )
                        break

    def create_patt_a(self, TI, TO, YLa):
        #create pattern a
        #checking how many fields separate the beginning and the end 
        move_about = 0
        which_side = -1
        for pat_num in range(0, len(YLa[0])):
            if YLa[0][pat_num] in TI and YLa[1][pat_num] in TO:
                pass
            elif (YLa[0][pat_num] not in TI and YLa[1][pat_num] in TO) or (YLa[0][pat_num] in TI and YLa[1][pat_num] not in TO):
                if which_side == -1:
                    move_about = 1
                    if YLa[0][pat_num] in TI:
                        which_side = 0
                    elif YLa[1][pat_num] in TO:
                        which_side = 1
                elif which_side == 0:
                    if YLa[1][pat_num] in TO:
                        move_about = 2
                        which_side = 2
                        break
                elif which_side == 1:
                    if YLa[0][pat_num] in TI :
                        move_about = 2
                        which_side = 2
                        break
            else:
                move_about = 2
                break
        if move_about > 0:
            #adding columns
            self.add_column( move_about)
            self.move_all_right( 2, move_about )
            #putting pattern a on board
            for pat_num in range(0, len(YLa[0])):
                if YLa[0][pat_num] in TI and YLa[1][pat_num] in TO:# if start activity and end activity is in pattern a
                    self.add_connection( self.find_in_board(YLa[0][pat_num]), self.find_in_board(YLa[1][pat_num]) )

                elif YLa[0][pat_num] in TI:# if start activity is in pattern a
                    coord = self.find_in_board( YLa[0][pat_num] )
                    if YLa[1][pat_num] not in self.already_on:# if end activity not already on board
                        if self._board[ coord[0]][ coord[1] + 1] == None:
                            self.add_elem_on_board( YLa[1][pat_num], [coord[0], coord[1] + 1] )
                            self.add_connection( coord, [coord[0], coord[1] + 1] )
                        else:
                            found = False
                            for row_num in range(0, self.height): 
                                if self._board[row_num][coord[1] + 1] == None:
                                    found = True
                                    self.add_elem_on_board( YLa[1][pat_num], [row_num, coord[1] + 1] )
                                    self.add_connection( coord, [row_num, coord[1] + 1] )
                                    break
                            if found == False:
                                self.add_row()
                                self.add_elem_on_board( YLa[1][pat_num], [self.height - 1, coord[1] + 1] )
                                self.add_connection( coord, [self.height - 1, coord[1] + 1] )
                    else:#if end activity is already on board
                        self.add_connection( coord, self.find_in_board( YLa[1][pat_num]  ) )
                    
                elif YLa[1][pat_num] in TO:# if end activity is in pattern a
                    coord = self.find_in_board( YLa[1][pat_num] )
                    if YLa[0][pat_num] not in self.already_on:# if start activity not already on board
                        if self._board[ coord[0]][ coord[1] - 1] == None:
                            self.add_elem_on_board( YLa[0][pat_num], [coord[0], coord[1] - 1] )
                            self.add_connection( [coord[0], coord[1] - 1], coord )
                        else:
                            found = False
                            for row_num in range(0, self.height): 
                                if self._board[row_num][coord[1] -1 ] == None:
                                    found = True
                                    self.add_elem_on_board( YLa[0][pat_num], [row_num, coord[1] - 1] )
                                    self.add_connection( coord, [row_num, coord[1] - 1] )
                                    break
                            if found == False:
                                self.add_row()
                                self.add_elem_on_board( YLa[0][pat_num], [self.height - 1, coord[1] - 1] )
                                self.add_connection( coord, [self.height - 1, coord[1] - 1] )
                    else:# if start activity is already on board
                        self.add_connection( self.find_in_board( YLa[0][pat_num]  ) , coord)

            for pat_num in range(0, len(YLa[0])):
                found = False
                if YLa[0][pat_num] not in self.already_on and YLa[1][pat_num] not in self.already_on:
                    if YLa[0][pat_num] not in TI and YLa[1][pat_num] not in TO:
                        for row_num in range(0, self.height):
                            if self._board[row_num][self.start_width] == None and self._board[row_num][self.start_width + 1] == None:
                                found = True
                                if YLa[0][pat_num] not in self.already_on:
                                    self.add_elem_on_board( YLa[0][pat_num], [row_num, self.start_width] )
                                if YLa[1][pat_num] not in self.already_on:
                                    self.add_elem_on_board( YLa[1][pat_num], [row_num, self.start_width + 1] )
                                self.add_connection( self.find_in_board( YLa[0][pat_num]  ), self.find_in_board( YLa[1][pat_num]  ) )
                                break
                        if found == False:
                            self.add_row()
                            if YLa[0][pat_num] not in self.already_on:
                                self.add_elem_on_board( YLa[0][pat_num], [self.height - 1, self.start_width] )
                            if YLa[1][pat_num] not in self.already_on:
                                self.add_elem_on_board( YLa[1][pat_num], [self.height - 1, self.start_width + 1] )
                            self.add_connection( self.find_in_board( YLa[0][pat_num]  ), self.find_in_board( YLa[1][pat_num]  ) )
                else:
                    self.add_connection( self.find_in_board( YLa[0][pat_num]  ), self.find_in_board( YLa[1][pat_num]  ) )

    def create_patt_b(self, YLb):
        #create pattern b
        #put YLb[0] and "exclusive" on board
        for pat_num in range(0, len(YLb[0])):
            if YLb[0][pat_num] not in YLb[0][0:pat_num]:# if you haven't checked this name yet
                if YLb[0][pat_num] not in self.already_on:# YLb[0][pat_num] isn't already on board
                    found = False
                    for row_num in range(0, self.height):# we try to find two places with "None" placed next to each other
                        if found == False:
                            for col_num in range( self.start_width, self.width - 2 ):
                                if self._board[row_num][col_num] == None and self._board[row_num][col_num + 1] == None:
                                    found = True
                                    self.add_elem_on_board( YLb[0][pat_num], [row_num, col_num] )
                                    self.add_elem_on_board( "exclusive", [row_num, col_num + 1] )
                                    self.add_connection( [row_num, col_num], [row_num, col_num + 1] )
                                    break
                    if found == False:# if we cant find two places with "None" placed next to each other we create the space
                        self.add_row()
                        self.add_elem_on_board( YLb[0][pat_num], [self.height - 1, self.start_width] )
                        self.add_elem_on_board( "exclusive", [self.height - 1, self.start_width + 1] )
                        self.add_connection( [self.height - 1, self.start_width ], [self.height - 1, self.start_width + 1] )
                else:#if YLb[0][pat_num] is already on board we just add exclusive
                    coord = self.find_in_board( YLb[0][pat_num] )
                    if self._board[ coord[0]][ coord[1] + 1 ] == None:
                        self.add_elem_on_board ( "exclusive", [ coord[0], coord[1] + 1 ] )
                        self.add_connection( [ coord[0], coord[1] ], [ coord[0], coord[1] + 1 ] )
                    else:
                        self.add_column()
                        for i in range(0, self.width - 2 - coord[1] ):
                            for row_num in range(0, self.height):
                                self.move_elem( [row_num, self.width - 1 - i - 1] , [row_num, self.width - 1 - i])
                        self.add_elem_on_board ( "exclusive", [ coord[0], coord[1] + 1 ] )
                        self.add_connection( [ coord[0], coord[1] ], [ coord[0], coord[1] + 1 ] )
        
        # put YLb[1] on board
        for pat_num in range(0, len(YLb[1])):
            elem_0 = YLb[1][pat_num][0]
            elem_1 = YLb[1][pat_num][1]
            coord = self.find_in_board( YLb[0][pat_num] )
            for con_num in range( 0, len( self._connections['from'] ) ):
                if self._connections['from'][con_num] == coord:
                    if self._board[ self._connections['to'][con_num][0] ][ self._connections['to'][con_num][1] ] == "exclusive":
                        coord = self._connections['to'][con_num]
                        break
            #coord = [ coord[0], coord[1] + 1 ]# set coord on coordinates of exclusive
            if elem_0 in self.already_on and elem_1 in self.already_on:
                coord_0 = self.find_in_board( elem_0 )
                coord_1 = self.find_in_board( elem_1 )
                self.add_connection( coord, coord_0)
                self.add_connection( coord, coord_1)
            elif (elem_0 not in self.already_on and elem_1 in self.already_on) or (elem_0 in self.already_on and elem_1 not in self.already_on):
                if elem_0 in self.already_on:
                    coord_0 = self.find_in_board( elem_0 )
                else:
                    coord_0 = self.find_in_board( elem_1 )
                # coord_0 is are cooridinates of element of YLb[1][pat_num] that is on board
                found = False
                if self.height >= coord_0[0] + 2:
                    if self._board[ coord_0[0] + 1 ][ coord_0[1] ] == None:
                        found = True
                if found == False:
                    self.add_row()
                    for row_num_of_move in range(0, self.height - 2 - coord_0[0] ):
                        self.move_elem( [coord_0[1] + 1 + row_num_of_move, coord_0[1] ], [coord_0[1] + 2 + row_num_of_move, coord_0[1] ])
                self.add_elem_on_board( elem_1, [ coord_0[0] + 1, coord_0[1] ] )
                self.add_connection( coord, coord_0)
                self.add_connection( coord, [ coord_0[0] + 1, coord_0[1] ])

            elif elem_0 not in self.already_on and elem_1 not in self.already_on:
                if self._board[ coord[0]][ coord[1] + 1 ] == None and self._board[ coord[0] + 1][ coord[1] + 1 ] == None:
                    pass
                else:
                    self.add_column()
                    for i in range(0, self.width - 2 - coord[1] ):
                        for row_num in range(coord[0], coord[0]+2):
                            self.move_elem( [row_num, self.width - 1 - i - 1] , [row_num, self.width - 1 - i])
                self.add_elem_on_board( elem_0, [ coord[0], coord[1] + 1 ] )
                self.add_elem_on_board( elem_1, [ coord[0] + 1, coord[1] + 1 ] )
                self.add_connection( coord, [ coord[0], coord[1] + 1 ] )
                self.add_connection( coord, [ coord[0] + 1, coord[1] + 1 ] )

    def create_patt_c(self, YLc):
        #create pattern c
        #put YLc[1] and "exclusive" on board
        for pat_num in range(0, len(YLc[1])):
            if YLc[1][pat_num] not in YLc[1][0:pat_num]:# if you haven't checked this name yet
                if YLc[1][pat_num] not in self.already_on:# YLc[1][pat_num] isn't already on board
                    found = False
                    for row_num in range(0, self.height):# we try to find two places with "None" placed next to each other
                        if found == False:
                            for col_num in range( self.start_width + 1, self.width - 2 ):
                                if self._board[row_num][col_num] == None and self._board[row_num][col_num - 1] == None:
                                    found = True
                                    self.add_elem_on_board( YLc[1][pat_num], [row_num, col_num] )
                                    self.add_elem_on_board( "exclusive", [row_num, col_num - 1] )
                                    self.add_connection( [row_num, col_num - 1], [row_num, col_num] )
                                    break
                    if found == False:
                        self.add_row()
                        self.add_elem_on_board( YLc[0][pat_num], [self.height - 1, self.width - 2] )
                        self.add_elem_on_board( "exclusive", [self.height - 1, self.width - 3] )
                        self.add_connection( [self.height - 1, self.width - 3 ], [self.height - 1, self.width - 2] )
                else:#if YLc[0][pat_num] is already on board we just add exclusive
                    coord = self.find_in_board( YLc[1][pat_num] )
                    if self._board[ coord[0]][ coord[1] - 1 ] == None:
                        self.add_elem_on_board ( "exclusive", [ coord[0], coord[1] - 1 ] )
                        self.add_connection( [ coord[0], coord[1] - 1], [ coord[0], coord[1] ] )
                    else:
                        self.add_column()
                        for i in range(0, self.width - 2 - coord[1] + 1 ):
                            for row_num in range(0, self.height):
                                self.move_elem( [row_num, self.width - 1 - i - 1] , [row_num, self.width - 1 - i])
                        self.add_elem_on_board ( "exclusive", [ coord[0], coord[1] ] ) # YLc[i] was moved on right so we put exclusive on place
                        self.add_connection( [ coord[0], coord[1] ], [ coord[0], coord[1] + 1 ] )
        # put YLc[0] on board
        for pat_num in range(0, len(YLc[1])):
            elem_0 = YLc[0][pat_num][0]
            elem_1 = YLc[0][pat_num][1]
            coord = self.find_in_board( YLc[1][pat_num] )
            coord = [ coord[0], coord[1] - 1 ]# set coord on coordinates of exclusive
            if elem_0 in self.already_on and elem_1 in self.already_on:
                coord_0 = self.find_in_board( elem_0 )
                coord_1 = self.find_in_board( elem_1 )
                self.add_connection( coord_0, coord)
                self.add_connection( coord_1, coord)
            elif (elem_0 not in self.already_on and elem_1 in self.already_on) or (elem_0 in self.already_on and elem_1 not in self.already_on):
                if elem_0 in self.already_on:
                    coord_0 = self.find_in_board( elem_0 )
                else:
                    coord_0 = self.find_in_board( elem_1 )
                # coord_0 is are cooridinates of element of YLc[0][pat_num] that is on board
                found = False
                if self.height >= coord_0[0] + 2: # check if there is one more row under elem_0
                    if self._board[ coord_0[0] + 1 ][ coord_0[1] ] == None:
                        found = True
                if found == False:
                    self.add_row()
                    for row_num_of_move in range(0, self.height - 2 - coord_0[0] ):# how many objects you need to move
                        self.move_elem( [coord_0[1] + 1 + row_num_of_move, coord_0[1] ], [coord_0[1] + 2 + row_num_of_move, coord_0[1] ])
                self.add_elem_on_board( elem_1, [ coord_0[0] + 1, coord_0[1] ] )
                self.add_connection( coord_0, coord)
                self.add_connection( [ coord_0[0] + 1, coord_0[1] ], coord)

            elif elem_0 not in self.already_on and elem_1 not in self.already_on:
                if self._board[ coord[0]][ coord[1] - 1 ] == None and self._board[ coord[0] + 1][ coord[1] - 1 ] == None:
                    pass
                else:
                    self.add_column()
                    for i in range(0, self.width - 2 - coord[1] + 1 ):
                        for row_num in range(coord[0], coord[0]+2):
                            self.move_elem( [row_num, self.width - 1 - i - 1] , [row_num, self.width - 1 - i])
                self.add_elem_on_board( elem_0, [ coord[0], coord[1] ] )
                self.add_elem_on_board( elem_1, [ coord[0] + 1, coord[1] ] )
                self.add_connection( [ coord[0], coord[1] ], coord )
                self.add_connection( [ coord[0] + 1, coord[1] ], coord )

    def create_patt_d(self):
        #create pattern d
        for activity in self.already_on:
            connections = []
            activities = []
            coord = self.find_in_board( activity )
            for con_num in range(0, len( self._connections['from'] )):
                if self._connections['from'][con_num] == coord:
                    if len( self._board[ self._connections['to'][con_num][0] ][ self._connections['to'][con_num][1] ] ) == 1:
                        connections.append( [ self._connections['to'][con_num][0], self._connections['to'][con_num][1] ])
                        activities.append( self._board[ self._connections['to'][con_num][0] ][ self._connections['to'][con_num][1] ])
            if len(connections) >= 2: 
                self.add_column()
                for i in range(0, self.width - 2 - coord[1] ):
                    for row_num in range(0, self.height):
                        self.move_elem( [row_num, self.width - 1 - i - 1] , [row_num, self.width - 1 - i])
                self.add_elem_on_board( "parallel", [coord[0], coord[1] + 1] )
                self.add_connection( coord, [coord[0], coord[1] + 1] )

                for con_num in range(0, len( self._connections['from'] )):
                    if self._connections['from'][con_num] == coord:
                        for activ in activities:
                            if self._connections['to'][con_num] == self.find_in_board( activ ):
                                self._connections['from'][con_num][1] += 1
    
    def create_patt_e(self):
        #create pattern e
        for activity in self.already_on:
            connections = []
            activities = []
            coord = self.find_in_board( activity )
            for con_num in range(0, len( self._connections['to'] )):
                if self._connections['to'][con_num] == coord:
                    if len( self._board[ self._connections['from'][con_num][0] ][ self._connections['from'][con_num][1] ] ) == 1:
                        connections.append( [ self._connections['from'][con_num][0], self._connections['from'][con_num][1] ])
                        activities.append( self._board[ self._connections['from'][con_num][0] ][ self._connections['from'][con_num][1] ])
            if len(connections) >= 2: 
                self.add_column()
                for i in range(0, self.width - 2 - coord[1] + 1):
                    for row_num in range(0, self.height):
                        self.move_elem( [row_num, self.width - 1 - i - 1] , [row_num, self.width - 1 - i])
                self.add_elem_on_board( "parallel", [coord[0], coord[1]] )
                self.add_connection(  coord, [coord[0], coord[1] + 1])

                for con_num in range(0, len( self._connections['to'] )):
                    if self._connections['to'][con_num] == [ coord[0], coord[1] + 1 ]:
                        for activ in activities:
                            if self._connections['from'][con_num] == self.find_in_board( activ ):
                                self._connections['to'][con_num][1] -= 1

    def merge_exclusive(self):
        for j in range(0, 2):
            #merging exclusive if they same set of incomming connections or outgoing connections
            for col_num1 in range(0, len(self._board)):
                for row_num1 in range(0, len(self._board[col_num1])):
                    if self._board[col_num1][row_num1] == "exclusive":#choose that exclusive
                        if j == 0:
                            con_to = self.find_connections_to( [col_num1, row_num1] ) # possitions of all elements on board that are connected to chosen exclusive 
                        elif j == 1:
                            con_from = self.find_connections_from( [col_num1, row_num1] ) # possitions of all elements on board that are connected from chosen exclusive 
                        same_exc_pos = []# possitions of exlusives that have the same elements incomming/outgoing into/from that exclusive like chosen exclusive
                        for col_num2 in range(0, len(self._board)):
                            for row_num2 in range(0, len(self._board[col_num2])):
                                if col_num1 != col_num2 or row_num1 != row_num2:
                                    if self._board[col_num2][row_num2] == "exclusive":
                                        if j == 0:
                                            if self.find_connections_to( [col_num2, row_num2] ) == con_to:
                                                same_exc_pos.append([col_num2, row_num2])
                                        elif j == 1:
                                            if self.find_connections_from( [col_num2, row_num2] ) == con_from:
                                                same_exc_pos.append([col_num2, row_num2])
                        for i in range(0, len(same_exc_pos)):
                            self.move_elem(same_exc_pos[i], [col_num1, row_num1], True)
        
        for col_num1 in range(0, len(self._board)):# merging exclusives if their connections are a subgroup of connections of other exclusive
            for row_num1 in range(0, len(self._board[col_num1])):
                if self._board[col_num1][row_num1] == "exclusive":#choose that exclusive
                    con_to = self.find_connections_to( [col_num1, row_num1] )#saving connections to and from chosen exclusive
                    con_from = self.find_connections_from( [col_num1, row_num1] )
                    merged = False
                    for col_num2 in range(0, len(self._board)):
                        if merged == False:
                            for row_num2 in range(0, len(self._board[col_num2])):
                                if col_num1 != col_num2 or row_num1 != row_num2:
                                    if self._board[col_num2][row_num2] == "exclusive":
                                        is_subgroup = True
                                        for con_to_num in range(0, len(con_to)):
                                            if con_to[con_to_num] not in self.find_connections_to( [col_num2, row_num2] ):
                                                is_subgroup = False
                                                break
                                        for con_from_num in range(0, len(con_from)):
                                            if con_from[con_from_num] not in self.find_connections_from( [col_num2, row_num2] ):
                                                is_subgroup = False
                                                break
                                        if is_subgroup: 
                                            self.move_elem([col_num1, row_num1], [col_num2, row_num2], True)
                                            merged = True
                                            break

    def organize(self):
        board_copy = []
        connections_copy = { "from" : [],
                              "to" : []}

        for row_num in range(0, len(self._board)):
            board_copy.append(self._board[row_num][:])
        for con_num in range(0, len(self._connections["from"])):
            connections_copy["from"].append( self._connections["from"][con_num][:] )
            connections_copy["to"].append( self._connections["to"][con_num][:] )
        
        self._board = [[None]]
        self._connections = { "from" : [],
                              "to" : []}

        current_pos = [[0,0]]
        current_pos_next = []
        con_to1 = [] # possitions of elements that element on current pos is connected 
        con_to2 = [] # possitions of elements that element connected to element on current possition are connected

        already_on = { "copy" : [],# "from" list of all coordintaest from board_copy that are added into self._board
                        "real" : []}# "from" list of all coordintaest from self._board where are added elements from "from" pos
        self.already_on = []

        col_counter = 0
        row_counter = 0

        self.add_elem_on_board(board_copy[current_pos[0][0]][current_pos[0][1]], [0,0] )
        already_on["copy"].append([0,0])
        already_on["real"].append([0,0])

        licznik = 0 # USUNAC !!!!!!!!!
        adjustment = True
        while adjustment:
            return_con = { "from" : [], # from and to are possitions on board_copy
                        "to" : []}
            non_return_con = { "from" : [],# from and to are possitions on board_copy
                        "to" : []}
            for con_num0 in range(0, len(current_pos)):# go through all currently under consideration activities 
                con_to1 = self.find_connections_from( current_pos[con_num0], connections_copy ) # save all connections from current activity
                for con_num1 in range(0, len(con_to1)): # go through all connections from current activity 
                    con_to2 = self.find_connections_from(con_to1[con_num1], connections_copy) # save all connections from activity connected from current activity
                    comming_back = True # flag says if activity connected from current activity has connections going back in graph
                    for con_num2 in range(0, len(con_to2)): # go through all connections from activity connected from current activity
                        if con_to2[con_num2] in already_on["copy"] or con_to2[con_num2] in con_to1: # if connection is going back 
                            return_con["from"].append(current_pos[con_num0])
                            return_con["to"].append(con_to1[con_num1])
                            comming_back = False
                            break
                    if comming_back == True:
                        non_return_con["from"].append(current_pos[con_num0])
                        non_return_con["to"].append(con_to1[con_num1])
                    if (con_to1[con_num1] not in already_on["copy"]) and (con_to1[con_num1] not in current_pos_next):
                        current_pos_next.append(con_to1[con_num1])
                        
            self.add_column()
            row_counter = 0
            for non_ret_num in range(0, len(non_return_con["to"])):
                if len(self._board) == row_counter:
                    self.add_row()
                element_concerned_pos = current_pos.index(non_return_con["from"][non_ret_num]) # possition of concerned element in current_pos table
                start_pos = already_on["real"][already_on["copy"].index(current_pos[element_concerned_pos])]
                if non_return_con["to"][non_ret_num] not in already_on["copy"]:
                    self.add_elem_on_board(board_copy[non_return_con["to"][non_ret_num][0]][non_return_con["to"][non_ret_num][1]], [row_counter, col_counter + 1])
                    already_on["real"].append([row_counter, col_counter + 1])
                    already_on["copy"].append(non_return_con["to"][non_ret_num])
                    self.add_connection(start_pos, [row_counter, col_counter + 1])
                    row_counter += 1
                else:
                    end_pos = already_on["real"][already_on["copy"].index(non_return_con["to"][non_ret_num])]
                    self.add_connection(start_pos, end_pos)
                
            for ret_num in range(0, len(return_con["to"])):
                if len(self._board) == row_counter:
                    self.add_row()
                element_concerned_pos = current_pos.index(return_con["from"][ret_num]) # possition of concerned element in current_pos table
                start_pos = already_on["real"][already_on["copy"].index(current_pos[element_concerned_pos])]
                if return_con["to"][ret_num] not in already_on["copy"]:
                    self.add_elem_on_board(board_copy[return_con["to"][ret_num][0]][return_con["to"][ret_num][1]], [row_counter, col_counter + 1])
                    self.add_connection(start_pos, [row_counter, col_counter + 1])
                    already_on["real"].append([row_counter, col_counter + 1])
                    already_on["copy"].append(return_con["to"][ret_num])
                    row_counter += 1
                else:
                    end_pos = already_on["real"][already_on["copy"].index(return_con["to"][ret_num])]
                    self.add_connection(start_pos, end_pos)

            current_pos = []
            for pos_num in range(0, len(current_pos_next)):
                current_pos.append(current_pos_next[pos_num])
            current_pos_next = []

            col_counter += 1
            
            if len(current_pos) == 0:
                #if licznik == 4:
                adjustment = False
            else:
                licznik+=1

    def run(self, TI, TO, YLa, YLb, YLc):
        self.create_start( TI )
        self.create_end( TI, TO )
        self.create_patt_a( TI, TO, YLa )
        self.create_patt_b( YLb )
        self.create_patt_c( YLc )
        self.create_patt_d()
        self.create_patt_e()
        self.merge_exclusive()
        self.organize()
    
        return self.width, self.height

    def add_elem_on_board(self, elem_name, pos):
        """
        put elem surface and elem surface_rect into board on pos
        :param elem: name of element that will be added on board e.g "a"
        :param pos: position on the board on which the element is to be placed e.g [0, 5], 0 - row, 5 - col
        """
        #if (elem_name not in self.already_on) or (elem_name == "start" or elem_name == "end" or elem_name == "exclusive" or elem_name == "parallel"):
        if elem_name not in self.already_on:
            if self.get_activity(pos) == None:
                self._board[ pos[0] ][ pos[1] ] = elem_name 
                if elem_name != "start" and elem_name != "end" and elem_name != "exclusive" and elem_name != "parallel":
                    self.already_on.append(elem_name)
            else:
                print("you wanted to place: ", elem_name, " on place: ", pos[0], pos[1], " but there is already some surf")
        else:
            print("you wanted to place ", elem_name, "but it's already on board")

    def move_elem(self, from_pos, where_pos, old_one = False):
        if old_one:
            self._board[from_pos[0]][from_pos[1]] = None
        else:
            self._board[where_pos[0]][where_pos[1]] = self._board[from_pos[0]][from_pos[1]]
            self._board[from_pos[0]][from_pos[1]] = None
        
        to_delete = []
        for start_pos_num in range(0, len(self._connections["from"])):
            if from_pos == self._connections["from"][start_pos_num]:
                to_delete.append(start_pos_num)
                self.add_connection(where_pos, self._connections["to"][start_pos_num])
        for end_pos_num in range(0, len(self._connections["to"])):
            if from_pos == self._connections["to"][end_pos_num]:
                to_delete.append(end_pos_num)
                self.add_connection(self._connections["from"][end_pos_num], where_pos)
        to_delete.sort()
        for i in range(0, len(to_delete)):
            self._connections["from"] = self._connections["from"][0:to_delete[len(to_delete) - i - 1]] + self._connections["from"][to_delete[len(to_delete) - i - 1]+1:len(self._connections["from"])]
            self._connections["to"] = self._connections["to"][0:to_delete[len(to_delete) - i - 1]] + self._connections["to"][to_delete[len(to_delete) - i - 1]+1:len(self._connections["to"])]
        
    def move_all_right(self, start_col, how_much = 1):
        """moves all elements on board to the right starting from "start_width" column

        :param start_col: number of column from where all columns will be move to the right
        :param how_much: number of fileds that all element will be moved to the right
        """
        for shift_num in range(0, self.width - start_col - how_much ):
            for row_num in range(0, self.height):
                self.move_elem( [row_num, self.width - 1 - shift_num - how_much] , [row_num, self.width - 1 - shift_num])

    def find_in_board(self, name):
        """can find position of activity on the board when you give its name"""
        for row_num in range(0, len(self._board)):
            for col_num in range(0, len(self._board[row_num])):
                if self._board[row_num][col_num] == name:
                    return [row_num, col_num]

    def find_connections_to(self, end_pos, connections = None):
        if connections == None:
            connections = self._connections
        connections_to = []
        for con_num in range(0, len(connections["from"])):
            if connections["to"][con_num] == end_pos:
                connections_to.append( connections["from"][con_num] )
        return connections_to

    def find_connections_from(self, start_pos, connections = None):
        if connections == None:
            connections = self._connections
        connections_from = []
        for con_num in range(0, len(connections["to"])):
            if connections["from"][con_num] == start_pos:
                connections_from.append( connections["to"][con_num] )
        return connections_from

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
        not_double = True
        for conn_num in range(0, len( self._connections['from'] ) ):
            if self._connections['from'][conn_num] == start_pos and self._connections['to'][conn_num] == end_pos:
                not_double = False
        if not_double:
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
            self._board.append( [ None for i in range(0, len(self._board[0]) ) ] )

    def add_column(self, how_many = 1):
        for j in range(0, how_many):
            for i in range(0, self.height):
                self._board[i].append( None )

    def draw_line(self, surf, start_pos, end_pos, arrow = False, size = 3 ):
        if arrow:
            pg.draw.line( surf, (72, 144, 220), start_pos, end_pos, size )
            if start_pos[0] <= end_pos[0]:
                self.arrow_right_rect.right = end_pos[0]
                self.arrow_right_rect.top = end_pos[1] - self.arrow_right_rect.height/2 + 1
                surf.blit( self.arrow_right, self.arrow_right_rect )
            elif start_pos[0] > end_pos[0]:
                self.arrow_left_rect.left = end_pos[0]
                self.arrow_left_rect.top = end_pos[1] - self.arrow_left_rect.height/2 + 1
                surf.blit( self.arrow_left, self.arrow_left_rect )
        else:
            pg.draw.line(surf, (72, 144, 220), start_pos, end_pos, size)

    def draw_on(self, surf):
        """drawing BPMN model on given surface
        
        :param surface: surface on which the BPMN model will be drawn"""
        
        #bliting activities, events ....
        for c in range(0, len(self._board)):
            for r in range(0, len(self._board[c])):
                if self._board[c][r] != None:#If there is name on possition
                    elem_surf, elem_surf_rect = self.get_activity_surf( self._board[c][r] )
                    elem_surf_rect.center = self.ele_pos(surf, [c, r])
                    surf.blit( elem_surf, elem_surf_rect )


        #bliting connections
        for connection_num in range(0, len(self._connections["from"]) ):
            move_start = [0,0]
            move_end = [0,0]
            
            start_pos = self.ele_pos( surf, self._connections["from"][connection_num] )
            if self.get_activity_surf(self.get_activity( self._connections["from"][connection_num] )) != None:
                start_surf, start_surf_rect = self.get_activity_surf(self.get_activity( self._connections["from"][connection_num] ))
            else:
                print("you try to get activity surf of start element with pos", self._connections["from"][connection_num], " but on this pos there is no elem")
            
            end_pos = self.ele_pos( surf, self._connections["to"][connection_num] )
            if self.get_activity_surf( self.get_activity( self._connections["to"][connection_num] )) != None:
                end_surf, end_surf_rect = self.get_activity_surf( self.get_activity( self._connections["to"][connection_num] )) #connection must end before activity, not in middle
            else:
                print("you try to get activity surf of end element with pos", self._connections["to"][connection_num], " but on this pos there is no elem")
            
            #start elements
            #start element is "start"
            if self._board[ self._connections["from"][connection_num][0] ][ self._connections["from"][connection_num][1] ] == "start":
                if start_pos[1] == end_pos[1]:
                    move_start[0] += 10
                    move_start[1] -= 10
                elif start_pos[1] < end_pos[1]:
                    move_start[0] += 15
                
            #start element is exlucsive or parallel
            elif self._board[ self._connections["from"][connection_num][0] ][ self._connections["from"][connection_num][1] ] == "exclusive"\
                or self._board[ self._connections["from"][connection_num][0] ][ self._connections["from"][connection_num][1] ] == "parallel":
                if start_pos[0] < end_pos[0]: 
                    if start_pos[1] >= end_pos[1]:
                        move_start[0] += 10
                        move_start[1] -= 10
                    elif start_pos[1] < end_pos[1]:
                        move_start[0] += 20
                elif start_pos[0] == end_pos[0]:
                    move_start[0] += 10
                    move_start[1] += 10
                elif start_pos[0] > end_pos[0]:
                    move_start[0] -= 10
                    move_start[1] += 10
                    #move_start[1] -= 10
            #start element is smth else then start, exclusive, parallel
            else:
                if start_pos[0] < end_pos[0]:#end element is to the right of the start element
                    if start_pos[1] < end_pos[1]:#end element is to the RIGHT-DOWN of the start element
                        move_start[0] += start_surf_rect.width/2
                    elif start_pos[1] == end_pos[1]:#end element is to the RIGHT-MID of the start element
                        move_start[0] += start_surf_rect.width/4
                        move_start[1] -= start_surf_rect.height/2
                    elif start_pos[1] > end_pos[1]:#end element is to the RIGHT-TOP of the start element
                        move_start[0] += start_surf_rect.width/4
                        move_start[1] -= start_surf_rect.height/2
                elif start_pos[0] == end_pos[0]:#end element is to the RIGHT/UP of the start element
                    if start_pos[1] < end_pos[1]:#end element is to the LEFT-DOWN of the start element
                        move_start[1] += start_surf_rect.height/2
                    elif start_pos[1] > end_pos[1]:#end element is to the LEFT-TOP of the start element
                        move_start[1] -= start_surf_rect.height/2
                elif start_pos[0] > end_pos[0]:#end element is to the LEFT of the start element
                    if start_pos[1] < end_pos[1]:#end element is to the LEFT-DOWN of the start element
                        move_start[1] += start_surf_rect.height/2
                    elif start_pos[1] == end_pos[1]:#end element is to the LEFT-MID of the start element
                        move_start[0] -= start_surf_rect.width/2
                    elif start_pos[1] > end_pos[1]:#end element is to the LEFT-TOP of the start element
                        move_start[0] -= start_surf_rect.width/4
                        move_start[1] -= start_surf_rect.height/2


            #end elements
            #end element is "end"
            if self._board[ self._connections["to"][connection_num][0] ][ self._connections["to"][connection_num][1] ] == "end":
                if start_pos[1] <= end_pos[1]:
                    move_end[0] -= 10
                    move_end[1] -= 10
                elif start_pos[1] > end_pos[1]:
                    move_end[0] -= 10
                    move_end[0] += 10
            #end element is exclusive or parallel
            elif self._board[ self._connections["to"][connection_num][0] ][ self._connections["to"][connection_num][1] ] == "exclusive" \
                or self._board[ self._connections["to"][connection_num][0] ][ self._connections["to"][connection_num][1] ] == "parallel":
                if start_pos[0] < end_pos[0]:
                    if start_pos[1] <= end_pos[1]:
                        move_end[0] -= 10
                        move_end[1] -= 10
                    elif start_pos[1] > end_pos[1]:
                        move_end[0] -= 10
                        move_end[1] += 10
                elif start_pos[0] == end_pos[0]:
                    if start_pos[1] < end_pos[1]:
                        move_end[1] -= 15
                    elif start_pos[1] > end_pos[1]:
                        move_end[1] += 15
                elif start_pos[0] > end_pos[0]:
                    if start_pos[1] < end_pos[1]:
                        move_end[0] += 10
                        move_end[1] -= 10
                    elif start_pos[1] == end_pos[1]:
                        pass
                    elif start_pos[1] > end_pos[1]:
                        move_end[0] += 10
                        move_end[1] += 10

            #end element is smth else then exclusive or parallel
            else:
                if start_pos[0] < end_pos[0]:#end element is to the right of the start element
                    if start_pos[1] < end_pos[1]:#end element is to the RIGHT-DOWN of the start element
                        move_end[0] -= end_surf_rect.width/4
                        move_end[1] -= end_surf_rect.height/2
                    elif start_pos[1] == end_pos[1]:#end element is to the RIGHT-MID of the start element
                        move_end[0] -= end_surf_rect.width*3/8
                        move_end[1] -= end_surf_rect.height/2 + 2 
                    elif start_pos[1] > end_pos[1]:#end element is to the RIGHT-TOP of the start element
                        move_end[0] -= end_surf_rect.width/2
                elif start_pos[0] == end_pos[0]:#end element is to the RIGHT/UP of the start element
                    if start_pos[1] < end_pos[1]:
                        move_end[0] += end_surf_rect.width/4
                        move_end[1] -= end_surf_rect.height/2
                    elif start_pos[1] == end_pos[1]:
                        pass#cant be ! 
                    elif start_pos[1] > end_pos[1]:
                        move_end[0] += end_surf_rect.width/4
                        move_end[1] += end_surf_rect.height/2
                elif start_pos[0] > end_pos[0]:#end element is to the LEFT of the start element
                    if start_pos[1] < end_pos[1]:#end element is to the LEFT-DOWN of the start element
                        move_end[0] += end_surf_rect.width/2
                    elif start_pos[1] == end_pos[1]:#end element is to the LEFT-MID of the start element
                        move_end[0] += end_surf_rect.width*3/8
                        move_end[1] += end_surf_rect.height/2 + 2
                    elif start_pos[1] > end_pos[1]:#end element is to the LEFT-TOP of the start element
                        move_end[0] += end_surf_rect.width/4
                        move_end[1] += end_surf_rect.height/2

            # if connection_num >= 15 and connection_num < 22:
            #     #print(f'poczatek: {start_pos}, przesuniecie poczatek: {move_start}, koniec: {end_pos}, przesuniecie koniec: {move_end}')
            #     print(f'poczatek: ({start_pos[0]+move_start[0]},{start_pos[1]+move_start[1]})   koniec: ({end_pos[0]+move_end[0]},{end_pos[1]+move_end[1]})')
            #     draw_arc(surf, [start_pos[0] + move_start[0], start_pos[1] + move_start[1]], [end_pos[0] + move_end[0], end_pos[1] + move_end[1]], arc_color = (200,0,0) )
            # else:
            #     draw_arc(surf, [start_pos[0] + move_start[0], start_pos[1] + move_start[1]], [end_pos[0] + move_end[0], end_pos[1] + move_end[1]], arc_color = (0,200,0) )
        
            draw_arc(surf, [start_pos[0] + move_start[0], start_pos[1] + move_start[1]], [end_pos[0] + move_end[0], end_pos[1] + move_end[1]], arc_color = (200,0,0) )

        
        
