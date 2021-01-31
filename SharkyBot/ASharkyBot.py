
from discord.ext import commands
import re
from datetime import datetime


class ASharkyBot(commands.Bot):

    def __init__(self, command_prefix, **options):
        super().__init__(command_prefix, **options)
        self.abyss_day = 26

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


