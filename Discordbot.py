# from typing import Optional
import os
import datetime
import disnake
from disnake.ext import commands
import random
import os

bot = commands.Bot(command_prefix="$", help_command=None, intents=disnake.Intents.all(),
                   test_guilds=[793728158150557707])

CENSORED_WORDS = []


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
@bot.command(name='кик', help='Выгнать пользователя(Только администрация)')
@commands.has_permissions(kick_members=True, administrator=True)
async def kick(ctx, member: disnake.Member, *, reason='Нарушение правил.'):
    await ctx.send(
        f'Администратор {ctx.author.mention} исключил пользователя {member.mention} "Нарушение правил сервера"')
    await member.kick(reason=reason)
    await ctx.message.delete()


# мут пользователя
@bot.command(name='мут', help='Замьютит участника(Только администрация)')
@commands.has_permissions(administrator=True)
async def mute(ctx, member: disnake.Member, *, reason=None):
    mute_role = disnake.utils.get(ctx.message.guild.roles, name='петушок молчит')

    await member.add_roles(mute_role)
    await ctx.send(f'{ctx.author.mention} замутил {member.mention} по причине {reason}.')


# анмут пользователя
@bot.command(name='анмут', help='Размьютить участника(Только администрация)')
@commands.has_permissions(administrator=True)
async def unmute(ctx, member: disnake.Member):
    mute_role = disnake.utils.get(ctx.guild.roles, name='петушок молчит')

    await member.remove_roles(mute_role)
    await ctx.send(f'{ctx.author.mention} размутил {member.mention}.')


# бан пользователя
@bot.command(name='бан', help='Забанить пользователя(Только администрация)')
@commands.has_permissions(ban_members=True, administrator=True)
async def ban(ctx, member: disnake.Member, *, reason='Нарушение правил.'):
    await ctx.send(
        f'Администратор {ctx.author.mention} забанил пользователя {member.mention} "Нарушение правил сервера"')
    await member.ban(reason=reason)
    await ctx.message.delete()


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


@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def clear(ctx, amount=30):
    await ctx.channel.purge(limit=amount)


bot.run("token")
