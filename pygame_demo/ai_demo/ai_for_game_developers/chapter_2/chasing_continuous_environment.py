#!/usr/bin/env python
# -*- coding: utf-8 -*-


import pygame
from pygame.locals import *
from random import randint
from time import ctime,sleep
import math

pygame.init()

# 30 * 30
row = 30
col = 30

# 每个方块宽高都是20px
square_width = 20
screen = pygame.display.set_mode((row * square_width, col * square_width), 0, 32)

# 定义一些颜色
white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
deep_sky_blue = (0, 191, 255)
red = (255, 0, 0)

class Boat(object):
    def __init__(self, x, y, direction, boat_length, boat_width, speed=10, color=deep_sky_blue):
        self.center_x = x
        self.center_y = y
        self.direction = direction
        self.boat_length = boat_length
        self.boat_width = boat_width
        self.color = color
        self.border_width = 1
        self.speed = speed


boat1 = Boat(100, 100, 30, 40, 20, 10)

def draw_boat(screen, boat):
    # 绘制多边形
    center_x = boat.center_x
    center_y = boat.center_y
    boat_length = boat.boat_length
    boat_width = boat.boat_width

    width = 1
    color = boat.color

    #boat_length边与x轴的夹角
    angle_degrees = boat.direction

    #对角线
    diagonal = math.sqrt(boat_length ** 2 + boat_width ** 2)
    #对角线与boat_length边的夹角
    #弧度
    angle1_radians = math.atan(boat_width * 1.0/boat_length)
    angle1_degrees = math.degrees(angle1_radians)
    #对角线与x轴夹角
    angle2_degrees = angle_degrees - angle1_degrees

    p4 = {}
    p4['x'] = center_x + diagonal * 0.5 * math.cos(math.radians(angle2_degrees))
    p4['y'] = center_y + diagonal * 0.5 * math.sin(math.radians(angle2_degrees))

    angle3_degrees = angle_degrees + angle1_degrees
    p2 = {}
    p2['x'] = center_x + diagonal * 0.5 * math.cos(math.radians(angle3_degrees))
    p2['y'] = center_y + diagonal * 0.5 * math.sin(math.radians(angle3_degrees))

    p3 = {}
    p3['x'] = center_x + (boat_length + boat_width) * 0.5 * math.cos(math.radians(angle_degrees))
    p3['y'] = center_y + (boat_length + boat_width) * 0.5 * math.sin(math.radians(angle_degrees))

    # 对称性
    p1 = {}
    p1['x'] = center_x * 2 - p4['x']
    p1['y'] = center_y * 2 - p4['y']

    p5 = {}
    p5['x'] = center_x * 2 - p2['x']
    p5['y'] = center_y * 2 - p2['y']

    # pygame.draw.circle
    # 原型：pygame.draw.circle(Surface, color, pos, radius, width=0): return Rect
    # 当不传入width参数的时候，绘制的是一个填充了的圆
    #pygame.draw.circle(screen, color, position, radius)
    # Rect(left,top,width,height)用来定义位置和宽高
    #pygame.draw.rect(screen, color, [p1['x'], p1['y'], boat_length, boat_width], 0)
    # polygon存在锯齿
    #pygame.draw.polygon(screen, color, [(p1['x'], p1['y']), (p2['x'], p2['y']), (p3['x'], p3['y']), (p4['x'], p4['y']), (p5['x'], p5['y'])], 0)
    # 消除锯齿
    pygame.draw.aalines(screen, color, True, [(p1['x'], p1['y']), (p2['x'], p2['y']), (p3['x'], p3['y']), (p4['x'], p4['y']), (p5['x'], p5['y'])], 1)
    # 画出中心
    pygame.draw.aaline(screen, color, (center_x, center_y), (center_x, center_y), 1)

# 移动向量(delta_row, delta_col)
move = (0, 0)

# 追逐者的路径
path = [(0, 0)]


# 计算巨人移动方向的bresenham算法，会以起点（ball1）和终点（ball2）为数据，算出ball1要走的一连串步伐，使其能以一连串步伐走向ball2。
# 每次ball2移动位置，都需要重新调用这个方法一遍来计算步伐
def chase_bresenham(ball1, ball2):
    # 计算移动方向
    delta_row = ball2.current_row_index - ball1.current_row_index
    delta_col = ball2.current_col_index - ball1.current_col_index

    if delta_row == 0 and delta_col == 0:
        return (0, 0)

    if math.fabs(delta_row) > math.fabs(delta_col):
        move = (int(delta_row/math.fabs(delta_row)), 0)
    elif math.fabs(delta_row) < math.fabs(delta_col):
        move = (0, int(delta_col / math.fabs(delta_col)))
    else:
        move = (int(delta_row/math.fabs(delta_row)), int(delta_col / math.fabs(delta_col)))

    return move


while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                # 船的角度
                boat1.direction -= 5

            elif event.key == K_RIGHT:
                # 船的角度
                boat1.direction += 5

            elif event.key == K_UP:
                boat1.speed += 1

            elif event.key == K_DOWN:
                boat1.speed -= 1

        elif event.type == KEYUP:
            # 如果用户放开了键盘，图就不要动了
            move = (0, 0)

    # 计算运动
    speed = boat1.speed
    angle_degrees = boat1.direction
    speed_x = speed * math.cos(math.radians(angle_degrees))
    speed_y = speed * math.sin(math.radians(angle_degrees))

    boat1.center_x = boat1.center_x + speed_x
    boat1.center_y = boat1.center_y + speed_y

    # 绘制白色背景色
    screen.fill(white)
    # 绘制boat1
    draw_boat(screen, boat1)

    pygame.display.update()
    sleep(0.5)