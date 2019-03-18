import platform
import charset
import curses
import time
import sys
import os

# clock.py -- clock app made using curses
# used in cmder/conemu for windows os
__author__  = "Sam Whang"
__email__   = "sangwoowhang@gmail.com"

def main(scr):
    # function returns a tuple pair from a one or two digit number
    splitter = lambda x: (0, x) if x < 9 else (x // 10, x % 10)

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
        timeformat = [ht, ho, ':', mt, mo, ':', st, so]
        
        
        scr.clear()
        scr.border()

        # TODO: only need to change a portion of the screen every time
        # ex: Change only the singles second => 10:00 -> 10:01
        # Very few cases where the entire screen needs to change
        # ex: tens of minutes => 10:49 -> 10:50 (00:11) 1's indicate changes
        #     hourly changes => 10:59 -> 11:00 (01:11)
        #     noon and midnight => 12:59 -> 01:00 (11:11)
        # iteration through each portion of the clock from hour to min to sec
        for k in range(len(timeformat)):
            for i in range(len(val[0])):
                for j in range(len(val[0][0])):
                    if val[timeformat[k]][i][j] == 1:
                        for v in range(8):
                            # may need to revisit this again and separate
                            # for loop variable usages
                            line = v * 2
                            if v > 3:
                                line_offset = 1
                            column = k * 21 + j * 4
                            column_offset = v % 4
                            scr.addch(line + line_offset,
                                      column + column_offset,
                                      key[v])
                            # programmatically calculate values to save time
                            # scr.addch(i * 2, k * 21 + j * 4, key[0])
                            # scr.addch(i * 2, k * 21 + j * 4 + 1, key[1])
                            # scr.addch(i * 2, k * 21 + j * 4 + 2, key[2])
                            # scr.addch(i * 2, k * 21 + j * 4 + 3, key[3])
                            # scr.addch(i * 2 + 1, k * 21 + j * 4 + 0, key[4])
                            # scr.addch(i * 2 + 1, k * 21 + j * 4 + 1, key[5])
                            # scr.addch(i * 2 + 1, k * 21 + j * 4 + 2, key[6])
                            # scr.addch(i * 2 + 1, k * 21 + j * 4 + 3, key[7])
        scr.refresh()

        # prevents screen flickering due to refreshing multiple times per second
        time.sleep(0.1)

        # user input to exit program
        ch = scr.getch()
        if ch == ord('q'):
            break

if __name__ == "__main__":
    # current terminal size
    rows, columns = os.popen('stty size', 'r').read().split()

    # resize to fit the clock
    y, x = 14, 168
    curses.use_env(True)
    os.environ['LINES'] = str(y)
    os.environ['COLUMNS'] = str(x)

    # using conemu/cmder terminal
    if platform.system() == "Windows":
        os.system('conemuc -guimacro windowpossize 0 0 {} {}'.format(x, y)) 
    else:
        raise NotImplementedError
        exit(1)  

    curses.wrapper(main)
