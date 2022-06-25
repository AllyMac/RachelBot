import discord
from git import Repo
from discord.ext import commands,tasks
import time
import datetime
import xml.etree.ElementTree as ET
import os
import sys
import random
from datetime import date
import calendar
from discord.ext import commands
from itertools import cycle
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import shutil


client = commands.Bot(command_prefix = ["-","Pls ","pls ", "PLS "], help_command=None)

tree = ET.parse('/home/pi/Rachel Bot/RachelData.xml')
root = tree.getroot()
discordToken =root[0].text


#-----------------EVENTS-----------------

@client.event
async def on_ready():
    print('Rachel Bot Online!')
    change_status.start()

#second part of horny bot. delets the message
@client.event
async def on_message(message):
    if message.author.id == 270904126974590976:
        day = date.today()
        dayString = calendar.day_name[day.weekday()]
        now = datetime.datetime.now()
        hour = now.hour
        minute = now.minute
        if dayString == "Monday" or dayString == "Tuesday" or dayString == "Wednesday" or dayString == "Thursday":
            if hour < 18:
                await message.delete()
        elif dayString == "Friday":
            if hour < 12:
                await message.delete()

    await client.process_commands(message)

#-----------------TASKS-----------------
@tasks.loop(seconds=3600)
async def change_status():
    day = date.today()
    dayString = calendar.day_name[day.weekday()]
    now = datetime.datetime.now()
    hour = now.hour
    minute = now.minute
    today = datetime.date.today()
    seshDate = datetime.date(2021,6,25)
    diff = seshDate - today
    seshCounter = FormatStatus(diff.days-1)
    print("status update @ "+str(hour)+':'+str(minute))

    if dayString == "Friday":

        if (hour % 2) == 0:
            await client.change_presence(activity=discord.Game(name=seshCounter))
            print(' - ' + seshCounter)
        else:
            await client.change_presence(activity=discord.Game(name="It\'s Friday then"))
            print(" - It\'s Friday then")

        if hour == 16:
            botChannel = client.get_channel(710989960408465560)
            await botChannel.send("It\'s Friday then")
            await botChannel.send("https://giphy.com/gifs/friday-its-JmVcakKIdojgpBC2iw")
            print('It\'s friday then time!')
    else:
        await client.change_presence(activity=discord.Game(name=seshCounter))
        print(' - ' + seshCounter)



#-----------------COMMANDS-----------------

#self updates from github MAIN Branch only
@client.command(aliases = ['update','UPDATE'])
async def Update(ctx):
    tempFolder = '/home/pi/Rachel Bot/GithubTemp'
    mainFolder = '/home/pi/Rachel Bot/Github'
    await ctx.send("Updating from github...")
    time.sleep(5)
    Repo.clone_from('https://github.com/AllyMac/RachelBot/', tempFolder)
    time.sleep(30)

    #copy files from temp to
    for src_dir, dirs, files in os.walk(tempFolder):
        dst_dir = src_dir.replace(tempFolder, mainFolder, 1)
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        for file_ in files:
            src_file = os.path.join(src_dir, file_)
            dst_file = os.path.join(dst_dir, file_)
            if os.path.exists(dst_file):
                # in case of the src and dst are the same file
                if os.path.samefile(src_file, dst_file):
                    continue
                os.remove(dst_file)
            shutil.move(src_file, dst_dir)


    shutil.rmtree(tempFolder)
    await ctx.send("Restarting...")
    os.execv(sys.executable, ['python'] + sys.argv)


