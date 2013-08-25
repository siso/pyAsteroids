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

from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from mainmenu import MainMenu
import pygame

def main():
    pygame.init()
    
    pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('pyAsteroids')
    screen = pygame.display.get_surface()
    
    MainMenu(screen)

if __name__ == '__main__':
    main()
