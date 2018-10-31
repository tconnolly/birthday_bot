import discord
import logging
from datetime import datetime
from discord.ext import commands

log = logging.getLogger(__name__)


class BirthdayClient(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='!')
        self.add_command(self.add)
        self.add_command(self.list)
        self.birthdays = {}

    def add_birthday(self, date, channel_id, user_id):
        # Create list of birthdays for the date if one doesn't already exist
        if date not in self.birthdays:
            self.birthdays[date] = []

        self.birthdays[date].append((channel_id, user_id))

    @commands.command()
    async def add(self, ctx, user_id, iso_date):
        log.debug(f'add({user_id}, {iso_date})')
        date = None

        try:
            date = datetime.strptime(iso_date, '%Y-%m-%d')
        except ValueError:
            await ctx.send('Invalid date format. Must be YYYY-MM-DD.')
            return

        self.add_birthday(date, ctx.channel.id, user_id)

        ctx.send(f'Added {user_id}\'s birthday!')

    @commands.command()
    async def list(self, ctx):
        for birthday in self.birthdays:
            channels = self.birthdays[birthday]

            for (channel_id, user_id) in channels:
                channel = self.get_channel(channel_id)
                await channel.send(f'Happy birthday {user_id}!')
