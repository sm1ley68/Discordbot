import disnake
from pip._internal import commands

from Discordbot import bot


@bot.command(name='кик', help='Выгнать пользователя(Только администрация)')
@commands.has_permissions(kick_members=True, administrator=True)
async def kick(ctx, member: disnake.Member, *, reason='Нарушение правил.'):
    await ctx.send(
        f'Администратор {ctx.author.mention} исключил пользователя {member.mention} "Нарушение правил сервера"')
    await member.kick(reason=reason)
    await ctx.message.delete()


@bot.command(name='мут', help='Замьютит участника(Только администрация)')
@commands.has_permissions(administrator=True)
async def mute(ctx, member: disnake.Member, *, reason=None):
    mute_role = disnake.utils.get(ctx.message.guild.roles, name='петушок молчит')

    await member.add_roles(mute_role)
    await ctx.send(f'{ctx.author.mention} замутил {member.mention} по причине {reason}.')


@bot.command(name='анмут', help='Размьютить участника(Только администрация)')
@commands.has_permissions(administrator=True)
async def unmute(ctx, member: disnake.Member):
    mute_role = disnake.utils.get(ctx.guild.roles, name='петушок молчит')

    await member.remove_roles(mute_role)
    await ctx.send(f'{ctx.author.mention} размутил {member.mention}.')


@bot.command(name='бан', help='Забанить пользователя(Только администрация)')
@commands.has_permissions(ban_members=True, administrator=True)
async def ban(ctx, member: disnake.Member, *, reason='Нарушение правил.'):
    await ctx.send(
        f'Администратор {ctx.author.mention} забанил пользователя {member.mention} "Нарушение правил сервера"')
    await member.ban(reason=reason)
    await ctx.message.delete()
