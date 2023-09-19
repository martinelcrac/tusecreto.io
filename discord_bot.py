import discord
from discord.ext import commands, tasks
import requests
import random
import time
import asyncio

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

msg = 'hola mundo =)'
is_nsfw = False
gender = 'male'
access_token = ''
loop_task = None  # Variable to store the looping task

headers = {
    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'Content-Type': 'application/json;charset=UTF-8',
    'Accept': 'application/json, text/plain, */*',
    'Referer': 'https://tusecreto.io/',
    'x-access-token': access_token,
    'sec-ch-ua-platform': '"Linux"'
}

async def send_message():
    json_data = {
        'age': str(random.randint(20, 30)),
        'gender': gender,
        'geolocation': '',
        'is_nsfw': is_nsfw,
        'nsfw_hint_visible': False,
        'rules_visible': False,
        'text': msg
    }
    response = requests.post('https://tusecreto.io/api/secrets', headers=headers, json=json_data)
    print(response.status_code)
    print(response.content)
    await asyncio.sleep(5)  # Use asyncio sleep for asynchronous behavior

spam_loop_task = None  # Variable para almacenar la tarea de spam en bucle
loop_interval = 0  # Tiempo en segundos entre cada envío del mensaje

# ... (resto del código) ...

@bot.command()
async def start_spam_loop(ctx):
    global spam_loop_task
    if spam_loop_task and not spam_loop_task.done():
        await ctx.send('El spam en bucle ya está en ejecución.')
    else:
        spam_loop_task = bot.loop.create_task(spam_loop_messages(ctx))
        await ctx.send('Spam en bucle iniciado.')

@bot.command()
async def stop_spam_loop(ctx):
    global spam_loop_task
    if spam_loop_task and not spam_loop_task.done():
        spam_loop_task.cancel()
        await ctx.send('Spam en bucle detenido.')
    else:
        await ctx.send('No hay un bucle de spam en ejecución.')

async def spam_loop_messages(ctx):
    while True:
        global is_nsfw
        is_nsfw = not is_nsfw  # Alternamos entre NSFW activado y desactivado
        await send_message()
        await asyncio.sleep(loop_interval)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def set_message(ctx, *, message):
    global msg
    msg = message
    await ctx.send('Mensaje configurado exitosamente!')

@bot.command()
async def set_nsfw(ctx, is_nsfw_val: bool):
    global is_nsfw
    is_nsfw = is_nsfw_val
    await ctx.send(f'NSFW set to {is_nsfw_val}!')

@bot.command()
async def set_gender(ctx, gender_val: str):
    global gender
    gender = gender_val
    await ctx.send(f'Gender set to {gender_val}!')

@bot.command()
async def set_token(ctx, token):
    global access_token
    access_token = token
    headers['x-access-token'] = access_token
    await ctx.send('Access token set successfully!')

@bot.command()
async def start_loop(ctx):
    global loop_task
    if loop_task and not loop_task.is_running():
        loop_task.start()
        await ctx.send('Loop started!')
    elif not loop_task:
        loop_task = bot.loop.create_task(loop_messages(ctx))

@bot.command()
async def send_once(ctx):
    await send_message()
    await ctx.send('Mensaje enviado a la API una vez.')

@bot.command()
async def stop_loop(ctx):
    global loop_task
    if loop_task and loop_task.is_running():
        loop_task.cancel()
        await ctx.send('Loop stopped!')
    else:
        await ctx.send('No active loop to stop.')

async def loop_messages(ctx):
    while True:
        await send_message()
        await asyncio.sleep(3)  # Loop every 5 seconds

@bot.command()
async def config(ctx):
    response = (
        f"**Configuración actual:**\n"
        f"Mensaje: `{msg}`\n"
        f"NSFW: `{'Sí' if is_nsfw else 'No'}`\n"
        f"Género: `{gender}`\n"
        f"Token de Acceso: `{access_token if access_token else 'No configurado'}`"
    )
    await ctx.send(response)

@bot.command()
async def commands(ctx):
    command_list = [f"!{command.name}" for command in bot.commands]
    response = "Comandos disponibles:\n" + "\n".join(command_list)
    await ctx.send(response)

# Run the bot
bot.run('')  # Replace with your bot token
