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

"""
simple asteroids-like game
"""


#Import Modules
import os, pygame, sys, math, random
from pygame.locals import *
from euclid import *

# import prj modules
from constants import *
#from menu import *
##import menu
import mainmenu
from rock import *
from spaceship import *
from utils import *

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

class Game:
    """Game class"""
    def __init__(self, screen):
        self.screen = screen
        self.level = 1
        self.d_sounds = {}
        load_sounds(self.d_sounds)
        print '**' + str(self.d_sounds) + '**'
        
        # background
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill(pygame.Color(SCREEN_BACKGROUND_COLOR))
    
    def run(self, level = 1):
        """Game main method"""
        
        # game clock
        clock = pygame.time.Clock()

        # hide mouse pointer
        pygame.mouse.set_visible(False)

        # test font system
        if pygame.font.get_init() == True:
            print "font system initialized"
        else:
            print "font system not initialized"

        # generating objects
        self.spaceship = SpaceShip(self.screen.get_rect())

        # generating groups of sprites
        self.group_bullets = pygame.sprite.RenderUpdates()
        self.group_rocks = pygame.sprite.RenderUpdates()
        for i in xrange(self.level):
            self.group_rocks.add(Rock(self.screen.get_rect()))
        self.group_spaceship = pygame.sprite.Group((self.spaceship))

        # initial position for the objects
        self.spaceship.move_to((self.screen.get_rect()[2] / 2,
                                self.screen.get_rect()[3] / 2))

        # set players vars
        self.player_lives = PLAYER_LIVES

        # set lives surface
        if pygame.font:
            (lives_surface, lives_rect) = self.get_lives_surface()
            (score_surface, score_rect) = self.get_lives_surface()

        self.show_message("get ready", timeout = 1)

        while True:
            # time-ticks
            clock.tick(GAME_FRAMERATE)

            # handle events
            self.input(pygame.event.get())
            
            # update sprite groups
            self.group_rocks.update()
            self.group_spaceship.update()
            self.group_bullets.update()

            # draw everything
            self.screen.blit(self.background, (0, 0))
            self.group_bullets.draw(self.screen)
            self.group_rocks.draw(self.screen)
            if not self.spaceship.get_exploding():
                self.group_spaceship.draw(self.screen)

            # update score
            if pygame.font:
                (score_surface, score_rect) = self.get_score_surface()

            # update game status
            if self.player_lives == 0:
                self.screen.blit(self.background, (0, 0)) # blank bg
                self.show_message("GAME OVER", timeout = 2)
                mainmenu.MainMenu(self.screen)

            if len(self.group_rocks.sprites()) == 0:
                self.screen.blit(self.background, (0, 0)) # blank bg
                self.show_message("LEVEL CLEAR", timeout = 2)
                self.level += 1
                self.group_bullets.empty()
                self.group_rocks.empty()
                for i in xrange(self.level):
                    self.group_rocks.add(Rock(self.screen.get_rect()))
                self.spaceship.reset()

            # collision spaceship-rocks
            if (self.spaceship.get_exploding() == False and
                pygame.sprite.spritecollideany(self.spaceship, self.group_rocks)):
                print "debug: spaceship hits a rock!"
                self.player_lives -= 1
                self.spaceship.explode()
                # update lives surface
                if pygame.font:
                    (lives_surface, lives_rect) = self.get_lives_surface()

            # collision bullets-rocks
            dict_bullets_rocks_collision = pygame.sprite.groupcollide(self.group_bullets, self.group_rocks, True, True)
            if len(dict_bullets_rocks_collision) > 0:
                # a bullet collides with one or more rocks
                # every rock will be divided in two half-rock until it reaches ROCK_MIN_RADIOUS
                for b in dict_bullets_rocks_collision:
                    for r in dict_bullets_rocks_collision[b]:
                        # rock explosion and division
                        r_pos = r.get_pos()
                        r_radious = r.get_radious()
                        self.group_rocks.remove(r)
                        # score
                        self.spaceship.add_to_score(ROCK_RADIOUS_MAX - r_radious + ROCK_RADIOUS_MIN)
                        del(r)
                        if r_radious > ROCK_RADIOUS_MIN:
                            self.group_rocks.add(Rock(self.screen.get_rect(), pos = r_pos, radious = r_radious / 2))
                            self.group_rocks.add(Rock(self.screen.get_rect(), pos = r_pos, radious = r_radious / 2))
                    # destroy bullet
                    self.group_bullets.remove(b)
                    del(b)

            # text on screen
            if pygame.font:
                self.screen.blit(lives_surface, lives_rect)
                self.screen.blit(score_surface, score_rect)
                if self.spaceship.get_exploding():
                    self.screen.blit(*self.get_message_surface('spaceship destroyed! :(', position = self.screen.get_rect().center))

            # flip
            pygame.display.flip()


    def input(self, events):
        """input handler method

        This method handles all user's input and passes them to the right game object.

        """
        for event in events:
            if event.type == QUIT:
                sys.exit(0)
            elif event.type == KEYDOWN:
                if (event.key == K_q) or (event.key == K_ESCAPE):
                    #print 'q/Q/Esc'
                    if pygame.key.get_mods() & (KMOD_LSHIFT | KMOD_SHIFT):
                        # panic quit
                        pygame.event.post(pygame.event.Event(QUIT))
                    e = self.show_message("quit game [y/n]?",
                                          allowed_keys = [K_y, K_n, K_ESCAPE])
                    if e.key == K_y:
                        mainmenu.MainMenu(self.screen)
                elif (event.key == K_LEFT or event.key == K_RIGHT or
                      event.key == K_UP or event.key == K_DOWN):
                    self.spaceship.control(event.type, event.key)
                if pygame.key.get_mods() & (KMOD_LCTRL | KMOD_RCTRL):
                    if not self.spaceship.get_exploding():
                        bullet = self.spaceship.fire_bullet()
                        bullet.add(self.group_bullets)
                        self.d_sounds['shoot'].play()
                if pygame.key.get_mods() & (KMOD_LALT | KMOD_RALT):
                    self.spaceship.hyperspace()
            elif event.type == KEYUP:
                if (event.key == K_LEFT or event.key == K_RIGHT or
                    event.key == K_UP or event.key == K_DOWN):
                    self.spaceship.control(event.type, event.key)
            else:
                pass

    def get_lives_surface(self):
        """Updates lives surface.

        returns surface with updated lives

        """
        font = pygame.font.Font(None, 18)
        text = font.render("lives: " + str(self.player_lives), 1,
                           pygame.Color(LIVES_SURFACE_COLOR))
        textpos = text.get_rect()
        textpos.topleft = LIVES_SURFACE_POS
        return (text, textpos)

    def get_score_surface(self):
        """Updates score surface.

        returns surface with updated score

        """
        font = pygame.font.Font(None, 18)
        text = font.render("spaceships: " + str(self.spaceship.get_score()), 1,
                           pygame.Color(LIVES_SURFACE_COLOR))
        textpos = text.get_rect()
        textpos.topright = (SCREEN_WIDTH - 5, 5)
        return (text, textpos)

    def get_message_surface(self, msg, position = None):
        """render message to surface"""
        font = load_font(FONT_NAME_DEFAULT, 18)
        text = font.render(msg, 1, pygame.Color(GAME_TEXT_COLOR))
        text_rect = text.get_rect()
        if position != None:
            text_rect.center = position
        return (text, text_rect)

    def show_message(self, msg, position = None, allowed_keys = None,
                     timeout = 0):
        """shows a message and wait for user's input

        text -- text string or list of text strings to render
        position -- (x, y) (default is center of the screen)
        allowed_keys -- key that user is allowed to type (defining 'allowed_keys' disable 'timeout')
        timeout -- timeout of the message in seconds, 0 to disable
        """
        if position == None: position = self.screen.get_rect().center

        # creating the rendered text
        #font = pygame.font.Font(None, 18)
        #text = font.render(msg, 1, pygame.Color(GAME_TEXT_COLOR))
        #text_rect = text.get_rect()
        text, text_rect = self.get_message_surface(msg)
        text_rect.topleft = position
        self.screen.blit(text, text_rect)
        pygame.display.flip()

        if allowed_keys == None:
            pygame.time.delay(timeout * 1000)
        else:
            while True:
                # handle events
                for event in pygame.event.get():
                    if event.type == KEYDOWN:
                        if event.key in (allowed_keys):
                            return event
