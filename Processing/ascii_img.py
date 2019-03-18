from PIL import Image
import ansi_colors as colors
img = Image.open("sampleimg.png")

stmt = "STATEMENT"

print(colors.CBLUE+stmt+colors.CEND)
print(colors.CBLUE2+stmt+colors.CEND)