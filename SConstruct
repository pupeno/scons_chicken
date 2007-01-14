# -*- coding: utf-8 -*-
# Copyright (C) 2005 José Pablo Ezequiel "Pupeno" Fernández Silva
#
# This file is part of SCons Chicken.
#
# SCons Chicken is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.
# SCons Chicken is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with SCons Chicken; if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA

import os

# Create an environment.
env = Environment(tools = ["default", "chicken"], toolpath=["./"])

# Check for Chicken.
conf = Configure(env, custom_tests = {"CheckChickenProgram" : env.CheckChickenProgram})
if not conf.CheckChickenProgram():
    print "It seems you don't have Chicken installed or it is not"
    print "installed correctly. For more information:"
    print "http://www.call-with-current-continuation.org/"
    Exit(1)
env = conf.Finish()

# Configuration.
opts = Options(".scons-chicken.conf")
opts.Add(PathOption("SCONSPREFIX", "Prefix directory for SCons", os.environ.get("PYTHON_ROOT","/usr/local")))
opts.Add(PathOption("PREFIX", "Prefix directory for everything else", "/usr/local"))
opts.Update(env)
opts.Save(".scons-chicken.conf", env)

# Help.
Help(opts.GenerateHelpText(env))

# Install directories.
sconsInstallDir = "$SCONSPREFIX/lib/scons/SCons/Tool/"
binInstallDir = "$PREFIX/bin/"

# chicken.py, no build needed.
env.Install(sconsInstallDir, "chicken.py")

# chicken-include-list
cil = env.Program("chicken-include-list.scm")
env.Install(binInstallDir, cil)

# Alias for installing.
env.Alias("install", sconsInstallDir)
env.Alias("install", binInstallDir)
