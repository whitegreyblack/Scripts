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

for j in range(h):
	for i in range(w):
		try:
			r, g, b, a = pixels[i, j]
			if printed:
				printed = False
				print("r,b,g,a")
			listed.append((r,b,g,a))
		except:
			r, g, b = pixels[i, j]
			if printed:
				printed = False
				print("r,g,b")
			listed.append((0,r,g,b))
sort1 = sorted(listed, key=lambda x: x[::1])

for i in range(w):
	for j in range(h):
		tup = (j, i, j+1, i+1)
		#tup = (0,i,w,i+1) if w < h else (i,0,i+1,h)
		drawer.rectangle(tup, sort1[j*w])

f, e = filename.split('.')
print(f, '+', e)
new_img.save(f+'-new_img_rbga.'+e)