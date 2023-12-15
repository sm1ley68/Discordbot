# from typing import Optional
import os
import datetime
import disnake
from disnake.ext import commands
import random
import os

import Moderation as moderation

bot = commands.Bot(command_prefix="$", help_command=None, intents=disnake.Intents.all(),
                   test_guilds=[793728158150557707])

CENSORED_WORDS = []

with open('token.txt', 'r') as file:
    TOKEN = file.read().replace('\n', '')
@bot.event
async def on_ready():
    print(f'Bot {bot.user} in ready to work!')

# @bot.event
# async def panel_menu(member):
#     embed = disnake.Embed(
#         title='Приветствуем тебя!',
#
#     )


# пока не работает


# описание ошибок
@bot.event
async def on_command_error(ctx, error):
    print(error)

    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f'{ctx.author}, у вас недостаточно прав для выполнения данной команды')
    elif isinstance(error, commands.UserInputError):
        await ctx.send(embed=disnake.Embed(
            description=f'Правильное использование команды: `{ctx.prefix}{ctx.command.name}`, ({ctx.command.brief})\n'
        ))


# Удаляет мат
@bot.event
async def on_message(message):
    await bot.process_commands(message)
    for content in message.content.split():
        for censored_word in CENSORED_WORDS:
            if content.lower() == censored_word:
                await message.delete()
                await message.channel.send(f'{message.author.mention} Братух, такое писать не стоит :chicken:')


# кик пользователя
    if message.content == 'кик':
        member = message.mentions[0]
        await moderation.kick(member)


# мут пользователя
    if message.content == '$мут':
        member = message.mentions[0]
        await moderation.mute(member)


# анмут пользователя
    if message.content == '$анмут':
        member = message.mentions[0]
        await moderation.anmute(member)

# бан пользователя
    if message.content == '$бан':
        member = message.mentions[0]
        await moderation.ban(member)


# бросок кубика
@bot.command(name='roll', aliases=['ролл', 'роллим'], help='Бросить шестигранный кубик')
async def roll(ctx):
    # Генерируем случайное число от 1 до 6
    result = random.randint(1, 6)

    # Отправляем результат в чат
    if result == 1:
        await ctx.send(f'{ctx.author.mention} 🎲бросает шестигранный кубик и получает: {result}')
        await ctx.send('https://tenor.com/bPgW2.gif')
    elif result == 2:
        await ctx.send(f'{ctx.author.mention} 🎲бросает шестигранный кубик и получает: {result}')
        await ctx.send('https://tenor.com/bPgW3.gif')
    elif result == 3:
        await ctx.send(f'{ctx.author.mention} 🎲бросает шестигранный кубик и получает: {result}')
        await ctx.send('https://tenor.com/bPgW4.gif')
    elif result == 4:
        await ctx.send(f'{ctx.author.mention} 🎲бросает шестигранный кубик и получает: {result}')
        await ctx.send('https://tenor.com/bPgXb.gif')
    elif result == 5:
        await ctx.send(f'{ctx.author.mention} 🎲бросает шестигранный кубик и получает: {result}')
        await ctx.send('https://tenor.com/bPgW8.gif')
    elif result == 6:
        await ctx.send(f'{ctx.author.mention} 🎲бросает шестигранный кубик и получает: {result}')
        await ctx.send('https://tenor.com/bPgXc.gif')


@bot.command(name='r', help='Бросить кубик с указанным значением')
async def roll(ctx, max_value: int):
    if max_value < 1:
        await ctx.send('Максимальное значение должно быть не менее 1.')
        return

    # Генерируем случайное число от 1 до max_value
    result = random.randint(1, max_value)

    # Отправляем результат в чат
    await ctx.send(f'{ctx.author.mention} выпадает число: {result}')


random_number = None


# Команда для начала новой игры
@bot.command(name='startgame', help='Начать новую игру "Угадай число"')
async def start_game(ctx):
    global random_number
    # Генерируем случайное число от 1 до 100
    random_number = random.randint(1, 100)
    await ctx.send('Новая игра началась! Я загадал число от 1 до 100. Попробуйте угадать командой $guess [число].')


# Команда для угадывания числа
@bot.command(name='guess', help='Попробовать угадать число')
async def guess_number(ctx, user_guess: int):
    global random_number

    if random_number is None:
        await ctx.send('Сначала начните новую игру командой $startgame.')
        return

    if user_guess == random_number:
        await ctx.send(f':tada:Поздравляю! Вы угадали число {random_number}.')
        random_number = None
    elif user_guess < random_number:
        await ctx.send('Ваше число меньше загаданного. Попробуйте еще раз!')
    else:
        await ctx.send('Ваше число больше загаданного. Попробуйте еще раз!')


@bot.command(name='commands', aliases=['хелп', 'команды'], help='Показать список команд бота')
async def show_commands(ctx):
    # Получаем список команд бота
    command_list = [f'{command.name}: {command.help}' for command in bot.commands]

    # Форматируем список команд в виде строки и отправляем в чат
    commands_str = '\n'.join(command_list)
    await ctx.send(f'Список команд:\n```\n{commands_str}\n```')


# чистит чат
@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def clear(ctx, amount=30):
    await ctx.channel.purge(limit=amount)


# Список вопросов и ответов
questions_and_answers = [
    {"question": "Какая столица России?", "answer": "Москва"},
    {"question": "Какое самое большое озеро в мире?", "answer": "Байкал"},
    {"question": "Сколько планет в Солнечной системе?", "answer": "8"},
    {"question": "Как зовут луну в мире Minecraft?", "answer": "Луна"}
]

# Глобальные переменные для текущего вопроса и ответа
current_question = None
current_answer = None


# Команда для начала викторины
@bot.command(name='startquiz', help='Начать викторину')
async def start_quiz(ctx):
    global current_question
    global current_answer

    # Выбираем случайный вопрос
    current_question = random.choice(questions_and_answers)
    current_answer = current_question["answer"]

    # Отправляем вопрос в чат
    await ctx.send(f'{current_question["question"]}')


# Команда для ответа на вопрос
@bot.command(name='answer', help='Ответить на текущий вопрос')
async def answer_question(ctx, user_answer: str):
    global current_answer

    if user_answer.lower() == current_answer.lower():
        await ctx.send(f'Правильно! {ctx.author.mention} получает 1 очко.')
        await start_quiz(ctx)
    else:
        await ctx.send(f'Неправильно. Попробуйте еще раз!')


bot.run(TOKEN)