@client.command(aliases = ["climb", "theClimb", "TheClimb","theclimb"])
async def Climb(ctx,*,text):
    textList = text.split(", ")
    img = Image.open('/home/pi/Rachel Bot/image/climb.png')
    draw = ImageDraw.Draw(img)

    # specified font size
    font = ImageFont.truetype('/home/pi/Rachel Bot/fonts/arial.ttf', 100)
    fontShadow = ImageFont.truetype('/home/pi/Rachel Bot/fonts/arial.ttf', 102)

    topList=textList[1].split(' ')
    topText = listNewlines(topList)

    bottomList=textList[0].split(' ')
    bottomText = listNewlines(bottomList)

    if(len(topList) < 7 and len(bottomList) < 7):

        topPosition=formatPosition(len(topList),'top')
        bottomPosition=formatPosition(len(bottomList),'bottom')

        draw.text((600, topPosition),topText,(0,0,0),font=fontShadow)
        draw.text((100, bottomPosition),bottomText,(0,0,0),font=fontShadow)

        draw.text((600, topPosition),topText,(255,255,0),font=font)
        draw.text((100, bottomPosition),bottomText,(255,255,0),font=font)



        img.save('/home/pi/Rachel Bot/image/climbMeme.png')
        await ctx.send(file=discord.File('/home/pi/Rachel Bot/image/climbMeme.png'))

    else:
        await ctx.send('Six words max')

@client.command(aliases = ["Kieran"])
async def KieranWork(ctx):
    await ctx.send("Kieran's usual work schedule can be found below")
    await ctx.send("Sunday night | Monday night | Tuesday night")

@client.command(aliases = ["Friday","FRIDAY"])
async def friday(ctx):
    day = date.today()
    dayString = calendar.day_name[day.weekday()]
    if dayString == "Friday":
        await ctx.send("It\'s Friday then")
        await ctx.send("https://giphy.com/gifs/friday-its-JmVcakKIdojgpBC2iw")
    else:
        await ctx.send("Not yet...")
        await ctx.send("https://media1.tenor.com/images/22c01fbd229cfcf2eee71f824c97f538/tenor.gif?itemid=13377463")

#randomly creates two teams
@client.command(aliases = ["Teams","team","Team","TEAMS","TEAM"])
async def teams(ctx, gamers):
    list = gamers.split(",")
    random.shuffle(list)
    team1="__**team 1**__" +"\n"
    team2="__**team 2**__" +"\n"
    length = len(list)
    middle_index = length//2
    first_half = list[:middle_index]
    second_half = list[middle_index:]
    for i in first_half:
        team1+=i+"\n"
    for i in second_half:
        team2+=i+"\n"

    await ctx.send(str(team1+team2))

#List of all current commands
@client.command(aliases = ["Help","HELP"])
async def help(ctx):
    helpResponse=""
    helpResponse +="__**Rachel bot Commands**__" +"\n"
    helpResponse +="**ping:**   *how long it takes you to get to my pi(e)*" +"\n"
    helpResponse +="**bullshit:**   *lists a bullshit reason*" +"\n"
    helpResponse +="**dua:**   *helps you through a tough time*" +"\n"
    helpResponse +="**beer:**   *How long till each sesh*" +"\n"
    helpResponse +="**playlists:**   *List of playlists for DJ Aki*" +"\n"
    helpResponse +="**gamers:**   *@'s the gamers*" +"\n"
    helpResponse +="**teams:**   *splits a list of gamers into two teams* '-teams name1,name2,name3,name4...'" +"\n"
    helpResponse +="**trumpet:**   *Bust out the trumpet*" +"\n"
    helpResponse +="**climb:**   *Callums coming up* '-climb bottomText, topText'" +"\n"
    await ctx.send(helpResponse)

@client.command(aliases = ["trumpets", "Trumpet", "trumpet","TRUMPET","TRUMPETS", "Ace", "ace", "ACE"])
async def Trumpets(ctx):
    await ctx.send("https://cdn.discordapp.com/attachments/693234427249033266/820313898971824128/O-yp-VtEfzuDLPYp.mp4")

