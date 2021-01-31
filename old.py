import asyncio
import discord
from discord.ext import commands, timers
from datetime import datetime, timedelta
import configparser
import re
import pandas as pd

# ////////////////////////// < HELPERS FUNCTION > /////////////////////////////////////////


def get_channel_id(name):
    for guild in bot.guilds:
        for channel in guild.channels:
            if channel.name == name:
                return channel.id


def get_user_id(name):
    for guild in bot.guilds:
        for m in guild.members:
            if m.name == name:
                return m.id


def get_member(name):
    members = bot.get_all_members()

    if "@" in name:
        name = re.findall(r'\d+', name)
        id = int(name[0])
        for m in members:
            if m.id == id:
                return m

    for m in members:
        if m.name == name:
            return m


def get_role(name):
    for guild in bot.guilds:
        for r in guild.roles:
            if r.name == name:
                return r


def init_channel(args):
    config = configparser.ConfigParser()
    config.read('config.ini')

    if args == "welcome":
        if config['BOTDATA']['WELCOME_CHANNEL'] is not None:
            id = get_channel_id(config['BOTDATA']['WELCOME_CHANNEL'])
            return bot.get_channel(id)

    elif args == "goodbye":
        if config['BOTDATA']['GOODBYE_CHANNEL'] is not None:
            id = get_channel_id(config['BOTDATA']['GOODBYE_CHANNEL'])
            return bot.get_channel(id)

    elif args == "annonce":
        if config['BOTDATA']['CHANNEL_ANNONCE'] is not None:
            id = get_channel_id(config['BOTDATA']['CHANNEL_ANNONCE'])
            return bot.get_channel(id)


def is_abys():
    now = datetime.now()
    if now.day == 26:
        return True
    else:
        return False


def is_adim(ctx):
    perm = ctx.author.guild_permissions
    return perm.administrator


async def abys_function():
    already_annonce = False
    while True:
        if is_abys() and already_annonce is False:
            desc = "L'antre des abysses est réinitialisée aujourd'hui ! Bon jeu et Bonne chances dans les tréfonds :D"
            client.loop.create_task(on_reminder(desc))
            already_annonce = True
        else:
            already_annonce = False
            await asyncio.sleep(3600)


def predict_events(events_name):
    events = ["NAVIRE_MARCHANDS", "CIO", "MONSTRE", "RECHERCHE", "NAVIRE", "TACTICIEN", "EQUIPMENT", "BATIMENT"]
    events_date = []
    index = 0
    total = len(events)

    for e in events:
        index += 1
        if events_name == e:
            events.remove(e)
            events.insert(0, e)
            events_date.append(str(datetime.now().day) + "/" + str(datetime.now().month) + "/" + str(datetime.now().year))
            index += 1
            new_position = 1

            while index <= total:
                element = events[index - 1]
                events.remove(events[index - 1])
                events.insert(new_position, element)
                new_position += 1
                index += 1

    index = 1
    total = len(events)-1
    while index <= total:
        days = index * 2.5
        new_date = datetime.now() + timedelta(days=days)
        events_date.append(str(new_date.day) + "/" + str(new_date.month) + "/" + str(new_date.year))
        index += 1

    data = {'events': events, 'dates': events_date}
    dataFrame = pd.DataFrame(data=data)

    return dataFrame


# ////////////////////////// < GLOBAL FUNCTION > /////////////////////////////////////////

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='$', intents=intents)
client = discord.Client()
bot.timer_manager = timers.TimerManager(bot)


# ////////////////////////// < EVENT FUNCTION > /////////////////////////////////////////

@bot.event
async def on_ready():
    print("Bot Ready !")
    config = configparser.ConfigParser()
    config.read('config.ini')

    if config['ANNONCES']['GENERALE'] is not None and config['ANNONCES']['HOURS'] is not None:
        desc = config['ANNONCES']['GENERALE']
        hours = int(config['ANNONCES']['HOURS'])
        # client.loop.create_task(annonce_quotidienne(hours, desc))

    await bot.change_presence(activity=discord.Game('Tide of War'))
    # client.loop.create_task(abys_function())


@bot.event
async def on_member_join(member):
    desc = f"Un merveilleux pirates du nom de {member.mention}, nous rejoinds \n" \
           f"souhaiter lui la bienvenue avec un bon verre de rhum  \n\n" \
           f"N'oubliez pas les règles suivantes : \n" \
           f"1) Mettez un shield 24h avant d'aller dormir \n" \
           f"2) Vérifiez les Check in tout les jours \n" \
           f"3) Ne pas attaquez les batiments sous aucun prétexte sous peine d'exclusion \n"

    mbed = discord.Embed(
        colour=(discord.Colour.dark_blue()),
        title=f"Bienvenue chez LSB",
        description=desc
    )

    mbed.set_image(url="https://tel.img.pmdstatic.net/fit/http.3A.2F.2Fprd2-bone-image.2Es3-website-eu-west-1.2Eamazonaws.2Ecom.2FTEL.2F2019.2F09.2F20.2F4ef6192a-9f74-4f2b-a4ac-96b8cc01bc72.2Ejpeg/619x450/quality/65/pirates-des-caraibes-1-dans-la-saga-disney-tous-les-ingredients-d-un-film-de-pirates-sont-reunis-ici-le-rhum.jpg")
    welcome_channel = init_channel("welcome")
    await welcome_channel.send(embed=mbed)
    await member.send(embed=mbed)


