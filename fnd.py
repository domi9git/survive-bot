import json
import random
def findi(biome):
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
                for j in load[0][i]["biomes"]:
                    print(j)
                    print(biome)
                    if j == biome[0]:
                        common.append(i)
        for i in load[0]:
            if load[0][i]["rarity"] == 1:
                for j in load[0][i]["biomes"]:
                    if j == biome[0]:
                        uncommon.append(i)
        for i in load[0]:
            if load[0][i]["rarity"] == 2:
                for j in load[0][i]["biomes"]:
                    if j == biome[0]:
                        rare.append(i)
        for i in load[0]:
            if load[0][i]["rarity"] == 3:
                for j in load[0][i]["biomes"]:
                    if j == biome[0]:
                        epic.append(i)
        for i in load[0]:
            if load[0][i]["rarity"] == 4:
                for j in load[0][i]["biomes"]:
                    if j == biome[0]:
                        legendary.append(i)
        for i in load[0]:
            if load[0][i]["rarity"] == 5:
                for j in load[0][i]["biomes"]:
                    if j == biome[0]:
                        mythic.append(i)
        for i in range(0,10):
            if random.randrange(0,2) == 0:
                rarities = ["common","uncommon","rare","epic","legendary","mythic"]
                chances = [200,75,25,10,5,1]
                results = random.choices(rarities,chances)
                if results[0] == "common" and common:
                    item_list.append(random.choice(common))
                if results[0] == "uncommon" and uncommon:
                    item_list.append(random.choice(uncommon))
                if results[0] == "rare" and rare:
                    item_list.append(random.choice(rare))
                if results[0] == "epic" and epic:
                    item_list.append(random.choice(epic))
                if results[0] == "legendary" and legendary:
                    item_list.append(random.choice(legendary))
                if results[0] == "mythic" and mythic:
                    item_list.append(random.choice(mythic))
    return(item_list)