@client.command(aliases = ["Sheesh", "SHEESH", "sheeesh","sheeeesh","sheeeeesh", "sheeeeeesh", "sheeeeeeesh", "sheeeeeeeesh"])
async def sheesh(ctx):
    list = [
        'https://cdn.everskies.com/media/attachment/R_p6G_ICnk9_iU0G8h5i.gif',
        'https://giphy.com/embed/m9toV3zKSM3CXA9AmJ',
        'https://media.giphy.com/media/S8Hcuja2jgkiBfunXE/giphy.gif',
        'https://media.giphy.com/media/3dhB0SujUADaWxWGcj/giphy.gif'
        'https://media.giphy.com/media/WtbQ32iLiSBllSJWic/giphy.gif'
        ]

    await ctx.send(random.choice(list))

#@'s the gamer
@client.command(aliases = ["Gamers",'gamer','Gamer',"GAMER","GAMERS"])
async def gamers(ctx):
    gamersResponse=""
    gamersResponse+="<@216213062510706688>"+', '
    gamersResponse+="<@298841687709581312>"+', '
    gamersResponse+="<@424912229855395843>"+', '
    gamersResponse+="<@403335000629444608>"+', '
    gamersResponse+="<@106856751961284608>"+', '
    gamersResponse+="<@291263593712844810>"+', '
    gamersResponse+="<@637683077015142420>"+', '
    gamersResponse+="<@169136251595784201>"+' '
    await ctx.send(gamersResponse)

def FormatPlaylist(name, link):
    return "**"+name+":**   *-play <"+link+">*" +"\n"

@client.command(aliases = ["Playlists","playlist","play lists", "Play Lists","PLAYLISTS","PLAYLIST"])
async def playlists(ctx):
    playlistResponse=""
    playlistResponse +="**   **" +"\n"
    playlistResponse +="__**Playlists**__" +"\n"
    playlistResponse +=FormatPlaylist("Brit-pop Classsics","https://open.spotify.com/playlist/2x6uIHNTIuGINT0Dmv32nL?si=K_c2Ubw3Qm-D6HX7EtwYVg")
    playlistResponse +=FormatPlaylist("Cheesy Hits","https://open.spotify.com/playlist/37i9dQZF1DX7pykHKVxv6o?si=v1eSmI07SMCYnrauuu3Biw")
    playlistResponse +=FormatPlaylist("Propaganda","https://open.spotify.com/playlist/6e1gRgTdc0MytsBTfkY0fQ?si=u9u0cV17RlaUGcAg1noVCQ")
    playlistResponse +=FormatPlaylist("All out 10s","https://open.spotify.com/playlist/37i9dQZF1DX5Ejj0EkURtP?si=rpXNJfI5QG2KaizsboHU_A")
    playlistResponse +=FormatPlaylist("All out 00s","https://open.spotify.com/playlist/37i9dQZF1DX4o1oenSJRJd?si=uwHyMCiMQgi2IjAS4_khuw")
    playlistResponse +=FormatPlaylist("All out 90s","https://open.spotify.com/playlist/37i9dQZF1DXbTxeAdrVG2l?si=9WzlwHeTRqa8sMdVkhkWhQ")
    playlistResponse +=FormatPlaylist("All out 80s","https://open.spotify.com/playlist/37i9dQZF1DX4UtSsGT1Sbe?si=nswkzemNTMyws_nQIr0-tg")
    playlistResponse +=FormatPlaylist("Alt 80s","https://open.spotify.com/playlist/37i9dQZF1DWTSKFpOdYF1r?si=yMWgdo2XTqGWYUKXJ4iu0g")
    playlistResponse +=FormatPlaylist("All out 70s","https://open.spotify.com/playlist/37i9dQZF1DWTJ7xPn4vNaz?si=BbHZIEtXSTmbGH33qWDa6A")
    playlistResponse +=FormatPlaylist("Koppabergs on the grass","https://open.spotify.com/playlist/2FPXj6jhxk38Xkn1dE2V7N?si=RwDubRl4QhaPchQhSQxHNA")
    await ctx.send(playlistResponse)

