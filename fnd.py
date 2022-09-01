import json
import random
def findi():
    item_list = []
    common = []
    uncommon = []
    rare = []
    epic = []
    legendary = []
    mythic = []
    with open("json/items.json","r") as file:
        load = json.load(file)
        for i in load[0]:
            if load[0][i]["rarity"] == 0:
                common.append(i)
        for i in load[0]:
            if load[0][i]["rarity"] == 1:
                uncommon.append(i)
        for i in load[0]:
            if load[0][i]["rarity"] == 2:
                rare.append(i)
        for i in load[0]:
            if load[0][i]["rarity"] == 3:
                epic.append(i)
        for i in load[0]:
            if load[0][i]["rarity"] == 4:
                legendary.append(i)
        for i in load[0]:
            if load[0][i]["rarity"] == 5:
                mythic.append(i)
        for i in range(0,10):
            if random.randrange(0,2) == 0:
                rarities = ["common","uncommon","rare","epic","legendary","mythical"]
                chances = [60,20,10,5,3,2]
                results = random.choices(rarities,chances)
                print(results)
                if results[0] == "common":
                    item_list.append(random.choice(common))
                if results[0] == "uncommon":
                    item_list.append(random.choice(uncommon))
                if results[0] == "rare":
                    item_list.append(random.choice(rare))
                if results[0] == "epic":
                    item_list.append(random.choice(epic))
                if results[0] == "legendary":
                    item_list.append(random.choice(legendary))
                if results[0] == "mythic":
                    item_list.append(random.choice(mythic))
            else:
                print("nope")
    return(item_list)