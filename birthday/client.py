import discord
import logging
from birthday.db import Session, AnnouncementChannel, Birthday
from datetime import datetime
from discord.ext import commands

log = logging.getLogger(__name__)


class BirthdayClient(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='!')
        self.add_command(self.add)
        self.add_command(self.channel)
        self.add_command(self.list)
        self.session = Session()

    def add_announcement_channel(self, guild_id, channel_id):
        """Adds an announcement channel if one does not already exist for the guild_id."""
        if self.session.query(AnnouncementChannel).filter_by(guild_id=guild_id).first() == None:
            self.session.add(AnnouncementChannel(guild_id, channel_id))
            self.session.commit()

    def update_announcement_channel(self, guild_id, channel_id):
        for announcement_channel in self.session.query(AnnouncementChannel).filter_by(guild_id=guild_id):
            announcement_channel.channel_id = channel_id
            self.session.add(announcement_channel)
            self.session.commit()

    def add_birthday(self, date, guild_id, user_id):
        """Adds a birthday if one does not alreay exist for the guild_id and user_id combination."""
        if self.session.query(Birthday).filter_by(guild_id=guild_id, user_id=user_id).first() == None:
            self.session.add(Birthday(date, guild_id, user_id))
            self.session.commit()

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
        # Trim the Discord user ID formatting <@123456789>
        self.add_birthday(date, ctx.guild.id, user_id[2:-1])

        await ctx.send(f'Added {user_id}\'s birthday!')

    @commands.command()
    async def channel(self, ctx, channel_id):
        # Trim the Discord channel ID formatting <#123456789>
        channel_id = channel_id[2:-1]
        self.add_announcement_channel(ctx.guild.id, channel_id)
        self.update_announcement_channel(ctx.guild.id, channel_id)

        await ctx.send(f'Set announcement channel to: <#{channel_id}>')

    @commands.command()
    async def list(self, ctx):
        for user_id, channel_id in self.session.query(Birthday.user_id, AnnouncementChannel.channel_id).\
                filter(Birthday.guild_id == ctx.guild.id).\
                filter(AnnouncementChannel.guild_id == ctx.guild.id):

            channel = self.get_channel(channel_id)
            await channel.send(f'Happy birthday <@{user_id}>!')
