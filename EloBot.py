import discord
from discord.ext import commands,tasks
from itertools import cycle
from discord.utils import get
from discord import FFmpegPCMAudio
from riotwatcher import LolWatcher, ApiError
import time
import asyncio
import requests
import json
from time import strftime
from time import gmtime
import datetime




lol_watcher = LolWatcher('RGAPI-de495ce7-8036-4f76-b3e3-399cc5d04a02')



TOKEN = 'ODAyOTY2MzgxNjc5MjE0NjAy.YA26tw.Tu2_Z805AEqKfFKiCwUl4Olh4P0'
OWNERID = 432163622878183424

client = discord.Client()

channel = client.get_channel(802967377159389317)

client = commands.Bot(command_prefix =['!e ','!E ','!elo ','!Elo ','!ELO ','!e','!E','!elo','!Elo','!ELO'])



ROLE = "Member"

status = cycle(['League of Legends', '!e commands', '!e elo'])

#@client.command()
#async def setPrefix(ctx, arg):
    #command_prefix = arg
    


@client.event
async def on_ready():
    change_status.start()
    print('Bot is ready')

@tasks.loop(seconds=6)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))

@client.command()
async def servers(ctx):
  servers = list(client.guilds)
  await ctx.send(f"Connected on {str(len(servers))} servers:")
  await ctx.send('\n'.join(guild.name for guild in servers))
        
    

#Autorole join
@client.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name=ROLE)
    await member.add_roles(role)
    print(f"{member} was given {role}")
##################################################################################################
##################################################################################################
@client.command(pass_context = True)
async def playlist(ctx):
    if(ctx.author.voice):
        channel = ctx.message.author.voice.channel
        voice = await channel.connect()
        source = FFmpegPCMAudio('playlist.mp3')
        player = voice.play(source)
        embed=discord.Embed(title = "Playlist songs",description='All songs from !e playlist command',color=discord.Color.purple())
        embed.add_field(name = "Songs with timestamps", value = f"00:00 - 03:30 Adam Jensen - The Hunter \n 03:30 - 06:51 Sinner's Heist - Streetlight People \n 06:51 - 09:27 apze - Darkness \n 09:27 - 12:12 Julius Dreisig - In My Head \n 12:12 - 15:33 Coopex - Draw Youur Life \n 15:33 - 19:00 Clarx - Zig Zag \n 19:00 - 22:49 Adam Vitali - Relapse \n 22:49 - 26:41 Rvmor - Sorry \n  29:31 - 32:33 Zeus X Crona - Colours \n 32:33 - 35:46 Rivan x Cadmium - Seasons \n 35:46 - 38:24 Le Winter x Jack Daniel - Play With Me \n 38:24 - 41:22 Mario Ayuda - Don't Feel Right \n 41:22 - 44:19 Mike Wit - I Feel That \n 44:19 - 47:09 Shipe Wrek &  The Highrollers - Waiting \n 47:09 - 50:26 Kozah - Haha \n 50:26 - 54:35 Sad Puppy - Doing It \n 54:35 - 57:15 NEFFEX - With You \n 57:15 - 1:00:33 Ben Woodward - TRY")
        embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/802967377159389317/823146868410155038/elomusicicon.png")
        await ctx.send(embed=embed)
    else:
        await ctx.send("You are not in voice channel, you must be in a voice channel to run this command!")
