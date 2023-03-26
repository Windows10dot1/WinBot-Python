import asyncio
import discord
import json
from discord.ext import commands

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents, case_insensitive=True)
#### Language Variables Setup ####
Languages = ["en","tr"]
en = ["Pizzeria Name: ", "Level: ", "Pizzas: ", "Money: ", "XP: ", "Create a pizzeria first!", "You already have a pizzeria!", "Cook some pizzas to sell!", "Not enough pizza!"]
tr = ["Pizzacı Adı: ", "Seviye: ", "Pizza Sayısı: ", "Para: ", "Tecrübe: ", "Önce bir pizzacı açın!", "Zaten bir pizzacınız var!", "Satmak için biraz pizza pişirin!", "Yetersiz pizza!"]
CurrentLanguage = en

#### Pizerria Variables Setup ####
PizzeriaData = ""
PizzeriaXPMultiplier = 0.85
PizzeriaMoneyMultiplier = 1.15

async def OpenPizzeriaJson() -> str:
    global PizzeriaData
    try:
        PizzeriaJson = open('Pizzerias.json')
        PizzeriaData = json.load(PizzeriaJson)
    except FileNotFoundError:
        await CreatePizzeriasJson()
    return PizzeriaData

async def CreatePizzeriasJson():
    try:
        PizzeriaJson = open('Pizzerias.json', 'r+')
        PizzeriaJson.close()
    except:
        PizzeriaJson = open('Pizzerias.json', 'w')
        PizzeriaJson.close()
@bot.event
async def on_ready():
    await CreatePizzeriasJson()
#### #### Language Commands #### ####
@bot.command()
async def ListLanguages(ctx):
    for Langs in Languages:
        await ctx.send(Langs)
@bot.command()
async def ChangeLanguage(ctx, Language):
    if Language in Languages:
        global CurrentLanguage
        SelectedLanguage = Language
        CurrentLanguage = globals()[SelectedLanguage]
    else:
        await ctx.send("Language doesn't exists")

#### #### Pizza Game #### #### 
@bot.command()
#### Pizzeria Information ####
async def Pizzeria(ctx):
    global PizzeriaData
    PizzeriaFound = False
    try:
        PizzeriaData = await OpenPizzeriaJson()
        for PizzeriaInfo in PizzeriaData:
            if ctx.author.name == PizzeriaInfo['PizzeriaName']:
                PizzeriaFound = True
                await ctx.send(CurrentLanguage[0] + PizzeriaInfo['PizzeriaName']+  "\n" + 
                                CurrentLanguage[1] + str(PizzeriaInfo['PizzeriaLevel']) + "\n" + 
                                CurrentLanguage[2] + str(PizzeriaInfo['PizzeriaPizzas']) + "\n" +
                                CurrentLanguage[3] + str(PizzeriaInfo['PizzeriaMoney']) + "\n"+ 
                                CurrentLanguage[4] + str(PizzeriaInfo['PizzeriaXP']))
                break
        if PizzeriaFound != True:
            await ctx.send(CurrentLanguage[5])
    except:
        await ctx.send(CurrentLanguage[5])
#### Create New Pizzeria ####
@bot.command()
async def CreatePizzeria(ctx):
    global PizzeriaData
    PizzeriaFound = False
    try:
        PizzeriaData = await OpenPizzeriaJson()
        for PizzeriaInfo in PizzeriaData:
            if ctx.author.name == PizzeriaInfo['PizzeriaName']:
                await ctx.send(CurrentLanguage[6])
                PizzeriaFound = True
                break
        if PizzeriaFound != True:
            PizzeriaInitData = {'PizzeriaName': ctx.author.name,
                                'PizzeriaLevel': 0,
                                'PizzeriaPizzas': 0,
                                'PizzeriaMoney': 0,
                                'PizzeriaXP': 0}
            with open('Pizzerias.json', 'r', encoding='utf8') as PizzeriasJson:
                TempJson = json.load(PizzeriasJson)
                TempJson.append(PizzeriaInitData)
                with open('Pizzerias.json', 'w', encoding='utf8') as Pizzerias:
                    json.dump(TempJson, Pizzerias, ensure_ascii=False, indent=4, separators=(",", ": "))
                    PizzeriasJson.close()
                    Pizzerias.close()
    except:
        with open('Pizzerias.json', 'r+', encoding='utf8') as PizzeriasJson:
            PizzeriaInitData = [{'PizzeriaName': ctx.author.name,
                                'PizzeriaLevel': 0,
                                'PizzeriaPizzas': 0,
                                'PizzeriaMoney': 0,
                                'PizzeriaXP': 0}]
            json.dump(PizzeriaInitData, PizzeriasJson, ensure_ascii=False, indent=4, separators=(',', ': '))
            PizzeriasJson.close()
