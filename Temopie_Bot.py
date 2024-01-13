import discord
import random
from discord.ext import commands
client = discord.Client()

bot = commands.Bot(command_prefix = "!", description = "Bot en developpement")
bot.remove_command('help')

@bot.event
async def on_ready():
	await bot.change_presence(activity=discord.Game(name=f"sur {len(bot.guilds)} serveurs • !help"))
	print("Ready ! ^^")

	bot.reaction_roles = []

#@bot.event
#async def on_command_error(ctx,error):
#	print(f"Error in {ctx.channel} : {error}")
#	if isinstance(error,commands.MissingPermissions):
#		await ctx.send("Vous ne disposez pas des permissions requises !")

#@bot.event
#async def on_raw_reaction_add(playload):
#	for role, msg, emoji in bot.reaction_roles:
#		if msg.id == playload.message_id and emoji == playload.emoji.name:
#			await playload.member.add_roles(role)

#@bot.event
#async def on_raw_reaction_remove(playload):
#	for role, msg, emoji in bot.reaction_roles:
#		if msg.id == playload.message_id and emoji == playload.emoji.name:
#			await bot.get_guild(playload.guild_id).get_member(playload.member_id).remove_roles(role)

#@bot.command(aliases=['sr'])
#async def set_reaction(ctx, role:discord.Role=None, msg: discord.Message=None, emoji=None):
#	if role != None and msg != None and emoji != None:
#		await msg.add_reaction("<:yes:757652907486347405>")
#		bot.reaction_roles.append((role, msg, emoji))
#	
#	else:
#		await ctx.send("Arguments invalides !")
#msg.add_reaction("<:nom:id émoji>") pour add réaction

@bot.event
async def on_member_join(member):
	guild = member.guild
	await member.send(f"hey ! bienvenue dans le serveur {guild.name}")


@bot.command(aliases=['h'])
async def help(ctx):
	embed = discord.Embed(
		title = "**❔ • Voici la liste de mes commandes • ❔**" ,
		description = "> Pour utiliser mes commandes : ` ! `" ,
		color = discord.Colour.dark_grey()
	)
	embed.add_field(name = "🔨 **• Commandes de modérations**", value = "`ban [@mention]` → **bannis du serveur** l'utilisateur mentionné.\n`unban [nom avec le #]` → **retire de la liste des ban** l'utilisateur.\n`kick [@mention]` → **expulse du serveur** l'utilisateur mentonné.\n`clear [nombre]` → **supprime les dernier messages** suivant le nombre indiqué. (si vous n'**indiquez rien** alors **100 messages seront supprimés**" , inline = False )
	embed.add_field(name = "🌀 **• Commandes informatives**" , value = "`serveurinfo` → **affiche les information du serveur** où la commande est effectuée.\n`getinfo [membre/channel/nom/description]` → **affiche l'information** de ce que vous avez demandé.\n`userinfo [@mention]` → **affiche les information** de l'utilisateur mentionné." , inline = False )
	embed.add_field(name = "🔌 **• Commandes autres**" , value = "`invite` → **affiche le **lien et les information** afin de **m'inviter sur vos serveurs**.")
	await ctx.send(embed=embed)

@bot.command(aliases=['si'])
async def serveurinfo(ctx):
	server = ctx.guild
	numberOfTextChannels = len(server.text_channels)
	numberOfVoiceChannels = len(server.voice_channels)
	numberOfPerson = server.member_count
	serverName = server.name
	embed = discord.Embed(title = f"🗒️**• Informations du serveur `{serverName}` •🗒️**" , description = f"__**Membres :**__ `{numberOfPerson}` **membres** \n__**Salons :**__ `{numberOfTextChannels}` **salons textuels** et `{numberOfVoiceChannels}` **salons vocaux**" , color = discord.Colour.blue())
	await ctx.send(embed=embed)

@bot.command()
async def getinfo(ctx, info):
	server = ctx.guild
	if info == "membre":
		messagemembre = f"Il y a exactement **{server.member_count}** membres sur le serveur ! "
		await ctx.send(messagemembre)
	elif info == "channel":
		nombredechannel = f"Le nombre de channels du serveur est de **{len(server.voice_channels) + len(server.text_channels)}**"
		await ctx.send(nombredechannel)
	elif info == "nom":
		messagenom = f"Le nom du serveur est **{server.name}**"
		await ctx.send(messagenom)
	elif info == "description":
		messagedescription = f"La description du serveur est : **{server.description}**"
		await ctx.send(messagedescription)
	else:
		await ctx.send("Veuilez inclure ce sur quoi vous souhaitez être informé...")

@bot.command(aliases=['b'])
@commands.has_permissions(ban_members = True)
async def ban(ctx, member : discord.User,*,reason = "pas de raison donnée"):
	try:
		await member.send(f"Vous avez été **bannis** du serveur `{ctx.guild}` par {ctx.author.name} : **{reason}**")
	except:
		await ctx.send("L'utilisateur à ses messages privé fermé.")
	embed = discord.Embed(
		title="**BAN**",
		description=f"**{member}** à été ban du serveur !",
		color = discord.Colour.dark_red()
	)
	embed.add_field(name="**RAISON**" , value=f"{reason}")
	await ctx.guild.ban(member, reason = reason)
	await ctx.send(embed=embed)

@bot.command(aliases=['ub'])
@commands.has_permissions(ban_members = True)
async def unban(ctx,*,member):
	banned_users = await ctx.guild.bans()
	member_name, member_disc = member.split('#')

	for banned_entry in banned_users:
		user = banned_entry.user

		if(user.name, user.discriminator)==(member_name,member_disc):

			await ctx.guild.unban(user)
			embed = discord.Embed(
				title="**UNBAN**",
				description=f"{member} à été débanni du serveur",
				color = discord.Colour.purple()
			)
			await ctx.send(embed=embed)
			return
		
	await ctx.send(member+" n'est pas dans la liste des bans !")

