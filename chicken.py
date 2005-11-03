# -*- coding: utf-8 -*-
# Copyright (C) 2005 José Pablo Ezequiel "Pupeno" Fernández Silva
#
# This file is part of scons-chicken.
#
# scons-chicken is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.
# scons-chicken is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with scons-chicken; if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA

import SCons.Tool
import os
from string import strip

def generate(env):
    c_file, cxx_file = SCons.Tool.createCFileBuilders(env)

    c_file.add_action('.scm', SCons.Action.Action("$CHICKENCOM"))

    env['CHICKEN'] = env.Detect('chicken') or 'chicken'
    env['CHICKENFLAGS'] = SCons.Util.CLVar('')
    env['CHICKENCOM'] = '$CHICKEN $CHICKENFLAGS $SOURCE -output-file $TARGET'

    env['CHICKENLIBHOME'] = strip(os.popen('chicken-config -lib-home').read().split('=', 1)[1]) + '/'

    
def exists(env):
    return env.Detect(['chicken'])

# A procedure to check if we can build .scm with Chicken.
def CheckChicken(context):
    context.Message("Checking for Chicken... ")
    result = context.TryRun("(+ 1 2)", ".scm")
    context.Result(result[0])
    return result[0]
