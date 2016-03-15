import random
class Witcher:
    def __init__(self,name,hp,mana,weapons,armor):
        self.name=name
        self.hp=hp
        self.mana=mana
        self.weapons=weapons
        self.armor=armor
        self.signs=["Yrden","Quen","Aard","Igni","Axia"]
    def Magicattack(self,objetive):
        attack=self.signs[random.randint(0,5)]
        print("{0} used {1}".format(self.name,self.attack))
    def changeArmor(self,new_armor):
        self.armor=new_armor
class Dragon:
    def __init__(self,name):
        self.name=name
        self.power=9999999999999999
    def Attack(self,objetive):
        print("You are so f*cking dead")
aa=Witcher("Geralt",120,80,["BulvaSword"],["Daedric Helmet","Daedric Armor","Skirt"])
aa.changeArmor(["Rainbow Helmet","Kitty Armor","Nothing"])
aaa=Dragon("Fistandantilus")
aaa.Attack(aa)
cositasabrosa=Dragon("Saphira")

