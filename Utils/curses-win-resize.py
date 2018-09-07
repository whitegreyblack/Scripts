#!/usr/bin/env python
'''Resize tool for window command propmts'''

__author__ = "Sam Whang"


import os
import platform
import sys
import curses

if __name__ == "__main__":
    y, x = 40, 100
    curses.use_env(True)
    os.environ['LINES']="40"
    os.environ['COLUMNS']="100"
    
    if platform.system() == "Windows":
        # cmd prompt, powershell
        os.system('mode con: cols={} lines={}'.format(x, y))

        os.system('mode con > out.txt')
        lines, cols = 0, 0
        
        with open('out.txt') as f:
            for line in f.read().split('\n'):
                if 'Lines' in line:
                    lines = line.split(":")[1].strip()
                if 'Columns' in line:
                    cols = line.split(":")[1].strip()
                    
        if int(lines) != y or int(cols) != x:
            try:
                os.system('conemuc -guimacro windowpossize 0 0 836px 720px')
            except:
                raise NotImplementedError
    else:
        raise NotImplementedError("Cannot run script for this os")
        exit(-1)  
    curses.wrapper(main)