def FormatStatus(days):
    returnString =""
    if(days<0):
        returnString="Gone seshin'"
    elif(days==0):
        dt = datetime.datetime.now()
        timeToMidnight= str(datetime.timedelta(seconds=((24 - dt.hour - 1) * 60 * 60) + ((60 - dt.minute - 1) * 60) + (60 - dt.second)))
        split = timeToMidnight.split(":")
        returnString=split[0]  +" hours "+split[1]  +" minutes "+split[2]  +" seconds"+" till sesh"
    else:
        returnString=str(days)+" day till sesh"
    return returnString


def FormatDays(days):
    returnString =""
    if(days<0):
        returnString="**:white_check_mark: Can now have **"
    elif(days==0):
        dt = datetime.datetime.now()
        timeToMidnight= str(datetime.timedelta(seconds=((24 - dt.hour - 1) * 60 * 60) + ((60 - dt.minute - 1) * 60) + (60 - dt.second)))
        split = timeToMidnight.split(":")
        returnString="**" +split[0]  +" hours "+split[1]  +" minutes "+split[2]  +" seconds"+"** till "
    else:
        if(days==1):
            returnString="**"+str(days)+" day** till "
        else:
            returnString="**"+str(days)+" days** till "
    return returnString

def formatPosition(count,line):
    position=None
    if (line == 'top'):
        if (count == 1 or count == 2):
            position=50
        elif (count == 3 or count == 4):
            position=50
        elif (count == 5 or count == 6):
            position=25
    else:
        if (count == 1 or count == 2):
            position=1000
        elif (count == 3 or count ==4):
            position=900
        elif (count == 5 or count == 6):
            position=850
    return position

def listNewlines(list):
    newLine=False
    text=''
    for i in list:
        if (newLine):
           text+=i+'\n'
           newLine=False
        else:
           text+=i+' '
           newLine=True
    return text


#Beer counter
@client.command(aliases = ["Beer", "beers", "Beers", "BEERS", "BEER", "SESH", "sesh", "Sesh"])
async def beer(ctx):
    today = datetime.date.today()




    beerResponse = ""
    beerResponse +="__**Countdown to beers**__" +"\n"

    #June 25th times
    beerResponse +="\n"+"__**:beers:Manchester:beers:**__" +"\n"
    manchesterDate=datetime.date(2021,6,25)
    diff = manchesterDate - today
    seshCounter = FormatDays(diff.days-1)
    beerResponse +=seshCounter+"Sesh in Manchester, the BIG one" +"\n"

    #Scotland times
    beerResponse +="\n"+"__**:scotland:Scotland:scotland:**__" +"\n"

    scotGardenDate=datetime.date(2021,4,16)
    scotBeerGardenDate=datetime.date(2021,4,26)
    scotPubDate=datetime.date(2021,5,17)
    scotPubFiveDate=datetime.date(2021,6,14)
    scotFinalDate=datetime.date(2021,6,30)

    diff = scotGardenDate - today
    seshCounter = FormatDays(diff.days-1)
    beerResponse +=seshCounter+"beers in a garden, with 5 mates" +"\n"

    diff = scotBeerGardenDate - today
    seshCounter = FormatDays(diff.days-1)
    beerResponse +=seshCounter+"beers in a beer garden, with 5 mates" +"\n"

    diff = scotPubDate - today
    seshCounter = FormatDays(diff.days-1)
    beerResponse +=seshCounter+"beers in the pub, with 3 mates" +"\n"

    diff = scotPubFiveDate - today
    seshCounter = FormatDays(diff.days-1)
    beerResponse +=seshCounter+"beers in the pub, with 5 mates" +"\n"

    diff = scotFinalDate - today
    seshCounter = FormatDays(diff.days-1)
    beerResponse +=seshCounter+"beers with everyone, everywhere!" +"\n"

    #England times
    beerResponse +="\n"+"__**:england:England:england:**__" +"\n"

    parkDate = datetime.date(2021,3,29)
    beerGardenDate=datetime.date(2021,4,12)
    PubDate=datetime.date(2021,5,17)
    finalDate=datetime.date(2021,6,21)

    diff = parkDate - today
    seshCounter = FormatDays(diff.days-1)
    beerResponse +=seshCounter+"beers in the park, with 5 mates" +"\n"

    diff = beerGardenDate - today
    seshCounter = FormatDays(diff.days-1)
    beerResponse +=seshCounter+"beers in a beer garden, with 5 mates" +"\n"

    diff = PubDate - today
    seshCounter = FormatDays(diff.days-1)
    beerResponse +=seshCounter+"beers in the pub, with 5 mates" +"\n"

    diff = finalDate - today
    seshCounter = FormatDays(diff.days-1)
    beerResponse +=seshCounter+"beers with everyone, everywhere!" +"\n"
    await ctx.send(beerResponse)