#### Cook Pizza ####
@bot.command()
async def FireupPizzas(ctx, PizzaCount):
    global PizzeriaData
    PizzeriaFound = False
    try:
        PizzeriaData = await OpenPizzeriaJson()
        for PizzeriaInfo in PizzeriaData:
            if ctx.author.name == PizzeriaInfo['PizzeriaName']:
                SelectedIndex = PizzeriaData.index(PizzeriaInfo)
                CurrentPizzas = PizzeriaInfo['PizzeriaPizzas']
                await asyncio.sleep(int(PizzaCount)*0.5)
                CurrentPizzas = CurrentPizzas + int(PizzaCount)
                PizzeriaInfo['PizzeriaPizzas'] = CurrentPizzas
                PizzeriaData[SelectedIndex] = PizzeriaInfo
                with open('Pizzerias.json', 'r+', encoding='utf8') as PizzeriasJson:
                    json.dump(PizzeriaData, PizzeriasJson, ensure_ascii=False, indent=4, separators=(',', ': '))
    except:
        await ctx.send(CurrentLanguage[5])
#### Sell Pizza ####
@bot.command()
async def SellPizzas(ctx, PizzaCount):
    global PizzeriaData
    PizzeriaFound = False
    try:
        PizzeriaData = await OpenPizzeriaJson()
        for PizzeriaInfo in PizzeriaData:
            if ctx.author.name == PizzeriaInfo['PizzeriaName']:
                SelectedIndex = PizzeriaData.index(PizzeriaInfo)
                CurrentPizzas = PizzeriaInfo['PizzeriaPizzas']
                CurrentMoney = PizzeriaInfo['PizzeriaMoney']
                CurrentXP = PizzeriaInfo['PizzeriaXP']
                if CurrentPizzas != 0:
                    if int(PizzaCount) > CurrentPizzas:
                        await ctx.send(CurrentLanguage[8])
                    else:
                        CurrentPizzas = CurrentPizzas - int(PizzaCount)
                        CurrentMoney = int(CurrentMoney + int(PizzaCount) * PizzeriaMoneyMultiplier)
                        CurrentXP = int(CurrentXP + int(PizzaCount) / PizzeriaXPMultiplier)
                        PizzeriaInfo['PizzeriaPizzas'] = CurrentPizzas
                        PizzeriaInfo['PizzeriaMoney'] = CurrentMoney
                        PizzeriaInfo['PizzeriaXP'] = CurrentXP
                        PizzeriaData[SelectedIndex] = PizzeriaInfo
                        with open('Pizzerias.json', 'r+', encoding='utf8') as PizzeriasJson:
                            json.dump(PizzeriaData, PizzeriasJson, ensure_ascii=False, indent=4, separators=(',', ': '))
                else:
                    await ctx.send(CurrentLanguage[7])
    except Exception as e :
        await ctx.send(e)
        await ctx.send(CurrentLanguage[5])

bot.help_command=MyHelpCommand()
#### Start Bot ####
bot.run('OTQ5MDU4MzMyMzM1OTQ3ODY3.GpdJyu.6zQqRvcLmeN_OJOpdkuFCOQcFwKMRuCuwO-vEk')