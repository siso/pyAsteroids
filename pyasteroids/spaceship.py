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

# import prj modules
from bullet import *
from constants import *
#from particle import *

class SpaceShip(pygame.sprite.Sprite):
    """SpaceShipobject

    It's the player's spaceship, used to fire the rocks.

    """
    def __init__(self, gameArea):
        #call Sprite initializer
        pygame.sprite.Sprite.__init__(self)

        # generate SpaceShip image
        self.points = ((0, 0), (10, 10), (0, 20), (30, 10))
        self.image = pygame.Surface((30,20))
        pygame.draw.polygon(self.image, pygame.Color(SPACESHIP_COLOR),
                            self.points, SPACESHIP_THICKNESS)
        self.rect = self.image.get_rect()
        self.image.set_colorkey(pygame.Color(SPACESHIP_COLORKEY),
                                pygame.RLEACCEL)
        self.image.convert()
        self.image_original = self.image
        self.score = 0

        # set boundaries
        self.gameArea = gameArea

        # spaceship model
        self.reset()

        self.use_antialias = GAME_USE_ANTIALIAS

    def reset(self):
        self.rect.center = self.gameArea.center
        self.image = self.image_original
        self.angle = 0
        self.velocity = Vector2(0.0, 0.0)
        self.moving = [None,None]   # ([CCW|None|CW], [FW|None|BW])
        self.exploding = False
        self.respawn_timeout = SPACESHIP_RESPAWN_TIMEOUT

    def __str__(self):
        s_out =     "** SPACESHIP **"
        s_out +=    "\tposition: (%d, %d)" % (self.rect.center)
        s_out +=    "\tvelocity: (%g, %g)" % (self.velocity.x, self.velocity.y)
        s_out +=    "\tangle: %g" % (self.angle)
        return s_out


    def update(self):
        """move the starship based on the mouse position"""

        if self.exploding:
            self._exploding()
        else:
            # rotation
            if self.moving[0] == 'CCW':
                self.rotate(SPACESHIP_ANGLE_STEP)
            elif self.moving[0] == 'CW':
                self.rotate(-1 * SPACESHIP_ANGLE_STEP)

            # moving forward/backward
            if self.moving[1] == 'FW':
                self.velocity += (Vector2(math.cos(math.radians(self.angle)),
                                         -1 * math.sin(math.radians(self.angle))
                                         ))
                if self.velocity.magnitude() > SPACESHIP_MAX_VELOCITY:
                    self.velocity = self.velocity.normalized() * SPACESHIP_MAX_VELOCITY
            elif self.moving[1] == 'BW':
                pass
            self.move()

    def control(self, event_type, event_key):
        if event_key == K_LEFT:
            if event_type == KEYDOWN:
                self.moving[0] = 'CCW'
            elif event_type == KEYUP:
                self.moving[0] = None
        elif event_key == K_RIGHT:
            if event_type == KEYDOWN:
                self.moving[0] = 'CW'
            elif event_type == KEYUP:
                self.moving[0] = None
        elif event_key == K_UP:
            if event_type == KEYDOWN:
                self.moving[1] = 'FW'
            elif event_type == KEYUP:
                self.moving[1] = None
        elif event_key == K_DOWN:
            if event_type == KEYDOWN:
                self.moving[1] = 'BW'
            elif event_type == KEYUP:
                self.moving[1] = None
        else:
            if pygame.key.get_mods() and (K_RCTRL | K_LCTRL):
                # "LEFT|RIGHT CTRL"
                self.fire()
            else:
                print "DUNNO WHAT TO DO!"

    def fire(self):
        print "fire"

    def move_to(self, pos):
        self.rect.center = pos

    def move(self):
        self.rect.move_ip(self.velocity.x, self.velocity.y)
        # spaceship re-enter the opposite side of the screen
        if self.rect.right < self.gameArea.left:
            self.rect.left = self.gameArea.right
        if self.rect.left > self.gameArea.right:
            self.rect.right = self.gameArea.left
        if self.rect.bottom < self.gameArea.top:
            self.rect.top = self.gameArea.bottom
        if self.rect.top > self.gameArea.bottom:
            self.rect.bottom = self.gameArea.top

    def rotate(self, angle_step):
        self.angle += angle_step
        if self.angle >= 360 or self.angle <= -360:
            self.angle = 0
            self.image = self.image_original
        else:
            self.image = pygame.transform.rotate(self.image_original,
                                                 self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def get_velocity_vector_surface(self):
        """NON FUNZIONA!!!!"""
        surface = pygame.Surface((SPACESHIP_MAX_VELOCITY,
                                  SPACESHIP_MAX_VELOCITY))
        rect = surface.get_rect()
        screen_center = (int(self.gameArea.w/2), int(self.gameArea.h/2))
        #print screen_center
        screen_velocity = (Vector2(screen_center[0], screen_center[1]) +
                           self.velocity)
        pygame.draw.circle(surface, pygame.Color('red'), screen_center, 3)
        pygame.draw.line(surface, pygame.Color('red'), screen_center,
                         (screen_velocity.x, screen_velocity.y), 3)
        return surface, surface.get_rect()

    def set_exploding(self, exploding = True):
        """set spaceship exploding status"""
        self.exploding = exploding

    def get_exploding(self):
        """return spaceship exploding status"""
        return self.exploding

    def explode(self):
        """explode event"""
        pos = self.rect.center
        #for i in range(15):
            #Particle(pos, self.gameArea)
        self.set_exploding(True)

    def _exploding(self):
        """handle exploding event

        draws exploding spaceship and then reset it

        """
        self.respawn_timeout -= 1
        if self.respawn_timeout > 0:
            print "debug: spaceship exploding"
        else:
            print "debug: spaceship respawn"
            # reset the spaceship
            self.reset()

    def fire_bullet(self):
        """build a bullet based on spaceship position and velocity"""
        #print self
        return Bullet(self.gameArea, self.rect.center,
                      Vector2(math.cos(math.radians(self.angle)),
                              -1.0 * math.sin(math.radians(self.angle))))

    def add_to_score(self, i):
        """add i points to score"""
        self.score += i

    def get_score(self):
        """return score"""
        return self.score

    def hyperspace(self):
        """spaceship goes hyperspace!"""
        self.rect.center = (random.randint(self.gameArea[0], self.gameArea[2]),
                            random.randint(self.gameArea[1], self.gameArea[3]))
        self.image = self.image_original
        self.image = pygame.transform.rotate(self.image_original, self.angle)
