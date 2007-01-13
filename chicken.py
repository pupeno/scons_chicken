# -*- coding: utf-8 -*-
# Copyright (C) 2005 José Pablo Ezequiel "Pupeno" Fernández Silva
#
# This file is part of SCons Chicken.
#
# SCons Chicken is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.
# SCons Chicken is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with SCons Chicken; if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA

import SCons
from SCons.Builder import Builder
#import SCons.Tool
#import SCons.Scanner
#from SCons.Node.FS import File
import os

def generate(env):
    #Not needed# env["CSI"] = env.Detect("csi") or "csi"
    env["CSC"] = env.Detect("csc") or "csc" # Only used to gather flags.
    env["CHICKEN"] = env.Detect("chicken") or "chicken"
    env["CHICKENFLAGS"] = SCons.Util.CLVar("")
    #env["CHICKENREPOSITORY"] = strip(os.popen("chicken-setup -repository").read()) + "/"
    env["CHICKENCOM"] = "$CHICKEN $CHICKENFLAGS $SOURCE -output-file $TARGET"
    
    ccflags =  SCons.Util.CLVar(os.popen("csc -cflags").read())
    linkflags = SCons.Util.CLVar(os.popen("csc -ldflags").read())
    libs = os.popen("csc -libs").read().strip().replace("-l", "").split()
    
    env.Append(CCFLAGS = ccflags,
               LINKFLAGS = linkflags,
               LIBS = libs)
    
    # The .scm to .c builders.
    c_file, cxx_file = SCons.Tool.createCFileBuilders(env)
    c_file.add_action(".scm", SCons.Action.Action(env["CHICKENCOM"]))
    
    #def includedFiles(node, env, path):
    #    for path in env["ENV"]["PATH"].split(":"):
    #        cil = path + "/" + "chicken-include-list"
    #        if os.path.exists(cil):
    #            includes = split(strip(os.popen(cil + " " + str(node)).read()))
    #            return includes
    #    else:
    #        print "Not running chicken-il, nothing to be worried about when building/installing SCons Chicken, but if that is not the case, your installation may be corrupt."
    #        return []
    #
    #chickenScanner = SCons.Scanner.Scanner(function = includedFiles,
    #                                       name = "ChickenScanner",
    #                                       skeys = [".scm"],
    #                                       recursive = True)
    #env.Append(SCANNERS = chickenScanner)
    #
    #def ChickenSetup(target = None, source = None, env = None):
        #""" Function that works as a builder action wrapping chickenSetup. """
        
        ## Meta information passed to us.
        #meta = None
        #if env._dict.has_key("meta"):
            #meta = env._dict["meta"]

        ## Open the .setup file for writing.
        #setupFile = open(str(target[0]), "w")

        ## Generate and write its content.
        #setupFile.write(chickenSetup(source, meta))

        ## Close it.
        #setupFile.close()

        #return None

    #env["BUILDERS"]["ChickenSetup"] = SCons.Builder.Builder(action = ChickenSetup,
                                                            #suffix = ".setup")

    #def chickenSetup(files, meta = None):
        #""" This procedure works like a builder and it builds the .setup files.
            #Parameters:
            #1. Name or list of names of the .so files that will be linked from the setup file.
            #Optional parameters:
            #documentation = Where is the HTML documentation.
            #syntax = Whether (true or false) this contain syntax extensions.
            #requires = other or list of other required extensions."""

        #def makeLispList(head, items, prefix = ""):
            #""" This procedure builds a string that resembles a Lisp list of strings.
                #The first parameter is the header of the Lisp-like list.
                #The second parameter is either a string or a list of strings that
                #will form the Lisp-like list.
                #Prefix is an optional parameter that will be prepended to each item
                #on the list."""

            #def prepareObject(item):
                #""" Prepares the object to be output as a string. If there"s a prefix, try to use it. """
                #if isinstance(item, str):
                    #return "\"" + prefix + item + "\""
                #elif isinstance(item, File):
                    #return "\"" + prefix + item.name + "\""
                #else:
                    #return str(item)
                
            #l = "(" + head

            #if isinstance(items, list):
                #for i in items:
                    #l += " " + prepareObject(i)
            #elif items is not None:
                #l += " " + prepareObject(items)

            #l += ")" 
            #return l

        ## Open the list (a .setup is a list).
        #content = "("

        ## Make a list of installed files. All located on CHICKENREPOSITORY.
        #content += makeLispList("files", files, env["CHICKENREPOSITORY"])

        ## Create the rest of the meta-information.
        #if meta:
            #for k in meta:
                #content += "\n" + makeLispList(k, meta[k])
            
        ## Close the list.
        #content += ")\n"

        ## Return the generated content.
        #return content

    #def EmitEggContents(target = None, source = None, env = None):
        #""" Return the files that should go into an egg. """
        
        #def getLeafSources(sources):
            #""" Get all the sources that are leafs, not branches. """
            #contents = list()
            #for source in sources:
                #if len(source.sources) == 0:
                    #contents.append(source)
                    #contents += source.get_found_includes(env, chickenScanner, source.path)
                #else:
                    #contents += getLeafSources(source.sources)
            #return contents

        #contents = list(set(getLeafSources(source)))
        #return target, contents
    
    #env["BUILDERS"]["ChickenEgg"] = SCons.Builder.Builder(action = "$TARCOM",
                                                          #emitter = EmitEggContents,
                                                          #suffix = ".egg")
    
    #def CheckChickenProgram(context):
        #""" Check if a Chicken program can be built and run. If not, try adding the libraries. """
        #context.Message("Checking for building Chicken programs... ")
        #result = context.TryRun("(display (+ 1 2))", ".scm")
        #if not result[0]:
            #context.env.ParseConfig("chicken-config -cflags -libs")
            #result = context.TryRun("(display (+ 1 2))", ".scm")
            
        #context.Result(result[0])
        #return result[0]

    #def CheckChickenLibrary(context):
        #""" Check if a Chicken library can be built after adding the libraries. """
        #context.Message("Checking for building Chicken libraries... ")
        ## A library compiles correctly even without the right flags (in that case, it compiles, but it can't be used. So, we just add the flags.
        #context.env.ParseConfig("chicken-config -shared -cflags -libs")
        #result = context.TryBuild(context.env.SharedLibrary, "(display (+ 1 2))", ".scm")
        #context.Result(result)
        #return result

    ## Export the checkers.
    #env.CheckChickenProgram = CheckChickenProgram
    #env.CheckChickenLibrary = CheckChickenLibrary
    
def exists(env):
    return env.Detect(["csc"])
