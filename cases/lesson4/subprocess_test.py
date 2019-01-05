import subprocess

s = subprocess.Popen(['python', '/Volumes/Seagate/tdclass/TDClass2_Nuke/cases/lesson4/print_ten.py'],
                     stdout=subprocess.PIPE)

for line in iter(s.stdout.readline, ''):
    print line
