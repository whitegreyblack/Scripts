#!/usr/bin/env python

'''Greyscale to color converter'''

__author__ = "Sam Whang"

from PIL import Image, ImageDraw
import sys

if len(sys.argv) < 2:
    exit("usage: python image.py [filename]")
filename = sys.argv[1]

with Image.open(filename).convert('RGBA') as img:
    pixels = img.load()
    w, h = img.size
	
listed = []
new_img = Image.new('RGBA', (w, h))
drawer = ImageDraw.Draw(new_img)
printed = True

# determine if alpha channel exists in pixels
# may not need to do this for every pixel, maybe just one
for j in range(h):
    for i in range(w):
        try:
            r, g, b, a = pixels[i, j]
            if printed:
                printed = False
                print("r, b, g, a")
            listed.append((r, b, g, a))
        except:
            r, g, b = pixels[i, j]
            if printed:
                printed = False
                print("r, g, b")
            listed.append((0, r, g, b))

sort1 = sorted(listed, key=lambda x: x[::1])

for i in range(w):
    for j in range(h):
        tup = (j, i, j + 1, i + 1)
        drawer.rectangle(tup, sort1[j * w])

fname, extension = filename.split('.')
print(fname + '+' + extension)
new_img.save(f + '-new_img_rbga.' + e)
