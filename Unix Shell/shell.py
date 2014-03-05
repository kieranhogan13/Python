# Very basic Posix shell
import os
import sys
import readline
import shlex
import glob

prompt = "sh>> "

def copyright():
  sys.stderr.write("""
Copyright (C) 2012-13 Brian Gillespie
This program comes with ABSOLUTELY NO WARRANTY; This is free
software, and you are welcome to redistribute it under certain
conditions; Type "copyright" or "license" for more information.
""" + "\n")
  return True
	
# Given the skeleton code for a python shell that needs
# file globbing(*.), output redirection(>), input redirection (<)
# and background exec of commands implemented(&).
 
# Parsed splitting of input into constituent arguments
def parse(cmd):
  check = shlex.split(cmd) 
  if len(check) <= 1:
	return check
  else:
    for i in range (0, len(check)):
	  if '*' in check[i]:
        check.extend(glob.glob(check[i]))
		check.pop()
    return check
	

# at start of program
def internal(argv):
  cmd = argv[0]
  if cmd == "copyright":
    return copyright()

  return False

# Execute an execute command (i.e. run a  program on disk)
# If this succeeds it never returns
def execute(cmd, argv):
  try:
    os.execv(cmd, argv)
  except OSError: pass

#FORKS THE SHELL
def call(argv):
  if os.fork() == 0:
   cmd = argv[0]
  # child half
    if '>' in argv:
	  fd = os.open(argv[-1], os.O_CREAT | os.O_TRUNC | os.O_RDWR)
	  os.dup2(fd,1)
	  argv.pop()
	  argv.pop()
	  if '/' in cmd:
        # Relative or absolute path specified
        execute(cmd, argv)
      else:
        for dir in os.getenv('PATH').split(':'):
          # Keep trying each directory in PATH until we find it
          execute(dir + '/' + cmd, argv)
		  
	elif '<' in agrv:
	  fd = os.open(agrv[-1], os.O_RDONLY)
	  os.dup2(fd, 0)
      if '/' in cmd:
        # Relative or absolute path specified
        execute(cmd, argv)
      else:
        for dir in os.getenv('PATH').split(':'):
          # Keep trying each directory in PATH until we find it
          execute(dir + '/' + cmd, argv)
	
	else:
      if '/' in cmd:
        # Relative or absolute path specified
        execute(cmd, argv)
      else:
        for dir in os.getenv('PATH').split(':'):
          # Keep trying each directory in PATH until we find it
          execute(dir + '/' + cmd, argv)

    # If we get here then execution has failed
    sys.stderr.write('Unrecognised command: ' + cmd + '\n')
    os._exit(1)
  else:
  # parent half
    if argv[-1] != "&": 
      os.wait()
		
#MAIN OF SHELL	
# Read, print, eval, loop (REPL) 
copyright()
while True:
  try:
    cmd = input(prompt).strip() #string
    if cmd == "":
      # Empty command so just prompt again
      pass 
    elif cmd == "exit":
      # Exit the shell
      break
    else:
      argv = parse(cmd) #list/array
      if not internal(argv):
        call(argv)
  except EOFError:
      # User has pressed Ctrl-D
    break