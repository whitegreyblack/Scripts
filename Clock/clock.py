import platform
import charset
import curses
import time
import sys
import os

# clock.py -- clock app made using curses
# used in cmder/conemu for windows os
__author__  = "Sam WHang | WGB"
__email__   = "sangwoowhang@gmail.com"
__license__ = "MIT"

def main(scr):

    # function returns a tuple pair from a one/two pair digit
    splitter = lambda x: (0, x) if x < 9 else (x//10, x%10)

    # retrieves character set key and number mappings
    key = charset.circle
    val = charset.number

    # setting curses input delay and cursor visibility
    curses.curs_set(0)
    scr.nodelay(1)
    
    # main program logic
    while True:
        
        # splits time into hour/min/sec sections
        t = time.localtime()
        ht, ho = splitter(t.tm_hour)
        mt, mo = splitter(t.tm_min)
        st, so = splitter(t.tm_sec)
        
        # form a list of these items including colons for seperators
        form = [ht,ho,':',mt,mo,':',st,so]
        
        
        scr.clear()
        scr.border()

        # iteration through each portion of the clock from hour to min to sec
        for k in range(len(form)):
            for i in range(len(val[0])):
                for j in range(len(val[0][0])):
                    if val[form[k]][i][j] == 1:
                        scr.addch(i*2, k*21+j*4, key[0])
                        scr.addch(i*2, k*21+j*4+1, key[1])
                        scr.addch(i*2, k*21+j*4+2, key[2])
                        scr.addch(i*2, k*21+j*4+3, key[3])
                        scr.addch(i*2+1, k*21+j*4+0, key[4])
                        scr.addch(i*2+1, k*21+j*4+1, key[5])
                        scr.addch(i*2+1, k*21+j*4+2, key[6])
                        scr.addch(i*2+1, k*21+j*4+3, key[7])
        scr.refresh()

        # prevents screen flickering due to refreshing multiple times per second
        time.sleep(0.1)

        # user input to exit program
        ch = scr.getch()
        if ch == ord('q'):
            break

if __name__ == "__main__":
    rows, columns = os.popen('stty size', 'r').read().split()
    # resize to fit the clock
    y, x = 14, 168
    curses.use_env(True)
    os.environ['LINES']=str(y)
    os.environ['COLUMNS']=str(x)
    # using conemu/cmder terminal
    if platform.system() == "Windows":
        os.system('conemuc -guimacro windowpossize 0 0 {} {}'.format(x, y)) 
    else:
        raise NotImplementedError
        exit(-1)  

    curses.wrapper(main)
