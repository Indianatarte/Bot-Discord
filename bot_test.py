import discord
from discord.ext import commands 

bot = commands.Bot(command_prefix = "!", description = "Bot en developpement")

@bot.event
async def on_ready():
	print("Ready !")


@bot.command()
async def getget(ctx):
	await ctx.send("moi aussi!")

@bot.command()
async def serverinfo(ctx):
	server = ctx.guild
	numberOfTextChannels = len(server.text_channels)
	numberOfVoiceChannels = len(server.voice_channels)
	numberOfPerson = server.member_count
	serverName = server.name
	message = f"Le serveur **{serverName}** contient *{numberOfPerson}* personnes dont moi :) ! \n Ce serveur possède *{numberOfTextChannels}* salons écrit et *{numberOfVoiceChannels}* salon vocaux."
	await ctx.send(message)

@bot.command()
async def ping(ctx):
	await ctx.send("pong!")


@bot.command()
async def getinfo(ctx, info):
	server = ctx.guild
	if info == "membre":
		messagemembre = f"Il y a exactement {server.member_count} membres sur le serveur! "
		await ctx.send(messagemembre)
	elif info == "channel":
		nombredechannel = f"Le nombre de channels du serveur est de {len(server.voice_channels) + len(server.text_channels)}"
		await ctx.send(nombredechannel)
	elif info == "nom":
		messagenom = f"Le nom du serveur est {server.name}"
		await ctx.send(messagenom)
	elif info == "description":
		messagedescription = f"La description du serveur est : {server.description}"
		await ctx.send(messagedescription)
	else:
		await ctx.send("Heu... quoi?")

@bot.command()
async def h(ctx):
	await ctx.send("Voici la liste des commandes : \n-getinfo (membre/channel/nom/description) : c'est pour obtenir une information presice sur le serveur ;) \n-h : pour la lise des commandes, pratique non? \n-getget : getgetget \n-serverinfo : pour avoir toute les information du serveur d'un seul coup! \n-ping : heu... pong? \n-clear {nombre}: supprime un nombre donné de message \n-ban {@utilisateur} {raison} : pour ban des gents (des fois ca fait du bien...) \n-unban {utilisateur#0000} {raison} : on a peut etre fait une erreur... \n-kick {@utilisateur} {raison} : va-t-il revenir ? ")

@bot.command()
async def ban(ctx, user : discord.User, *reason):
	reason = " ".join(reason)
	await ctx.guild.ban(user, reason = reason)
	await ctx.send(f"{user} à été ban pour la raison suivante : {reason}.")

@bot.command()
async def unban(ctx, user, *reason):
	reason = " ".join(reason)
	userName, userId = user.split("#")
	bannedUsers = await ctx.guild.bans()
	for i in bannedUsers:
		if i.user.name == userName and i.user.discriminator == userId:
			await ctx.guild.unban(i.user, reason = reason)
			await ctx.send(f"{user} à été unban.")
			return
	await ctx.send(f"L'utilisateur {user} n'est pas dans la liste des bans")

@bot.command()
async def kick(ctx, user : discord.User, *reason):
	reason = " ".join(reason)
	await ctx.guild.kick(user, reason = reason)
	await ctx.send(f"{user} à été kick.")

@bot.command()
async def clear(ctx, nombre : int):
	messages = await ctx.channel.history(limit = nombre + 1).flatten()
	for message in messages:
		await message.delete()

@bot.command()
async def create_embed(ctx, title, description, color):
		embed = discord.Embed()
		embed.title = title
		embed.description = description
		embed.colour = color
		return embed

bot.run("NzU0MzA5MzU0NDU4NzEwMDQ3.X1y3VA.3rtVWhy0x17rEGzQkzNNs6Fu7r8")