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


# Import Modules
import os, pygame, sys, math, random
from pygame.locals import *
from euclid import *

# import prj modules
from constants import *
from gameobjects import *
from menu import *
from utils import *

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'


class GameObject(pygame.sprite.Sprite):
    """
    implements a game object from which every other object inherits
    """
    def __init__(self, gameArea, pos, velocity):
        pass

    def _surface_factory(self):
        """renders object shape to a pygame surface"""
        pass

    def update(self):
        pass


class Bullet(pygame.sprite.Sprite):
    """
    Spaceship fires this bullet
    """
    def __init__(self, gameArea, pos, velocity):
        """initialise a Bullet object"""
        pygame.sprite.Sprite.__init__(self)

        # set boundaries
        self.gameArea = gameArea

        # generate rock image
        self.image = pygame.Surface((BULLET_RADIOUS * 2, BULLET_RADIOUS * 2))
        self.rect = self.image.get_rect()
        pygame.draw.circle(self.image, pygame.Color(BULLET_COLOR),
                           self.rect.center, BULLET_RADIOUS, BULLET_THICKNESS)
        self.image.set_colorkey(pygame.Color(BULLET_COLOR_KEY), pygame.RLEACCEL)
        self.image.convert()

        # sets bullet position and velocity normalised
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
        self.rect.move_ip(self.velocity.x, self.velocity.y)
        # bullet re-enter the opposite side of the screen
        if self.rect.right < self.gameArea.left:
            self.rect.left = self.gameArea.right  # exit left: ok
        if self.rect.left > self.gameArea.right:
            self.rect.right = self.gameArea.left  # exit right: --
        if self.rect.bottom < self.gameArea.top:
            self.rect.top = self.gameArea.bottom  # exit top: ok
        if self.rect.top > self.gameArea.bottom:
            self.rect.bottom = self.gameArea.top  # exit bottom: ok


class Rock(pygame.sprite.Sprite):
    """
    A random moving rock
    """
    def __init__(self, gameArea, pos=None, velocity=None, radius=ROCK_RADIOUS_MAX):
        """
        initialize a Rock object

        Keyword arguments:
        gameArea -- pygame.Rect which defines the area in which the Rock can move
        pos -- tuple (x, y): initial position
        velocity -- euclid.Vector2(x, y): initial velocity
        radius -- rock radius
        """
        # call Sprite initializer
        pygame.sprite.Sprite.__init__(self)

        # set boundaries
        self.gameArea = gameArea

        # position
        if pos == None:
            pos = (random.randint(gameArea[0], gameArea[2]),
                   random.randint(gameArea[1], gameArea[3]))

        # velocity
        if velocity == None:
            self.velocity = Vector2(random.randint(-ROCK_VELOCITY_MAX,
                                                   ROCK_VELOCITY_MAX),
                                    random.randint(-ROCK_VELOCITY_MAX,
                                                   ROCK_VELOCITY_MAX))
        else:
            self.velocity = velocity

        # radius
        self.radius = radius

        # generate rock image and position it
        self.image, self.rect = self._surface_factory()
        self.rect.center = pos

        self.use_antialias = GAME_USE_ANTIALIAS

    def _surface_factory(self):
        """
        builds main surface, returns it and the rect
        """
        # randomise rock vertexes (radius) with gauss distribution
        gauss_mean = self.radius
        gauss_variance = ROCK_RADIOUS_VARIANCE
        vertexes_list = list()
        angle = 0
        radius = math.fabs(random.gauss(gauss_mean, gauss_variance))
        vertexes_list.append((int(radius * math.cos(angle)),
                              int(radius * math.sin(angle))))
        for i in xrange(ROCK_SEGMENTS - 1):
            angle += 2.0 * math.pi / ROCK_SEGMENTS
            radius = math.fabs(random.gauss(gauss_mean, gauss_variance))
            vertexes_list.append((int(radius * math.cos(angle)),
                                  int(radius * math.sin(angle))))

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
        rect = pygame.draw.polygon(image, pygame.Color(ROCK_COLOR), vertexes_list, ROCK_THICKNESS)

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
            self.rect.left = self.gameArea.right  # exit left: ok
        if self.rect.left > self.gameArea.right:
            self.rect.right = self.gameArea.left  # exit right: --
        if self.rect.bottom < self.gameArea.top:
            self.rect.top = self.gameArea.bottom  # exit top: ok
        if self.rect.top > self.gameArea.bottom:
            self.rect.bottom = self.gameArea.top  # exit bottom: ok

    def get_radius(self):
        return self.radius

    def get_pos(self):
        return self.rect.center


