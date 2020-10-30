import discord
from discord.ext import commands
import random
from random import choice
import os
import time

TOKEN = "NzYwODcwNTIyODQxMDcxNjQ4.X3SV5A.Mot9n0Z52wZY43rePpN2CSIeEXs"

client = commands.Bot(command_prefix = 'h!')

@client.event
async def on_ready(): #when the bots ready and on
    await client.change_presence(status=discord.Status.online, activity=discord.Game('Type h!help')) #the status for the bot
    print('Bot is ready and online.')
        
@client.event
async def on_member_join(member):
    print(f'{member} has joined {member.guild.name}.') #When someone joins

@client.event
async def on_member_remove(member):
    print(f'{member} has left {member.guild.name}.') #when someone leaves
    
@client.command(aliases=['ping', 'PING'])
async def Ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms') #a ping command

@client.command(pass_context=True)
async def help_2(ctx):
    author = ctx.message.author
    embed=discord.Embed(title="Loki Bot Commnads Help", description="", color=0xfd0000)#COLOR
    embed.add_field(name="8ball", value="Ask A Question The Bot Responds With An Random Answer", inline=True)
    embed.add_field(name="Ping", value="A Ping Command", inline=True)
    embed.add_field(name="Purge", value="Delete The Messages", inline=True)
    embed.add_field(name="Say|Echo", value="Say Something With The Bot", inline=True)
    embed.add_field(name="Avatar|Av", value="See The Avatar Of An User", inline=True)
    await ctx.send(embed=embed)

@client.command()
async def whois(ctx, member : discord.Member):
    embed = discord.Embed(title = member.name , description = member.mention , color = discord.Color.red())
    embed.add_field(name = "ID", value = member.id , inline = True )
    embed.set_thumbnail(url = member.avatar_url)
    embed.set_footer(icon_url = ctx.author.avatar_url, text = f"Requested by {ctx.author.name}")
    await ctx.send(embed=embed)

@client.command(aliases=['avatar', 'Avatar', 'Av', 'icon', 'Icon'])
async def av(ctx, member: discord.Member):
    embed = discord.Embed(title = member.name , color = discord.Color.red())
    embed.set_image(url = member.avatar_url)
    await ctx.send(embed=embed)

@client.command(aliases=['8ball']) #aliases for the bot. any will respond.
async def _8ball(ctx, *, question):
    responses = ['It is certain.',
                 'It is decidedly so.',
                 'Without a doubt.',
                 'Yes - definitely.',
                 'You may rely on it.',
                 'As I see it, yes.',
                 'Most likely.',
                 'Outlook good.',
                 'Yes.',
                 'Signs point to yes.',
                 'Reply hazy, try again.',
                 'Ask again later.',
                 'Better not tell you now.',
                 'Cannot predict now.',
                 'Concentrate and ask again.',
                 'Don\'t count on it.',
                 'My reply is no.',
                 'My sources say no.',
                 'Outlook not so good.',
                 'Very doubtful.']
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}') #sends the message
    
@client.command(aliases=['pu', 'clear', 'purge'])
@commands.has_any_role("Trail Mod", "Mod", "Admin", "Co-Owner", "Owner", "STAFF") #They need to have one of these roles in order for them to use this command
async def Purge(ctx, amount=0):
    await ctx.channel.purge(limit=amount + 1)

@client.command(aliases=['say', 'echo', 'Echo'])# a say command. the bot basically copies your message.
@commands.has_any_role("Giveaway Manager", "Admin", "Mod", "Co-Owner", "Owner") #They need to have one of these roles in order for them to use this command
async def Say(ctx, *, message):
    await ctx.channel.purge(limit=1)
    await ctx.send(message)

@client.command(aliases=['k'])
@commands.has_permissions(kick_members = True)
async def kick(ctx,member : discord.Member, *, reason= "No Reason Provided"):
        await member.kick(reason=reason)
        await ctx.send(f'Kicked {member.mention}')
        return await ctx.send("I dont have the permissions to kick people")
    
@client.command()
@commands.has_any_role("Moderator", "Admin", "Co-Owner") #must have one of those roles. (remember, the name must be exact)
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'Banned {member.mention}')

@client.command()
@commands.has_any_role("Moderator", "Admin", "Co-Owner") #must have one of those roles
async def unban(ctx, *, member):
    banned_users = await ctx.guid.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users: #checks if they are banned
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return


client.run(TOKEN)