@client.command(aliases = ["PING"])
async def ping(ctx):
    await ctx.send("Ping: "+str(round(client.latency * 1000))+"ms")
    print('command: -ping')
    print('response: Ping: '+str(round(client.latency * 1000))+"ms")

#Horny jail (checks time and date and if within time returns picture and random reply for user)
@client.command(aliases = ["boobs","anal","boobies","booty","porn","porngif","BOOBS","ANAL","BOOBIES","BOOTY","PORN","PORNGIF"])
async def hornyBot(ctx):
    day = date.today()
    dayString = calendar.day_name[day.weekday()]
    now = datetime.datetime.now()
    hour = now.hour
    minute = now.minute
    hornyList = [
        'go to horny jail!',
        'is down bad',
        'you know its '+str(hour)+':'+str(minute)+' on a '+dayString+' right?'
        ]

    if dayString == "Monday" or dayString == "Tuesday" or dayString == "Wednesday" or dayString == "Thursday":
        if hour < 18:
            time.sleep(0.3)
            await ctx.send(ctx.message.author.mention +" "+ "***" +random.choice(hornyList)+ "***")
            await ctx.send("https://pbs.twimg.com/media/EguJJngXcBc0tH_?format=jpg&name=large")
    elif dayString == "Friday":
        if hour < 12:
            time.sleep(0.3)
            await ctx.send(ctx.message.author.mention +" "+ "***"+ random.choice(hornyList)+ "***")
            await ctx.send("https://pbs.twimg.com/media/EguJJngXcBc0tH_?format=jpg&name=large")

#gets random bullshit excuse from list
@client.command(aliases = ["Bullshit","BULLSHIT"])
async def bullshit(ctx):
    bullshitList = [
        'Ping too high',
        'Ping too low',
        'Frankfurt server',
        'Live in the server room',
        'Default Skin',
        'Using Prime skin',
        'The lads a nonce',
        'They paid to win',
        'They had a 3090',
        'They had better RGB',
        'Headshot whilst running',
        'Better gamer chair',
        'No G-fuel',
        'Skipped your weetabix',
        'Shrouds smurf account',
        'word.exe',
        'wall hacks',
        'They\'re built different',
        'Left hand',
        'Jett diff',
        'right hand',
        'crosshair too big',
        'crosshair too small',
        'sense too high',
        'sense too low',
        'Drinks game-girl bathwater'
        ]

    await ctx.send("https://creazilla-store.fra1.digitaloceanspaces.com/cliparts/23243/turd-clipart-md.png")
    await ctx.send("**"+random.choice(bullshitList)+"**")