@bot.event
async def on_member_remove(member):
    mbed = discord.Embed(
        colour=(discord.Colour.dark_blue()),
        title=f"LSB vous dit Aurevoir !",
        description=f"Nous vous remercions d'avoir participé dans notre alliance {member.mention} \n"
    )
    mbed.set_image(url="https://static1.terrafemina.com/articles/9/28/00/69/@/316508-anne-dieuleveut-622x0-2.jpg")
    goodbye_channel = init_channel("goodbye")
    await goodbye_channel.send(embed=mbed)
    await member.send(embed=mbed)


@bot.event
async def on_reminder(*text):
    textes = ""
    for t in text:
        textes += t

    desc = "@eveyone \n\n"
    desc += "Hello tout le monde je suis SharkyBot, je vous envoie ce message pour rappeller ceci : \n\n"
    desc += textes

    mbed = discord.Embed(
        colour=(discord.Colour.dark_blue()),
        title=f"Sharkybot Rappel ",
        description=desc
    )

    channel = init_channel("annonce")
    await channel.send(embed=mbed)

# ////////////////////////// < TIMER FUNCTION > /////////////////////////////////////////


@bot.command(name="remind")
async def remind(ctx, time, *, text):
    await ctx.channel.purge(limit=1)

    if is_adim(ctx):
        """Remind to do something on a date.
        The date must be in ``Y/M/D`` format."""
        date = datetime(*map(int, time.split("/")))
        bot.timer_manager.create_timer("reminder", date, args=text)
    else:
        await ctx.channel.send(f"SharkyBot dis que {ctx.author.mention} n'est pas authorisé a faire sa !")


@bot.command()
async def new_annonce(ctx, timers, *_desc):
    await ctx.channel.purge(limit=1)

    if is_adim(ctx):
        try:
            desc = ""
            for d in _desc:
                desc += d

            print(str(timers) + " " + str(desc))
            client.loop.create_task(global_annonce(int(timers), str(desc)))
        except ValueError:
            await ctx.channel.send("Commande non acceptée timer n'est pas un chiffre en secondes ! => $new_annnonce 120 annonce")
    else:
        await ctx.channel.send(f"SharkyBot dis que {ctx.author.mention} n'est pas authorisé a faire sa !")


async def global_annonce(_timers, _desc):
    while True:
        desc = "@eveyone \n\n"
        desc += "Hello tout le monde je suis SharkyBot, je vous envoie ce message pour rappeller ceci : \n\n"
        desc += _desc

        mbed = discord.Embed(
            colour=(discord.Colour.dark_blue()),
            title=f"Sharkybot Rappel ",
            description=desc
        )

        channel = init_channel("annonce")
        await channel.send(embed=mbed)
        await asyncio.sleep(_timers)


async def annonce_quotidienne(hours_global, _desc):
    annonce = False
    first_day = datetime.now().day

    while True:
        hours = datetime.now().hour
        day = datetime.now().day

        if day != first_day:
            first_day = day
            annonce = False

        if hours == hours_global and not annonce:

            desc = "@eveyone \n\n"
            desc += "Hello tout le monde je suis SharkyBot,\n Je vous rappelle ceci : \n\n"
            desc += _desc

            mbed = discord.Embed(
                colour=(discord.Colour.dark_blue()),
                title=f"Sharkybot Rappel ",
                description=desc
            )

            channel = init_channel("annonce")
            await clear_all(None, channel=channel)
            await channel.send(embed=mbed)
            annonce = True

        await asyncio.sleep(300)


# ////////////////////////// < COMMAND FUNCTION > /////////////////////////////////////////

@bot.command()
async def au_goulag_timer(ctx, username=None, _time=None):
    await ctx.channel.purge(limit=1)

    if is_adim(ctx):
        if _time is not None and username is not None:
            try:
                time = int(_time)
                client.loop.create_task(au_goulag(ctx, username, True))
                await asyncio.sleep(time)
                client.loop.create_task(remove_goulag(ctx, username, True))
            except ValueError:
                await ctx.channel.send("La commande n'est pas correcte utiliser $au_goulag_timer username seconds ")
            finally:
                pass
        else:
            await ctx.channel.send("La commande n'est pas correcte utiliser $au_goulag_timer username seconds ")
    else:
        await ctx.channel.send(f"SharkyBot dis que {ctx.author.mention} n'est pas authorisé a faire sa !")


