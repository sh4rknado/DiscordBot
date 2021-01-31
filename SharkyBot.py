
from SharkyBot.ASharkyBot import ASharkyBot
from discord.ext import timers
import discord
from datetime import datetime
import asyncio


class SharkyBot:
    def __init__(self):
        intents = discord.Intents.all()
        intents.members = True
        self.bot = ASharkyBot(command_prefix='$', intents=intents)
        self.client = discord.Client()
        self.bot.timer_manager = timers.TimerManager(self.bot)
        self.abyss_annonce = False

        # ////////////////////////// < EVENT FUNCTION > /////////////////////////////////////////

        @self.bot.event
        async def on_ready():
            await self.bot.change_presence(activity=discord.Game('Tide of War'))
            self.bot.loop.create_task(abys_function())
            self.bot.loop.create_task(annonce_quotidienne())
            print("Bot Ready !")

        @self.bot.event
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
            await self.bot.welcom_channel.send(embed=mbed)
            await member.send(embed=mbed)

        @self.bot.event
        async def on_member_remove(member):
            mbed = discord.Embed(
                colour=(discord.Colour.dark_blue()),
                title=f"LSB vous dit Aurevoir !",
                description=f"Nous vous remercions d'avoir participé dans notre alliance {member.mention} \n"
            )
            mbed.set_image(url="https://static1.terrafemina.com/articles/9/28/00/69/@/316508-anne-dieuleveut-622x0-2.jpg")
            await self.bot.goodbye_channel.send(embed=mbed)

        @self.bot.event
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
            await self.bot.annonce_channel.send(embed=mbed)

        # ////////////////////////// < COMMAND FUNCTION > /////////////////////////////////////////

        @self.bot.command()
        async def au_goulag_timer(ctx, username=None, _time=None):
            await ctx.channel.purge(limit=1)

            if self.bot.is_admin(ctx):
                if _time is not None and username is not None:
                    try:
                        time = int(_time)
                        self.bot.loop.create_task(au_goulag(ctx, username, True))
                        await asyncio.sleep(time)
                        self.bot.loop.create_task(remove_goulag(ctx, username, True))
                    except ValueError:
                        await ctx.channel.send(
                            "La commande n'est pas correcte utiliser $au_goulag_timer username seconds ")
                    finally:
                        pass
                else:
                    await ctx.channel.send("La commande n'est pas correcte utiliser $au_goulag_timer username seconds ")
            else:
                await ctx.channel.send(f"SharkyBot dis que {ctx.author.mention} n'est pas authorisé a faire sa !")

        @self.bot.command()
        async def au_goulag(ctx, username=None, Remove=None):

            if Remove is None:
                await ctx.channel.purge(limit=1)

            if self.bot.is_admin(ctx):
                if username is not None:
                    member = self.bot.get_member(username)
                    role = self.bot.get_role("GOULAG")
                    role_lsb = self.bot.get_role("lsb menber")
                    id = self.bot.get_channel_id("au-goulag")
                    channel = self.bot.get_channel(id)
                    await member.add_roles(role)
                    await member.remove_roles(role_lsb)
                    await channel.send(f"L'utilisateur {member.mention} à été envoyé au goulag @everyone ")
            else:
                await ctx.channel.send(f"SharkyBot dis que {ctx.author.mention} n'est pas authorisé à faire sa !")

        @self.bot.command()
        async def remove_goulag(ctx, username=None, Remove=None):

            if Remove is None:
                await ctx.channel.purge(limit=1)

            if self.bot.is_admin(ctx):
                if username is not None:
                    member = self.bot.get_member(username)
                    role = self.bot.get_role("GOULAG")
                    role_lsb = self.bot.get_role("lsb menber")
                    id = self.bot.get_channel_id("au-goulag")
                    channel = self.bot.get_channel(id)
                    await member.remove_roles(role)
                    await member.add_roles(role_lsb)
                    await channel.send(f"L'utilisateur {member.mention} à été sortie du goulag @everyone ")
            else:
                await ctx.channel.send(f"SharkyBot dis que {ctx.author.mention} n'est pas authorisé a faire sa !")

        @self.bot.command()
        async def hello(ctx):
            await ctx.channel.purge(limit=1)
            await ctx.channel.send("Bonjour " + str(ctx.author.mention) + " !")

        @self.bot.command()
        async def get_members(ctx):
            await ctx.channel.purge(limit=1)
            members = ""
            if self.bot.is_admin(ctx):
                for guild in self.bot.guilds:
                    for m in guild.members:
                        members += m.name + " - "
                await ctx.channel.send("members : " + members)
            else:
                await ctx.channel.send(f"SharkyBot dis que {ctx.author.mention} n'est pas authorisé a faire sa !")

        @self.bot.command()
        async def ping(ctx, arg=None):
            await ctx.channel.purge(limit=1)

            if self.bot.is_admin(ctx):
                if arg == "pong":
                    await ctx.channel.send("Vous avez déjà Ping vous-même !")
                else:
                    await ctx.channel.send(str(ctx.author.mention) + " Pong !")
            else:
                await ctx.channel.send(f"SharkyBot dis que {ctx.author.mention} n'est pas authorisé a faire sa !")

        # ////////////////////////// < CLEAR FUNCTION > /////////////////////////////////////////

        @self.bot.command()
        async def clear_limit(ctx, arg):
            await ctx.channel.purge(limit=1)
            if self.bot.is_admin(ctx):
                try:
                    nb = int(arg)
                    await ctx.channel.purge(limit=nb)
                except ValueError:
                    await ctx.channel.send('commande impossible veuillez entrer un numéro ! => $clear_limit (number)')
                finally:
                    pass
            else:
                await ctx.channel.send(f"SharkyBot dis que {ctx.author.mention} n'est pas authorisé a faire sa !")

        @self.bot.command()
        async def clear_channel(ctx, arg=None):
            await ctx.channel.purge(limit=1)

            if self.bot.is_admin(ctx):
                if arg is None:
                    ctx.channel.send('Veuillez entrer un channel ! Sinon je ne peut pas le nettoyer :)')
                else:
                    try:
                        id = self.bot.get_channel_id(arg)
                        channel = self.bot.get_channel(id)
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

        @self.bot.command()
        async def clear_all(ctx, channel=None):
            await self.bot.clear_all(ctx=ctx, channel=channel)

        # ////////////////////////// < TIMER FUNCTION > /////////////////////////////////////////

        @self.bot.command(name="remind")
        async def remind(ctx, time, *, text):
            await ctx.channel.purge(limit=1)

            if self.bot.is_admin(ctx):
                """Remind to do something on a date.
                The date must be in ``Y/M/D`` format."""
                date = datetime(*map(int, time.split("/")))
                self.bot.timer_manager.create_timer("reminder", date, args=text)
            else:
                await ctx.channel.send(f"SharkyBot dis que {ctx.author.mention} n'est pas authorisé a faire sa !")

        @self.bot.command()
        async def new_annonce(ctx, timers, *_desc):
            await ctx.channel.purge(limit=1)

            if self.bot.is_admin(ctx):
                try:
                    desc = ""
                    for d in _desc:
                        desc += d

                    print(str(timers) + " " + str(desc))
                    self.bot.loop.create_task(self.bot.global_annonce(int(timers), str(desc)))
                except ValueError:
                    await ctx.channel.send(
                        "Commande non acceptée timer n'est pas un chiffre en secondes ! => $new_annnonce 120 annonce")
            else:
                await ctx.channel.send(f"SharkyBot dis que {ctx.author.mention} n'est pas authorisé a faire sa !")

        # ////////////////////////// < EVENTS FUNCTION > /////////////////////////////////////////

        async def abys_function():
            self.abyss_annonce = False
            while True:
                if self.bot.is_abyss() and self.abyss_annonce is False:
                    desc = "L'antre des abysses est réinitialisée aujourd'hui ! Bon jeu et Bonne chances dans les tréfonds :D"
                    self.bot.loop.create_task(on_reminder(desc))
                    self.abyss_annonce = True
                else:
                    self.abyss_annonce = False
                    # Waitting 24H
                    await asyncio.sleep(86400)

        async def annonce_quotidienne():
            self.bot.annonce_quotidienne = False
            next_day = datetime.now().day

            while True:
                hours = datetime.now().hour
                day = datetime.now().day

                if day == next_day and hours == self.bot.hours_annonce_quotidienne and self.bot.annonce_quotidienne is False:
                    print("Il est 16H00 je dois faire une annonce !")

                    desc = "@eveyone \n\n"
                    desc += "Hello tout le monde je suis SharkyBot,\n Je vous rappelle ceci : \n\n"
                    desc += self.bot.desc_annonce_quotidienne

                    mbed = discord.Embed(
                        colour=(discord.Colour.dark_blue()),
                        title=f"Sharkybot Rappel ",
                        description=desc
                    )

                    await self.bot.clear_all(channel=self.bot.annonce_channel)
                    self.bot.annonce_channel.send(embed=mbed)
                    self.bot.annonce_quotidienne = True
                    await asyncio.sleep(300)

                elif day != next_day:
                    print("Le jour quotidien a changé !")
                    next_day = day
                    self.bot.annonce_quotidienne = False

        # @self.bot.command()
        # async def next_event(ctx, current_event=None):
        #     await ctx.channel.purge(limit=1)
        #
        #     if current_event is not None:
        #         desc = "events    -    date de début \n\n"
        #         data = self.predict_events(current_event)
        #         total = len(data.events)
        #         index = 0
        #
        #         while index < total:
        #             desc += data.events[index] + "    " + data.dates[index] + "\n\n"
        #             index += 1
        #
        #         mbed = discord.Embed(
        #             colour=(discord.Colour.dark_blue()),
        #             title=f"Sharkybot : voici la liste des prochains events ",
        #             description=desc
        #         )
        #         await ctx.channel.send(embed=mbed)
        #     else:
        #         await ctx.channel.send(
        #             "Si vous voulez savoir quel est le prochains events donnez moi l'évènement en cours \n"
        #             "obtenez la liste des évents ICI $list_event ou $next_event BATIMENT")

        # @self.bot.command()
        # async def list_event(ctx):
        #     await ctx.channel.purge(limit=1)
        #     desc = ""
        #     data = predict_events("BATIMENT")
        #     for d in data.event:
        #         desc += d + " - "
        #
        #     mbed = discord.Embed(
        #         colour=(discord.Colour.dark_blue()),
        #         title=f"Sharkybot : prédiction des évènements suivants : ",
        #         description=desc
        #     )
        #     await ctx.channel.send(embed=mbed)

    def running_bot(self):
        self.bot.run(self.bot.token)


if __name__ == '__main__':
    bot = SharkyBot()
    bot.running_bot()
