from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class GuildChannel(Base):
    __tablename__ = 'guild_channels'

    id = Column(Integer, primary_key=True)
    guild_id = Column(Integer)
    channel_id = Column(Integer)

    def __init__(self, guild_id, channel_id):
        self.guild_id = guild_id
        self.channel_id = channel_id


class Birthday(Base):
    __tablename__ = 'birthdays'

    id = Column(Integer, primary_key=True)
    date = Column(String)
    guild_id = Column(Integer)
    user_id = Column(String)

    def __init__(self, date, guild_id, user_id):
        self.date = date
        self.guild_id = guild_id
        self.user_id = user_id


# Create an engine that stores data in the local directory's
# birthday_bot.db file.
engine = create_engine('sqlite:///birthday_bot.db')

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
