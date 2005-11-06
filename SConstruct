# -*- coding: utf-8 -*-
# Copyright (C) 2005 José Pablo Ezequiel "Pupeno" Fernández Silva
#
# This file is part of scons-chicken.
#
# scons-chicken is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.
# scons-chicken is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with scons-chicken; if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA

env = Environment(tools = ["default", "chicken"], toolpath=["../../"])

# Configuration.
opts = Options(".scons-chicken.conf")
opts.Add(PathOption("BINPREFIX", "Prefix directory for binaries", "/usr/local"))
opts.Add(PathOption("SCONSPREFIX", "Prefix directory for scons", "/usr/local"))
opts.Update(env)
opts.Save(".scons-chicken.conf", env)

# Help.
Help(opts.GenerateHelpText(env))

# Parse the parameters that Chicken tell us we'll need to pass to the C compiler.
env.ParseConfig('chicken-config -libs -cflags -shared')

# Start some checks.
conf = env.Configure(custom_tests = {'CheckChicken' : env.CheckChicken})

# Check if Chicken is present and it can create binaries.
if not conf.CheckChicken():
    print "It seems you don't have Chicken installed or it is not"
    print "installed correctly. For more information:"
    print "http://www.call-with-current-continuation.org/"
    exit(1)

# Finished checking.
env = conf.Finish()

chickenll = env.Program("chicken-ll.scm")

# Install.
sconsInstallDir = "$SCONSPREFIX/lib/scons/SCons/Tool/"
binInstallDir = "$BINPREFIX/bin"
env.Install(sconsInstallDir, 'chicken.py')
env.Install(binInstallDir, chickenll)
env.Alias('install', sconsInstallDir)
env.Alias('install', binInstallDir)
