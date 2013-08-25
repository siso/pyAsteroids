Python Asteroids
================

Old-school (Nov '79!) *Asteroids* vector video-game remake.

See: http://en.wikipedia.org/wiki/Asteroids\_(video\_game)

Download
--------

Clone *pyasteroids* Git repository:

::

    $ git clone https://github.com/siso/pyAsteroids

Usage
-----

Just run it:

::

    $ cd pyasteroids
    $ ./runme.py

Commands
--------

+--------------------------+---------------------+
| key                      | action              |
+==========================+=====================+
| up, left, right arrows   | spaceship control   |
+--------------------------+---------------------+
| left/right ctrl          | fire                |
+--------------------------+---------------------+
| left/right alt           | hyperspace          |
+--------------------------+---------------------+
| esc                      | quit game           |
+--------------------------+---------------------+
| esc + esc                | panic quit (TODO)   |
+--------------------------+---------------------+

Installation
------------

It is possible to install *pyasteroids* as a Python package:

::

    $ python setup.py build
    $ sudo python setup.py install

then run it:

::

    $ pyasteroids

Why this game?
--------------

I read interesting articles about pygame, sprites collision and game
programming, and wanted to poke around. If you are interested take a
look at the source code and see how it works. Again, my aim was playing
with pygame and game programming techniques, hence do not expect too
much from this. Just give it a shot! :)

Feel free to drop me a few lines to make suggestions.

Author
------

Simone Soldateschi simone.soldateschi@gmail.com

Copyright
---------

Copyright (c) 2013, Simone Soldateschi All rights reserved.

License
-------

GPL version 3, see LICENSE file.
