from CommandList import command
from subprocess import PIPE, run

res = run(command['Beep'].split(" "), stdout=PIPE, stderr=PIPE, universal_newlines=True)