@client.command(pass_context = True)
async def leave(ctx):
    if (ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.send("I left the voice channel!")
    else:
        await ctx.send("I am not in a voice channel!")

##################################################################################################
##################################################################################################


#commands list
@client.command()
async def commands(ctx):
    embed=discord.Embed(title="Bot Commands", description='',name=ctx.author.display_name, color=discord.Color.purple())
    embed.add_field(name = 'Basic Commands <:elocheck:820980129383055381>', value = f"**!e id [discord username]** \n __Find user identity__ \n **!e prefix** \n __Shows the available prefixes__ \n **!e ping** \n __Shows your ping__ \n **!e elo** \n __Shows bot info and more__",inline = False)
    embed.add_field(name = '\u200B',value = "\u200B",inline = False)
    embed.add_field(name = 'League of Legends Commands <:elocheck:820980129383055381>', value = f"**!e stats [region] [summoner name]** \n __Find summoner's stats__ \n **!e check [region] [summoner name]** \n __Find a summoner in OP.GG__ \n **!e build [champion]** \n __Find build for given champion__ \n **!e champ [champion]** \n __Everything you need to know about champion__ \n **!e counter [champion]** \n __Counters for champion__ \n **!e clash** \n __Shows Clash schedule__ \n **!e patch** \n __See patch notes__",inline = False)
    embed.add_field(name = '\u200B',value = "\u200B",inline = False)
    embed.add_field(name = 'Music Commands <:elocheck:820980129383055381>',value = '**!e playlist** \n __A playlist for playing League of Legends__ \n **!e leave** \n __The bot leaving the voice channel__',inline = False)
    embed.add_field(name = '\u200B',value = "\u200B",inline = False)
    embed.add_field(name = 'VIP Commands <:elocheck:820980129383055381>',value = '__Coming soon!__',inline = False)
    embed.set_thumbnail(url='https://cdn.discordapp.com/icons/802967377159389315/a339f7b9081a63c073651eafd0175d56.webp?size=1024')
    embed.set_footer(text='Elo.GG The new way to play')
    
    await ctx.send(embed=embed)

#############################################################
ddragonVersion = 'https://ddragon.leagueoflegends.com/api/versions.json'
response = requests.get(ddragonVersion)
json_object = response.json()
latestVersion = json_object[0]

def findChampionName(championID):
    url = 'http://ddragon.leagueoflegends.com/cdn/' + latestVersion + '/data/en_US/champion.json'
    r = requests.get(url)
    json_obj = r.json()
    data = json_obj['data']
    for name, attributes in data.items():
        if attributes['key'] == str(championID):
            return name
#############################################################
#Clash Schedule
@client.command()
async def clash(ctx):
    clashSchedule = lol_watcher.clash.tournaments('eun1')
    day1name = clashSchedule[0]['nameKey']
    day1day = clashSchedule[0]['nameKeySecondary']
    day1schedule = clashSchedule[0]['schedule']
    day1regist = day1schedule[0]['registrationTime']
    day1registTime = time.strftime("%d/%m/%Y %H:%M", gmtime(day1regist/1000))
    day1start = day1schedule[0]['startTime']
    day1startTime = time.strftime("%d/%m/%Y %H:%M", gmtime(day1start/1000))

    day2name = clashSchedule[1]['nameKey']
    day2day = clashSchedule[1]['nameKeySecondary']
    day2schedule = clashSchedule[1]['schedule']
    day2regist = day2schedule[0]['registrationTime']
    day2registTime = time.strftime("%d/%m/%Y %H:%M", gmtime(day2regist/1000))
    day2start = day2schedule[0]['startTime']
    day2startTime = time.strftime("%d/%m/%Y %H:%M", gmtime(day2start/1000))

    day3name = clashSchedule[2]['nameKey']
    day3day = clashSchedule[2]['nameKeySecondary']
    day3schedule = clashSchedule[2]['schedule']
    day3regist = day3schedule[0]['registrationTime']
    day3registTime = time.strftime("%d/%m/%Y %H:%M", gmtime(day3regist/1000))
    day3start = day3schedule[0]['startTime']
    day3startTime = time.strftime("%d/%m/%Y %H:%M", gmtime(day3start/1000))

    day4name = clashSchedule[3]['nameKey']
    day4day = clashSchedule[3]['nameKeySecondary']
    day4schedule = clashSchedule[3]['schedule']
    day4regist = day4schedule[0]['registrationTime']
    day4registTime = time.strftime("%d/%m/%Y %H:%M", gmtime(day4regist/1000))
    day4start = day4schedule[0]['startTime']
    day4startTime = time.strftime("%d/%m/%Y %H:%M", gmtime(day4start/1000))

    day1name = day1name.title()

    embed=discord.Embed(title=f"<:eloicon:820974785168801802> Clash Schedule - {day1name} Cup", description=' ',color=discord.Color.purple())
    embed.add_field(name = f"Day 1 <:elocheck:820980129383055381>", value = f"**Registration Time:** {day1registTime} \n **Start Time:** {day1startTime}", inline = False)
    embed.add_field(name = f"Day 2 <:elocheck:820980129383055381>", value = f"**Registration Time:** {day2registTime} \n **Start Time:** {day2startTime}", inline = False)
    embed.add_field(name = f"Day 3 <:elocheck:820980129383055381>", value = f"**Registration Time:** {day3registTime} \n **Start Time:** {day3startTime}", inline = False)
    embed.add_field(name = f"Day 4 <:elocheck:820980129383055381>", value = f"**Registration Time:** {day4registTime} \n **Start Time:** {day4startTime}", inline = False)
    embed.set_footer(text = "The time maybe is not in your time zone.")
    embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/802967377159389317/822458948992368640/clash.png")
    await ctx.send(embed=embed)
################################################################    

#League of Legends Stats
@client.command()
async def stats(ctx, region, *, arg):    
    region1 = 'eun1'

    waitstatsmessage = await ctx.send(":red_circle: Please wait while we are fetching data for summoner's stats...")
    
    if region == 'eune':
        ign = lol_watcher.summoner.by_name('eun1', arg)
        ranked = lol_watcher.league.by_summoner('eun1', ign['id'])
        championmastery = lol_watcher.champion_mastery.by_summoner('eun1', ign['id'])
    elif region == 'EUNE':
        ign = lol_watcher.summoner.by_name('eun1', arg)
        ranked = lol_watcher.league.by_summoner('eun1', ign['id'])
        championmastery = lol_watcher.champion_mastery.by_summoner('eun1', ign['id'])
    elif region == 'euw':
        ign = lol_watcher.summoner.by_name('euw1', arg)
        ranked = lol_watcher.league.by_summoner('euw1', ign['id'])
        championmastery = lol_watcher.champion_mastery.by_summoner('euw1', ign['id'])
    elif region == 'EUW':
        ign = lol_watcher.summoner.by_name('euw1', arg)
        ranked = lol_watcher.league.by_summoner('euw1', ign['id'])
        championmastery = lol_watcher.champion_mastery.by_summoner('euw1', ign['id'])
    elif region == 'na':
        ign = lol_watcher.summoner.by_name('na1', arg)
        ranked = lol_watcher.league.by_summoner('na1', ign['id'])
        championmastery = lol_watcher.champion_mastery.by_summoner('na1', ign['id'])
    elif region == 'NA':
        ign = lol_watcher.summoner.by_name('na1', arg)
        ranked = lol_watcher.league.by_summoner('na1', ign['id'])
        championmastery = lol_watcher.champion_mastery.by_summoner('na1', ign['id'])
    elif region == 'kr':
        ign = lol_watcher.summoner.by_name('kr', arg)
        ranked = lol_watcher.league.by_summoner('kr', ign['id'])
        championmastery = lol_watcher.champion_mastery.by_summoner('kr', ign['id'])
    elif region == 'KR':
        ign = lol_watcher.summoner.by_name('kr', arg)
        ranked = lol_watcher.league.by_summoner('kr', ign['id'])
        championmastery = lol_watcher.champion_mastery.by_summoner('kr', ign['id'])
    elif region == 'br':
        ign = lol_watcher.summoner.by_name('br1', arg)
        ranked = lol_watcher.league.by_summoner('br1', ign['id'])
        championmastery = lol_watcher.champion_mastery.by_summoner('br1', ign['id'])
    elif region == 'BR':
        ign = lol_watcher.summoner.by_name('br1', arg)
        ranked = lol_watcher.league.by_summoner('br1', ign['id'])
        championmastery = lol_watcher.champion_mastery.by_summoner('br1', ign['id'])
    elif region == 'lan':
        ign = lol_watcher.summoner.by_name('la1', arg)
        ranked = lol_watcher.league.by_summoner('la1', ign['id'])
        championmastery = lol_watcher.champion_mastery.by_summoner('la1', ign['id'])
    elif region == 'LAN':
        ign = lol_watcher.summoner.by_name('la1', arg)
        ranked = lol_watcher.league.by_summoner('la1', ign['id'])
        championmastery = lol_watcher.champion_mastery.by_summoner('la1', ign['id'])
    elif region == 'las':
        ign = lol_watcher.summoner.by_name('la2', arg)
        ranked = lol_watcher.league.by_summoner('la2', ign['id'])
        championmastery = lol_watcher.champion_mastery.by_summoner('la2', ign['id'])
    elif region == 'LAS':
        ign = lol_watcher.summoner.by_name('la2', arg)
        ranked = lol_watcher.league.by_summoner('la2', ign['id'])
        championmastery = lol_watcher.champion_mastery.by_summoner('la2', ign['id'])
    elif region == 'jp':
        ign = lol_watcher.summoner.by_name('jp1', arg)
        ranked = lol_watcher.league.by_summoner('jp1', ign['id'])
        championmastery = lol_watcher.champion_mastery.by_summoner('jp1', ign['id'])
    elif region == 'JP':
        ign = lol_watcher.summoner.by_name('jp1', arg)
        ranked = lol_watcher.league.by_summoner('jp1', ign['id'])
        championmastery = lol_watcher.champion_mastery.by_summoner('jp1', ign['id'])
    elif region == 'ru':
        ign = lol_watcher.summoner.by_name('ru', arg)
        ranked = lol_watcher.league.by_summoner('ru', ign['id'])
        championmastery = lol_watcher.champion_mastery.by_summoner('ru', ign['id'])
    elif region == 'RU':
        ign = lol_watcher.summoner.by_name('ru', arg)
        ranked = lol_watcher.league.by_summoner('ru', ign['id'])
        championmastery = lol_watcher.champion_mastery.by_summoner('ru', ign['id'])
        
    for i in range(len(ranked)):
        if ranked[i]['queueType'] == 'RANKED_FLEX_SR':
            del ranked[i]
            break

    icon = str(ign['profileIconId'])

    firstchampion = championmastery[0]['championId']
    firstchampionlevel = championmastery[0]['championLevel']
    firstchampionpoints = championmastery[0]['championPoints']

    secondchampion = championmastery[1]['championId']
    secondchampionlevel = championmastery[1]['championLevel']
    secondchampionpoints = championmastery[1]['championPoints']

    thirdchampion = championmastery[2]['championId']
    thirdchampionlevel = championmastery[2]['championLevel']
    thirdchampionpoints = championmastery[2]['championPoints']

    if firstchampionlevel == 7:
        firstchampionlevel = '<:mastery7:819475734589472779>'
    elif firstchampionlevel == 6:
        firstchampionlevel = '<:mastery6:819476263072432128>'
    elif firstchampionlevel == 5:
        firstchampionlevel = '<:mastery5:819476251386576909>'
    elif firstchampionlevel == 4:
        firstchampionlevel = '<:mastery4:819476240494362634>'
    elif firstchampionlevel == 3:
        firstchampionlevel = '<:mastery3:819476222886805504>'
    elif firstchampionlevel == 2:
        firstchampionlevel = '<:mastery2:819476206092550155>'
    elif firstchampionlevel == 1:
        firstchampionlevel = '<:mastery1:819476168323366932>'

    if secondchampionlevel == 7:
        secondchampionlevel = '<:mastery7:819475734589472779>'
    elif secondchampionlevel == 6:
        secondchampionlevel = '<:mastery6:819476263072432128>'
    elif secondchampionlevel == 5:
        secondchampionlevel = '<:mastery5:819476251386576909>'
    elif secondchampionlevel == 4:
        secondchampionlevel = '<:mastery4:819476240494362634>'
    elif secondchampionlevel == 3:
        secondchampionlevel = '<:mastery3:819476222886805504>'
    elif secondchampionlevel == 2:
        secondchampionlevel = '<:mastery2:819476206092550155>'
    elif secondchampionlevel == 1:
        secondchampionlevel = '<:mastery1:819476168323366932>'

    if thirdchampionlevel == 7:
        thirdchampionlevel = '<:mastery7:819475734589472779>'
    elif thirdchampionlevel == 6:
        thirdchampionlevel = '<:mastery6:819476263072432128>'
    elif thirdchampionlevel == 5:
        thirdchampionlevel = '<:mastery5:819476251386576909>'
    elif thirdchampionlevel == 4:
        thirdchampionlevel = '<:mastery4:819476240494362634>'
    elif thirdchampionlevel == 3:
        thirdchampionlevel = '<:mastery3:819476222886805504>'
    elif thirdchampionlevel == 2:
        thirdchampionlevel = '<:mastery2:819476206092550155>'
    elif thirdchampionlevel == 1:
        thirdchampionlevel = '<:mastery1:819476168323366932>'
    
    if ranked == []:
        embed=discord.Embed(title="<:eloicon:820974785168801802> League of Legends Stats", description='',color=discord.Color.purple())
        embed.add_field(name = "Summoner Name", value = ign['name'], inline = True)
        embed.add_field(name = "Summoner Level", value = ign['summonerLevel'], inline = True)
        embed.add_field(name = "\u200B", value = "\u200b", inline = True)
        embed.add_field(name = "Most Played Champions", value =f'{firstchampionlevel} **{findChampionName(firstchampion)} {firstchampionpoints:,d}**  Points \n {secondchampionlevel} **{findChampionName(secondchampion)} {secondchampionpoints:,d}**  Points \n {thirdchampionlevel} **{findChampionName(thirdchampion)} {thirdchampionpoints:,d}**  Points', inline = True)
        embed.add_field(name = "Ranked Stats", value = 'Unranked', inline = True)
        embed.set_thumbnail(url = "http://opgg-static.akamaized.net/images/profile_icons/profileIcon" + icon + ".jpg")
        embed.set_image(url ="https://cdn.discordapp.com/attachments/802967377159389317/821679083444109323/unranked.png")
        await ctx.send(embed=embed)


    years = ranked[0]['veteran']
    tier = ranked[0]['tier']
    rank = ranked[0]['rank']
    wins = ranked[0]['wins']
    losses = ranked[0]['losses']
    lp = ranked[0]['leaguePoints']
    hotstreak = ranked[0]['hotStreak']
    wl = wins + losses
    towr = wins * 100
    wr = towr//wl
    symbol = '%'
    icon = str(ign['profileIconId'])
    
    


    if tier == 'IRON':
        tier = '<:iron:817360753173463060> Iron'
    elif tier == 'BRONZE':
        tier = '<:bronze:817361809295671326> Bronze'
    elif tier == 'SILVER':
        tier = '<:silver:817361823312773141> Silver'
    elif tier == 'GOLD':
        tier = '<:gold:817361901339148318> Gold'
    elif tier == 'PLATINUM':
        tier = '<:platinum:817361924857659444> Platinum'
    elif tier == 'DIAMOND':
        tier = '<:diamond:817361937913872404> Diamond'
    elif tier == 'MASTER':
        tier = '<:master:817361953269088276> Master'
    elif tier == 'GRANDMASTER':
        tier = '<:grandmaster:817361970243043341> GrandMaster'
    elif tier == 'CHALLENGER':
        tier = '<:challenger:817361981513400320> Challenger'

    if rank == 'IV':
        rank = '4'
    elif rank == 'III':
        rank = '3'
    elif rank == 'II':
        rank = '2'
    elif rank == 'I':
        rank = '1'

    await waitstatsmessage.delete()
    
    embed=discord.Embed(title="<:eloicon:820974785168801802> League of Legends Stats", description='',color=discord.Color.purple())
    #group1
    embed.add_field(name = "Summoner Name", value = ign['name'], inline = True)
    embed.add_field(name = "Summoner Level", value = ign['summonerLevel'], inline = True)
    embed.add_field(name = '\u200B', value ='\u200B', inline = True)

    #group2
    embed.add_field(name = "Solo/Duo Rank", value=f'{tier} {rank} ({lp} LP)', inline = True)
    embed.add_field (name = 'Winrate', value = f'{wr} {symbol}', inline = True)
    embed.add_field(name = '\u200B', value ='\u200B', inline = True)

    
    #group3
    embed.add_field(name = "Most Played Champions", value =f'{firstchampionlevel} **{findChampionName(firstchampion)} {firstchampionpoints:,d}**  Points \n {secondchampionlevel} **{findChampionName(secondchampion)} {secondchampionpoints:,d}**  Points \n {thirdchampionlevel} **{findChampionName(thirdchampion)} {thirdchampionpoints:,d}**  Points', inline = True)
    embed.add_field(name = 'Wins/Losses', value =f'{wins} / {losses}', inline = True)
    embed.add_field(name = '\u200B', value ='\u200B', inline = True)
    
    if hotstreak == False:
        embed.add_field(name = "Hot Streak", value = '<:elowrong:820980129605091338>', inline = True)
    elif hotstreak == True:
        embed.add_field(name = "Hot Streak", value = '<:elocheck:820980129383055381>', inline = True)

    if years == False:
        embed.add_field(name = "Hardstuck", value = '<:elowrong:820980129605091338>', inline = True)
    elif years == True:
        embed.add_field(name = "Hardstuck", value = '<:elocheck:820980129383055381>', inline = True)

    embed.add_field(name = '\u200B', value ='\u200B', inline = True)

    embed.set_thumbnail(url = "http://opgg-static.akamaized.net/images/profile_icons/profileIcon" + icon + ".jpg")



    #IRON IMAGE

    if tier == '<:iron:817360753173463060> Iron' and rank == '4':
        embed.set_image(url = "https://cdn.discordapp.com/attachments/811303510733226024/811303612998483969/Iron4.png")

        

    elif tier == '<:iron:817360753173463060> Iron' and rank == '3':
        embed.set_image(url = "https://cdn.discordapp.com/attachments/811303510733226024/811303608456708106/Iron3.png")

    elif tier == '<:iron:817360753173463060> Iron' and rank == '2':
        embed.set_image(url = "https://cdn.discordapp.com/attachments/811303510733226024/811303607051747345/Iron2.png")

    elif tier == '<:iron:817360753173463060> Iron' and rank == '1':
        embed.set_image(url = "https://cdn.discordapp.com/attachments/811303510733226024/811303606258630686/Iron1.png")

    #BRONZE IMAGE

    if tier == '<:bronze:817361809295671326> Bronze' and rank == '4':
        embed.set_image(url = "https://cdn.discordapp.com/attachments/811303510733226024/811304707573153822/Bronze4.png")

    elif tier == '<:bronze:817361809295671326> Bronze' and rank == '3':
        embed.set_image(url = "https://cdn.discordapp.com/attachments/811303510733226024/811304705895694391/Bronze3.png")

    elif tier == '<:bronze:817361809295671326> Bronze' and rank == '2':
        embed.set_image(url = "https://cdn.discordapp.com/attachments/811303510733226024/811304703148163072/Bronze2.png")

    elif tier == '<:bronze:817361809295671326> Bronze' and rank == '1':
        embed.set_image(url = "https://cdn.discordapp.com/attachments/811303510733226024/811304710266814534/Bronze1.png")

    #SILVER IMAGE

    if tier == '<:silver:817361823312773141> Silver' and rank == '4':
        embed.set_image(url = "https://cdn.discordapp.com/attachments/811303510733226024/811303542454747208/Silver4.png")

    elif tier == '<:silver:817361823312773141> Silver' and rank == '3':
        embed.set_image(url = "https://cdn.discordapp.com/attachments/811303510733226024/811303541045198848/Silver3.png")

    elif tier == '<:silver:817361823312773141> Silver' and rank == '2':
        embed.set_image(url = "https://cdn.discordapp.com/attachments/811303510733226024/811303539791233024/Silver2.png")

    elif tier == '<:silver:817361823312773141> Silver' and rank == '1':
        embed.set_image(url = "https://cdn.discordapp.com/attachments/811303510733226024/811303537463787542/Silver1.png")

    #GOLD IMAGE

    if tier == '<:gold:817361901339148318> Gold' and rank == '4':
        embed.set_image(url = "https://cdn.discordapp.com/attachments/811303510733226024/811306010111246366/Gold4.png")

    elif tier == '<:gold:817361901339148318> Gold' and rank == '3':
        embed.set_image(url = "https://cdn.discordapp.com/attachments/811303510733226024/811306008793055262/Gold3.png")

    elif tier == '<:gold:817361901339148318> Gold' and rank == '2':
        embed.set_image(url = "https://cdn.discordapp.com/attachments/811303510733226024/811306007338024980/Gold2.png")

    elif tier == '<:gold:817361901339148318> Gold' and rank == '1':
        embed.set_image(url = "https://cdn.discordapp.com/attachments/811303510733226024/811306012212330566/Gold1.png")

    #PLATINUM IMAGE

    if tier == '<:platinum:817361924857659444> Platinum' and rank == '4':
        embed.set_image(url = "https://cdn.discordapp.com/attachments/811303510733226024/811306595417718875/Plat4.png")

    elif tier == '<:platinum:817361924857659444> Platinum' and rank == '3':
        embed.set_image(url = "https://cdn.discordapp.com/attachments/811303510733226024/811306591621218374/Plat3.png")

    elif tier == '<:platinum:817361924857659444> Platinum' and rank == '2':
        embed.set_image(url = "https://cdn.discordapp.com/attachments/811303510733226024/811306590208262204/Plat2.png")

    elif tier == '<:platinum:817361924857659444> Platinum' and rank == '1':
        embed.set_image(url = "https://cdn.discordapp.com/attachments/811303510733226024/811306588970680330/Plat1.png")

    #DIAMOND IMAGE

    if tier == '<:diamond:817361937913872404> Diamond' and rank == '4':
        embed.set_image(url = "https://cdn.discordapp.com/attachments/811303510733226024/811307345962598400/d4.png")

    elif tier == '<:diamond:817361937913872404> Diamond' and rank == '3':
        embed.set_image(url = "https://cdn.discordapp.com/attachments/811303510733226024/811307346151604234/d3.png")

    elif tier == '<:diamond:817361937913872404> Diamond' and rank == '2':
        embed.set_image(url = "https://cdn.discordapp.com/attachments/811303510733226024/811307342540832768/d2.png")

    elif tier == '<:diamond:817361937913872404> Diamond' and rank == '1':
        embed.set_image(url = "https://cdn.discordapp.com/attachments/811303510733226024/811307348567785492/d1.png")

    #MASTER/GRANDMASTER/CHALLENGER IMAGE

    if tier == '<:master:817361953269088276> Master':
        embed.set_image(url = "https://cdn.discordapp.com/attachments/811303510733226024/811307791696265266/Master.png")

    elif tier == '<:grandmaster:817361970243043341> GrandMaster':
        embed.set_image(url = "https://cdn.discordapp.com/attachments/811303510733226024/811307786989600788/Grandmaster.png")
        
    elif tier == '<:challenger:817361981513400320> Challenger':
        embed.set_image(url = "https://cdn.discordapp.com/attachments/811303510733226024/811307785542303774/Challenger.png")

    

    
        

    await ctx.send(embed=embed)


@stats.error
 
async def stats_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        embed=discord.Embed(title=":warning: Stats Command", description='__Wrong Use__!',color=discord.Color.gold())
        embed.add_field(name = 'Use:', value = '!e stats (region) (summoner name)', inline = False)
        embed.add_field(name = 'Available Regions:', value = 'eune, euw, na, kr, br, lan, las, jp, ru', inline = False)
        embed.set_thumbnail(url = 'https://cdn.discordapp.com/attachments/802967377159389317/819155421108371467/poroerror.png')
        
        await ctx.send(embed=embed)
    
       



#ping σε ms
@client.command()
async def ping(ctx):
    await ctx.send(str((round(client.latency * 1000))) + str('ms'))

    

#Βρες εναν summoner μεσω op.gg(EUNE)
@client.command()
async def check(ctx, reg, *,arg):
    arg = arg.replace(" ", "%20")
    
    if reg == 'eune':
        await ctx.send('http://eune.op.gg/summoner/userName='+arg)
    elif reg == 'EUNE':
        await ctx.send('http://eune.op.gg/summoner/userName='+arg)
    elif reg == 'euw':
        await ctx.send('http://euw.op.gg/summoner/userName='+arg)
    elif reg == 'EUW':
        await ctx.send('http://euw.op.gg/summoner/userName='+arg)
    elif reg == 'na':
        await ctx.send('http://na.op.gg/summoner/userName='+arg)
    elif reg == 'NA':
        await ctx.send('http://na.op.gg/summoner/userName='+arg)
    elif reg == 'kr':
        await ctx.send('http://op.gg/summoner/userName='+arg)
    elif reg == 'KR':
        await ctx.send('http://op.gg/summoner/userName='+arg)

@check.error
async def check_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        embed=discord.Embed(title=":warning: Check Command", description='__Wrong Use__!',color=discord.Color.gold())
        embed.add_field(name = 'Use:', value ='!e check (region) (summoner name)', inline = False)
        embed.add_field(name = 'Available Regions:', value = 'eune, euw, na, kr, br, la1, la2, jp, ru', inline = False)
        embed.set_thumbnail(url = 'https://cdn.discordapp.com/attachments/802967377159389317/819155421108371467/poroerror.png')
        await ctx.send(embed=embed)

#Βρες πληροφοριες για εναν champion
@client.command()
async def champ(ctx, *,champ):
    champ = champ.replace(" ", "")
    await ctx.send('http://champion.gg/champion/'+champ)

@champ.error
async def champ_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        embed=discord.Embed(title=":warning: Champion Command", description='\u200B',color=discord.Color.gold())
        embed.add_field(name = 'Use:', value = '!e champ (champion name)')
        embed.set_thumbnail(url = 'https://cdn.discordapp.com/attachments/802967377159389317/819155421108371467/poroerror.png')
        await ctx.send(embed=embed)

#Βρες build για εναν champion
@client.command()
async def build(ctx, *,champbuild):
    champbuild = champbuild.replace(" ", "")
    await ctx.send('http://www.probuilds.net/champions/details/'+champbuild)

@build.error
async def build_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        embed=discord.Embed(title=":warning: Build Command", description='\u200B',color=discord.Color.gold())
        embed.add_field(name = 'Use:', value= '!e build (champion name)')
        embed.set_thumbnail(url = 'https://cdn.discordapp.com/attachments/802967377159389317/819155421108371467/poroerror.png')
        await ctx.send(embed=embed)

#Βρες πληροφοριες για το counter ενος champion
@client.command()
async def counter(ctx, *, champcounter):
    champcounter = champcounter.replace(" ", "")
    await ctx.send('http://www.championcounter.com/'+champcounter)

@counter.error
async def counter_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        embed=discord.Embed(title=":warning: Counter Command", description='\u200B',color=discord.Color.gold())
        embed.add_field(name = 'Use:', value= '!e counter (champion name)')
        embed.set_thumbnail(url = 'https://cdn.discordapp.com/attachments/802967377159389317/819155421108371467/poroerror.png')
        await ctx.send(embed=embed)

#Δες τα patch notes
@client.command()
async def patch(ctx):
    await ctx.send('https://eune.leagueoflegends.com/en-us/news/tags/patch-notes')


#Για profile id
@client.command()
async def id(ctx, member: discord.Member):
    roles = [role for role in member.roles]
    
    embed = discord.Embed(title="User Identity", description="", color= discord.Color.purple())
    embed.add_field(name="Username:", value=member.name, inline=True)
    embed.add_field(name="ID:",value=member.id, inline=True)
    embed.add_field(name="Server:", value=f"{ctx.guild.name}")
    embed.add_field(name="Region:", value=f"{ctx.guild.region}")
    embed.add_field(name="Primary Role:", value = member.top_role.mention)
    embed.add_field(name=f"Other roles:({len(roles)})", value=" ".join([role.mention for role in roles]))
    embed.set_thumbnail(url=member.avatar_url)
    await ctx.send(content=None, embed=embed)

@id.error
async def id_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        embed=discord.Embed(title=":warning: ID Command", description='__Wrong use!__',color=discord.Color.gold())
        embed.add_field(name = 'Use:', value= '!e id (discord username)')
        await ctx.send(embed=embed)

@client.command()
async def live(ctx, region, *, arg):

    waitmessage = await ctx.send(":red_circle: Please wait while we are fetching live game data...")

    


    if region == 'eune':
        ign = lol_watcher.summoner.by_name('eun1', arg)
        match = lol_watcher.spectator.by_summoner('eun1', ign['id'])

        
    elif region == 'EUNE':
        ign = lol_watcher.summoner.by_name('eun1', arg)
        match = lol_watcher.spectator.by_summoner('eun1', ign['id'])
        
    elif region == 'euw':
        ign = lol_watcher.summoner.by_name('euw1', arg)
        match = lol_watcher.spectator.by_summoner('euw1', ign['id'])
        
    elif region == 'EUW':
        ign = lol_watcher.summoner.by_name('euw1', arg)
        match = lol_watcher.spectator.by_summoner('euw', ign['id'])
        
    elif region == 'na':
        ign = lol_watcher.summoner.by_name('na1', arg)
        match = lol_watcher.spectator.by_summoner('na1', ign['id'])
        
    elif region == 'NA':
        ign = lol_watcher.summoner.by_name('na1', arg)
        match = lol_watcher.spectator.by_summoner('na1', ign['id'])
        
    elif region == 'kr':
        ign = lol_watcher.summoner.by_name('kr', arg)
        match = lol_watcher.spectator.by_summoner('kr', ign['id'])
        
    elif region == 'KR':
        ign = lol_watcher.summoner.by_name('kr', arg)
        match = lol_watcher.spectator.by_summoner('kr', ign['id'])

    elif region == 'br':
        ign = lol_watcher.summoner.by_name('br1', arg)
        match = lol_watcher.spectator.by_summoner('br1', ign['id'])
        
                                           
    elif region == 'BR':
        ign = lol_watcher.summoner.by_name('br1', arg)
        match = lol_watcher.spectator.by_summoner('br1', ign['id'])

    elif region == 'lan':
        ign = lol_watcher.summoner.by_name('la1', arg)
        match = lol_watcher.spectator.by_summoner('la1', ign['id'])
        
    elif region == 'LAN':
        ign = lol_watcher.summoner.by_name('la1', arg)
        match = lol_watcher.spectator.by_summoner('la1', ign['id'])
        
    elif region == 'las':
        ign = lol_watcher.summoner.by_name('la2', arg)
        match = lol_watcher.spectator.by_summoner('la2', ign['id'])

    elif region == 'LAS':
        ign = lol_watcher.summoner.by_name('la2', arg)
        match = lol_watcher.spectator.by_summoner('la2', ign['id'])

    elif region == 'jp':
        ign = lol_watcher.summoner.by_name('jp1', arg)
        match = lol_watcher.spectator.by_summoner('jp1', ign['id'])
        
    elif region == 'JP':
        ign = lol_watcher.summoner.by_name('jp1', arg)
        match = lol_watcher.spectator.by_summoner('jp1', ign['id'])
        
    elif region == 'ru':
        ign = lol_watcher.summoner.by_name('ru', arg)
        match = lol_watcher.spectator.by_summoner('ru', ign['id'])
        
    elif region == 'RU':
        ign = lol_watcher.summoner.by_name('ru', arg)
        match = lol_watcher.spectator.by_summoner('ru', ign['id'])
        
        

    GameDuration = match['gameLength']
    Time = strftime("%M:%S", gmtime(GameDuration)) #time.strftime('%M:%S', time.gmtime(GameDuration))
    

    p = (match['participants'])
    #rank gia p1
    p1 = p[0]['summonerName']
    id_p1 = p[0]['summonerId']
    p1champion = p[0]['championId']
    if region == 'eune':
        rankp1 = lol_watcher.league.by_summoner('eun1',id_p1)
    elif region == 'EUNE':
        rankp1 = lol_watcher.league.by_summoner('eun1',id_p1)
    elif region == 'euw':
        rankp1 = lol_watcher.league.by_summoner('euw1',id_p1)
    elif region == 'EUW':
        rankp1 = lol_watcher.league.by_summoner('euw1',id_p1)
    elif region == 'na':
        rankp1 = lol_watcher.league.by_summoner('na1',id_p1)
    elif region == 'NA':
        rankp1 = lol_watcher.league.by_summoner('na1',id_p1)
    elif region == 'KR':
        rankp1 = lol_watcher.league.by_summoner('kr',id_p1)
    elif region == 'kr':
        rankp1 = lol_watcher.league.by_summoner('kr',id_p1)
    elif region == 'BR':
        rankp1 = lol_watcher.league.by_summoner('br1',id_p1)
    elif region == 'br':
        rankp1 = lol_watcher.league.by_summoner('br1',id_p1)
    elif region == 'LAN':
        rankp1 = lol_watcher.league.by_summoner('la1',id_p1)
    elif region == 'lan':
        rankp1 = lol_watcher.league.by_summoner('la1',id_p1)
    elif region == 'LAS':
        rankp1 = lol_watcher.league.by_summoner('la2',id_p1)
    elif region == 'las':
        rankp1 = lol_watcher.league.by_summoner('la2',id_p1)
    elif region == 'JP':
        rankp1 = lol_watcher.league.by_summoner('jp1',id_p1)
    elif region == 'jp':
        rankp1 = lol_watcher.league.by_summoner('jp1',id_p1)
    elif region == 'RU':
        rankp1 = lol_watcher.league.by_summoner('ru',id_p1)
    elif region == 'ru':
        rankp1 = lol_watcher.league.by_summoner('ru',id_p1)

    for i in range(len(rankp1)):
        if rankp1[i]['queueType'] == 'RANKED_FLEX_SR':
            del rankp1[i]
            break

    if rankp1 == []:
        tier1 = '<:unranked:817365350969769994> Unranked'
    else: tier1 = rankp1[0]['tier']

    if rankp1 == []:
        rank1 = '\u200B'
    else: rank1 = rankp1[0]['rank']

    if rankp1 == []:
        wins1 = 1
    else: wins1 = rankp1[0]['wins']

    if rankp1 == []:
        lose1 = 0
    else: lose1 = rankp1[0]['losses']

    if rankp1 == []:
        lp1 = '0'
    else: lp1 = rankp1[0]['leaguePoints']

    #tiers kai ranks pros allagh
    if tier1 == 'IRON':
        tier1 = '<:iron:817360753173463060> Iron'
    elif tier1 == 'BRONZE':
        tier1 = '<:bronze:817361809295671326> Bronze'
    elif tier1 == 'SILVER':
        tier1 = '<:silver:817361823312773141> Silver'
    elif tier1 == 'GOLD':
        tier1 = '<:gold:817361901339148318> Gold'
    elif tier1 == 'PLATINUM':
        tier1 = '<:platinum:817361924857659444> Platinum'
    elif tier1 == 'DIAMOND':
        tier1 = '<:diamond:817361937913872404> Diamond'
    elif tier1 == 'MASTER':
        tier1 = '<:master:817361953269088276> Master'
    elif tier1 == 'GRANDMASTER':
        tier1 = '<:grandmaster:817361970243043341> GrandMaster'
    elif tier1 == 'CHALLENGER':
        tier1 = '<:challenger:817361981513400320> Challenger'

    if rank1 == 'IV':
        rank1 = '4'
    elif rank1 == 'III':
        rank1 = '3'
    elif rank1 == 'II':
        rank1 = '2'
    elif rank1 == 'I':
        rank1 = '1'
    #tiers kai ranks pros allagh

   
    games1 = wins1 + lose1
    workwr1 = wins1 * 100
    wr1 = workwr1//games1

    runesp1 = p[0]['perks']
    rp1 = runesp1['perkStyle']
    rs1 = runesp1['perkSubStyle']

    if rp1 == 8000:
        rp1 = '<:precision:818050788118233089>'
    elif rp1 == 8100:
        rp1 = '<:domination:818050737589846026>'
    elif rp1 == 8200:
        rp1 = '<:sorcery:818050843143700502>'
    elif rp1 == 8300:
        rp1 = '<:inspiration:818050767642558464>'
    elif rp1 == 8400:
        rp1 = '<:resolve:818050828333613076>'

    if rs1 == 8000:
        rs1 = '<:precision:818050788118233089>'
    elif rs1 == 8100:
        rs1 = '<:domination:818050737589846026>'
    elif rs1 == 8200:
        rs1 = '<:sorcery:818050843143700502>'
    elif rs1 == 8300:
        rs1 = '<:inspiration:818050767642558464>'
    elif rs1 == 8400:
        rs1 = '<:resolve:818050828333613076>'
    

    #rank gia p2
    p2 = p[1]['summonerName']
    id_p2 = p[1]['summonerId']
    p2champion = p[1]['championId']
    if region == 'eune':
        rankp2 = lol_watcher.league.by_summoner('eun1',id_p2)
    elif region == 'EUNE':
        rankp2 = lol_watcher.league.by_summoner('eun1',id_p2)
    elif region == 'euw':
        rankp2 = lol_watcher.league.by_summoner('euw1',id_p2)
    elif region == 'EUW':
        rankp2 = lol_watcher.league.by_summoner('euw1',id_p2)
    elif region == 'na':
        rankp2 = lol_watcher.league.by_summoner('na1',id_p2)
    elif region == 'NA':
        rankp2 = lol_watcher.league.by_summoner('na1',id_p2)
    elif region == 'KR':
        rankp2 = lol_watcher.league.by_summoner('kr',id_p2)
    elif region == 'kr':
        rankp2 = lol_watcher.league.by_summoner('kr',id_p2)
    elif region == 'BR':
        rankp2 = lol_watcher.league.by_summoner('br1',id_p2)
    elif region == 'br':
        rankp2 = lol_watcher.league.by_summoner('br1',id_p2)
    elif region == 'LAN':
        rankp2 = lol_watcher.league.by_summoner('la1',id_p2)
    elif region == 'lan':
        rankp2 = lol_watcher.league.by_summoner('la1',id_p2)
    elif region == 'LAS':
        rankp2 = lol_watcher.league.by_summoner('la2',id_p2)
    elif region == 'las':
        rankp2 = lol_watcher.league.by_summoner('la2',id_p2)
    elif region == 'JP':
        rankp2 = lol_watcher.league.by_summoner('jp1',id_p2)
    elif region == 'jp':
        rankp2 = lol_watcher.league.by_summoner('jp1',id_p2)
    elif region == 'RU':
        rankp2 = lol_watcher.league.by_summoner('ru',id_p2)
    elif region == 'ru':
        rankp2 = lol_watcher.league.by_summoner('ru',id_p2)


    for i in range(len(rankp2)):
        if rankp2[i]['queueType'] == 'RANKED_FLEX_SR':
            del rankp2[i]
            break

    

    if rankp2 == []:
        tier2 = '<:unranked:817365350969769994> Unranked'
    else: tier2 = rankp2[0]['tier']
    

    if rankp2 == []:
        rank2 = '\u200B'
    else: rank2 = rankp2[0]['rank']

    if rankp2 == []:
        wins2 = 1
    else: wins2 = rankp2[0]['wins']

    if rankp2 == []:
        lose2 = 0
    else: lose2 = rankp2[0]['losses']

    if rankp2 == []:
        lp2 = '0'
    else: lp2 = rankp2[0]['leaguePoints']

    #tiers kai ranks pros allagh
    if tier2 == 'IRON':
        tier2 = '<:iron:817360753173463060> Iron'
    elif tier2 == 'BRONZE':
        tier2 = '<:bronze:817361809295671326> Bronze'
    elif tier2 == 'SILVER':
        tier2 = '<:silver:817361823312773141> Silver'
    elif tier2 == 'GOLD':
        tier2 = '<:gold:817361901339148318> Gold'
    elif tier2 == 'PLATINUM':
        tier2 = '<:platinum:817361924857659444> Platinum'
    elif tier2 == 'DIAMOND':
        tier2 = '<:diamond:817361937913872404> Diamond'
    elif tier2 == 'MASTER':
        tier2 = '<:master:817361953269088276> Master'
    elif tier2 == 'GRANDMASTER':
        tier2 = '<:grandmaster:817361970243043341> GrandMaster'
    elif tier2 == 'CHALLENGER':
        tier2 = '<:challenger:817361981513400320> Challenger'

    if rank2 == 'IV':
        rank2 = '4'
    elif rank2 == 'III':
        rank2 = '3'
    elif rank2 == 'II':
        rank2 = '2'
    elif rank2 == 'I':
        rank2 = '1'
    #tiers kai ranks pros allagh

        

    
   
    games2 = wins2 + lose2
    workwr2 = wins2 * 100
    wr2 = workwr2//games2

    runesp2 = p[1]['perks']
    rp2 = runesp2['perkStyle']
    rs2 = runesp2['perkSubStyle']

    if rp2 == 8000:
        rp2 = '<:precision:818050788118233089>'
    elif rp2 == 8100:
        rp2 = '<:domination:818050737589846026>'
    elif rp2 == 8200:
        rp2 = '<:sorcery:818050843143700502>'
    elif rp2 == 8300:
        rp2 = '<:inspiration:818050767642558464>'
    elif rp2 == 8400:
        rp2 = '<:resolve:818050828333613076>'

    if rs2 == 8000:
        rs2 = '<:precision:818050788118233089>'
    elif rs2 == 8100:
        rs2 = '<:domination:818050737589846026>'
    elif rs2 == 8200:
        rs2 = '<:sorcery:818050843143700502>'
    elif rs2 == 8300:
        rs2 = '<:inspiration:818050767642558464>'
    elif rs2 == 8400:
        rs2 = '<:resolve:818050828333613076>'

   


    
    #rank gia p3
    p3 = p[2]['summonerName']
    id_p3 = p[2]['summonerId']
    p3champion = p[2]['championId']
    if region == 'eune':
        rankp3 = lol_watcher.league.by_summoner('eun1',id_p3)
    elif region == 'EUNE':
        rankp3 = lol_watcher.league.by_summoner('eun1',id_p3)
    elif region == 'euw':
        rankp3 = lol_watcher.league.by_summoner('euw1',id_p3)
    elif region == 'EUW':
        rankp3 = lol_watcher.league.by_summoner('euw1',id_p3)
    elif region == 'na':
        rankp3 = lol_watcher.league.by_summoner('na1',id_p3)
    elif region == 'NA':
        rankp3 = lol_watcher.league.by_summoner('na1',id_p3)
    elif region == 'KR':
        rankp3 = lol_watcher.league.by_summoner('kr',id_p3)
    elif region == 'kr':
        rankp3 = lol_watcher.league.by_summoner('kr',id_p3)
    elif region == 'BR':
        rankp3 = lol_watcher.league.by_summoner('br1',id_p3)
    elif region == 'br':
        rankp3 = lol_watcher.league.by_summoner('br1',id_p3)
    elif region == 'LAN':
        rankp3 = lol_watcher.league.by_summoner('la1',id_p3)
    elif region == 'lan':
        rankp3 = lol_watcher.league.by_summoner('la1',id_p3)
    elif region == 'LAS':
        rankp3 = lol_watcher.league.by_summoner('la2',id_p3)
    elif region == 'las':
        rankp3 = lol_watcher.league.by_summoner('la2',id_p3)
    elif region == 'JP':
        rankp3 = lol_watcher.league.by_summoner('jp1',id_p3)
    elif region == 'jp':
        rankp3 = lol_watcher.league.by_summoner('jp1',id_p3)
    elif region == 'RU':
        rankp3 = lol_watcher.league.by_summoner('ru',id_p3)
    elif region == 'ru':
        rankp3 = lol_watcher.league.by_summoner('ru',id_p3)


    for i in range(len(rankp3)):
        if rankp3[i]['queueType'] == 'RANKED_FLEX_SR':
            del rankp3[i]
            break

    if rankp3 == []:
        tier3 = '<:unranked:817365350969769994> Unranked'
    else: tier3 = rankp3[0]['tier']

    if rankp3 == []:
        rank3 = '\u200B'
    else: rank3 = rankp3[0]['rank']

    if rankp3 == []:
        wins3 = 1
    else: wins3 = rankp3[0]['wins']

    if rankp3 == []:
        lose3 = 0
    else: lose3 = rankp3[0]['losses']

    if rankp3 == []:
        lp3 = '0'
    else: lp3 = rankp3[0]['leaguePoints']

    #tiers kai ranks pros allagh
    if tier3 == 'IRON':
        tier3 = '<:iron:817360753173463060> Iron'
    elif tier3 == 'BRONZE':
        tier3 = '<:bronze:817361809295671326> Bronze'
    elif tier3 == 'SILVER':
        tier3 = '<:silver:817361823312773141> Silver'
    elif tier3 == 'GOLD':
        tier3 = '<:gold:817361901339148318> Gold'
    elif tier3 == 'PLATINUM':
        tier3 = '<:platinum:817361924857659444> Platinum'
    elif tier3 == 'DIAMOND':
        tier3 = '<:diamond:817361937913872404> Diamond'
    elif tier3 == 'MASTER':
        tier3 = '<:master:817361953269088276> Master'
    elif tier3 == 'GRANDMASTER':
        tier3 = '<:grandmaster:817361970243043341> GrandMaster'
    elif tier3 == 'CHALLENGER':
        tier3 = '<:challenger:817361981513400320> Challenger'

    if rank3 == 'IV':
        rank3 = '4'
    elif rank3 == 'III':
        rank3 = '3'
    elif rank3 == 'II':
        rank3 = '2'
    elif rank3 == 'I':
        rank3 = '1'
    #tiers kai ranks pros allagh
    

    
    games3 = wins3 + lose3
    workwr3 = wins3 * 100
    wr3 = workwr3//games3

    runesp3 = p[2]['perks']
    rp3 = runesp3['perkStyle']
    rs3 = runesp3['perkSubStyle']

    if rp3 == 8000:
        rp3 = '<:precision:818050788118233089>'
    elif rp3 == 8100:
        rp3 = '<:domination:818050737589846026>'
    elif rp3 == 8200:
        rp3 = '<:sorcery:818050843143700502>'
    elif rp3 == 8300:
        rp3 = '<:inspiration:818050767642558464>'
    elif rp3 == 8400:
        rp3 = '<:resolve:818050828333613076>'

    if rs3 == 8000:
        rs3 = '<:precision:818050788118233089>'
    elif rs3 == 8100:
        rs3 = '<:domination:818050737589846026>'
    elif rs3 == 8200:
        rs3 = '<:sorcery:818050843143700502>'
    elif rs3 == 8300:
        rs3 = '<:inspiration:818050767642558464>'
    elif rs3 == 8400:
        rs3 = '<:resolve:818050828333613076>'
    
    #rank gia p4
    p4 = p[3]['summonerName']
    id_p4 = p[3]['summonerId']
    p4champion = p[3]['championId']
    if region == 'eune':
        rankp4 = lol_watcher.league.by_summoner('eun1',id_p4)
    elif region == 'EUNE':
        rankp4 = lol_watcher.league.by_summoner('eun1',id_p4)
    elif region == 'euw':
        rankp4 = lol_watcher.league.by_summoner('euw1',id_p4)
    elif region == 'EUW':
        rankp4 = lol_watcher.league.by_summoner('euw1',id_p4)
    elif region == 'na':
        rankp4 = lol_watcher.league.by_summoner('na1',id_p4)
    elif region == 'NA':
        rankp4 = lol_watcher.league.by_summoner('na1',id_p4)
    elif region == 'KR':
        rankp4 = lol_watcher.league.by_summoner('kr',id_p4)
    elif region == 'kr':
        rankp4 = lol_watcher.league.by_summoner('kr',id_p4)
    elif region == 'BR':
        rankp4 = lol_watcher.league.by_summoner('br1',id_p4)
    elif region == 'br':
        rankp4 = lol_watcher.league.by_summoner('br1',id_p4)
    elif region == 'LAN':
        rankp4 = lol_watcher.league.by_summoner('la1',id_p4)
    elif region == 'lan':
        rankp4 = lol_watcher.league.by_summoner('la1',id_p4)
    elif region == 'LAS':
        rankp4 = lol_watcher.league.by_summoner('la2',id_p4)
    elif region == 'las':
        rankp4 = lol_watcher.league.by_summoner('la2',id_p4)
    elif region == 'JP':
        rankp4 = lol_watcher.league.by_summoner('jp1',id_p4)
    elif region == 'jp':
        rankp4 = lol_watcher.league.by_summoner('jp1',id_p4)
    elif region == 'RU':
        rankp4 = lol_watcher.league.by_summoner('ru',id_p4)
    elif region == 'ru':
        rankp4 = lol_watcher.league.by_summoner('ru',id_p4)


    for i in range(len(rankp4)):
        if rankp4[i]['queueType'] == 'RANKED_FLEX_SR':
            del rankp4[i]
            break

    if rankp4 == []:
        tier4 = '<:unranked:817365350969769994> Unranked'
    else: tier4 = rankp4[0]['tier']

    if rankp4 == []:
        rank4 = '\u200B'
    else: rank4 = rankp4[0]['rank']

    if rankp4 == []:
        wins4 = 1
    else: wins4 = rankp4[0]['wins']

    if rankp4 == []:
        lose4 = 0
    else: lose4 = rankp4[0]['losses']

    if rankp4 == []:
        lp4 = '0'
    else: lp4 = rankp4[0]['leaguePoints']

    #tiers kai ranks pros allagh
    if tier4 == 'IRON':
        tier4 = '<:iron:817360753173463060> Iron'
    elif tier4 == 'BRONZE':
        tier4 = '<:bronze:817361809295671326> Bronze'
    elif tier4 == 'SILVER':
        tier4 = '<:silver:817361823312773141> Silver'
    elif tier4 == 'GOLD':
        tier4 = '<:gold:817361901339148318> Gold'
    elif tier4 == 'PLATINUM':
        tier4 = '<:platinum:817361924857659444> Platinum'
    elif tier4 == 'DIAMOND':
        tier4 = '<:diamond:817361937913872404> Diamond'
    elif tier4 == 'MASTER':
        tier4 = '<:master:817361953269088276> Master'
    elif tier4 == 'GRANDMASTER':
        tier4 = '<:grandmaster:817361970243043341> GrandMaster'
    elif tier4 == 'CHALLENGER':
        tier4 = '<:challenger:817361981513400320> Challenger'

    if rank4 == 'IV':
        rank4 = '4'
    elif rank4 == 'III':
        rank4 = '3'
    elif rank4 == 'II':
        rank4 = '2'
    elif rank4 == 'I':
        rank4 = '1'
    #tiers kai ranks pros allagh
    

    
    games4 = wins4 + lose4
    workwr4 = wins4 * 100
    wr4 = workwr4//games4

    runesp4 = p[3]['perks']
    rp4 = runesp4['perkStyle']
    rs4 = runesp4['perkSubStyle']

    if rp4 == 8000:
        rp4 = '<:precision:818050788118233089>'
    elif rp4 == 8100:
        rp4 = '<:domination:818050737589846026>'
    elif rp4 == 8200:
        rp4 = '<:sorcery:818050843143700502>'
    elif rp4 == 8300:
        rp4 = '<:inspiration:818050767642558464>'
    elif rp4 == 8400:
        rp4 = '<:resolve:818050828333613076>'

    if rs4 == 8000:
        rs4 = '<:precision:818050788118233089>'
    elif rs4 == 8100:
        rs4 = '<:domination:818050737589846026>'
    elif rs4 == 8200:
        rs4 = '<:sorcery:818050843143700502>'
    elif rs4 == 8300:
        rs4 = '<:inspiration:818050767642558464>'
    elif rs4 == 8400:
        rs4 = '<:resolve:818050828333613076>'

    #rank gia p5
    p5 = p[4]['summonerName']
    id_p5 = p[4]['summonerId']
    p5champion = p[4]['championId']
    if region == 'eune':
        rankp5 = lol_watcher.league.by_summoner('eun1',id_p5)
    elif region == 'EUNE':
        rankp5 = lol_watcher.league.by_summoner('eun1',id_p5)
    elif region == 'euw':
        rankp5 = lol_watcher.league.by_summoner('euw1',id_p5)
    elif region == 'EUW':
        rankp5 = lol_watcher.league.by_summoner('euw1',id_p5)
    elif region == 'na':
        rankp5 = lol_watcher.league.by_summoner('na1',id_p5)
    elif region == 'NA':
        rankp5 = lol_watcher.league.by_summoner('na1',id_p5)
    elif region == 'KR':
        rankp5 = lol_watcher.league.by_summoner('kr',id_p5)
    elif region == 'kr':
        rankp5 = lol_watcher.league.by_summoner('kr',id_p5)
    elif region == 'BR':
        rankp5 = lol_watcher.league.by_summoner('br1',id_p5)
    elif region == 'br':
        rankp5 = lol_watcher.league.by_summoner('br1',id_p5)
    elif region == 'LAN':
        rankp5 = lol_watcher.league.by_summoner('la1',id_p5)
    elif region == 'lan':
        rankp5 = lol_watcher.league.by_summoner('la1',id_p5)
    elif region == 'LAS':
        rankp5 = lol_watcher.league.by_summoner('la2',id_p5)
    elif region == 'las':
        rankp5 = lol_watcher.league.by_summoner('la2',id_p5)
    elif region == 'JP':
        rankp5 = lol_watcher.league.by_summoner('jp1',id_p5)
    elif region == 'jp':
        rankp5 = lol_watcher.league.by_summoner('jp1',id_p5)
    elif region == 'RU':
        rankp5 = lol_watcher.league.by_summoner('ru',id_p5)
    elif region == 'ru':
        rankp5 = lol_watcher.league.by_summoner('ru',id_p5)


    for i in range(len(rankp5)):
        if rankp5[i]['queueType'] == 'RANKED_FLEX_SR':
            del rankp5[i]
            break

    if rankp5 == []:
        tier5 = '<:unranked:817365350969769994> Unranked'
    else: tier5 = rankp5[0]['tier']

    if rankp5 == []:
        rank5 = '\u200B'
    else: rank5 = rankp5[0]['rank']

    if rankp5 == []:
        wins5 = 1
    else: wins5 = rankp5[0]['wins']

    if rankp5 == []:
        lose5 = 0
    else: lose5 = rankp5[0]['losses']

    if rankp5 == []:
        lp5 = '0'
    else: lp5 = rankp5[0]['leaguePoints']

    #tiers kai ranks pros allagh
    if tier5 == 'IRON':
        tier5 = '<:iron:817360753173463060> Iron'
    elif tier5 == 'BRONZE':
        tier5 = '<:bronze:817361809295671326> Bronze'
    elif tier5 == 'SILVER':
        tier5 = '<:silver:817361823312773141> Silver'
    elif tier5 == 'GOLD':
        tier5 = '<:gold:817361901339148318> Gold'
    elif tier5 == 'PLATINUM':
        tier5 = '<:platinum:817361924857659444> Platinum'
    elif tier5 == 'DIAMOND':
        tier5 = '<:diamond:817361937913872404> Diamond'
    elif tier5 == 'MASTER':
        tier5 = '<:master:817361953269088276> Master'
    elif tier5 == 'GRANDMASTER':
        tier5 = '<:grandmaster:817361970243043341> GrandMaster'
    elif tier5 == 'CHALLENGER':
        tier5 = '<:challenger:817361981513400320> Challenger'

    if rank5 == 'IV':
        rank5 = '4'
    elif rank5 == 'III':
        rank5 = '3'
    elif rank5 == 'II':
        rank5 = '2'
    elif rank5 == 'I':
        rank5 = '1'
    #tiers kai ranks pros allagh
    
    
    
    games5 = wins5 + lose5
    workwr5 = wins5 * 100
    wr5 = workwr5//games5

    runesp5 = p[4]['perks']
    rp5 = runesp5['perkStyle']
    rs5 = runesp5['perkSubStyle']

    if rp5 == 8000:
        rp5 = '<:precision:818050788118233089>'
    elif rp5 == 8100:
        rp5 = '<:domination:818050737589846026>'
    elif rp5 == 8200:
        rp5 = '<:sorcery:818050843143700502>'
    elif rp5 == 8300:
        rp5 = '<:inspiration:818050767642558464>'
    elif rp5 == 8400:
        rp5 = '<:resolve:818050828333613076>'

    if rs5 == 8000:
        rs5 = '<:precision:818050788118233089>'
    elif rs5 == 8100:
        rs5 = '<:domination:818050737589846026>'
    elif rs5 == 8200:
        rs5 = '<:sorcery:818050843143700502>'
    elif rs5 == 8300:
        rs5 = '<:inspiration:818050767642558464>'
    elif rs5 == 8400:
        rs5 = '<:resolve:818050828333613076>'
    
    #rank gia p6
    p6 = p[5]['summonerName']
    id_p6 = p[5]['summonerId']
    p6champion = p[5]['championId']
    if region == 'eune':
        rankp6 = lol_watcher.league.by_summoner('eun1',id_p6)
    elif region == 'EUNE':
        rankp6 = lol_watcher.league.by_summoner('eun1',id_p6)
    elif region == 'euw':
        rankp6 = lol_watcher.league.by_summoner('euw1',id_p6)
    elif region == 'EUW':
        rankp6 = lol_watcher.league.by_summoner('euw1',id_p6)
    elif region == 'na':
        rankp6 = lol_watcher.league.by_summoner('na1',id_p6)
    elif region == 'NA':
        rankp6 = lol_watcher.league.by_summoner('na1',id_p6)
    elif region == 'KR':
        rankp6 = lol_watcher.league.by_summoner('kr',id_p6)
    elif region == 'kr':
        rankp6 = lol_watcher.league.by_summoner('kr',id_p6)
    elif region == 'BR':
        rankp6 = lol_watcher.league.by_summoner('br1',id_p6)
    elif region == 'br':
        rankp6 = lol_watcher.league.by_summoner('br1',id_p6)
    elif region == 'LAN':
        rankp6 = lol_watcher.league.by_summoner('la1',id_p6)
    elif region == 'lan':
        rankp6 = lol_watcher.league.by_summoner('la1',id_p6)
    elif region == 'LAS':
        rankp6 = lol_watcher.league.by_summoner('la2',id_p6)
    elif region == 'las':
        rankp6 = lol_watcher.league.by_summoner('la2',id_p6)
    elif region == 'JP':
        rankp6 = lol_watcher.league.by_summoner('jp1',id_p6)
    elif region == 'jp':
        rankp6 = lol_watcher.league.by_summoner('jp1',id_p6)
    elif region == 'RU':
        rankp6 = lol_watcher.league.by_summoner('ru',id_p6)
    elif region == 'ru':
        rankp6 = lol_watcher.league.by_summoner('ru',id_p6)


    for i in range(len(rankp6)):
        if rankp6[i]['queueType'] == 'RANKED_FLEX_SR':
            del rankp6[i]
            break

    if rankp6 == []:
        tier6 = '<:unranked:817365350969769994> Unranked'
    else: tier6 = rankp6[0]['tier']

    if rankp6 == []:
        rank6 = '\u200B'
    else: rank6 = rankp6[0]['rank']

    if rankp6 == []:
        wins6 = 1
    else: wins6 = rankp6[0]['wins']

    if rankp6 == []:
        lose6 = 0
    else: lose6 = rankp6[0]['losses']

    if rankp6 == []:
        lp6 = '0'
    else: lp6 = rankp6[0]['leaguePoints']

    #tiers kai ranks pros allagh
    if tier6 == 'IRON':
        tier6 = '<:iron:817360753173463060> Iron'
    elif tier6 == 'BRONZE':
        tier6 = '<:bronze:817361809295671326> Bronze'
    elif tier6 == 'SILVER':
        tier6 = '<:silver:817361823312773141> Silver'
    elif tier6 == 'GOLD':
        tier6 = '<:gold:817361901339148318> Gold'
    elif tier6 == 'PLATINUM':
        tier6 = '<:platinum:817361924857659444> Platinum'
    elif tier6 == 'DIAMOND':
        tier6 = '<:diamond:817361937913872404> Diamond'
    elif tier6 == 'MASTER':
        tier6 = '<:master:817361953269088276> Master'
    elif tier6 == 'GRANDMASTER':
        tier6 = '<:grandmaster:817361970243043341> GrandMaster'
    elif tier6 == 'CHALLENGER':
        tier6 = '<:challenger:817361981513400320> Challenger'

    if rank6 == 'IV':
        rank6 = '4'
    elif rank6 == 'III':
        rank6 = '3'
    elif rank6 == 'II':
        rank6 = '2'
    elif rank6 == 'I':
        rank6 = '1'
    #tiers kai ranks pros allagh
    
    
    games6 = wins6 + lose6
    workwr6 = wins6 * 100
    wr6 = workwr6//games6

    runesp6 = p[5]['perks']
    rp6 = runesp6['perkStyle']
    rs6 = runesp6['perkSubStyle']

    if rp6 == 8000:
        rp6 = '<:precision:818050788118233089>'
    elif rp6 == 8100:
        rp6 = '<:domination:818050737589846026>'
    elif rp6 == 8200:
        rp6 = '<:sorcery:818050843143700502>'
    elif rp6 == 8300:
        rp6 = '<:inspiration:818050767642558464>'
    elif rp6 == 8400:
        rp6 = '<:resolve:818050828333613076>'

    if rs6 == 8000:
        rs6 = '<:precision:818050788118233089>'
    elif rs6 == 8100:
        rs6 = '<:domination:818050737589846026>'
    elif rs6 == 8200:
        rs6 = '<:sorcery:818050843143700502>'
    elif rs6 == 8300:
        rs6 = '<:inspiration:818050767642558464>'
    elif rs6 == 8400:
        rs6 = '<:resolve:818050828333613076>'
   
    #rank gia p7
    p7 = p[6]['summonerName']
    id_p7 = p[6]['summonerId']
    p7champion = p[6]['championId']
    if region == 'eune':
        rankp7 = lol_watcher.league.by_summoner('eun1',id_p7)
    elif region == 'EUNE':
        rankp7 = lol_watcher.league.by_summoner('eun1',id_p7)
    elif region == 'euw':
        rankp7 = lol_watcher.league.by_summoner('euw1',id_p7)
    elif region == 'EUW':
        rankp7 = lol_watcher.league.by_summoner('euw1',id_p7)
    elif region == 'na':
        rankp7 = lol_watcher.league.by_summoner('na1',id_p7)
    elif region == 'NA':
        rankp7 = lol_watcher.league.by_summoner('na1',id_p7)
    elif region == 'KR':
        rankp7 = lol_watcher.league.by_summoner('kr',id_p7)
    elif region == 'kr':
        rankp7 = lol_watcher.league.by_summoner('kr',id_p7)
    elif region == 'BR':
        rankp7 = lol_watcher.league.by_summoner('br1',id_p7)
    elif region == 'br':
        rankp7 = lol_watcher.league.by_summoner('br1',id_p7)
    elif region == 'LAN':
        rankp7 = lol_watcher.league.by_summoner('la1',id_p7)
    elif region == 'lan':
        rankp7 = lol_watcher.league.by_summoner('la1',id_p7)
    elif region == 'LAS':
        rankp7 = lol_watcher.league.by_summoner('la2',id_p7)
    elif region == 'las':
        rankp7 = lol_watcher.league.by_summoner('la2',id_p7)
    elif region == 'JP':
        rankp7 = lol_watcher.league.by_summoner('jp1',id_p7)
    elif region == 'jp':
        rankp7 = lol_watcher.league.by_summoner('jp1',id_p7)
    elif region == 'RU':
        rankp7 = lol_watcher.league.by_summoner('ru',id_p7)
    elif region == 'ru':
        rankp7 = lol_watcher.league.by_summoner('ru',id_p7)


    for i in range(len(rankp7)):
        if rankp7[i]['queueType'] == 'RANKED_FLEX_SR':
            del rankp7[i]
            break

    if rankp7 == []:
        tier7 = '<:unranked:817365350969769994> Unranked'
    else: tier7 = rankp7[0]['tier']

    if rankp7 == []:
        rank7 = '\u200B'
    else: rank7 = rankp7[0]['rank']

    if rankp7 == []:
        wins7 = 1
    else: wins7 = rankp7[0]['wins']

    if rankp7 == []:
        lose7 = 0
    else: lose7 = rankp7[0]['losses']

    if rankp7 == []:
        lp7 = '0'
    else: lp7 = rankp7[0]['leaguePoints']

    #tiers kai ranks pros allagh
    if tier7 == 'IRON':
        tier7 = '<:iron:817360753173463060> Iron'
    elif tier7 == 'BRONZE':
        tier7 = '<:bronze:817361809295671326> Bronze'
    elif tier7 == 'SILVER':
        tier7 = '<:silver:817361823312773141> Silver'
    elif tier7 == 'GOLD':
        tier7 = '<:gold:817361901339148318> Gold'
    elif tier7 == 'PLATINUM':
        tier7 = '<:platinum:817361924857659444> Platinum'
    elif tier7 == 'DIAMOND':
        tier7 = '<:diamond:817361937913872404> Diamond'
    elif tier7 == 'MASTER':
        tier7 = '<:master:817361953269088276> Master'
    elif tier7 == 'GRANDMASTER':
        tier7 = '<:grandmaster:817361970243043341> GrandMaster'
    elif tier7 == 'CHALLENGER':
        tier7 = '<:challenger:817361981513400320> Challenger'

    if rank7 == 'IV':
        rank7 = '4'
    elif rank7 == 'III':
        rank7 = '3'
    elif rank7 == 'II':
        rank7 = '2'
    elif rank7 == 'I':
        rank7 = '1'
    #tiers kai ranks pros allagh
    

    
    games7 = wins7 + lose7
    workwr7 = wins7 * 100
    wr7 = workwr7//games7

    runesp7 = p[6]['perks']
    rp7 = runesp7['perkStyle']
    rs7 = runesp7['perkSubStyle']

    if rp7 == 8000:
        rp7 = '<:precision:818050788118233089>'
    elif rp7 == 8100:
        rp7 = '<:domination:818050737589846026>'
    elif rp7 == 8200:
        rp7 = '<:sorcery:818050843143700502>'
    elif rp7 == 8300:
        rp7 = '<:inspiration:818050767642558464>'
    elif rp7 == 8400:
        rp7 = '<:resolve:818050828333613076>'

    if rs7 == 8000:
        rs7 = '<:precision:818050788118233089>'
    elif rs7 == 8100:
        rs7 = '<:domination:818050737589846026>'
    elif rs7 == 8200:
        rs7 = '<:sorcery:818050843143700502>'
    elif rs7 == 8300:
        rs7 = '<:inspiration:818050767642558464>'
    elif rs7 == 8400:
        rs7 = '<:resolve:818050828333613076>'

    #rank gia p8
    p8 = p[7]['summonerName']
    id_p8 = p[7]['summonerId']
    p8champion = p[7]['championId']
    if region == 'eune':
        rankp8 = lol_watcher.league.by_summoner('eun1',id_p8)
    elif region == 'EUNE':
        rankp8 = lol_watcher.league.by_summoner('eun1',id_p8)
    elif region == 'euw':
        rankp8 = lol_watcher.league.by_summoner('euw1',id_p8)
    elif region == 'EUW':
        rankp8 = lol_watcher.league.by_summoner('euw1',id_p8)
    elif region == 'na':
        rankp8 = lol_watcher.league.by_summoner('na1',id_p8)
    elif region == 'NA':
        rankp8 = lol_watcher.league.by_summoner('na1',id_p8)
    elif region == 'KR':
        rankp8 = lol_watcher.league.by_summoner('kr',id_p8)
    elif region == 'kr':
        rankp8 = lol_watcher.league.by_summoner('kr',id_p8)
    elif region == 'BR':
        rankp8 = lol_watcher.league.by_summoner('br1',id_p8)
    elif region == 'br':
        rankp8 = lol_watcher.league.by_summoner('br1',id_p8)
    elif region == 'LAN':
        rankp8 = lol_watcher.league.by_summoner('la1',id_p8)
    elif region == 'lan':
        rankp8 = lol_watcher.league.by_summoner('la1',id_p8)
    elif region == 'LAS':
        rankp8 = lol_watcher.league.by_summoner('la2',id_p8)
    elif region == 'las':
        rankp8 = lol_watcher.league.by_summoner('la2',id_p8)
    elif region == 'JP':
        rankp8 = lol_watcher.league.by_summoner('jp1',id_p8)
    elif region == 'jp':
        rankp8 = lol_watcher.league.by_summoner('jp1',id_p8)
    elif region == 'RU':
        rankp8 = lol_watcher.league.by_summoner('ru',id_p8)
    elif region == 'ru':
        rankp8 = lol_watcher.league.by_summoner('ru',id_p8)


    for i in range(len(rankp8)):
        if rankp8[i]['queueType'] == 'RANKED_FLEX_SR':
            del rankp8[i]
            break

    if rankp8 == []:
        tier8 = '<:unranked:817365350969769994> Unranked'
    else: tier8 = rankp8[0]['tier']

    if rankp8 == []:
        rank8 = '\u200B'
    else: rank8 = rankp8[0]['rank']

    if rankp8 == []:
        wins8 = 1
    else: wins8 = rankp8[0]['wins']

    if rankp8 == []:
        lose8 = 0
    else: lose8 = rankp8[0]['losses']

    if rankp8 == []:
        lp8 = '0'
    else: lp8 = rankp8[0]['leaguePoints']

    #tiers kai ranks pros allagh
    if tier8 == 'IRON':
        tier8 = '<:iron:817360753173463060> Iron'
    elif tier8 == 'BRONZE':
        tier8 = '<:bronze:817361809295671326> Bronze'
    elif tier8 == 'SILVER':
        tier8 = '<:silver:817361823312773141> Silver'
    elif tier8 == 'GOLD':
        tier8 = '<:gold:817361901339148318> Gold'
    elif tier8 == 'PLATINUM':
        tier8 = '<:platinum:817361924857659444> Platinum'
    elif tier8 == 'DIAMOND':
        tier8 = '<:diamond:817361937913872404> Diamond'
    elif tier8 == 'MASTER':
        tier8 = '<:master:817361953269088276> Master'
    elif tier8 == 'GRANDMASTER':
        tier8 = '<:grandmaster:817361970243043341> GrandMaster'
    elif tier8 == 'CHALLENGER':
        tier8 = '<:challenger:817361981513400320> Challenger'

    if rank8 == 'IV':
        rank8 = '4'
    elif rank8 == 'III':
        rank8 = '3'
    elif rank8 == 'II':
        rank8 = '2'
    elif rank8 == 'I':
        rank8 = '1'
    #tiers kai ranks pros allagh
    

    
    games8 = wins8 + lose8
    workwr8 = wins8 * 100
    wr8 = workwr8//games8
    
    runesp8 = p[7]['perks']
    rp8 = runesp8['perkStyle']
    rs8 = runesp8['perkSubStyle']

    if rp8 == 8000:
        rp8 = '<:precision:818050788118233089>'
    elif rp8 == 8100:
        rp8 = '<:domination:818050737589846026>'
    elif rp8 == 8200:
        rp8 = '<:sorcery:818050843143700502>'
    elif rp8 == 8300:
        rp8 = '<:inspiration:818050767642558464>'
    elif rp8 == 8400:
        rp8 = '<:resolve:818050828333613076>'

    if rs8 == 8000:
        rs8 = '<:precision:818050788118233089>'
    elif rs8 == 8100:
        rs8 = '<:domination:818050737589846026>'
    elif rs8 == 8200:
        rs8 = '<:sorcery:818050843143700502>'
    elif rs8 == 8300:
        rs8 = '<:inspiration:818050767642558464>'
    elif rs8 == 8400:
        rs8 = '<:resolve:818050828333613076>'

    p9 = p[8]['summonerName']
    id_p9 = p[8]['summonerId']
    p9champion = p[8]['championId']
    if region == 'eune':
        rankp9 = lol_watcher.league.by_summoner('eun1',id_p9)
    elif region == 'EUNE':
        rankp9 = lol_watcher.league.by_summoner('eun1',id_p9)
    elif region == 'euw':
        rankp9 = lol_watcher.league.by_summoner('euw1',id_p9)
    elif region == 'EUW':
        rankp9 = lol_watcher.league.by_summoner('euw1',id_p9)
    elif region == 'na':
        rankp9 = lol_watcher.league.by_summoner('na1',id_p9)
    elif region == 'NA':
        rankp9 = lol_watcher.league.by_summoner('na1',id_p9)
    elif region == 'KR':
        rankp9 = lol_watcher.league.by_summoner('kr',id_p9)
    elif region == 'kr':
        rankp9 = lol_watcher.league.by_summoner('kr',id_p9)
    elif region == 'BR':
        rankp9 = lol_watcher.league.by_summoner('br1',id_p9)
    elif region == 'br':
        rankp9 = lol_watcher.league.by_summoner('br1',id_p9)
    elif region == 'LAN':
        rankp9 = lol_watcher.league.by_summoner('la1',id_p9)
    elif region == 'lan':
        rankp9 = lol_watcher.league.by_summoner('la1',id_p9)
    elif region == 'LAS':
        rankp9 = lol_watcher.league.by_summoner('la2',id_p9)
    elif region == 'las':
        rankp9 = lol_watcher.league.by_summoner('la2',id_p9)
    elif region == 'JP':
        rankp9 = lol_watcher.league.by_summoner('jp1',id_p9)
    elif region == 'jp':
        rankp9 = lol_watcher.league.by_summoner('jp1',id_p9)
    elif region == 'RU':
        rankp9 = lol_watcher.league.by_summoner('ru',id_p9)
    elif region == 'ru':
        rankp9 = lol_watcher.league.by_summoner('ru',id_p9)


    for i in range(len(rankp9)):
        if rankp9[i]['queueType'] == 'RANKED_FLEX_SR':
            del rankp9[i]
            break

    if rankp9 == []:
        tier9 = '<:unranked:817365350969769994> Unranked'
    else: tier9 = rankp9[0]['tier']

    if rankp9 == []:
        rank9 = '\u200B'
    else: rank9 = rankp9[0]['rank']

    if rankp9 == []:
        wins9 = 1
    else: wins9 = rankp9[0]['wins']

    if rankp9 == []:
        lose9 = 0
    else: lose9 = rankp9[0]['losses']

    if rankp9 == []:
        lp9 = '0'
    else: lp9 = rankp9[0]['leaguePoints']

    #tiers kai ranks pros allagh
    if tier9 == 'IRON':
        tier9 = '<:iron:817360753173463060> Iron'
    elif tier9 == 'BRONZE':
        tier9 = '<:bronze:817361809295671326> Bronze'
    elif tier9 == 'SILVER':
        tier9 = '<:silver:817361823312773141> Silver'
    elif tier9 == 'GOLD':
        tier9 = '<:gold:817361901339148318> Gold'
    elif tier9 == 'PLATINUM':
        tier9 = '<:platinum:817361924857659444> Platinum'
    elif tier9 == 'DIAMOND':
        tier9 = '<:diamond:817361937913872404> Diamond'
    elif tier9 == 'MASTER':
        tier9 = '<:master:817361953269088276> Master'
    elif tier9 == 'GRANDMASTER':
        tier9 = '<:grandmaster:817361970243043341> GrandMaster'
    elif tier9 == 'CHALLENGER':
        tier9 = '<:challenger:817361981513400320> Challenger'

    if rank9 == 'IV':
        rank9 = '4'
    elif rank9 == 'III':
        rank9 = '3'
    elif rank9 == 'II':
        rank9 = '2'
    elif rank9 == 'I':
        rank9 = '1'
    #tiers kai ranks pros allagh
    

    
    games9 = wins9 + lose9
    workwr9 = wins9 * 100
    wr9 = workwr9//games9

    runesp9 = p[8]['perks']
    rp9 = runesp9['perkStyle']
    rs9 = runesp9['perkSubStyle']

    if rp9 == 8000:
        rp9 = '<:precision:818050788118233089>'
    elif rp9 == 8100:
        rp9 = '<:domination:818050737589846026>'
    elif rp9 == 8200:
        rp9 = '<:sorcery:818050843143700502>'
    elif rp9 == 8300:
        rp9 = '<:inspiration:818050767642558464>'
    elif rp9 == 8400:
        rp9 = '<:resolve:818050828333613076>'

    if rs9 == 8000:
        rs9 = '<:precision:818050788118233089>'
    elif rs9 == 8100:
        rs9 = '<:domination:818050737589846026>'
    elif rs9 == 8200:
        rs9 = '<:sorcery:818050843143700502>'
    elif rs9 == 8300:
        rs9 = '<:inspiration:818050767642558464>'
    elif rs9 == 8400:
        rs9 = '<:resolve:818050828333613076>'

    p10 = p[9]['summonerName']
    id_p10 = p[9]['summonerId']
    p10champion = p[9]['championId']
    if region == 'eune':
        rankp10 = lol_watcher.league.by_summoner('eun1',id_p10)
    elif region == 'EUNE':
        rankp10 = lol_watcher.league.by_summoner('eun1',id_p10)
    elif region == 'euw':
        rankp10 = lol_watcher.league.by_summoner('euw1',id_p10)
    elif region == 'EUW':
        rankp10 = lol_watcher.league.by_summoner('euw1',id_p10)
    elif region == 'na':
        rankp10 = lol_watcher.league.by_summoner('na1',id_p10)
    elif region == 'NA':
        rankp10 = lol_watcher.league.by_summoner('na1',id_p10)
    elif region == 'KR':
        rankp10 = lol_watcher.league.by_summoner('kr',id_p10)
    elif region == 'kr':
        rankp10 = lol_watcher.league.by_summoner('kr',id_p10)
    elif region == 'BR':
        rankp10 = lol_watcher.league.by_summoner('br1',id_p10)
    elif region == 'br':
        rankp10 = lol_watcher.league.by_summoner('br1',id_p10)
    elif region == 'LAN':
        rankp10 = lol_watcher.league.by_summoner('la1',id_p10)
    elif region == 'lan':
        rankp10 = lol_watcher.league.by_summoner('la1',id_p10)
    elif region == 'LAS':
        rankp10 = lol_watcher.league.by_summoner('la2',id_p10)
    elif region == 'las':
        rankp10 = lol_watcher.league.by_summoner('la2',id_p10)
    elif region == 'JP':
        rankp10 = lol_watcher.league.by_summoner('jp1',id_p10)
    elif region == 'jp':
        rankp10 = lol_watcher.league.by_summoner('jp1',id_p10)
    elif region == 'RU':
        rankp10 = lol_watcher.league.by_summoner('ru',id_p10)
    elif region == 'ru':
        rankp10 = lol_watcher.league.by_summoner('ru',id_p10)


    for i in range(len(rankp10)):
        if rankp10[i]['queueType'] == 'RANKED_FLEX_SR':
            del rankp10[i]
            break

    if rankp10 == []:
        tier10 = '<:unranked:817365350969769994> Unranked'
    else: tier10 = rankp10[0]['tier']


    if rankp10 == []:
        rank10 = '\u200B'
    else: rank10 = rankp10[0]['rank']

    if rankp10 == []:
        wins10 = 1
    else: wins10 = rankp10[0]['wins']

    if rankp10 == []:
        lose10 = 0
    else: lose10 = rankp10[0]['losses']

    if rankp10 == []:
        lp10 = '0'
    else: lp10 = rankp10[0]['leaguePoints']

    #tiers kai rank pros allagh
    if tier10 == 'IRON':
        tier10 = '<:iron:817360753173463060> Iron'
    elif tier10 == 'BRONZE':
        tier10 = '<:bronze:817361809295671326> Bronze'
    elif tier10 == 'SILVER':
        tier10 = '<:silver:817361823312773141> Silver'
    elif tier10 == 'GOLD':
        tier10 = '<:gold:817361901339148318> Gold'
    elif tier10 == 'PLATINUM':
        tier10 = '<:platinum:817361924857659444> Platinum'
    elif tier10 == 'DIAMOND':
        tier10 = '<:diamond:817361937913872404> Diamond'
    elif tier10 == 'MASTER':
        tier10 = '<:master:817361953269088276> Master'
    elif tier10 == 'GRANDMASTER':
        tier10 = '<:grandmaster:817361970243043341> GrandMaster'
    elif tier10 == 'CHALLENGER':
        tier10 = '<:challenger:817361981513400320> Challenger'

    if rank10 == 'IV':
        rank10 = '4'
    elif rank10 == 'III':
        rank10 = '3'
    elif rank10 == 'II':
        rank10 = '2'
    elif rank10 == 'I':
        rank10 = '1'
    #tiers kai rank pros allagh
    
    games10 = wins10 + lose10
    workwr10 = wins10 * 100
    wr10 = workwr10//games10

    runesp10 = p[9]['perks']
    rp10 = runesp10['perkStyle']
    rs10 = runesp10['perkSubStyle']

    if rp10 == 8000:
        rp10 = '<:precision:818050788118233089>'
    elif rp10 == 8100:
        rp10 = '<:domination:818050737589846026>'
    elif rp10 == 8200:
        rp10 = '<:sorcery:818050843143700502>'
    elif rp10 == 8300:
        rp10 = '<:inspiration:818050767642558464>'
    elif rp10 == 8400:
        rp10 = '<:resolve:818050828333613076>'

    if rs10 == 8000:
        rs10 = '<:precision:818050788118233089>'
    elif rs10 == 8100:
        rs10 = '<:domination:818050737589846026>'
    elif rs10 == 8200:
        rs10 = '<:sorcery:818050843143700502>'
    elif rs10 == 8300:
        rs10 = '<:inspiration:818050767642558464>'
    elif rs10 == 8400:
        rs10 = '<:resolve:818050828333613076>'



    #await waitmessage.delete()

    #WORK_IN_ALPHA
    if match['gameQueueConfigId'] == 420:
        gamemode = "**Summoner's Rift** : __Ranked Solo/Duo__"
    elif match['gameQueueConfigId'] == 440:
        gamemode = "**Summoner's Rift** : __Ranked Flex__ (Flex ranks are not ready yet)"
    elif match['gameQueueConfigId'] == 400:
        gamemode = "**Summoner's Rift** : __Normal Draft Pick__"
    elif match['gameQueueConfigId'] == 450:
        gamemode = "**Howling Abyss** : __ARAM__"
    elif match['gameQueueConfigId'] == 430:
        gamemode = "**Summoner's Rift** : __Normal Blind Pick__"
    else: gamemode = "**Summoner's Rift** : __Featured Game Mode__"    
    #WORK_IN_ALPHA

    ban = match['bannedChampions']
    ban1 = ban[0]['championId']
    ban2 = ban[1]['championId']
    ban3 = ban[2]['championId']
    ban4 = ban[3]['championId']
    ban5 = ban[4]['championId']
    ban6 = ban[5]['championId']
    ban7 = ban[6]['championId']
    ban8 = ban[7]['championId']
    ban9 = ban[8]['championId']
    ban10 = ban[9]['championId']

    arg = arg.replace(" ", "%20")

    embed=discord.Embed(title="<:eloicon:820974785168801802> Live Match <:liveicon:817500041107079249>", description=f"{gamemode} | __{Time}__ | [Spectate](https://lolspectator.tv/spectate?summoner="+arg+"&server="+region+")",color=discord.Color.purple())

    #BLUE TEAM
    embed.add_field(name = '**Blue Team <:blueteam:817370233211453460>**', value =f"**{rp1}{rs1} {p1} - **__{findChampionName(p1champion)}__ \n **{rp2}{rs2} {p2} - **__{findChampionName(p2champion)}__ \n **{rp3}{rs3} {p3} - **__{findChampionName(p3champion)}__ \n **{rp4}{rs4} {p4} - **__{findChampionName(p4champion)}__ \n **{rp5}{rs5} {p5} - **__{findChampionName(p5champion)}__", inline = True)
    embed.add_field(name = '**Rank <:rankblue:817495010089500702>**',value =f"{tier1} {rank1} ({lp1} LP) \n {tier2} {rank2} ({lp2} LP) \n {tier3} {rank3} ({lp3} LP) \n {tier4} {rank4} ({lp4} LP) \n {tier5} {rank5} ({lp5} LP)",inline = True)
    embed.add_field(name = '**Winrate <:wrlogoblue:817497953580744754>**',value =f"**{wr1}%** {games1}G \n **{wr2}%** {games2}G \n **{wr3}%** {games3}G \n **{wr4}%** {games4}G \n **{wr5}%** {games5}G",inline = True)


    #RED TEAM
    embed.add_field(name = '**Red Team <:redteam:817370254337769492>**', value =f"**{rp6}{rs6} {p6} - **__{findChampionName(p6champion)}__ \n **{rp7}{rs7} {p7} - **__{findChampionName(p7champion)}__ \n **{rp8}{rs8} {p8} - **__{findChampionName(p8champion)}__ \n **{rp9}{rs9} {p9} - **__{findChampionName(p9champion)}__ \n **{rp10}{rs10} {p10} - **__{findChampionName(p10champion)}__", inline = True)
    embed.add_field(name = '**Rank <:rankred:817495027608977499>**',value =f"{tier6} {rank6} ({lp6} LP) \n {tier7} {rank7} ({lp7} LP) \n {tier8} {rank8} ({lp8} LP) \n {tier9} {rank9} ({lp9} LP) \n {tier10} {rank10} ({lp10} LP)",inline = True)
    embed.add_field(name = '**Winrate <:wrlogored:817498416837165077>**',value =f"**{wr6}%** {games6}G \n **{wr7}%** {games7}G \n **{wr8}%** {games8}G \n **{wr9}%** {games9}G \n **{wr10}%** {games10}G",inline = True)
    embed.add_field(name = '**Bans <:banicon:819493635115843614>**', value = f'<:blueteam:817370233211453460> {findChampionName(ban1)} | {findChampionName(ban2)} | {findChampionName(ban3)} | {findChampionName(ban4)} | {findChampionName(ban5)} \n <:redteam:817370254337769492> {findChampionName(ban6)} | {findChampionName(ban7)} | {findChampionName(ban8)} | {findChampionName(ban9)} | {findChampionName(ban10)}')
    embed.set_footer(text = 'Predict the winner with the reactions below!')

    await waitmessage.delete()

    sent = await ctx.send(embed=embed)
    await sent.add_reaction(emoji = '<:blueteam:817370233211453460>')
    await sent.add_reaction(emoji = '<:redteam:817370254337769492>')


@live.error
async def live_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.CommandInvokeError):
        embed=discord.Embed(title=':warning: Live Command', description = '**This summoner is not in an active game!**', color = discord.Color.gold())
        embed.set_thumbnail(url = 'https://cdn.discordapp.com/attachments/802967377159389317/819155421108371467/poroerror.png')
        await ctx.send(embed=embed)
    elif isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        embed=discord.Embed(title=':warning: Live Command', description = '__Wrong Use!__', color = discord.Color.gold())
        embed.add_field(name = 'Use:', value = '!e live (region) (summoner name)', inline = False)
        embed.add_field(name = 'Available Regions:', value = 'eune, euw, na, kr, br, lan, las, jp, ru', inline = False)
        embed.set_thumbnail(url = 'https://cdn.discordapp.com/attachments/802967377159389317/819155421108371467/poroerror.png')
        await ctx.send(embed=embed)

