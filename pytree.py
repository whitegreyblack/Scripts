__author__  = "Sam WHang | WGB"
__email__   = "sangwoowhang@gmail.com"
__license__ = "MIT"


import os

#blue for directories
folder='\x1b[0;34;40m'
yellow='\x1b[0;33;40m'
red='\x1b[1;31;40m'
end ='\x1b[0m'

skip = ["__pycache__","migrations"]
exts = ['html','css','py']
def list_files(startpath):
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        if os.path.basename(root) not in skip:
            print('{}{}{}/{}'.format(folder,indent, os.path.basename(root),end))
            subindent = ' ' * 4 * (level + 1)
            for f in files:
                color=''
                if f.endswith(exts[0]): color = red
                if f.endswith('html'): color = yellow
                print('{}{}{}{}'.format(color,subindent, f,end))

if __name__ == "__main__":
    list_files(os.getcwd())
