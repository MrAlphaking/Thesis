from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import os
img = Image.open('white.jpg')

I1 = ImageDraw.Draw(img)


fonts = os.listdir('./fonts')

for index, font in enumerate(fonts):
    myFont = ImageFont.truetype(f'./fonts/{font}', 25)

    I1.text((40, 30*index), font.split('.')[1], font=myFont, fill=(0, 0, 0), align='center')
img.save("text_on_image.png")