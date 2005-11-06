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
from SCons.Node.FS import File
from string import strip

def generate(env):
    # Get the builders for c and c++
    c_file, cxx_file = SCons.Tool.createCFileBuilders(env)

    # and add .scm extensions to the c builder with our own action.
    c_file.add_action('.scm', SCons.Action.Action("$CHICKENCOM"))

    # Chicken variable/constans.
    env['CHICKEN'] = env.Detect('chicken') or 'chicken'
    env['CHICKENFLAGS'] = SCons.Util.CLVar('')
    env['CHICKENCOM'] = '$CHICKEN $CHICKENFLAGS $SOURCE -output-file $TARGET'

    env['CHICKENREPOSITORY'] = strip(os.popen('chicken-setup -repository').read()) + '/'
    
    def CheckChicken(context):
        """ This procedure should be running on a Configure context.
            It will return True if there's a working Chicken installation,
            false otherwise."""
        
        context.Message("Checking for Chicken... ")

        # Try to compile and run a simple Scheme program.
        result = context.TryRun("(display (+ 1 2))", ".scm")
        context.Result(result[0])
        return result[0]

    def ChickenSetup(env, target, source, *args, **kw):
        """ This procedure works like a builder and it builds the .setup files.
            Parameters:
            1. env (any way to fix this ?)
            2. Name of the .setup file to generate.
            3. Name or list of names of the .so files that will be linked from the setup file.
            Optional parameters:
            documentation = Where is the HTML documentation.
            syntax = Whether (true or false) this contain syntax extensions.
            requires = other or list of other required extensions."""
        
        def makeLispList(head, items, prefix = ""):
            """ This procedure builds a string that resembles a Lisp list of strings.
                The first parameter is the header of the Lisp-like list.
                The second parameter is either a string or a list of strings that
                will form the Lisp-like list.
                Prefix is an optional parameter that will be prepended to each item
                on the list."""

            def buildPath(item):
                """ Procedure that builds a path using the prefix and a string or
                    File object."""
                if isinstance(item, str):
                    return prefix + item
                elif isinstance(item, list):
                    return prefix + str(item[0])
                elif isinstance(item, File):
                    return prefix + item.name
                else:
                    print "Type not recognized to build .setup file."
                    return ""
                
                
            l = "(" + head
            
            if isinstance(items, list):
                for i in items:
                    l += " \"" + buildPath(i) + "\" "
            else:
                l += " \"" + buildPath(items) + "\""
                
            l += ")" 
            return l

        # Open the list (a .setup is a list).
        setup = "("

        # Make a list of the sources, the .so files. All located on CHICKENREPOSITOR.
        setup += makeLispList("files", source, env['CHICKENREPOSITORY'])

        # Add the documentation.
        if kw.has_key('documentation'):
            setup += "\n(documentation \"" + kw['documentation'] + "\")"

        # Is this a syntax extension ?
        if kw.has_key('syntax') and kw('syntax') == True:
            setup += "\n(syntax)"

        # What other extensions are necesary by this one ?
        if kw.has_key('requires'):
            # Make a list of extensions.
            setup += "\n" + makeLispList("requires", kw['requires'])

        # Close the list.
        setup += ")\n"

        # The target should be one and only one file, if it is a list, we take the first one.
        if(isinstance(target, list)):
            target = target[0]

        # Write the list (being hold as a string on setup) to the file.
        setupFile = open(target, 'w')
        setupFile.write(setup)
        setupFile.close()

        # Return an object representing the file for further handling.
        return env.File(target)

    # Put the procedures on env, so the SConstruct file can find them.
    env.CheckChicken = CheckChicken
    env.ChickenSetup = ChickenSetup        

def exists(env):
    return env.Detect(['chicken'])


