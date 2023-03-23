import asyncio
import discord
import json
from discord.ext import commands

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents, case_insensitive=True)
#### Language Variables Setup ####
Languages = ["en","tr"]
en = ["Pizzeria Name: ", "Level: ", "Pizzas: ", "Create a pizzeria first!", "You already have a pizzeria!"]
tr = ["Pizzacı Adı: ", "Seviye: ", "Pizza Sayısı: ", "Önce bir pizzacı açın!", "Zaten bir pizzacınız var!"]
CurrentLanguage = en

#### Pizerria Variables Setup ####
PizzeriaData = ""

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
@bot.command()
#### Language Commands ####
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
#### Pizza Game #### 
@bot.command()
#### User's Pizzeria Information ####
async def Pizzeria(ctx):
    global PizzeriaData
    PizzeriaFound = False
    try:
        PizzeriaData = await OpenPizzeriaJson()
        for PizzeriaInfo in PizzeriaData:
            if ctx.author.name == PizzeriaInfo['PizzeriaName']:
                PizzeriaFound = True
                await ctx.send(CurrentLanguage[0] + PizzeriaInfo['PizzeriaName']+  " " + 
                                CurrentLanguage[1] + str(PizzeriaInfo['PizzeriaLevel']) + " " + 
                                CurrentLanguage[2] + str(PizzeriaInfo['PizzeriaPizzas']))
                break
        if PizzeriaFound != True:
            await ctx.send(CurrentLanguage[3])
    except:
        await ctx.send(CurrentLanguage[3])
#### Create New Pizzeria ####
@bot.command()
async def CreatePizzeria(ctx):
    global PizzeriaData
    PizzeriaFound = False
    try:
        PizzeriaData = await OpenPizzeriaJson()
        for PizzeriaInfo in PizzeriaData:
            if ctx.author.name == PizzeriaInfo['PizzeriaName']:
                await ctx.send(CurrentLanguage[4])
                PizzeriaFound = True
                break
        if PizzeriaFound != True:
            PizzeriaInitData = {'PizzeriaName': ctx.author.name,
                                'PizzeriaLevel': 0,
                                'PizzeriaPizzas': 0}
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
                                'PizzeriaPizzas': 0}]
            json.dump(PizzeriaInitData, PizzeriasJson, ensure_ascii=False, indent=4, separators=(',', ': '))
            PizzeriasJson.close()
#### Cook Pizza ####
@bot.command()
async def FireupPizzas(ctx, PizzaCount):
    global PizzeriaData
    PizzeriaFound = False
    PizzeriaData = await OpenPizzeriaJson()
    for PizzeriaInfo in PizzeriaData:
        if ctx.author.name == PizzeriaInfo['PizzeriaName']:
            await asyncio.sleep(1*int(PizzaCount))
            TempPizzaCount = PizzeriaInfo['PizzeriaPizzas']
            TempPizzaCount = TempPizzaCount + int(PizzaCount)
            PizzeriaInfo['PizzeriaPizzas'] = TempPizzaCount
            with open('Pizzerias.json', 'r+') as PizzeriasJson:
                json.dump(PizzeriaInfo, PizzeriasJson, ensure_ascii=False, indent=4, separators=(',', ': '))
bot.run('token')