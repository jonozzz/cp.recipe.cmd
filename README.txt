=====================
cp.recipe.cmd package
=====================

.. contents::

What is cp.recipe.cmd ?
=======================


This recipe is used to run one or more command lines.

I stole this from iw.recipe.cmd (http://pypi.python.org/pypi/iw.recipe.cmd/0.1)

It works differently tho, when it comes to executing shell commands.  iw.recipe.cmd would push each command out separately in it's own shell.  Here I push them out to a shell script, and then run the shell script.  This way things like CD and other things that require state within the shell work great.

options:
shell= Set a shell to execute (default /bin/sh) (do not put the #!)
on_install= whether to run or not on_install (defaults True)
on_update= whether to run or not on_update (defaults True)
install_cmd = Commands to run when install happens.
update_cmd = Commands to run when an update happens.

Also, I changed the way it works in the config file (example):

[commandexample]
recipe = cp.recipe.cmd
shell = /bin/sh
install_cmd =
   echo "install commands go here"
	cd /tmp
	echo `pwd`
	echo 'see, I exist in one shell instance.'
update_cmd =
	echo "update commands go here"
	

On install, install_cmd will be turned into a shell script, and then ran.
on update, update_cmd will be turned into a shell script and then ran.  If you want update_cmds to be the same you can do something like this:
update_cmd = ${commandexample:install_cmd}

(where commandexample is the name of your part)


I've added a new option shell=
You can put whateer you want in there, sme nice examples:
/usr/bin/env python
(to run the python interpreter)
the default is /bin/sh, so all your old code using this will work just fine.

Also, I check the output of the script and if something returns >0 then
CmdExecutionFailed is raised, along with the output of the error, and the path
of where the script is, so you can see what was generated, do debugging, and
fix it.


a python example using the new shell= is here:


[buildout]
parts = cmds

[cmds]
recipe = cp.recipe.cmd
shell=/usr/bin/env python
update_cmd =
	f = open('testfile'.'w')
	f.write('this is a testfile')
	f.close()



Below are the original docs (which can be ignored probably):
=======================



We need a config file::

  >>> cfg = """
  ... [buildout]
  ... parts = cmds
  ...
  ... [cmds]
  ... recipe = iw.recipe.cmd
  ... on_install=true
  ... cmds= %s
  ... """

  >>> test_file = join(sample_buildout, 'test.txt')
  >>> cmds = 'touch %s' % test_file
  >>> write(sample_buildout, 'buildout.cfg', cfg % cmds)

Ok, so now we can touch a file for testing::

  >>> print system(buildout)
  Installing cmds.

  >>> 'test.txt' in os.listdir(sample_buildout)
  True

And remove it::

  >>> test_file = join(sample_buildout, 'test.txt')
  >>> cmds = 'rm -f %s' % test_file
  >>> write(sample_buildout, 'buildout.cfg', cfg % cmds)

  >>> print system(buildout)
  Uninstalling cmds.
  Installing cmds.

  >>> 'test.txt' in os.listdir(sample_buildout)
  False

We can run more than one commands::

  >>> cmds = '''
  ... touch %s
  ... rm -f %s
  ... ''' % (test_file, test_file)

  >>> test_file = join(sample_buildout, 'test.txt')
  >>> cmds = 'rm -f %s' % test_file
  >>> write(sample_buildout, 'buildout.cfg', cfg % cmds)

  >>> print system(buildout)
  Updating cmds.

  >>> 'test.txt' in os.listdir(sample_buildout)
  False

We can also run some python code::

  >>> cfg = """
  ... [buildout]
  ... parts = py py2
  ...
  ... [py]
  ... recipe = iw.recipe.cmd:py
  ... on_install=true
  ... cmds= 
  ...   >>> sample_buildout = buildout.get('directory', '.')
  ...   >>> print os.listdir(sample_buildout)
  ...   >>> shutil.rmtree(os.path.join(sample_buildout, "bin"))
  ...   >>> print os.listdir(sample_buildout)
  ... [py2]
  ... recipe = iw.recipe.cmd:py
  ... on_install=true
  ... cmds=
  ...   >>> def myfunc(value):
  ...   ...     return value and True or False
  ...   >>> v = 20
  ...   >>> print myfunc(v)
  ... """

  >>> write(sample_buildout, 'buildout.cfg', cfg)

Ok, so now we run it::

  >>> print system(buildout)
  Uninstalling cmds.
  Installing py.
  ['.installed.cfg', 'bin', 'buildout.cfg', 'develop-eggs', 'eggs', 'parts']
  ['.installed.cfg', 'buildout.cfg', 'develop-eggs', 'eggs', 'parts']
  Installing py2.
  True


