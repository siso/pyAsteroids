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

import os, pygame, sys
from pygame.locals import *

def load_font(file, size):
    """load font from './data/fonts' directory

    it handles properly file separator under different OSes"""
    this_dir, this_filename = os.path.split(__file__)
    path = os.path.join(this_dir, "data", "fonts", file)
    print "debug: loading font '" + path + "'"
    return pygame.font.Font(path, size)


def render_text(surface, text, font, pos, center=False):
    ren = font.render(text, 1, (255, 255, 255))
    if center:
        pos = [pos[0] - ren.get_width()/2, pos[1] - ren.get_height()/2]
    surface.blit(ren, pos)
    return ren

def load_sound(file, volume=1.0):
    this_dir, this_filename = os.path.split(__file__)
    path = os.path.join(this_dir, "data", "sounds", file)
    sound = pygame.mixer.Sound(path)
    sound.set_volume(volume)
    return sound

def load_sounds(d_sounds):
    """loads sounds files into sound vector 'v_sound'"""
    d_sounds['shoot'] = load_sound("shoot.wav", 0.2)
