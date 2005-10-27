# -*- coding: utf-8 -*-
# Tool for scons to support the Chicken Scheme compiler
# Copyright (C) 2005 José Pablo Ezequiel "Pupeno" Fernández Silva
# <pupeno@pupeno.com>
#
# This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import SCons.Tool
import SCons.Util
import SCons.Action
import SCons.Builder
import os.path
from subprocess import *

def generate(env):
    env['CHICKEN'] = env.Detect('chicken') or 'chicken'
    
    # Builder to compile a .scm file into a .c file.
    env.Chicken = SCons.Builder.Builder(action = '$CHICKEN $SOURCE -output-file $TARGET')


def exists(env):
    return env.Detect(['chicken'])