#!/usr/bin/env python
'''Simple color coded tree function'''

__author__  = "Samuel Whang"
__email__   = "sangwoowhang@gmail.com"

import os

def list_files(startpath: str) -> None:
    '''
    Walks through directory with os.walk and lists directories 
    and files with given extensions
    '''
    # color code directories and specific extensions
    # blue for directories
    folder='\x1b[0;34;40m'
    yellow='\x1b[0;33;40m'
    lightyellow = '\x1b[0;93;40m'
    magenta='\x1b[1;31;40m'
    cyan='\x1b[1;36;40m'
    blue = '\x1b[1;34;40m'
    green = '\x1b[1;32;40m'
    lightgreen = '\x1b[1;92;40m'
    lightcyan = '\x1b[1;96;40m'
    red = '\x1b[1;31;40m'
    lightred = '\x1b[1;91;40m'
    end ='\x1b[0m'

    skip_folders = ("__pycache__", "migrations", '.git')
    skip_extensions = (".swp",)
    skip_but_print = (".ini",)
    exts = {
        'html': blue,
        'css': cyan, 
        'py': lightyellow,
        'python': lightyellow,
        'md': magenta,
        'ps1': lightcyan,
        'csv': green,
        'cshtml': lightgreen,
        'sh': blue,
        'bash': blue,
        'bat': blue,
        'json': lightred,
        'js': folder,
    }
    
    for root, dirs, files in os.walk(startpath, topdown=True):
        dirs[:] = [d for d in dirs if d not in skip_folders]
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)

        # print valid folders
        if os.path.basename(root) not in skip_folders:
            print(f'{indent}{os.path.basename(root)}/{end}')
            subindent = ' ' * 4 * (level + 1)

            # color codes file before print
            for f in files:
                color = stop = ''

                # probably a configuration/encoded file
                if f.startswith('.'):
                    pass

                # known extensions
                elif f.endswith(tuple(exts.keys())):
                    try:
                        color = exts[f.split('.')[-1]]
                        stop = end
                    except:
                        pass

                # try reading the first line of file for shebangs
                else:
                    try:
                        with open(root+'\\'+f, 'r') as curr_file:
                            shebang = curr_file.readline().split(' ')[-1].strip()

                            if shebang in exts.keys():
                                color = exts[shebang]
                                stop = end

                            elif shebang.endswith(tuple(exts.keys())):
                                color = exts[shebang.split('/')[-1]]
                                stop = end
                    # just print plain on error
                    except:
                        pass
                print(f'{color}{subindent}{f}{stop}')

if __name__ == "__main__":
    list_files(os.getcwd())