@bot.command(aliases=['k'])
@commands.has_permissions(kick_members = True)
async def kick(ctx, member : discord.Member,*,reason = "pas de raison donnée"):
	try:
		await member.send(f"Vous avez été **kick** du serveur `{ctx.guild}` : **{reason}**")
	except:
		await ctx.send("L'utilisateur à ses messages privé fermé.")
	await member.kick(reason=reason)
	embed = discord.Embed(
		title="**KICK**",
		description=f"**{member}** à été kick du serveur !",
		color=discord.Colour.red()
	)
	embed.add_field(name="**RAISON**" , value= f"{reason}")
	await ctx.send(embed=embed)

@bot.command(aliases=['c'])
@commands.has_permissions(manage_messages = True)
async def clear(ctx, amount=100):
	embed = discord.Embed(
		title="🌪️ **CLEAR** 🌪️",
		description=f"Je viens de **supprimer** `{amount}` **messages !**",
		color = discord.Colour.orange()
	)
	embed.set_footer(icon_url = ctx.author.avatar_url, text = f"{ctx.author.name}")
	await ctx.channel.purge(limit=amount+1)
	await ctx.send(embed=embed)

@bot.command(aliases=['ui'])
async def userinfo(ctx, member : discord.Member):
	embed = discord.Embed(title = member.name , description = member.mention , color = discord.Colour.magenta())
	embed.add_field(name = "ID", value = member.id , inline = True )
	embed.set_thumbnail(url = member.avatar_url)
	embed.set_footer(icon_url = ctx.author.avatar_url, text = "auteur de la commande")
	await ctx.send(embed=embed)

@bot.command()
async def invite(ctx):
	embed = discord.Embed(title = "🔗**○ Invitez moi ○**🔗" , description = "https://discord.com/oauth2/authorize?client_id=754309354458710047&permissions=8&scope=bot \n**• Pour m'inviter sur votre serveur il vous suffit :** \n> 1• **cliquer** sur le lien au dessus \n> 2• **selectionner** le serveur où vous souhaitez m'ajouter \n> 3• **autoriser** mes permissions \n> 4• **accepter** et c'est bon ^^" , color = discord.Colour.blue())
	await ctx.send(embed=embed)

@bot.command()
async def regletemopie(ctx):
	server = ctx.guild
	serverName = server.name
	embed = discord.Embed(
		title=f"<a:blob_angel:757295987399196693> __**Règlement • `{serverName}`**__ <a:blob_angel:757295987399196693>",
		description=f"**Tout __non respect de ces règles__ entrainera des __sanctions__ au niveau du serveur voir plus si besoin !**",
	)
	embed.set_thumbnail(url="https://www.ellipseformation.com/images/pictos/ellipse-formation-reglement-interieur.png")
	embed.set_image(url="https://media.discordapp.net/attachments/754314139727298673/757225325036961792/rainbowgif-2.gif")
	embed.set_footer(icon_url="https://digital.ricoh.es/wp-content/uploads/2020/04/c6842479-e0ee-49a2-9053-d00639074f7a_tick.gif",text="validez le règlement afin d'avoir accès à l'entièreté du serveur !")
	embed.add_field(name="<a:alert:757299771244412949> • **Règles générales**",value="<:fleche:757653073534386236> Le **`spam` et les `mentions inutiles` sont interdites.**\n<:fleche:757653073534386236> Si vous avez un **`pseudo non mentionnable ou insultant`, il sera changé.**\n<:fleche:757653073534386236> La **`publicité` en message privés` est interdite.** Si vous en êtes victime merci de **contacter un Staff** .\n<:fleche:757653073534386236> Tout contenu **`NSFW` est interdit**,  ainsi que le `contenu violent`.\n<:fleche:757653073534386236> Le **`respect` est `obligatoire` envers tout le monde** notamment envers le staff.\n<:fleche:757653073534386236> Ne **pas tenir des `propos sexistes, homophobes`, ou même `racistes`** sur ce serveur.",inline=False)
	embed.add_field(name="<a:newsletter:757659210447323226> • **Règles publicités**",value="<:fleche:757653073534386236> Vos **publicités ne doivent `pas enfreindre le règlement`** du serveur.\n<:fleche:757653073534386236> Nous n'**acceptons pas les publicités** de serveurs `reward` ni `NSFW`\n<:fleche:757653073534386236> Veuillez **mettres vos publicitées dans les `salon correspondants`** __(<#756933356771606602> pour plus d'infos)__.\n<:fleche:757653073534386236> Vos publicités doivent **contenir une `description`**.\n<:fleche:757653073534386236> Il est **interdit de `mentionner une personne` ou un `rôle`** dans vos publicités.",inline=False)
	await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(manage_roles=True)
async def addrole(ctx, role: discord.Role, user: discord.Member):
	await user.add_roles(role)
	await ctx.send(f"J'ai ajouté avec succès le rôle {role.mention} à {user.mention}.")

@bot.command()
@commands.has_permissions(manage_roles=True)
async def removerole(ctx, role: discord.Role, user: discord.Member):
	await user.remove_roles(role)
	await ctx.send(f"J'ai retiré avec succès le rôle {role.mention} à {user.mention}.")

bot.run("NzU0MzA5MzU0NDU4NzEwMDQ3.X1y3VA.3rtVWhy0x17rEGzQkzNNs6Fu7r8")