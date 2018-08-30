# name: stringify.py
# desc: transforms an image from png to a list of strings for terminal printing
from PIL import Image

def stringify(image_path, debug=False):
    with Image.open(image_path) as image:
        pixels = image.load()
        w, h = image.size
        lines = []
        
        # row major, add line by line
        for j in range(h):
            line = ""
            for i in range(w):
                # check for alpha channel
                try:
                    r, g, b, _ = pixels[i,j]
                except:
                    r, g, b = pixels[i, j]
            
                # separate by colorless pixels
                line += "#" if (r, g, b) == (0, 0, 0) else "."
            lines.append(line)

        if debug:
            print("\n".join(lines))

        return lines

if __name__ == "__main__":
    stringify("testmap.png", debug=True)