@client.command()
async def freechampions(ctx):
    free = lol_watcher.champion.rotations('na1')
    c = free['freeChampionIds']
    c1 = c[0]
    c2 = c[1]
    c3 = c[2]
    c4 = c[3]
    c5 = c[4]
    c6 = c[5]
    c7 = c[6]
    c8 = c[7]
    c9 = c[8]
    c10 = c[9]
    c11 = c[10]
    c12 = c[11]
    c13 = c[12]
    c14 = c[13]
    c15 = c[14]

    embed=discord.Embed(title='<:eloicon:820974785168801802> Free Champion Rotations', description = '', color = discord.Color.purple())
    embed.add_field(name = 'Champions <:elocheck:820980129383055381>',value =f'{findChampionName(c1)} | {findChampionName(c2)} | {findChampionName(c3)} \n {findChampionName(c4)} | {findChampionName(c5)} | {findChampionName(c6)} \n {findChampionName(c7)} | {findChampionName(c8)} | {findChampionName(c9)} \n {findChampionName(c10)} | {findChampionName(c11)} | {findChampionName(c12)} \n {findChampionName(c13)} | {findChampionName(c14)} | {findChampionName(c15)}')
    embed.add_field(name = 'Schedule <:elocheck:820980129383055381>', value =f'15 champions are available for free play. \n New champions are added to the \n free champion rotation on the third \n week of their release.',inline = False)
    embed.set_thumbnail(url = 'https://cdn.discordapp.com/attachments/802967377159389317/820995271034929162/championsrots.png')
    await ctx.send(embed=embed)

