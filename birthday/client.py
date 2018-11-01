import discord
import logging
from datetime import datetime
from discord.ext import commands
from .db import Session, GuildChannel, Birthday
from .repository import GuildChannelRepository, BirthdayRepository
from .util import strip_id_wrapper, wrap_channel_id, wrap_user_id

log = logging.getLogger(__name__)


class Client(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='!')
        self.add_command(self.add)
        self.add_command(self.channel)
        self.add_command(self.list)

        self.session = Session()
        self.guild_channel_repository = GuildChannelRepository(self.session)
        self.birthday_repository = BirthdayRepository(self.session)

    def add_guild_channel(self, guild_id, channel_id):
        """Adds an announcement channel if one does not already exist for the guild_id."""
        if not self.guild_channel_repository.exists(guild_id):
            guild_channel = GuildChannel(guild_id, channel_id)
            self.guild_channel_repository.save(guild_channel)

    def update_guild_channel(self, guild_id, channel_id):
        for guild_channel in self.guild_channel_repository.find_by(guild_id=guild_id):
            guild_channel.channel_id = channel_id
            self.guild_channel_repository.save(guild_channel)

    def add_birthday(self, date, guild_id, user_id):
        """Adds a birthday if one does not alreay exist for the guild_id and user_id combination."""
        if not self.birthday_repository.exists(guild_id, user_id):
            birthday = Birthday(date, guild_id, user_id)
            self.birthday_repository.save(birthday)

    @commands.command()
    async def add(self, ctx, user_id, iso_date):
        log.debug(f'add({user_id}, {iso_date})')
        date = None

        try:
            date = datetime.strptime(iso_date, '%Y-%m-%d')
        except ValueError:
            await ctx.send('Invalid date format. Must be YYYY-MM-DD.')
            return

        self.add_guild_channel(ctx.guild.id, ctx.channel.id)
        self.add_birthday(date, ctx.guild.id, strip_id_wrapper(user_id))

        await ctx.send(f"Added {user_id}'s birthday!")

    @commands.command()
    async def channel(self, ctx, channel_id):
        channel_id = strip_id_wrapper(channel_id)
        self.add_guild_channel(ctx.guild.id, channel_id)
        self.update_guild_channel(ctx.guild.id, channel_id)

        await ctx.send(f'Set announcement channel to: {wrap_channel_id(channel_id)}')

    @commands.command()
    async def list(self, ctx):
        guild_id = ctx.guild.id
        # TODO Extract session query
        for user_id, channel_id in self.session.query(Birthday.user_id, GuildChannel.channel_id).\
                filter(Birthday.guild_id == guild_id).\
                filter(GuildChannel.guild_id == guild_id):
            channel = self.get_channel(channel_id)
            await channel.send(f'Happy birthday {wrap_user_id(user_id)}!')
