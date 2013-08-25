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
from game import *
from menu import *
from utils import *

class MainMenu(Menu):
    """
    main Menu of the game"""

    def _build_menu(self):
        """
        customized menu
        
        to be redefined by each subclass
        """
        
        self._add_item("New Game", self.run_game)
        self._add_item("Options", self.run_options)
        self._add_item("High Scores", self.run_high_scores)
        self._add_item("Quit Game", self.run_quit_game)
    
    def _render_static_texts(self):
        """        
        rendering static texts
        
        to be redefined by each subclass
        """
        render_text(self.screen, "pyAsteroids", self.font2, (self.screen.get_width() / 2, 100), True)
        render_text(self.screen, "Copyright © 2013", self.font3, (self.screen.get_width() / 2, 200), True)
        render_text(self.screen, "Simone Soldateschi", self.font3, (self.screen.get_width() / 2, 225), True)

    def run_game(self):
        self.screen.fill((0, 0, 0))
        pygame.display.flip()
        Game(self.screen).run()

    def run_options(self):
        print "not implemented yet"

    def run_high_scores(self):
        print "not implemented yet"

    def run_quit_game(self):
        pygame.quit()
        sys.exit()
