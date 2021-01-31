import asyncio

from discord.ext import commands
import re
from datetime import datetime
import os
from configparser import ConfigParser
import discord


class ASharkyBot(commands.Bot):

    def __init__(self, command_prefix, **options):
        super().__init__(command_prefix, **options)
        self.goodbye_channel = None
        self.goodbye_channel_img = None
        self.welcom_channel = None
        self.welcom_channel_img = None
        self.annonce_channel = None
        self.abyss_day = None
        self.token = None
        self.init()

    # ////////////////////////// < INIT FUNCTION > /////////////////////////////////////////

    def init(self):
        if os.path.isfile('data/config.ini'):
            config = ConfigParser()
            config.read('data/config.ini')
            self.welcom_channel = self.get_channel(self.get_channel_id(config['BOTDATA']['WELCOME_CHANNEL']))
            self.goodbye_channel = self.get_channel(self.get_channel_id(config['BOTDATA']['GOODBYE_CHANNEL']))
            self.annonce_channel = self.get_channel(self.get_channel_id(config['BOTDATA']['CHANNEL_ANNONCE']))
            self.welcom_channel_img = config['BOTDATA']['WELCOME_CHANNEL_IMG']
            self.goodbye_channel_img = config['BOTDATA']['GOODBYE_CHANNEL_IMG']
            self.command_prefix = config['BOTDATA']['PREFIX']
            self.abyss_day = config['BOTDATA']['ABYSS_DAY']
            self.token = str(config['BOTDATA']['TOKEN'])
        else:
            print("File not found : config.ini ")

    # ////////////////////////// < HELPERS FUNCTION > /////////////////////////////////////////

    def get_channel_id(self, name):
        for guild in self.guilds:
            for channel in guild.channels:
                if channel.name == name:
                    return channel.id

    def get_user_id(self, name):
        for guild in self.guilds:
            for m in guild.members:
                if m.name == name:
                    return m.id

    def get_member(self, name):
        members = self.get_all_members()

        if "@" in name:
            name = re.findall(r'\d+', name)
            id = int(name[0])
            for m in members:
                print(m.name)
                if m.id == id:
                    return m

        for m in members:
            if m.name == name:
                return m

    def get_role(self, name):
        for guild in self.guilds:
            for r in guild.roles:
                if r.name == name:
                    return r

    def is_abyss(self):
        now = datetime.now()
        if now.day == self.abyss_day:
            return True
        else:
            return False

    def is_admin(self, ctx):
        perm = ctx.author.guild_permissions
        return perm.administrator

    async def clear_all(self, ctx, channel=None):
        if channel is None:
            await ctx.channel.purge(limit=1)

            if self.is_admin(ctx):
                await ctx.channel.purge()
            else:
                await ctx.channel.send(f"SharkyBot dis que {ctx.author.mention} n'est pas authorisé a faire sa !")
        else:
            await channel.purge()

    # ////////////////////////// < ANNONCES FUNCTION > /////////////////////////////////////////

    async def annonce(self, message):
        desc = "@eveyone \n\n"
        desc += "Hello tout le monde je suis SharkyBot, je vous envoie ce message pour rappeller ceci : \n\n"
        desc += message

        mbed = discord.Embed(
            colour=(discord.Colour.dark_blue()),
            title=f"Sharkybot Annonce",
            description=desc
        )

        await self.annonce_channel.send(embed=mbed)

    async def global_annonce(self, _timers, _desc):
        while True:
            desc = "@eveyone \n\n"
            desc += "Hello tout le monde je suis SharkyBot, je vous envoie ce message pour rappeller ceci : \n\n"
            desc += _desc

            mbed = discord.Embed(
                colour=(discord.Colour.dark_blue()),
                title=f"Sharkybot Rappel ",
                description=desc
            )

            await self.annonce_channel.send(embed=mbed)
            await asyncio.sleep(_timers)

    async def annonce_quotidienne(self, hours_global, _desc):
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

                await self.clear_all(None, channel=self.annonce_channel)
                await self.annonce_channel.send(embed=mbed)
                annonce = True
            await asyncio.sleep(300)