@bot.command()
async def au_goulag(ctx, username=None, Remove=None):

    if Remove is None:
        await ctx.channel.purge(limit=1)

    if is_adim(ctx):
        if username is not None:
            member = get_member(username)
            role = get_role("goulag")
            role_lsb = get_role("lsb member")
            id = get_channel_id("au-goulag")
            channel = bot.get_channel(id)
            await member.add_roles(role)
            await member.remove_roles(role_lsb)
            await channel.send(f"L'utilisateur {member.mention} à été envoyé au goulag @everyone ")
    else:
        await ctx.channel.send(f"SharkyBot dis que {ctx.author.mention} n'est pas authorisé à faire sa !")


@bot.command()
async def remove_goulag(ctx, username=None, Remove=None):

    if Remove is None:
        await ctx.channel.purge(limit=1)

    if is_adim(ctx):
        if username is not None:
            member = get_member(username)
            role = get_role("goulag")
            role_lsb = get_role("lsb member")
            id = get_channel_id("au-goulag")
            channel = bot.get_channel(id)
            await member.remove_roles(role)
            await member.add_roles(role_lsb)
            await channel.send(f"L'utilisateur {member.mention} à été sortie du goulag @everyone ")
    else:
        await ctx.channel.send(f"SharkyBot dis que {ctx.author.mention} n'est pas authorisé a faire sa !")


@bot.command()
async def next_event(ctx, current_event=None):
    await ctx.channel.purge(limit=1)

    if current_event is not None:
        desc = "events    -    date de début \n\n"
        data = predict_events(current_event)
        total = len(data.events)
        index = 0

        while index < total:
            desc += data.events[index] + "    " + data.dates[index] + "\n\n"
            index += 1

        mbed = discord.Embed(
            colour=(discord.Colour.dark_blue()),
            title=f"Sharkybot : voici la liste des prochains events ",
            description=desc
        )
        await ctx.channel.send(embed=mbed)
    else:
        await ctx.channel.send("Si vous voulez savoir quel est le prochains events donnez moi l'évènement en cours \n"
                               "obtenez la liste des évents ICI $list_event ou $next_event BATIMENT")


@bot.command()
async def list_event(ctx):
    await ctx.channel.purge(limit=1)
    desc = ""
    data = predict_events("BATIMENT")
    for d in data.event:
        desc += d + " - "

    mbed = discord.Embed(
        colour=(discord.Colour.dark_blue()),
        title=f"Sharkybot : prédiction des évènements suivants : ",
        description=desc
    )
    await ctx.channel.send(embed=mbed)


@bot.command()
async def hello(ctx):
    await ctx.channel.purge(limit=1)
    await ctx.channel.send("Bonjour " + str(ctx.author.mention) + " !")


@bot.command()
async def ping(ctx, arg=None):
    await ctx.channel.purge(limit=1)

    if is_adim(ctx):
        if arg == "pong":
            await ctx.channel.send("Vous avez déjà Ping vous-même !")
        else:
            await ctx.channel.send(str(ctx.author.mention) + " Pong !")
    else:
        await ctx.channel.send(f"SharkyBot dis que {ctx.author.mention} n'est pas authorisé a faire sa !")


# ////////////////////////// < CLEAR FUNCTION > /////////////////////////////////////////


@bot.command()
async def clear_limit(ctx, arg):
    await ctx.channel.purge(limit=1)

    if is_adim(ctx):
        try:
            nb = int(arg)
            await ctx.channel.purge(limit=nb)
        except ValueError:
            await ctx.channel.send('commande impossible veuillez entrer un numéro ! => $clear_limit (number)')
        finally:
            pass
    else:
        await ctx.channel.send(f"SharkyBot dis que {ctx.author.mention} n'est pas authorisé a faire sa !")


@bot.command()
async def clear_channel(ctx, arg=None):
    await ctx.channel.purge(limit=1)

    if is_adim(ctx):
        if arg is None:
            ctx.channel.send('Veuillez entrer un channel ! Sinon je ne peut pas le nettoyer :)')
        else:
            try:
                id = get_channel_id(arg)
                channel = bot.get_channel(id)

                if type(channel) is not None:
                    await channel.purge()
                else:
                    ctx.channel.send('Channel introuvable veuillez entrer le bon channel !')
            except ValueError:
                ctx.channel.send('Channel introuvable veuillez entrer le bon channel !')
            finally:
                pass
    else:
        await ctx.channel.send(f"SharkyBot dis que {ctx.author.mention} n'est pas authorisé a faire sa !")


@bot.command()
async def clear_all(ctx, channel=None):
    if channel is None:
        await ctx.channel.purge(limit=1)

        if is_adim(ctx):
            await ctx.channel.purge()
        else:
            await ctx.channel.send(f"SharkyBot dis que {ctx.author.mention} n'est pas authorisé a faire sa !")
    else:
        await channel.purge()


bot.run('ODAxODkyNDU4ODMyMzMwNzcy.YAnSjA.PFnIRI4KVIPXbb66_Wl_YhwYMrA')
