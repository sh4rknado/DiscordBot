
from SharkyBot.ASharkyBot import ASharkyBot
from discord.ext import timers
import discord


class SharkyBot:
    def __init__(self):
        intents = discord.Intents.all()
        self.bot = ASharkyBot(command_prefix='$', intents=intents)
        self.client = discord.Client()
        self.bot.timer_manager = timers.TimerManager(self.bot)

        # ////////////////////////// < EVENT FUNCTION > /////////////////////////////////////////

        @self.bot.event
        async def on_ready():
            await self.bot.change_presence(activity=discord.Game('Tide of War'))
            print("Bot Ready !")

    def running_bot(self, token):
        self.bot.run(token)


if __name__ == '__main__':
    bot = SharkyBot()
    bot.running_bot('')