#same commands
@client.command()
async def elo(ctx):
        embed = discord.Embed(title ='Follow us!',description = 'The new way to play!', color = discord.Color.purple())
        embed.add_field(name="Information:" ,value = f'**<:website:821128800153632830> Website:** [**elogg.github.io**](https://northstudios.github.io/elo.gg/) \n **<:developer:821128800514473994> Developer:** North Studios \n **<:support:821133106735480862> Support:** Work in progress \n **<:server:821128800427180102> Servers:** {str(len(client.guilds))} \n **<:youtube:821434540718292993> Youtube:** [North Studios](https://www.youtube.com/channel/UCBOXvGgeS5nLAsHO731JEIA) \n**<:reportbug:821291929224085514> Report Bugs:** northstudiosdev@gmail.com',inline = True)
        embed.add_field(name="\u200B", value = "\u200B", inline = True)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/802967377159389318/821089628974874624/cartoonizeelo.png")
        await ctx.send(embed=embed)
@client.command()
async def e(ctx):
        embed = discord.Embed(title ='Follow us!',description = 'The new way to play!', color = discord.Color.purple())
        embed.add_field(name="Information:" ,value = f'**<:website:821128800153632830> Website:** [**elogg.github.io**](https://northstudios.github.io/elo.gg/) \n **<:developer:821128800514473994> Developer:** North Studios \n **<:support:821133106735480862> Support:** Work in progress \n **<:server:821128800427180102> Servers:** {str(len(client.guilds))} \n **<:youtube:821434540718292993> Youtube:** [North Studios](https://www.youtube.com/channel/UCBOXvGgeS5nLAsHO731JEIA) \n**<:reportbug:821291929224085514> Report Bugs:** northstudiosdev@gmail.com',inline = True)
        embed.add_field(name="\u200B", value = "\u200B", inline = True)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/802967377159389318/821089628974874624/cartoonizeelo.png")
        await ctx.send(embed=embed)
