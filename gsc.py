# -*- coding: utf-8 -*-
# Tool for scons to support the Gambit-C compiler
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

def generate(env):
    env['GSC'] = env.Detect('gsc') or 'gsc'
    
    # Builder to compile a .scm file into a .c file.
    env.Gambit = SCons.Builder.Builder(action = '$GSC -c -o $TARGET $SOURCE')
    
    # Builder to create an incremental (default) link file.
    env.GambitLinkIncFile = SCons.Builder.Builder(action = '$GSC -o $TARGET $SOURCES')
    
    # Builder te create a flat link file.
    env.GambitLinkFlatFile = SCons.Builder.Builder(action = '$GSC -flat -o $TARGET $SOURCES')
    
    def GambitCommon(env, target, source):
        """Perform the set of common operations for any Gambit project."""
        # Lists for the names of the scheme sources and others respectively.
        schemeSources = []
        otherSources = []

        # Separate sources into scheme and other sources
        for s in source:
            if os.path.splitext(s)[1] == '.scm':
                schemeSources.append(s)
            else:
                otherSources.append(s)
        
        # Compile each scheme sources and store the compiled (nodes).
        compiledSchemeSources = []
        for ss in schemeSources:
            compiledSchemeSources.extend(
                env.Gambit(env, os.path.splitext(ss)[0]+'.c', ss))
        
        return target, compiledSchemeSources, otherSources

    def addLibrares(kw):
        """ Add the flags to link against the needed libraries for every gambit project on the current platform."""
        # Choose the libraries needed according to the platform. TODO: add more platforms.
        if env['PLATFORM'] == 'posix':
            libs = ['gambc', 'm', 'dl', 'util']
        elif env['PLATFORM'] == 'macosx':
            # TODO: test if macosx is the right string to test, it might be darwin or who knows?
            libs = ['gambc']

        # Use those libraries.
        if kw.has_key('LIBS'):
            kw['LIBS'].append = libs
        else:
            kw['LIBS'] = libs

        return kw

    def GambitProgram(env, target, source, *args, **kw):
        """Pseudo builder to make a gambit program."""
        # Do the common tasks.
        target, source, otherSource = GambitCommon(env, target, source)
        # Build the link file.
        linkFile = env.GambitLinkIncFile(env, target+'-linkfile.c', source)
        # Add the needed libraries.
        kw = addLibrares(kw)
        return apply(env.Program, (target, source+otherSource+linkFile) + args, kw)
    

    def GambitLoadableLibrary(env, target, source, *args, **kw):
        """Pseudo builder to make a gambit program."""
        # Do the common tasks.
        target, source, otherSource = GambitCommon(env, target, source)
        # Build the FLAT link file.
        linkFile = env.GambitLinkFlatFile(env, target+'.o1.c', source)
        # Add the needed libraries.
        kw = addLibrares(kw)

        # Choose the flags needed according to the platform. TODO: add more platforms.
        ccflags = ['-D___DYNAMIC']
        if env['PLATFORM'] == 'posix':
            linkflags = ['-shared']
        elif env['PLATFORM'] == 'macosx':
            # TODO: test if macosx is the right string to test, it might be darwin or who knows?
            linkflags = ['-bundle']

        # Use those libraries.
        if kw.has_key('CCFLAGS'):
            kw['CCFLAGS'].append = ccflags
        else:
            kw['CCFLAGS'] = ccflags

        if kw.has_key('LINKFLAGS'):
            kw['LINKFLAGS'].append = linkflags
        else:
            kw['LINKFLAGS'] = linkflags

        return apply(env.Program, (target+'.o1', source+otherSource+linkFile) + args, kw)

    # Attach the pseudo-Builders to the Environment so they can be called like a real Builder.
    env.GambitProgram = GambitProgram
    env.GambitLoadableLibrary = GambitLoadableLibrary

def exists(env):
    return env.Detect(['gsc'])