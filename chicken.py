# -*- coding: utf-8 -*-
# Copyright (C) 2005 José Pablo Ezequiel "Pupeno" Fernández Silva
#
# This file is part of scons-chicken.
#
# Scons-chicken is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.
# Scons-chicken is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with scons-chicken; if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA

import SCons.Tool
import SCons.Scanner
import os
from SCons.Node.FS import File
from string import strip,split

def generate(env):
    env["CHICKEN"] = env.Detect("chicken") or "chicken"
    env["CHICKENFLAGS"] = "-dynamic -feature chicken-compile-shared -feature compiling-extension"
    env["CHICKENREPOSITORY"] = strip(os.popen("chicken-setup -repository").read()) + "/"
    env["CHICKENCOM"] = "$CHICKEN $SOURCE -output-file $TARGET $CHICKENFLAGS"

    # The .scm to .c builders.
    c_file, cxx_file = SCons.Tool.createCFileBuilders(env)
    c_file.add_action(".scm", SCons.Action.Action(env["CHICKENCOM"]))

    def includedFiles(node, env, path):
        for path in env['ENV']['PATH'].split(':'):
            if os.path.exists(path + '/' + "chicken-il"):
                includes = split(strip(os.popen("chicken-il " + str(node)).read()))
                return includes
        else:
            print "Not running chicken-il, nothing to be worried about when building/installing scons-chicken, but if that is not the case, your installation may be corrupt."
            return []

    chickenScanner = SCons.Scanner.Scanner(function = includedFiles,
                                           name = "ChickenScanner",
                                           skeys = [".scm"],
                                           recursive = True)

    env.Append(SCANNERS = chickenScanner)

    def ChickenSetup(target = None, source = None, env = None):
        """ Function that works as a builder action wrapping chickenSetup. """

        # Do we have documentation ?
        if env._dict.has_key("DOCUMENTATION"):
            documentation = env._dict["DOCUMENTATION"]
        else:
            documentation = ""

        # Is this a syntax extension ?
        if env._dict.has_key("SYNTAX"):
            syntax = env._dict["SYNTAX"]
        else:
            syntax = False

        # What should we require ?
        if env._dict.has_key("REQUIRES"):
            requires = env._dict["REQUIRES"]
        else:
            requires = []

        # Open the .setup file for writing.
        setupFile = open(str(target[0]), "w")

        # Generate and write its content.
        setupFile.write(chickenSetup(source, documentation, syntax, requires))

        # Close it.
        setupFile.close()

        return None

    env["BUILDERS"]["ChickenSetup"] = SCons.Builder.Builder(action = ChickenSetup,
                                                            suffix = ".setup")

    def chickenSetup(files, documentation = None, syntax = False, requires = None):
        """ This procedure works like a builder and it builds the .setup files.
            Parameters:
            1. Name or list of names of the .so files that will be linked from the setup file.
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
        content = "("

        # Make a list of the sources, the .so files. All located on CHICKENREPOSITOR.
        content += makeLispList("files", files, env["CHICKENREPOSITORY"])

        # Add the documentation.
        if documentation:
            content += "\n(documentation \"" + documentation + "\")"

        # Is this a syntax extension ?
        if syntax == True:
            content += "\n(syntax)"

        # What other extensions are necesary by this one ?
        if requires:
            # Make a list of extensions.
            content += "\n" + makeLispList("requires", requires)

        # Close the list.
        content += ")\n"

        # Return the generated content.
        return content

    def ChickenEgg(target = None, source = None, env = None):
        """ Build an egg. """
        
        def getLeafSources(sources):
            """ Get all the sources that are leafs, not branches. """
            eggContents = list()
            for source in sources:
                if len(source.sources) == 0:
                    eggContents.append(source)
                    eggContents += source.get_found_includes(env, chickenScanner, source.path)
                else:
                    eggContents += getLeafSources(source.sources)
            return eggContents

        eggContents = set(getLeafSources(source))
        for egg in eggContents:
            print str(egg)
        return 0
    
    env["BUILDERS"]["ChickenEgg"] = SCons.Builder.Builder(action = ChickenEgg,
                                                          suffix = '.egg')
    
    def CheckChickenProgram(context):
        """ Check if a Chicken program can be built and run. If not, try adding the libraries. """
        context.Message("Checking for building Chicken programs... ")
        result = context.TryRun("(display (+ 1 2))", ".scm")
        if not result[0]:
            context.env.ParseConfig("chicken-config -cflags -libs")
            result = context.TryRun("(display (+ 1 2))", ".scm")
            
        context.Result(result[0])
        return result[0]

    def CheckChickenLibrary(context):
        """ Check if a Chicken library can be built after adding the libraries. """
        context.Message("Checking for building Chicken libraries... ")
        # A library compiles correctly even without the right flags (in that case, it compiles, but it can't be used. So, we just add the flags.
        context.env.ParseConfig("chicken-config -shared -cflags -libs")
        result = context.TryBuild(context.env.SharedLibrary, "(display (+ 1 2))", ".scm")
        context.Result(result)
        return result

    # Export the checkers.
    env.CheckChickenProgram = CheckChickenProgram
    env.CheckChickenLibrary = CheckChickenLibrary
    
def exists(env):
    return env.Detect(["chicken"])