#same commands ta e-elo

@client.command()
async def prefix(ctx):
        embed = discord.Embed(title ='Elo Prefixes',description = '**You can use these prefixes:** \n !e \n !E \n !elo \n !Elo \n !ELO \n !e[space] \n !E[space] \n !elo[space] \n !Elo[space] \n !ELO[space]', color = discord.Color.purple())
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/802967377159389318/821089628974874624/cartoonizeelo.png")
        await ctx.send(embed=embed)

############################################################################################################################################################################################################################
############################################################################################################################################################################################################################
@client.command()
async def match(ctx, region, *, arg):
    waitingmessage = await ctx.send(f":red_circle: Please wait while we are fetching data for {arg}'s match history...")
    if region == 'eune':
        ign = lol_watcher.summoner.by_name('eun1', arg)
        matchlist = lol_watcher.match.matchlist_by_account('eun1', ign['accountId'])

        
    elif region == 'EUNE':
        ign = lol_watcher.summoner.by_name('eun1', arg)
        matchlist = lol_watcher.match.matchlist_by_account('eun1', ign['accountId'])
        
    elif region == 'euw':
        ign = lol_watcher.summoner.by_name('euw1', arg)
        matchlist = lol_watcher.match.matchlist_by_account('euw1', ign['accountId'])
        
    elif region == 'EUW':
        ign = lol_watcher.summoner.by_name('euw1', arg)
        matchlist = lol_watcher.match.matchlist_by_account('euw1', ign['accountId'])
        
    elif region == 'na':
        ign = lol_watcher.summoner.by_name('na1', arg)
        matchlist = lol_watcher.match.matchlist_by_account('na1', ign['accountId'])
        
    elif region == 'NA':
        ign = lol_watcher.summoner.by_name('na1', arg)
        matchlist = lol_watcher.match.matchlist_by_account('na1', ign['accountId'])
        
    elif region == 'kr':
        matchlist = lol_watcher.match.matchlist_by_account('kr', ign['accountId'])
        
    elif region == 'KR':
        ign = lol_watcher.summoner.by_name('kr', arg)
        matchlist = lol_watcher.match.matchlist_by_account('kr', ign['accountId'])

    elif region == 'br':
        ign = lol_watcher.summoner.by_name('br1', arg)
        matchlist = lol_watcher.match.matchlist_by_account('br1', ign['accountId'])

    elif region == 'BR':
        ign = lol_watcher.summoner.by_name('br1', arg)
        matchlist = lol_watcher.match.matchlist_by_account('br1', ign['accountId'])

    elif region == 'lan':
        ign = lol_watcher.summoner.by_name('la1', arg)
        matchlist = lol_watcher.match.matchlist_by_account('la1', ign['accountId'])

    elif region == 'LAN':
        ign = lol_watcher.summoner.by_name('la1', arg)
        matchlist = lol_watcher.match.matchlist_by_account('la1', ign['accountId'])

    elif region == 'las':
        ign = lol_watcher.summoner.by_name('la2', arg)
        matchlist = lol_watcher.match.matchlist_by_account('la2', ign['accountId'])

    elif region == 'LAS':
        ign = lol_watcher.summoner.by_name('la2', arg)
        matchlist = lol_watcher.match.matchlist_by_account('la2', ign['accountId'])

    elif region == 'jp':
        ign = lol_watcher.summoner.by_name('jp1', arg)
        matchlist = lol_watcher.match.matchlist_by_account('jp1', ign['accountId'])

    elif region == 'JP':
        ign = lol_watcher.summoner.by_name('jp1', arg)
        matchlist = lol_watcher.match.matchlist_by_account('jp1', ign['accountId'])

    elif region == 'ru':
        ign = lol_watcher.summoner.by_name('r', arg)
        matchlist = lol_watcher.match.matchlist_by_account('ru', ign['accountId'])

    elif region == 'RU':
        ign = lol_watcher.summoner.by_name('ru', arg)
        matchlist = lol_watcher.match.matchlist_by_account('ru', ign['accountId'])

    findmatches = matchlist['matches'][0]
    latestMatch = findmatches['gameId']

    if region == 'eune':
        recentMatch = lol_watcher.match.by_id('eun1',latestMatch)
    elif region == 'EUNE':
        recentMatch = lol_watcher.match.by_id('eun1',latestMatch)
    elif region == 'euw':
        recentMatch = lol_watcher.match.by_id('euw1',latestMatch)
    elif region == 'EUW':
        recentMatch = lol_watcher.match.by_id('euw1',latestMatch)
    elif region == 'na':
        recentMatch = lol_watcher.match.by_id('na1',latestMatch)
    elif region == 'NA':
        recentMatch = lol_watcher.match.by_id('na1',latestMatch)
    elif region == 'kr':
        recentMatch = lol_watcher.match.by_id('kr',latestMatch)
    elif region == 'KR':
        recentMatch = lol_watcher.match.by_id('kr',latestMatch)
    elif region == 'br':
        recentMatch = lol_watcher.match.by_id('br1',latestMatch)
    elif region == 'BR':
        recentMatch = lol_watcher.match.by_id('br1',latestMatch)
    elif region == 'lan':
        recentMatch = lol_watcher.match.by_id('la1',latestMatch)
    elif region == 'LAN':
        recentMatch = lol_watcher.match.by_id('la1',latestMatch)
    elif region == 'las':
        recentMatch = lol_watcher.match.by_id('la2',latestMatch)
    elif region == 'LAS':
        recentMatch = lol_watcher.match.by_id('la2',latestMatch)
    elif region == 'jp':
        recentMatch = lol_watcher.match.by_id('jp1',latestMatch)
    elif region == 'JP':
        recentMatch = lol_watcher.match.by_id('jp1',latestMatch)
    elif region == 'ru':
        recentMatch = lol_watcher.match.by_id('ru',latestMatch)
    elif region == 'RU':
        recentMatch = lol_watcher.match.by_id('ru',latestMatch)

    participants = recentMatch['participants'][0]

    team1 = recentMatch['teams'][0]
    team1win = team1['win']
    if team1win == 'Win':
        team1win = 'Victory'
    elif team1win == 'Fail':
        team1win = 'Defeat'
        
    team2 = recentMatch['teams'][1]
    team2win = team2['win']
    if team2win == 'Win':
        team2win = 'Victory'
    elif team2win == 'Fail':
        team2win = 'Defeat'

    #player 1
    player1name = recentMatch['participantIdentities'][0]['player']['summonerName']
    player1champion = recentMatch['participants'][0]['championId']
    player1deaths = recentMatch['participants'][0]['stats']['deaths']
    player1kills = recentMatch['participants'][0]['stats']['kills']
    player1assists = recentMatch['participants'][0]['stats']['assists']
    player1deal = recentMatch['participants'][0]['stats']['totalDamageDealtToChampions']
    player1primaryrunes= recentMatch['participants'][0]['stats']['perkPrimaryStyle']
    player1subrunes= recentMatch['participants'][0]['stats']['perkSubStyle']
    player1minions = recentMatch['participants'][0]['stats']['totalMinionsKilled']
    player1camps = recentMatch['participants'][0]['stats']['neutralMinionsKilled']
    player1level = recentMatch['participants'][0]['stats']['champLevel']
    player1cs = player1minions + player1camps
    #Primary runes
    if player1primaryrunes == 8000:
        player1primaryrunes = '<:precision:818050788118233089>'
    elif player1primaryrunes == 8100:
        player1primaryrunes = '<:domination:818050737589846026>'
    elif player1primaryrunes == 8200:
        player1primaryrunes = '<:sorcery:818050843143700502>'
    elif player1primaryrunes == 8300:
        player1primaryrunes = '<:inspiration:818050767642558464>'
    elif player1primaryrunes == 8400:
        player1primaryrunes = '<:resolve:818050828333613076>'
    #Sub runes
    if player1subrunes == 8000:
        player1subrunes = '<:precision:818050788118233089>'
    elif player1subrunes == 8100:
        player1subrunes = '<:domination:818050737589846026>'
    elif player1subrunes == 8200:
        player1subrunes = '<:sorcery:818050843143700502>'
    elif player1subrunes == 8300:
        player1subrunes = '<:inspiration:818050767642558464>'
    elif player1subrunes == 8400:
        player1subrunes = '<:resolve:818050828333613076>'

