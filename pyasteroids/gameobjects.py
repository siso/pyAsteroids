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


class Particle(pygame.sprite.Sprite):

    def __init__(self, pos, gameArea):
        #call Sprite initializer
        pygame.sprite.Sprite.__init__(self)

        print str(pos)
        self.pos = pos
        self.gameArea = gameArea
        self.size = [1, 1]
        self.velocity = Vector2(random.random() * 5.0, random.random() * 5.0)
        self.color = 255

    def update(self):
        self.pos[0] += self.vx
        self.pos[1] += self.vy

        self.color -= 3
        if self.color <= 50:
            self.kill()

        if self.pos[0] < self.gameArea[0] or self.pos[0] > self.gameArea[2]:
            self.kill()
        if self.pos[1] < self.gameArea[1] or self.pos[1] > self.gameArea[3]:
            self.kill()

    def draw(self, surface):
        if self.use_antialias:
            surface.fill((self.color, self.color, self.color),
                         (int(self.pos[0]), int(self.pos[1]), self.size[0],
                          self.size[1]))
        else:
            surface.fill((200, 200, 200), (int(self.pos[0]), int(self.pos[1]),
                                           self.size[0], self.size[1]))
