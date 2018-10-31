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
        self.announcement_channels = {}
        self.birthdays = {}

    def add_announcement_channel(self, guild_id, channel_id):
        if guild_id not in self.announcement_channels:
            self.announcement_channels[guild_id] = channel_id

    def add_birthday(self, date, guild_id, user_id):
        # Create list of birthdays for the date if one doesn't already exist
        if date not in self.birthdays:
            self.birthdays[date] = []

        self.birthdays[date].append((guild_id, user_id))

    @commands.command()
    async def add(self, ctx, user_id, iso_date):
        log.debug(f'add({user_id}, {iso_date})')
        date = None

        try:
            date = datetime.strptime(iso_date, '%Y-%m-%d')
        except ValueError:
            await ctx.send('Invalid date format. Must be YYYY-MM-DD.')
            return

        self.add_announcement_channel(ctx.guild.id, ctx.channel.id)
        self.add_birthday(date, ctx.guild.id, user_id)

        await ctx.send(f'Added {user_id}\'s birthday!')

    @commands.command()
    async def channel(self, ctx, channel_id):
        self.add_announcement_channel(ctx.guild.id, channel_id)

        await ctx.send(f'Set announcement channel to: {channel_id}')

    @commands.command()
    async def list(self, ctx):
        for birthday in self.birthdays:
            birthdays = self.birthdays[birthday]

            for (guild_id, user_id) in birthdays:
                channel_id = self.announcement_channels[guild_id]
                channel = self.get_channel(channel_id)
                await channel.send(f'Happy birthday {user_id}!')
