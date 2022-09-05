from PIL import Image
def getloc(x, y):
    px_list = []
    im = Image.open(r"map/map.png")
    im = im.convert('RGBA')
    px = im.load()
    x -= 2
    y -= 2
    for n in range(5):
        for n in range(4):
            color = im.getpixel((x,y))
            if x < 0 or x > im.size[0] or y < 0 or y > im.size[1]:
                px_list.append("void")
            else:
                if color == (0,255,33,255):
                    px_list.append("plains")
                elif color == (0,38,255,255):
                    px_list.append("river")
                elif color == (0,127,14,255):
                    px_list.append("forest")
                elif color == (255,216,0,255):
                    px_list.append("desert")
            print(x,y)
            x += 1
        color = im.getpixel((x,y))
        if x < 0 or x > im.size[0] or y < 0 or y > im.size[1]:
            px_list.append("void")
        else:
            if color == (0,255,33,255):
                px_list.append("plains")
            elif color == (0,38,255,255):
                px_list.append("river")
            elif color == (0,127,14,255):
                px_list.append("forest")
            elif color == (255,216,0,255):
                px_list.append("desert")
            elif x < 0 or x > img.size[0] or y < 0 or y > img.size[1]:
                px_list.append("void")
        print(x,y)
        y += 1
        x -= 4
    print(px_list)
    return(px_list)