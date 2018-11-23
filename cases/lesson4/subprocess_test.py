import subprocess

s = subprocess.Popen(['bash'], stdout=subprocess.PIPE)

for line in iter(s.stdout.readline, ''):
	print line
