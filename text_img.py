from PIL import Image, ImageDraw, ImageFont
def profile():
    # make a blank image for the text, initialized to transparent text color
    txt = Image.new('RGBA', (200,200), (0,20,255,255))

    # get a font
    fnt = ImageFont.truetype('fonts/Roboto-Regular.ttf', 200)
    # get a drawing context
    d = ImageDraw.Draw(txt)

    # draw text, half opacity
    d.text((33,-10), "Charity", font=fnt,  fill=(0,255,0,255), align='center')
    # draw text, full opacity
# make a blank image for the text, initialized to transparent text color
txt = Image.new('RGBA', (110,50), (153, 153, 255,255))
#470
# get a font
fnt = ImageFont.truetype('fonts/Lemon.ttf', 32)
# get a drawing context
d = ImageDraw.Draw(txt)

# draw text, half opacity
d.text((0,2), "funity", font=fnt,  fill=(0, 51, 204,255), align='center')
# draw text, full opacity




#txt.show()
txt.save('files/lastest.ico')
txt.close()