#player 2
    player2name = recentMatch['participantIdentities'][1]['player']['summonerName']
    player2champion = recentMatch['participants'][1]['championId']
    player2deaths = recentMatch['participants'][1]['stats']['deaths']
    player2kills = recentMatch['participants'][1]['stats']['kills']
    player2assists = recentMatch['participants'][1]['stats']['assists']
    player2deal = recentMatch['participants'][1]['stats']['totalDamageDealtToChampions']
    player2primaryrunes= recentMatch['participants'][1]['stats']['perkPrimaryStyle']
    player2subrunes= recentMatch['participants'][1]['stats']['perkSubStyle']
    player2minions = recentMatch['participants'][1]['stats']['totalMinionsKilled']
    player2camps = recentMatch['participants'][1]['stats']['neutralMinionsKilled']
    player2level = recentMatch['participants'][1]['stats']['champLevel']
    player2cs = player2minions + player2camps
#Primary runes
    if player2primaryrunes == 8000:
        player2primaryrunes = '<:precision:818050788118233089>'
    elif player2primaryrunes == 8100:
        player2primaryrunes = '<:domination:818050737589846026>'
    elif player2primaryrunes == 8200:
        player2primaryrunes = '<:sorcery:818050843143700502>'
    elif player2primaryrunes == 8300:
        player2primaryrunes = '<:inspiration:818050767642558464>'
    elif player2primaryrunes == 8400:
        player2primaryrunes = '<:resolve:818050828333613076>'
