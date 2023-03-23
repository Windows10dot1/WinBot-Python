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

@bot.event
async def on_ready():
    global PizzeriaData
    try:
        PizzeriaJson = open('Pizzerias.json', 'r+')
    except:
        PizzeriaJson = open('Pizzerias.json', 'w')
    
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
async def Pizzeria(ctx):
    global PizzeriaData
    for PizzeriaInfo in PizzeriaData:
        if ctx.author.name == PizzeriaInfo['PizzeriaName']:
            print("c")
            await ctx.send(CurrentLanguage[0] + PizzeriaInfo['PizzeriaName']+  " " + 
                           CurrentLanguage[1] + str(PizzeriaInfo['PizzeriaLevel']) + " " + 
                           CurrentLanguage[2] + str(PizzeriaInfo['PizzeriaPizzas']))
        if ctx.author.name not in PizzeriaInfo['PizzeriaName']:
            await ctx.send(CurrentLanguage[3])
            print("d")

@bot.command()
async def CreatePizzeria(ctx):
    global PizzeriaData
    for PizzeriaInfo in PizzeriaData:
        if ctx.author.name == PizzeriaInfo['PizzeriaName']:
            await ctx.send(CurrentLanguage[4])
            print("a")
        else:
            PizzeriaStartData = [{'PizzeriaName': ctx.author.name,
                            'PizzeriaLevel': 0,
                            'PizzeriaPizzas': 0}]
            print("b")
            with open('Pizzerias.json', 'a', encoding='utf8') as PizzeriasJson:
                json.dump(PizzeriaStartData, PizzeriasJson, ensure_ascii=False)
bot.run('token')