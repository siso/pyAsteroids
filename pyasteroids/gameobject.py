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

import pygame.sprite


class GameObject(pygame.sprite.Sprite):
    """implements a game object from which every other object inherits"""
    def __init__(self, gameArea, pos, velocity):
        pass

    def _surface_factory(self):
        """renders object shape to a pygame surface"""
        pass

    def update(self):
        pass
