# -*- coding: utf-8 -*-

# This file is part of pyAsteroids.
#
# pyAsteroids is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# pyAsteroids is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with pyAsteroids.  If not, see <http://www.gnu.org/licenses/>.

import os, pygame, sys, math, random
from pygame.locals import *
from euclid import *

from constants import *

class Rock(pygame.sprite.Sprite):
    """rock"""
    def __init__(self, gameArea, pos = None, velocity = None,
                 radious = ROCK_RADIOUS_MAX):
        """initialize a Rock object

        Keyword arguments:
        gameArea -- pygame.Rect which defines the area in which the Rock can move
        pos -- tuple (x, y): initial position
        velocity -- euclid.Vector2(x, y): initial velocity
        radious -- rock radious
        """
        # call Sprite initializer
        pygame.sprite.Sprite.__init__(self)

        # set boundaries
        self.gameArea = gameArea

        # position
        if pos == None:
            pos = (random.randint(gameArea[0],gameArea[2]),
                   random.randint(gameArea[1],gameArea[3]))

        # velocity
        if velocity == None:
            self.velocity = (Vector2(random.randint(-ROCK_VELOCITY_MAX,
                                                    ROCK_VELOCITY_MAX),
                                     random.randint(-ROCK_VELOCITY_MAX,
                                                    ROCK_VELOCITY_MAX)))
        else:
            self.velocity = velocity

        # radious
        self.radious = radious

        # generate rock image and position it
        self.image, self.rect = self._surface_factory()
        self.rect.center = pos

        self.use_antialias = GAME_USE_ANTIALIAS

    def _surface_factory(self):
        """builds main surface, returns it and the rect"""

        # randomize rock vertexes (radious) with gauss distribution
        gauss_mean = self.radious
        gauss_variance = ROCK_RADIOUS_VARIANCE
        vertexes_list = list()
        angle = 0
        radious = math.fabs(random.gauss(gauss_mean, gauss_variance))
        vertexes_list.append((int(radious * math.cos(angle)),
                              int(radious * math.sin(angle))))
        for i in xrange(ROCK_SEGMENTS - 1):
            angle += 2.0 * math.pi / ROCK_SEGMENTS
            radious = math.fabs(random.gauss(gauss_mean, gauss_variance))
            vertexes_list.append((int(radious * math.cos(angle)), int(radious * math.sin(angle))))

        # shift vertexes to SDL coordinate-system
        x_min, y_min, x_max, y_max = (None, None, None, None)
        for i in xrange(len(vertexes_list)):
            if x_min == None or x_min > vertexes_list[i][0]:
                x_min = vertexes_list[i][0]
            if y_min == None or y_min > vertexes_list[i][1]:
                y_min = vertexes_list[i][1]
            if x_max == None or x_max < vertexes_list[i][0]:
                x_max = vertexes_list[i][0]
            if y_max == None or y_max < vertexes_list[i][1]:
                y_max = vertexes_list[i][1]
        
        for i in xrange(len(vertexes_list)):
            vertexes_list[i] = (vertexes_list[i][0] + int(math.fabs(x_min)),
                                vertexes_list[i][1] + int(math.fabs(y_min)))

        # recalculate image rect
        x_min, y_min, x_max, y_max = (0, 0, x_max + int(math.fabs(x_min)),
                                      y_max + int(math.fabs(y_min)))

        # create surface which fits the polygon
        image = pygame.Surface((x_max + 1, y_max + 1))

        # draw vertexes on surface
        rect = pygame.draw.polygon(image, pygame.Color(ROCK_COLOR),
                                   vertexes_list, ROCK_THICKNESS)

        image.set_colorkey(pygame.Color(ROCK_COLOR_KEY), pygame.RLEACCEL)
        image.convert()
        return (image, rect)

    def __str__(self):
        s_out = "** ROCK **"
        s_out += "\tpos = (%d,%d)" % self.rect.center
        s_out += "\tvelocity = (%g,%g)" % (self.velocity.x, self.velocity.y)
        return s_out


    def update(self):
        self.move()

    def move(self):
        self.rect.move_ip(self.velocity.x, self.velocity.y)
        # rock re-enter the opposite side of the screen
        if self.rect.right < self.gameArea.left:
            self.rect.left = self.gameArea.right
        if self.rect.left > self.gameArea.right:
            self.rect.right = self.gameArea.left
        if self.rect.bottom < self.gameArea.top:
            self.rect.top = self.gameArea.bottom
        if self.rect.top > self.gameArea.bottom:
            self.rect.bottom = self.gameArea.top

    def get_radious(self):
        return self.radious

    def get_pos(self):
        return self.rect.center