#gets random dua picture
@client.command(aliases = ["Dua", "dua lipa", "Dua Lipa","DUA", "DUA LIPA"])
async def dua(ctx):
    duaList = [
        'https://upload.wikimedia.org/wikipedia/commons/9/9a/200126_Dua_Lipa_on_the_2020_Grammys_Red_Carpet.jpg',
        'https://www.redbrick.me/wp-content/uploads/2020/04/dua-lipa.jpg',
        'https://media.gq.com/photos/5a5f79d835be9e1aebeceecf/16:9/w_2560%2Cc_limit/Dua_Lipa_01.jpg',
        'https://i.guim.co.uk/img/media/92490448b4d306d0c7861c5b458c6ca3a9f33b53/0_167_7382_4426/master/7382.jpg?width=700&quality=85&auto=format&fit=max&s=ddf21b31e22af9ad0817abb22849450e',
        'https://twitter.com/DUALIPA/status/1358540202537488384',
        'https://static.wikia.nocookie.net/dualipa/images/9/91/Dua_Lipa.png/revision/latest?cb=20200130023354',
        'https://media1.popsugar-assets.com/files/thumbor/-9_RtlAt8rdm-aXG7F5xN_zwaG4/fit-in/1024x1024/filters:format_auto-!!-:strip_icc-!!-/2021/03/14/085/n/1922564/34429b9cf1e7f938_GettyImages-1307104446/i/dua-lipa-versace-performance-outfits-grammys-2021.jpg',
        'https://media1.popsugar-assets.com/files/thumbor/Epft-lhXm4hmzNCl9OBmVyLA6ss/fit-in/1024x1024/filters:format_auto-!!-:strip_icc-!!-/2021/03/14/085/n/1922564/bad29f869444fbb1_GettyImages-1307104441/i/dua-lipa-versace-performance-outfits-grammys-2021.jpg',
        'https://media1.popsugar-assets.com/files/thumbor/tjZu3zVklevSKANstauVhf4R3FI/fit-in/1024x1024/filters:format_auto-!!-:strip_icc-!!-/2021/03/14/085/n/1922564/fff6a5955d5d8f29_GettyImages-1307104440/i/Dua-Lipa-Pink-Two-Piece-at-2021-Grammys.jpg',
        'https://i2.wp.com/bestofcomicbooks.com/wp-content/uploads/2020/06/Dua-Lipa-2.jpg?resize=696%2C870&ssl=1',
        'https://cellularnews.com/wp-content/uploads/2020/06/04-a-sexy-dua-lipa-in-a-mesh-outfit-325x485.jpg',
        'https://giphy.com/gifs/snl-saturday-night-live-season-43-l0NgSz8F1Kqbi4fzG',
        'https://qph.fs.quoracdn.net/main-qimg-6681b2dbb6b773391fb4904c190ae9ec',
        'https://qph.fs.quoracdn.net/main-qimg-86d6db2505ee2e0fc468ffa84e55dcd8',
        'https://qph.fs.quoracdn.net/main-qimg-1c013cbf7a07f04097e7ec37f23e09df',
        'https://giphy.com/gifs/recordingacademy-grammys-2021-7iYDzlpKLpUSrp8v8f',
        'https://giphy.com/gifs/amas-amas-2019-american-music-awards-eK7ke3ZyVhB9t797cd',
        'https://gfycat.com/optimisticdeliriouskestrel-dua-lipa-high-fifty-shades-freed'
        'https://gfycat.com/greedyuntidyiriomotecat'
        'https://gfycat.com/kaleidoscopicunfoldedaustralianshelduck-celebrity-dua-lipa'
        'https://gfycat.com/sillypowerlessclingfish'
        ]

    nasList= [
        'https://media.glamour.com/photos/6062187d7ef2bb6102406d4f/6:7/w_2560%2Cc_limit/1202216437',
        'https://media.them.us/photos/605e1431ff9a9929843f1d72/master/w_2560%2Cc_limit/lil-nas-x-montero.png',
        'https://dazedimg-dazedgroup.netdna-ssl.com/700/azure/dazed-prod/1290/9/1299932.jpg',
        'https://cached.imagescaler.hbpl.co.uk/resize/scaleWidth/815/cached.offlinehbpl.hbpl.co.uk/news/SUC/LILNASTY-20191016014623460.jpg',
        'https://assets.vogue.com/photos/5df006e30e3403000891fbb1/master/w_2560%2Cc_limit/lilnas-vw.jpg'
        ]

    response = ""
    now = datetime.date.today()
    year = now.year
    aprilFoolsDate=datetime.date(year,4,1)

    if now == aprilFoolsDate:
        response=random.choice(nasList)
    else:
        response=random.choice(duaList)

    await ctx.send(response)

#Token stored locally in XML
client.run(discordToken)
