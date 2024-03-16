import discord
import random
import requests
from discord.ext import commands
from bot_logic import gen_pass
from bot_logic import toss_coin
import get_model

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def genpass(ctx,pass_lenght = 8):
    await ctx.send(f'Ваш пароль: {gen_pass(pass_lenght)}')

@bot.command()
async def commands(ctx):
    await ctx.send('Существующие команды:\n'
                   '1. genpass - генерирует пароль указанной вами длины\n'
                   '2. tosscoin - подбрасывает монетку\n' 
                   '3. hello - бот представится своим именем\n'  
                   '4. heh - пишет сообщение со смехом указанной вами длины\n'
                   '5. repeat - повтоворяет ваше сообщение указанное количество раз\n'  
                   '6. mem - отправляет мемы про программирование\n'
                   '7. dog - отправляет случайное фото с собакой\n'  
                   '8. duck - отправляет случайное фото с уткой\n'
                   '9. howLongDecomposeHelp - Указывает поддерживаемы виды мусора для комманды howLongDecompose\n'
                   '10. howLongDecompose - рассказывает сколько разлагается тот или иной вид мусора и как его утилизировать(узнать виды мусора можно по команде howLongDecomposeHelp)')

@bot.command()
async def tosscoin(ctx):
    await ctx.send(toss_coin())

@bot.command()
async def hello(ctx):
    await ctx.send(f'Привет! Я бот {bot.user}!')

@bot.command()
async def heh(ctx, count_heh = 5):
    await ctx.send("he" * count_heh)

@bot.command()
async def repeat(ctx, times: int, content='repeating...'):
    """Repeats a message multiple times."""
    for i in range(times):
        await ctx.send(content)

@bot.command()
async def howLongDecomposeHelp(ctx):
    await ctx.send('Виды мусора:\n'
                   '1. пластик\n'
                   '2. дерево\n'
                   '3. железо\n'
                   '4. алюминий\n'
                   '5. биомусор')


@bot.command()
async def howLongDecompose(ctx, trash = "Вы не указали вид мусора, или он не поддерживается"):
    if trash == "пластик" or "Пластик":
        await ctx.send('В среднем, пластик разлагается 300 лет! Его следует выбрасывать отдельно от остальных видов.')
    elif trash == 'дерево'or 'Дерево':
        await ctx.send('В среднем, ничем не обработанная древесина разлагается 6 лет! Настоятельно рекомендуем использовать ее по максимуму, а не выкидывать')
    elif trash == 'железо' or 'Железо':
        await ctx.send('В среднем, железо в природе разлагается в природе за 95 лет! Лучшим советом по утилизации будет, сдача в пункт приёма металлов.')
    elif trash == 'алюминий' or 'Алюминий':
        await ctx.send('В среднем, алюминий разлагается намного дольше других металлов, это аж целых 500 лет! Его подобно железу следует сдать в пункт приема.')
    elif trash == 'биомусор' or 'Биомусор':
        await ctx.send('В среднем, биомусор разлагается всего за 2 недели. Его следует просто отправлять на свалку или сжигать. Данный вид мусора самый безвредный для экологии.')




@bot.command()
async def mem(ctx):
    a = random.randint(1,4)
    with open(f'images/mem{a}.jpg', 'rb') as f:
        # В переменную кладем файл, который преобразуется в файл библиотеки Discord!
        picture = discord.File(f)
   # Можем передавать файл как параметр!
    await ctx.send(file=picture)

def get_duck_image_url():
    url = 'https://random-d.uk/api/random'
    res = requests.get(url)
    data = res.json()
    return data['url']

def get_dog_image_url():
    url = 'https://random.dog/woof.json'
    res = requests.get(url)
    data = res.json()
    return data['url']

@bot.command()
async def animals(ctx):
    grade = ''
    a = random.randint(1,100)
    if 1 <= a <= 70:
        b = random.randint(1,5)
        grade = 'common'
        with open(f'animalsmemes/{grade}/mem{b}.jpg', 'rb') as f:
            picture = discord.File(f)
    elif 71 <= a <= 95:
        b = random.randint(1, 3)
        grade = 'rare'
        with open(f'animalsmemes/{grade}/mem{b}.jpg', 'rb') as f:
            picture = discord.File(f)
    elif 96 <= a <= 100:
        grade = 'legendary'
        with open(f'animalsmemes/{grade}/mem1.jpg', 'rb') as f:
            picture = discord.File(f)

    await ctx.send(file=picture)
    if grade == 'common':
        await ctx.send('Вам выпал обычный мем')
    elif grade == 'rare':
        await ctx.send('Вам выпал редкий мем')
    elif grade == 'legendary':
        await ctx.send('Вам выпал легендарный мем \nP.s: Ты везунчик)')

@bot.command('dog')
async def dog(ctx):
    '''По команде dog вызывает функцию get_dog_image_url'''
    image_url = get_dog_image_url()
    await ctx.send(image_url)

@bot.command('duck')
async def duck(ctx):
    '''По команде duck вызывает функцию get_duck_image_url'''
    image_url = get_duck_image_url()
    await ctx.send(image_url)

@bot.command(description='For when you wanna settle the score some other way')
async def choose(ctx, *choices: str):
    """Chooses between multiple choices."""
    await ctx.send(random.choice(choices))

@bot.command()
async def save(ctx):
    if ctx.message.attachments != []:

        for attachment in ctx.message.attachments:
            filename = attachment.filename
            await attachment.save(filename)
            await ctx.send(get_model.detect_object(filename))


bot.run("")