class SpaceShip(pygame.sprite.Sprite):
    """SpaceShipobject

    It's the player's spaceship, used to fire the rocks.

    """
    def __init__(self, gameArea):
        # call Sprite initializer
        pygame.sprite.Sprite.__init__(self)

        # generate SpaceShip image
        self.points = ((0, 0), (10, 10), (0, 20), (30, 10))
        self.image = pygame.Surface((30, 20))
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
        self.moving = [None, None]  # ([CCW|None|CW], [FW|None|BW])
        self.exploding = False
        self.respawn_timeout = SPACESHIP_RESPAWN_TIMEOUT

    def __str__(self):
        s_out = "** SPACESHIP **"
        s_out += "\tposition: (%d, %d)" % (self.rect.center)
        s_out += "\tvelocity: (%g, %g)" % (self.velocity.x, self.velocity.y)
        s_out += "\tangle: %g" % (self.angle)
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
                # multiply by '-1', as y-axis grows contrary to cartesian y-axis
                self.velocity += Vector2(math.cos(math.radians(self.angle)),
                                         -1 * math.sin(math.radians(self.angle))
                                         )
                if self.velocity.magnitude() > SPACESHIP_MAX_VELOCITY:
                    # limit spaceship speed if max reached
                    # (just kidding! :D)
                    self.velocity = (self.velocity.normalized() *
                                     SPACESHIP_MAX_VELOCITY)
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
            self.rect.left = self.gameArea.right  # exit left: ok
        if self.rect.left > self.gameArea.right:
            self.rect.right = self.gameArea.left  # exit right: --
        if self.rect.bottom < self.gameArea.top:
            self.rect.top = self.gameArea.bottom  # exit top: ok
        if self.rect.top > self.gameArea.bottom:
            self.rect.bottom = self.gameArea.top  # exit bottom: ok

    def rotate(self, angle_step):
        self.angle += angle_step
        if self.angle >= 360 or self.angle <= -360:
            self.angle = 0
            self.image = self.image_original
        else:
            self.image = pygame.transform.rotate(self.image_original, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def get_velocity_vector_surface(self):
        """TO FIX"""
        surface = pygame.Surface((SPACESHIP_MAX_VELOCITY,
                                  SPACESHIP_MAX_VELOCITY))
        rect = surface.get_rect()
        screen_center = (int(self.gameArea.w / 2), int(self.gameArea.h / 2))
        # print screen_center
        screen_velocity = (Vector2(screen_center[0], screen_center[1]) +
                           self.velocity)
        # print screen_velocity
        pygame.draw.circle(surface, pygame.Color('red'), screen_center, 3)
        pygame.draw.line(surface, pygame.Color('red'), screen_center,
                         (screen_velocity.x, screen_velocity.y), 3)
        return surface, surface.get_rect()

    def set_exploding(self, exploding=True):
        """set spaceship exploding status"""
        self.exploding = exploding

    def get_exploding(self):
        """return spaceship exploding status"""
        return self.exploding

    def explode(self):
        """explode event"""
        pos = self.rect.center
        for i in range(15):
            Particle(pos, self.gameArea)
        self.set_exploding(True)

    def _exploding(self):
        """handle exploding event

        draws exploding spaceship and then reset it

        """
        self.respawn_timeout -= 1
        if self.respawn_timeout > 0:
            print "debug: spaceship exploding"
        else:
            print "debug: spaceship respawned"
            # reset the spaceship
            self.reset()

    def fire_bullet(self):
        """build a bullet based on spaceship position and velocity"""
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

class Game:
    """Game class"""
    def __init__(self, screen):
        self.screen = screen
        self.level = 1

    def run(self, level=1):
        """Game main method"""

        # background
        background = pygame.Surface(self.screen.get_size())
        background = background.convert()
        background.fill(pygame.Color(SCREEN_BACKGROUND_COLOR))

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
        # print screen.get_rect()

        # set players vars
        self.player_lives = PLAYER_LIVES

        # set lives surface
        if pygame.font:
            (lives_surface, lives_rect) = self.get_lives_surface()
            (score_surface, score_rect) = self.get_lives_surface()

        self.show_message("get ready", timeout=1)

        while True:
            # time-ticks
            clock.tick(GAME_FRAMERATE)

            # handle events
            self.input(pygame.event.get())

            self.group_bullets.update()
            self.group_rocks.update()
            self.group_spaceship.update()

            # draw everything
            self.screen.blit(background, (0, 0))
            self.group_bullets.draw(self.screen)
            self.group_rocks.draw(self.screen)
            if not self.spaceship.get_exploding():
                self.group_spaceship.draw(self.screen)

            # update score
            if pygame.font:
                (score_surface, score_rect) = self.get_score_surface()

            # update game status
            if self.player_lives == 0:
                self.show_message("GAME OVER", timeout=2)
                Menu(self.screen).run()

            if len(self.group_rocks.sprites()) == 0:
                self.show_message("LEVEL CLEAR", timeout=2)
                self.level += 1
                self.group_bullets.empty()
                self.group_rocks.empty()
                for i in xrange(self.level):  # @UnusedVariable
                    self.group_rocks.add(Rock(self.screen.get_rect()))
                self.spaceship.reset()

            # collision spaceship-rocks
            if self.spaceship.get_exploding() == False and pygame.sprite.spritecollideany(self.spaceship, self.group_rocks):
                print "spaceship hits a rock!"
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
                        r_radius = r.get_radius()
                        self.group_rocks.remove(r)
                        # score
                        self.spaceship.add_to_score(ROCK_RADIOUS_MAX - r_radius + ROCK_RADIOUS_MIN)
                        del(r)
                        if r_radius > ROCK_RADIOUS_MIN:
                            self.group_rocks.add(Rock(self.screen.get_rect(), pos=r_pos, radius=r_radius / 2))
                            self.group_rocks.add(Rock(self.screen.get_rect(), pos=r_pos, radius=r_radius / 2))
                    # destroy bullet
                    self.group_bullets.remove(b)
                    del(b)

            # text on screen
            if pygame.font:
                self.screen.blit(lives_surface, lives_rect)
                self.screen.blit(score_surface, score_rect)
                if self.spaceship.get_exploding():
                    self.screen.blit(*self.get_message_surface('spaceship destroyed! :(', position=self.screen.get_rect().center))

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
                    # print 'q/Q/Esc'
                    if pygame.key.get_mods() & (KMOD_LSHIFT | KMOD_SHIFT):
                        # panic quit
                        pygame.event.post(pygame.event.Event(QUIT))
                    e = self.show_message("quit game [y/n]?",
                                          allowed_keys=[K_y, K_n, K_ESCAPE])
                    if e.key == K_y:
                        Menu(self.screen).run()
                elif (event.key == K_LEFT or event.key == K_RIGHT or
                      event.key == K_UP or event.key == K_DOWN):
                    self.spaceship.control(event.type, event.key)
                if pygame.key.get_mods() & (KMOD_LCTRL | KMOD_RCTRL):
                    if not self.spaceship.get_exploding():
                        bullet = self.spaceship.fire_bullet()
                        bullet.add(self.group_bullets)
                if pygame.key.get_mods() & (KMOD_LALT | KMOD_RALT):
                    self.spaceship.hyperspace()
            elif event.type == KEYUP:
                if (event.key == K_LEFT or event.key == K_RIGHT or
                    event.key == K_UP or event.key == K_DOWN):
                    self.spaceship.control(event.type, event.key)
            else:
                pass
            print event  # debug

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
        text = font.render("score: " + str(self.spaceship.get_score()), 1,
                           pygame.Color(LIVES_SURFACE_COLOR))
        textpos = text.get_rect()
        textpos.topright = (SCREEN_WIDTH - 5, 5)
        return (text, textpos)

    def get_message_surface(self, msg, position=None):
        """render message to surface"""
        font = load_font(FONT_NAME_DEFAULT, 18)
        text = font.render(msg, 1, pygame.Color(GAME_TEXT_COLOR))
        text_rect = text.get_rect()
        if position != None:
            text_rect.center = position
        return (text, text_rect)

    def show_message(self, msg, position=None, allowed_keys=None, timeout=0):
        """shows a message and wait for user's input

        text -- text string or list of text strings to render
        position -- (x, y) (default is center of the screen)
        allowed_keys -- key that user is allowed to type (defining 'allowed_keys' disable 'timeout')
        timeout -- timeout of the message in seconds, 0 to disable
        """
        # params parsing
        if position == None: position = self.screen.get_rect().center

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


class Main:
    def __init__(self):
        pygame.init()

        # main surface
        # create window based on image size
        pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('asteroids rulez!')
        self.screen = pygame.display.get_surface()

    def run(self):
        Menu(self.screen).run()
        # Game(self.screen).run()

if __name__ == "__main__":
    Main().run()
