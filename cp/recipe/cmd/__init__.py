# -*- coding: utf-8 -*-
# Copyright (C)2007 'Ingeniweb'

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; see the file COPYING. If not, write to the
# Free Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
"""Recipe cmd"""
import commands
import tempfile
import shutil
import os, sys


class CmdExecutionFailed(Exception):
	pass


class Cmd(object):
	"""This recipe is used by zc.buildout"""

	def __init__(self, buildout, name, options):
		self.buildout, self.name, self.options = buildout, name, options
		self.on_install = options.get('on-install', True)
		self.on_update = options.get('on-update', True)
		self.shell = options.get('shell','/bin/sh')

	def install(self):
		"""installer"""
		cmds = self.options.get('install-cmd', '')
		if self.on_install:
			self.execute(cmds)
		return tuple()

	def update(self):
		"""updater"""
		cmds = self.options.get('update-cmd', '')
		if self.on_update:
			self.execute(cmds)
		return tuple()

	def execute(self,cmds):
		"""run the commands
		"""
		cmds = cmds.strip()
		if not cmds:
			return
		if cmds:
			cmds = cmds.split('\n')
			dirname = tempfile.mkdtemp()
			lines = [line.strip() for line in cmds]
			tmpfile = os.path.join(dirname,'run.sh')
			fil = open(tmpfile,'w+')
			fil.write("#!%s\n" % self.shell)
			fil.write('\n'.join(lines))
			fil.close()
			#give execute permissions
			os.chmod(tmpfile,0700)
			status, results = commands.getstatusoutput(tmpfile)
			print results
			if status:
				raise CmdExecutionFailed,results
			return status


class Python(Cmd):

	def execute(self):
		"""run python code
		"""
		cmds = self.options.get('cmds', '')
		cmds = cmds.strip()
		def undoc(l):
			l = l.strip()
			l = l.replace('>>> ', '')
			l = l.replace('... ', '')
			return l

		if not cmds:
			return
		if cmds:
			name = self.name
			buildout = self.buildout
			options = self.options
			lines = cmds.split('\n')
			lines = [undoc(line) for line in lines if line.strip()]
			dirname = tempfile.mkdtemp()
			tmpfile = os.path.join(dirname, 'run.py')
			open(tmpfile, 'w').write('\n'.join(lines))
			execfile(tmpfile)
			shutil.rmtree(dirname)


