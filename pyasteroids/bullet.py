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

#Import Modules
import os, pygame, sys, math, random
from pygame.locals import *
from euclid import *

# import prj modules
from constants import *

class Bullet(pygame.sprite.Sprite):
    """Spaceship fires this bullet"""
    def __init__(self, gameArea, pos, velocity):
        """initialize a Bullet object"""
        pygame.sprite.Sprite.__init__(self)

        # set boundaries
        self.gameArea = gameArea

        # generate rock image
        self.image = pygame.Surface((BULLET_RADIOUS * 2, BULLET_RADIOUS * 2))
        self.rect = self.image.get_rect()
        #self.pos = ((rect[0] + rect[2]) / 2, (rect[1] + rect[3]) / 2)
        pygame.draw.circle(self.image, pygame.Color(BULLET_COLOR),
                           self.rect.center, BULLET_RADIOUS, BULLET_THICKNESS)
        self.image.set_colorkey(pygame.Color(BULLET_COLOR_KEY), pygame.RLEACCEL)
        self.image.convert()

        # sets bullet position and velocity normalized
        self.rect.center = pos
        self.velocity = velocity.normalized() * BULLET_VELOCITY

        # bullet frames-to-live
        self.framesToLive = BULLET_FRAMESTOLIVE

        self.use_antialias = GAME_USE_ANTIALIAS

    def __str__(self):
        s_out = "** " + type(self) + " **"
        s_out += "\tpos = (%d,%d)" % self.rect.center
        s_out += "\tvelocity = (%g,%g)" % (self.velocity.x, self.velocity.y)
        return s_out

    def update(self):
        self.framesToLive -= 1
        if self.framesToLive > 0:
            self.move()
        else:
            # destroy this object
            self.kill()

    def move(self):
        # brutto! e'     lo stesso codice della classe SpaceShip
        self.rect.move_ip(self.velocity.x, self.velocity.y)
        # bullet re-enter the opposite side of the screen
        if self.rect.right < self.gameArea.left:
            self.rect.left = self.gameArea.right   # exit left: ok
        if self.rect.left > self.gameArea.right:
            self.rect.right = self.gameArea.left   # exit right: --
        if self.rect.bottom < self.gameArea.top:
            self.rect.top = self.gameArea.bottom   # exit top: ok
        if self.rect.top > self.gameArea.bottom:
            self.rect.bottom = self.gameArea.top   # exit bottom: ok