#Sub runes
    if player2subrunes == 8000:
        player2subrunes = '<:precision:818050788118233089>'
    elif player2subrunes == 8100:
        player2subrunes = '<:domination:818050737589846026>'
    elif player2subrunes == 8200:
        player2subrunes = '<:sorcery:818050843143700502>'
    elif player2subrunes == 8300:
        player2subrunes = '<:inspiration:818050767642558464>'
    elif player2subrunes == 8400:
        player2subrunes = '<:resolve:818050828333613076>'


#player 3
    player3name = recentMatch['participantIdentities'][2]['player']['summonerName']
    player3champion = recentMatch['participants'][2]['championId']
    player3deaths = recentMatch['participants'][2]['stats']['deaths']
    player3kills = recentMatch['participants'][2]['stats']['kills']
    player3assists = recentMatch['participants'][2]['stats']['assists']
    player3deal = recentMatch['participants'][2]['stats']['totalDamageDealtToChampions']
    player3primaryrunes= recentMatch['participants'][2]['stats']['perkPrimaryStyle']
    player3subrunes= recentMatch['participants'][2]['stats']['perkSubStyle']
    player3minions = recentMatch['participants'][2]['stats']['totalMinionsKilled']
    player3camps = recentMatch['participants'][2]['stats']['neutralMinionsKilled']
    player3level = recentMatch['participants'][2]['stats']['champLevel']
    player3cs = player3minions + player3camps
    #Primary runes
    if player3primaryrunes == 8000:
        player3primaryrunes = '<:precision:818050788118233089>'
    elif player3primaryrunes == 8100:
        player3primaryrunes = '<:domination:818050737589846026>'
    elif player3primaryrunes == 8200:
        player3primaryrunes = '<:sorcery:818050843143700502>'
    elif player3primaryrunes == 8300:
        player3primaryrunes = '<:inspiration:818050767642558464>'
    elif player3primaryrunes == 8400:
        player3primaryrunes = '<:resolve:818050828333613076>'
    #Sub runes
    if player3subrunes == 8000:
        player3subrunes = '<:precision:818050788118233089>'
    elif player3subrunes == 8100:
        player3subrunes = '<:domination:818050737589846026>'
    elif player3subrunes == 8200:
        player3subrunes = '<:sorcery:818050843143700502>'
    elif player3subrunes == 8300:
        player3subrunes = '<:inspiration:818050767642558464>'
    elif player3subrunes == 8400:
        player3subrunes = '<:resolve:818050828333613076>'

#player 4
    player4name = recentMatch['participantIdentities'][3]['player']['summonerName']
    player4champion = recentMatch['participants'][3]['championId']
    player4deaths = recentMatch['participants'][3]['stats']['deaths']
    player4kills = recentMatch['participants'][3]['stats']['kills']
    player4assists = recentMatch['participants'][3]['stats']['assists']
    player4deal = recentMatch['participants'][3]['stats']['totalDamageDealtToChampions']
    player4primaryrunes= recentMatch['participants'][3]['stats']['perkPrimaryStyle']
    player4subrunes= recentMatch['participants'][3]['stats']['perkSubStyle']
    player4minions = recentMatch['participants'][3]['stats']['totalMinionsKilled']
    player4camps = recentMatch['participants'][3]['stats']['neutralMinionsKilled']
    player4level = recentMatch['participants'][3]['stats']['champLevel']
    player4cs = player4minions + player4camps
#Primary runes
    if player4primaryrunes == 8000:
        player4primaryrunes = '<:precision:818050788118233089>'
    elif player4primaryrunes == 8100:
        player4primaryrunes = '<:domination:818050737589846026>'
    elif player4primaryrunes == 8200:
        player4primaryrunes = '<:sorcery:818050843143700502>'
    elif player4primaryrunes == 8300:
        player4primaryrunes = '<:inspiration:818050767642558464>'
    elif player4primaryrunes == 8400:
        player4primaryrunes = '<:resolve:818050828333613076>'
#Sub runes
    if player4subrunes == 8000:
        player4subrunes = '<:precision:818050788118233089>'
    elif player4subrunes == 8100:
        player4subrunes = '<:domination:818050737589846026>'
    elif player4subrunes == 8200:
        player4subrunes = '<:sorcery:818050843143700502>'
    elif player4subrunes == 8300:
        player4subrunes = '<:inspiration:818050767642558464>'
    elif player4subrunes == 8400:
        player4subrunes = '<:resolve:818050828333613076>'

#player 5
    player5name = recentMatch['participantIdentities'][4]['player']['summonerName']
    player5champion = recentMatch['participants'][4]['championId']
    player5deaths = recentMatch['participants'][4]['stats']['deaths']
    player5kills = recentMatch['participants'][4]['stats']['kills']
    player5assists = recentMatch['participants'][4]['stats']['assists']
    player5deal = recentMatch['participants'][4]['stats']['totalDamageDealtToChampions']
    player5primaryrunes= recentMatch['participants'][4]['stats']['perkPrimaryStyle']
    player5subrunes= recentMatch['participants'][4]['stats']['perkSubStyle']
    player5minions = recentMatch['participants'][4]['stats']['totalMinionsKilled']
    player5camps = recentMatch['participants'][4]['stats']['neutralMinionsKilled']
    player5level = recentMatch['participants'][4]['stats']['champLevel']
    player5cs = player5minions + player5camps
#Primary runes
    if player5primaryrunes == 8000:
        player5primaryrunes = '<:precision:818050788118233089>'
    elif player5primaryrunes == 8100:
        player5primaryrunes = '<:domination:818050737589846026>'
    elif player5primaryrunes == 8200:
        player5primaryrunes = '<:sorcery:818050843143700502>'
    elif player5primaryrunes == 8300:
        player5primaryrunes = '<:inspiration:818050767642558464>'
    elif player5primaryrunes == 8400:
        player5primaryrunes = '<:resolve:818050828333613076>'
#Sub runes
    if player5subrunes == 8000:
        player5subrunes = '<:precision:818050788118233089>'
    elif player5subrunes == 8100:
        player5subrunes = '<:domination:818050737589846026>'
    elif player5subrunes == 8200:
        player5subrunes = '<:sorcery:818050843143700502>'
    elif player5subrunes == 8300:
        player5subrunes = '<:inspiration:818050767642558464>'
    elif player5subrunes == 8400:
        player5subrunes = '<:resolve:818050828333613076>'

#player 6
    player6name = recentMatch['participantIdentities'][5]['player']['summonerName']
    player6champion = recentMatch['participants'][5]['championId']
    player6deaths = recentMatch['participants'][5]['stats']['deaths']
    player6kills = recentMatch['participants'][5]['stats']['kills']
    player6assists = recentMatch['participants'][5]['stats']['assists']
    player6deal = recentMatch['participants'][5]['stats']['totalDamageDealtToChampions']
    player6primaryrunes= recentMatch['participants'][5]['stats']['perkPrimaryStyle']
    player6subrunes= recentMatch['participants'][5]['stats']['perkSubStyle']
    player6minions = recentMatch['participants'][5]['stats']['totalMinionsKilled']
    player6camps = recentMatch['participants'][5]['stats']['neutralMinionsKilled']
    player6level = recentMatch['participants'][5]['stats']['champLevel']
    player6cs = player6minions + player6camps
#Primary runes
    if player6primaryrunes == 8000:
        player6primaryrunes = '<:precision:818050788118233089>'
    elif player6primaryrunes == 8100:
        player6primaryrunes = '<:domination:818050737589846026>'
    elif player6primaryrunes == 8200:
        player6primaryrunes = '<:sorcery:818050843143700502>'
    elif player6primaryrunes == 8300:
        player6primaryrunes = '<:inspiration:818050767642558464>'
    elif player6primaryrunes == 8400:
        player6primaryrunes = '<:resolve:818050828333613076>'
    #Sub runes
    if player6subrunes == 8000:
        player6subrunes = '<:precision:818050788118233089>'
    elif player6subrunes == 8100:
        player6subrunes = '<:domination:818050737589846026>'
    elif player6subrunes == 8200:
        player6subrunes = '<:sorcery:818050843143700502>'
    elif player6subrunes == 8300:
        player6subrunes = '<:inspiration:818050767642558464>'
    elif player6subrunes == 8400:
        player6subrunes = '<:resolve:818050828333613076>'
    
#player 7
    player7name = recentMatch['participantIdentities'][6]['player']['summonerName']
    player7champion = recentMatch['participants'][6]['championId']
    player7deaths = recentMatch['participants'][6]['stats']['deaths']
    player7kills = recentMatch['participants'][6]['stats']['kills']
    player7assists = recentMatch['participants'][6]['stats']['assists']
    player7deal = recentMatch['participants'][6]['stats']['totalDamageDealtToChampions']
    player7primaryrunes= recentMatch['participants'][6]['stats']['perkPrimaryStyle']
    player7subrunes= recentMatch['participants'][6]['stats']['perkSubStyle']
    player7minions = recentMatch['participants'][6]['stats']['totalMinionsKilled']
    player7camps = recentMatch['participants'][6]['stats']['neutralMinionsKilled']
    player7level = recentMatch['participants'][6]['stats']['champLevel']
    player7cs = player7minions + player7camps
#Primary runes
    if player7primaryrunes == 8000:
        player7primaryrunes = '<:precision:818050788118233089>'
    elif player7primaryrunes == 8100:
        player7primaryrunes = '<:domination:818050737589846026>'
    elif player7primaryrunes == 8200:
        player7primaryrunes = '<:sorcery:818050843143700502>'
    elif player7primaryrunes == 8300:
        player7primaryrunes = '<:inspiration:818050767642558464>'
    elif player7primaryrunes == 8400:
        player7primaryrunes = '<:resolve:818050828333613076>'
