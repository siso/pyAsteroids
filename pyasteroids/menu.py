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

from constants import *
from utils import *
from game import *


class MenuItem:
    """implements a menu item"""
    
    def __init__(self, text, font, pos, command):
        self.text = text
        self.font = font
        self.pos = list(pos)
        ren = self.font.render(text, 1, (255, 255, 255))
        self.pos[0] -= ren.get_width() / 2
        self.cmd = command
        self.selected = False

    def command(self):
        """esegue il comando associato all'item"""
        if self.cmd: self.cmd()

    def select(self, selected = True):
        """seleziona l'item"""
        self.selected = selected

    def is_selected(self):
        """test selezione item"""
        return self.selected

    def render(self, screen):
        """rendering dell'item"""
        if self.selected:
            surface = self.font.render(self.text, 1, (255, 255, 255))
        else:
            surface = self.font.render(self.text, 1, (175, 175, 175))
        screen.blit(surface, self.pos)


class Menu:
    """implements a menu option

    This menu is composed of 'MenuItem' which can be scrolled using arrow keys,
    selected with ENTER. ESC to quit the menu.
    """
    def __init__(self, screen):
        self.screen = screen
        
        # load fonts
        self.font = load_font(FONT_NAME_DEFAULT, FONT_SIZE_MENU)
        self.font2 = load_font(FONT_NAME_DEFAULT, 70)
        self.font3 = load_font(FONT_NAME_DEFAULT, 20)
        
        # add items to menu
        self.items = []
        self._build_menu()
        
        self.clock = pygame.time.Clock()
        
        self._run()
        print 'foo'

    def _add_item(self, text, command):
        """add item to menu"""
        pos = (self.screen.get_width() / 2, 300 +
               len(self.items)*self.font.get_height())
        item = MenuItem(text, self.font, pos, command)
        self.items.append(item)

    def __index_selected_item(self):
        """get index of selected item"""
        for i in xrange(len(self.items)):
            if self.items[i].is_selected(): return i
        return None

    def __move_down(self):
        """select next item"""
        isi = self.__index_selected_item()
        assert isi != None
        self.items[isi].select(False)
        if isi < len(self.items) - 1:
            self.items[isi + 1].select(True)
        else:
            self.items[0].select(True)

    def __move_up(self):
        """select previous item"""
        isi = self.__index_selected_item()
        assert isi != None
        self.items[isi].select(False)
        if isi > 0:
            self.items[isi - 1].select(True)
        else:
            self.items[len(self.items) - 1].select(True)

    def __menu_input(self):
        """routine di controllo dello user input"""
        self.events = pygame.event.get()
        for e in self.events:
            if e.type == QUIT:
                pygame.quit()
                sys.exit()
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if e.key == K_UP:
                    self.__move_up()
                if e.key == K_DOWN:
                    self.__move_down()
                if e.key == K_RETURN:
                    isi = self.__index_selected_item()
                    assert isi != None
                    self.items[isi].command()
    
    def __loop(self):
        """menu main loop"""
        while True:
            self.clock.tick(GAME_FRAMERATE)
            self.__menu_input()
            self._draw_scene()

    def _run(self):
        """'execute' menu"""
        assert len(self.items) > 0, "self.items contains no item"
        self.items[0].select(True)
        self.__loop()
    
    def _draw_scene(self):
        """render menu on main surface"""
        self.screen.fill((0, 0, 0))
        for i in self.items:
            i.render(self.screen)
        self._render_static_texts()
        pygame.display.flip()
