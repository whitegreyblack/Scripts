#!/usr/bin/env python

'''Color sorter for images'''

from PIL import Image,ImageDraw
import sys

if len(sys.argv) < 2:
    print("usage: python image.py [filename]")
    exit()

filename = sys.argv[1]

img = Image.open(filename)
data = img.tobytes()
img.close()

# retrieve r, g, b values by skipping every 3rd data
r = data[0::3]
g = data[1::3]
b = data[2::3]

w,h = img.size
bri = min(w,h)
direction = min(w,h)

# detects brightness option with parameter
if len(sys.argv) == 4:
    if 'b' in sys.argv[2]:
        print("changing brightness")
        bri = int(sys.argv[3])

# detects brightness and size options
if len(sys.argv) == 3:
    if 'b' in sys.argv[2]:
        print("changing brightness to 75%")
        bri = int(bri * .70)
    elif 'h' in sys.argv[2]:
        direction = h
    elif 'v' in sys.argv[2]:
        direction = w

# new image objects with same dimensions as file
im1 = Image.new('RGB', (w, h))
im2 = Image.new('RGB', (w, h))
im3 = Image.new('RGB', (w, h))

# new canvases to hold colors as buffer before saving
draw1 = ImageDraw.Draw(im1)
draw2 = ImageDraw.Draw(im2)
draw3 = ImageDraw.Draw(im3)

def chunk(l, n):
    '''Selects portions of the image l based on length n'''
    return [l[i:i + n] for i in range(0, len(l), n)]

def average(ll):
    '''Gets the average value between values in list ll'''
    digs = []
    for j in ll:
        digs.append(
            (sum([i[0] for i in j]) // bri, 
             sum([i[1] for i in j]) // bri, 
             sum([i[2] for i in j]) // bri))
    return digs

def rgbHSL(x):
    '''
    TODO: work on functionality

    Converts rgb coloring scheme to HSL full color
    '''
    r, g, b = x[0] / 255, x[1] / 255, x[2] / 255
    maxa, mini = max([r, g, b]), min([r, g, b])
    h = s = l = (maxa + mini) / 2

    if maxa == mini or maxa - mini == 0 or maxa + mini == 2:
        h = s = 0
    else:
        d = maxa - mini
        if l > 0.5:
            s = d / (2 - maxa - mini)
        else:
            s = d / (maxa + mini)

        if maxa == r:
                h = (g - b) / d + (6 if g < b else 0)
        elif maxa == g:
                h = (b - r) / d + 2
        elif maxa == b:
                h = (r - g) / d + 4
    h /= 6
    return (h * 360, s * 100, l * 100)

# Begin color mapping and sorting
colors = {}
for i in range(len(r)): 
    if (r[i], g[i], b[i]) not in colors:
        colors[(r[i], g[i], b[i])] = 1
    else:
        colors[(r[i], g[i], b[i] = colors[(r[i], g[i], b[i])] + 1

maps = [[i, rgbHSL(i)]
            for i in average(chunk([i for i in colors.keys() 
                                        for j in range(colors[i])], direction))]

# different sorts for different results
sort1 = sorted(maps, 
               reverse=True, 
               key=lambda tup: (tup[0][2], 
                                tup[0][0], 
                                tup[0][1], 
                                tup[1][0], 
                                tup[1][1], 
                                tup[1][2]))
sort2 = sorted(maps,
               reverse=True,
               key=lambda tup: (tup[0][0],
                                tup[0][2],
                                tup[0][1],
                                tup[1][0],
                                tup[1][1],
                                tup[1][2]))
sort3 = sorted(maps,
               reverse=True,
               key=lambda tup: (sum(tup[0]), 
                                sum(tup[1])))

for i in range(len(maps)):
    if (w < h):
        tup = (0, i, w, i + 1)
    else:
        tup = (i, 0, i + 1, h)
    draw1.rectangle(tup, sort1[i][0])
    draw2.rectangle(tup, sort2[i][0])
    draw3.rectangle(tup, sort3[i][0])
	
fname, extension = filename.split('.')

im1.save('manips/' + fname + '-manip1.' + extension)
im2.save('manips/' + fname + '-manip2.' + extension)
im3.save('manips/' + fname + '-manip3.' + extension)
