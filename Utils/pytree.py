__author__  = "Sam WHang | WGB"
__email__   = "sangwoowhang@gmail.com"
__license__ = "MIT"

import os

def list_files(startpath):
    '''
    walks through directory with os.walk and lists directories 
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
    # green
    lightcyan = '\x1b[1;96;40m'
    end ='\x1b[0m'

    skip = ("__pycache__", "migrations", '.git')
    exts = {
        'html': blue,
        'css': cyan, 
        'py': lightyellow, 
        'md': lightcyan,
    }
    for root, dirs, files in os.walk(startpath, topdown=True):
        dirs[:] = [d for d in dirs if d not in skip]
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)

        if os.path.basename(root) not in skip:
            # prints folder
            print('{}{}{}/{}'.format(folder,indent, os.path.basename(root),end))
            subindent = ' ' * 4 * (level + 1)

            # color codes file before print
            for f in files:
                for ext in exts:
                    if f.endswith(ext):
                        print('{}{}{}{}'.format(exts[ext], subindent, f, end))
                        break
                else:
                    print('{}{}'.format(subindent, f))

if __name__ == "__main__":
    list_files(os.getcwd())