#Sub runes
    if player7subrunes == 8000:
        player7subrunes = '<:precision:818050788118233089>'
    elif player7subrunes == 8100:
        player7subrunes = '<:domination:818050737589846026>'
    elif player7subrunes == 8200:
        player7subrunes = '<:sorcery:818050843143700502>'
    elif player7subrunes == 8300:
        player7subrunes = '<:inspiration:818050767642558464>'
    elif player7subrunes == 8400:
        player7subrunes = '<:resolve:818050828333613076>'

#player 8
    player8name = recentMatch['participantIdentities'][7]['player']['summonerName']
    player8champion = recentMatch['participants'][7]['championId']
    player8deaths = recentMatch['participants'][7]['stats']['deaths']
    player8kills = recentMatch['participants'][7]['stats']['kills']
    player8assists = recentMatch['participants'][7]['stats']['assists']
    player8deal = recentMatch['participants'][7]['stats']['totalDamageDealtToChampions']
    player8primaryrunes= recentMatch['participants'][7]['stats']['perkPrimaryStyle']
    player8subrunes= recentMatch['participants'][7]['stats']['perkSubStyle']
    player8minions = recentMatch['participants'][7]['stats']['totalMinionsKilled']
    player8camps = recentMatch['participants'][7]['stats']['neutralMinionsKilled']
    player8level = recentMatch['participants'][7]['stats']['champLevel']
    player8cs = player8minions + player8camps
#Primary runes
    if player8primaryrunes == 8000:
        player8primaryrunes = '<:precision:818050788118233089>'
    elif player8primaryrunes == 8100:
        player8primaryrunes = '<:domination:818050737589846026>'
    elif player8primaryrunes == 8200:
        player8primaryrunes = '<:sorcery:818050843143700502>'
    elif player8primaryrunes == 8300:
        player8primaryrunes = '<:inspiration:818050767642558464>'
    elif player8primaryrunes == 8400:
        player8primaryrunes = '<:resolve:818050828333613076>'
#Sub runes
    if player8subrunes == 8000:
        player8subrunes = '<:precision:818050788118233089>'
    elif player8subrunes == 8100:
        player8subrunes = '<:domination:818050737589846026>'
    elif player8subrunes == 8200:
        player8subrunes = '<:sorcery:818050843143700502>'
    elif player8subrunes == 8300:
        player8subrunes = '<:inspiration:818050767642558464>'
    elif player8subrunes == 8400:
        player8subrunes = '<:resolve:818050828333613076>'

#player 9
    player9name = recentMatch['participantIdentities'][8]['player']['summonerName']
    player9champion = recentMatch['participants'][8]['championId']
    player9deaths = recentMatch['participants'][8]['stats']['deaths']
    player9kills = recentMatch['participants'][8]['stats']['kills']
    player9assists = recentMatch['participants'][8]['stats']['assists']
    player9deal = recentMatch['participants'][8]['stats']['totalDamageDealtToChampions']
    player9primaryrunes= recentMatch['participants'][8]['stats']['perkPrimaryStyle']
    player9subrunes= recentMatch['participants'][8]['stats']['perkSubStyle']
    player9minions = recentMatch['participants'][8]['stats']['totalMinionsKilled']
    player9camps = recentMatch['participants'][8]['stats']['neutralMinionsKilled']
    player9level = recentMatch['participants'][8]['stats']['champLevel']
    player9cs = player9minions + player9camps
#Primary runes
    if player9primaryrunes == 8000:
        player9primaryrunes = '<:precision:818050788118233089>'
    elif player9primaryrunes == 8100:
        player9primaryrunes = '<:domination:818050737589846026>'
    elif player9primaryrunes == 8200:
        player9primaryrunes = '<:sorcery:818050843143700502>'
    elif player9primaryrunes == 8300:
        player9primaryrunes = '<:inspiration:818050767642558464>'
    elif player9primaryrunes == 8400:
        player9primaryrunes = '<:resolve:818050828333613076>'
#Sub runes
    if player9subrunes == 8000:
        player9subrunes = '<:precision:818050788118233089>'
    elif player9subrunes == 8100:
        player9subrunes = '<:domination:818050737589846026>'
    elif player9subrunes == 8200:
        player9subrunes = '<:sorcery:818050843143700502>'
    elif player9subrunes == 8300:
        player9subrunes = '<:inspiration:818050767642558464>'
    elif player9subrunes == 8400:
        player9subrunes = '<:resolve:818050828333613076>'

#player 10
    player10name = recentMatch['participantIdentities'][9]['player']['summonerName']
    player10champion = recentMatch['participants'][9]['championId']
    player10deaths = recentMatch['participants'][9]['stats']['deaths']
    player10kills = recentMatch['participants'][9]['stats']['kills']
    player10assists = recentMatch['participants'][9]['stats']['assists']
    player10deal = recentMatch['participants'][9]['stats']['totalDamageDealtToChampions']
    player10primaryrunes= recentMatch['participants'][9]['stats']['perkPrimaryStyle']
    player10subrunes= recentMatch['participants'][9]['stats']['perkSubStyle']
    player10minions = recentMatch['participants'][9]['stats']['totalMinionsKilled']
    player10camps = recentMatch['participants'][9]['stats']['neutralMinionsKilled']
    player10level = recentMatch['participants'][9]['stats']['champLevel']
    player10cs = player10minions + player10camps
#Primary runes
    if player10primaryrunes == 8000:
        player10primaryrunes = '<:precision:818050788118233089>'
    elif player10primaryrunes == 8100:
        player10primaryrunes = '<:domination:818050737589846026>'
    elif player10primaryrunes == 8200:
        player10primaryrunes = '<:sorcery:818050843143700502>'
    elif player10primaryrunes == 8300:
        player10primaryrunes = '<:inspiration:818050767642558464>'
    elif player10primaryrunes == 8400:
        player10primaryrunes = '<:resolve:818050828333613076>'
#Sub runes
    if player10subrunes == 8000:
        player10subrunes = '<:precision:818050788118233089>'
    elif player10subrunes == 8100:
        player10subrunes = '<:domination:818050737589846026>'
    elif player10subrunes == 8200:
        player10subrunes = '<:sorcery:818050843143700502>'
    elif player10subrunes == 8300:
        player10subrunes = '<:inspiration:818050767642558464>'
    elif player10subrunes == 8400:
        player10subrunes = '<:resolve:818050828333613076>'

    gameDuration = recentMatch['gameDuration']
    gameXronos = strftime("%M:%S", gmtime(gameDuration))

    team1bans = team1['bans']
    champ1ban = team1bans[0]['championId']
    champ2ban = team1bans[1]['championId']
    champ3ban = team1bans[2]['championId']
    champ4ban = team1bans[3]['championId']
    champ5ban = team1bans[4]['championId']
    
    team2bans = team2['bans']
    champ6ban = team2bans[0]['championId']
    champ7ban = team2bans[1]['championId']
    champ8ban = team2bans[2]['championId']
    champ9ban = team2bans[3]['championId']
    champ10ban = team2bans[4]['championId']

    team1Drakes = team1['dragonKills']
    team2Drakes = team2['dragonKills']
    team1Barons = team1['baronKills']
    team2Barons = team2['baronKills']
    team1Towers = team1['towerKills']
    team2Towers = team1['towerKills']
    team1Inhibs = team1['inhibitorKills']
    team2Inhibs = team2['inhibitorKills']

    if recentMatch['queueId'] == 420:
        gamemode = "**Summoner's Rift** : __Ranked Solo/Duo__"
    elif recentMatch['queueId'] == 440:
        gamemode = "**Summoner's Rift** : __Ranked Flex__"
    elif recentMatch['queueId'] == 400:
        gamemode = "**Summoner's Rift** : __Normal Draft Pick__"
    elif recentMatch['queueId'] == 450:
        gamemode = "**Howling Abyss** : __ARAM__"
    elif recentMatch['queueId'] == 430:
        gamemode = "**Summoner's Rift** : __Normal Blind Pick__"
    else: gamemode = "**Summoner's Rift** : __Featured Game Mode__"

    await waitingmessage.delete()

    if team1win == 'Victory':
        embed=discord.Embed(title=f"<:eloicon:820974785168801802> Match History - Blue Team Wins", description=f"{gamemode} | {gameXronos}",color=discord.Color.dark_blue())
        embed.add_field(name = f'**Blue Team <:blueteam:817370233211453460> - {team1win}**', value =f"**{player1primaryrunes} {player1subrunes} {player1name} - **__{findChampionName(player1champion)}__ \n **{player2primaryrunes} {player2subrunes} {player2name} - **__{findChampionName(player2champion)}__ \n **{player3primaryrunes} {player3subrunes} {player3name} - **__{findChampionName(player3champion)}__ \n **{player4primaryrunes} {player4subrunes} {player4name} - **__{findChampionName(player4champion)}__ \n **{player5primaryrunes} {player5subrunes} {player5name} - **__{findChampionName(player5champion)}__", inline = True)
        embed.add_field(name = '**K / D / A | CS <:blueminions:822054719643975710>**',value =f"{player1kills} / {player1deaths} / {player1assists} **|** {player1cs} \n {player2kills} / {player2deaths} / {player2assists} **|** {player2cs} \n {player3kills} / {player3deaths} / {player3assists} **|** {player3cs} \n {player4kills} / {player4deaths} / {player4assists} **|** {player4cs} \n {player5kills} / {player5deaths} / {player5assists} **|** {player5cs}",inline = True)
        embed.add_field(name = f'**DMG / Level<:damagedealtblue:822059178574086194>**',value = f"{player1deal:,d} / {player1level} \n {player2deal:,d} / {player2level} \n {player3deal:,d} / {player3level} \n {player4deal:,d} / {player4level} \n {player5deal:,d} / {player5level}", inline = True)
        embed.add_field(name = f'**Red Team <:redteam:817370254337769492> - {team2win}**', value =f"**{player6primaryrunes} {player6subrunes} {player6name} - **__{findChampionName(player6champion)}__ \n **{player7primaryrunes} {player7subrunes} {player7name} - **__{findChampionName(player7champion)}__ \n **{player8primaryrunes} {player8subrunes} {player8name} - **__{findChampionName(player8champion)}__ \n **{player9primaryrunes} {player9subrunes} {player9name} - **__{findChampionName(player9champion)}__ \n **{player10primaryrunes} {player10subrunes} {player10name} - **__{findChampionName(player10champion)}__", inline = True)
        embed.add_field(name = '**K / D / A | CS <:redminions:822054719849496606>**',value =f"{player6kills} / {player6deaths} / {player6assists} **|** {player6cs}  \n {player7kills} / {player7deaths} / {player7assists} **|** {player7cs} \n {player8kills} / {player8deaths} / {player8assists} **|** {player8cs} \n {player9kills} / {player9deaths} / {player9assists} **|** {player9cs} \n {player10kills} / {player10deaths} / {player10assists} **|** {player10cs}",inline = True)
        embed.add_field(name = '**DMG / Level <:damagedealtred:822059335584186378>**',value = f"{player6deal:,d} / {player6level} \n {player7deal:,d} / {player7level} \n {player8deal:,d} / {player8level} \n {player9deal:,d} / {player9level} \n {player10deal:,d} / {player10level}",inline = True)    
        embed.add_field(name ='**Team Stats**',value = f"<:baronblue:822038343655227402> {team1Barons} <:dragonblue:822038343637532672> {team1Drakes} <:towerblue:822038343629275176> {team1Towers} <:blueteam:817370233211453460> {team1Inhibs} | <:baronred:822038343591395348> {team2Barons} <:dragonred:822038343604109332> {team2Drakes} <:towerred:822038343667548190> {team2Towers} <:redteam:817370254337769492> {team2Inhibs}",inline = False)
        embed.add_field(name = '**Bans <:banicon:819493635115843614>**', value = f'<:blueteam:817370233211453460> {findChampionName(champ1ban)} | {findChampionName(champ2ban)} | {findChampionName(champ3ban)} | {findChampionName(champ4ban)} | {findChampionName(champ5ban)} \n <:redteam:817370254337769492> {findChampionName(champ6ban)} | {findChampionName(champ7ban)} | {findChampionName(champ8ban)} | {findChampionName(champ9ban)} | {findChampionName(champ10ban)}')
        await ctx.send(embed=embed)
    elif team2win == 'Victory':
        embed= discord.Embed(title=f"<:eloicon:820974785168801802> Match History - Red Team Wins", description=f"{gamemode} | {gameXronos}",color=discord.Color.dark_red())
        embed.add_field(name = f'**Blue Team <:blueteam:817370233211453460> - {team1win}**', value =f"**{player1primaryrunes} {player1subrunes} {player1name} - **__{findChampionName(player1champion)}__ \n **{player2primaryrunes} {player2subrunes} {player2name} - **__{findChampionName(player2champion)}__ \n **{player3primaryrunes} {player3subrunes} {player3name} - **__{findChampionName(player3champion)}__ \n **{player4primaryrunes} {player4subrunes} {player4name} - **__{findChampionName(player4champion)}__ \n **{player5primaryrunes} {player5subrunes} {player5name} - **__{findChampionName(player5champion)}__", inline = True)
        embed.add_field(name = '**K / D / A | CS <:blueminions:822054719643975710>**',value =f"{player1kills} / {player1deaths} / {player1assists} **|** {player1cs} \n {player2kills} / {player2deaths} / {player2assists} **|** {player2cs} \n {player3kills} / {player3deaths} / {player3assists} **|** {player3cs} \n {player4kills} / {player4deaths} / {player4assists} **|** {player4cs} \n {player5kills} / {player5deaths} / {player5assists} **|** {player5cs}",inline = True)
        embed.add_field(name = f'**DMG / Level<:damagedealtblue:822059178574086194>**',value = f"{player1deal:,d} / {player1level} \n {player2deal:,d} / {player2level} \n {player3deal:,d} / {player3level} \n {player4deal:,d} / {player4level} \n {player5deal:,d} / {player5level}", inline = True)
        embed.add_field(name = f'**Red Team <:redteam:817370254337769492> - {team2win}**', value =f"**{player6primaryrunes} {player6subrunes} {player6name} - **__{findChampionName(player6champion)}__ \n **{player7primaryrunes} {player7subrunes} {player7name} - **__{findChampionName(player7champion)}__ \n **{player8primaryrunes} {player8subrunes} {player8name} - **__{findChampionName(player8champion)}__ \n **{player9primaryrunes} {player9subrunes} {player9name} - **__{findChampionName(player9champion)}__ \n **{player10primaryrunes} {player10subrunes} {player10name} - **__{findChampionName(player10champion)}__", inline = True)
        embed.add_field(name = '**K / D / A | CS <:redminions:822054719849496606>**',value =f"{player6kills} / {player6deaths} / {player6assists} **|** {player6cs}  \n {player7kills} / {player7deaths} / {player7assists} **|** {player7cs} \n {player8kills} / {player8deaths} / {player8assists} **|** {player8cs} \n {player9kills} / {player9deaths} / {player9assists} **|** {player9cs} \n {player10kills} / {player10deaths} / {player10assists} **|** {player10cs}",inline = True)
        embed.add_field(name = '**DMG / Level <:damagedealtred:822059335584186378>**',value = f"{player6deal:,d} / {player6level} \n {player7deal:,d} / {player7level} \n {player8deal:,d} / {player8level} \n {player9deal:,d} / {player9level} \n {player10deal:,d} / {player10level}",inline = True)    
        embed.add_field(name ='**Team Stats**',value = f"<:baronblue:822038343655227402> {team1Barons} <:dragonblue:822038343637532672> {team1Drakes} <:towerblue:822038343629275176> {team1Towers} <:blueteam:817370233211453460> {team1Inhibs} | <:baronred:822038343591395348> {team2Barons} <:dragonred:822038343604109332> {team2Drakes} <:towerred:822038343667548190> {team2Towers} <:redteam:817370254337769492> {team2Inhibs}",inline = False)
        embed.add_field(name = '**Bans <:banicon:819493635115843614>**', value = f'<:blueteam:817370233211453460> {findChampionName(champ1ban)} | {findChampionName(champ2ban)} | {findChampionName(champ3ban)} | {findChampionName(champ4ban)} | {findChampionName(champ5ban)} \n <:redteam:817370254337769492> {findChampionName(champ6ban)} | {findChampionName(champ7ban)} | {findChampionName(champ8ban)} | {findChampionName(champ9ban)} | {findChampionName(champ10ban)}')
        await ctx.send(embed=embed)


client.run(TOKEN)
