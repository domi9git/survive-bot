import nextcord
def getcolor(load,item):
    clr = nextcord.Colour
    if load[0][str(item)]["rarity"] == 0: #common
        clr = nextcord.Colour.from_rgb(255,255,255)
    elif load[0][str(item)]["rarity"] == 1: #uncommon
        clr = nextcord.Colour.from_rgb(0,255,0)
    elif load[0][str(item)]["rarity"] == 2: #rare
        clr = nextcord.Colour.from_rgb(0,0,255)
    elif load[0][str(item)]["rarity"] == 3: #epic
        clr = nextcord.Colour.from_rgb(112,0,255)
    elif load[0][str(item)]["rarity"] == 4: #legendary
        clr = nextcord.Colour.from_rgb(255,0,255)
    elif load[0][str(item)]["rarity"] == 5: #mythic
        clr = nextcord.Colour.from_rgb(255,208,0)
    return clr