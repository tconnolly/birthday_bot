from .db import Birthday, GuildChannel


class BaseRepository(object):
    def __init__(self, db_session, entity):
        self.session = db_session
        self.entity = entity

    def query(self, query):
        return self.session.\
            query(query)

    def find_by(self, **kwargs):
        return self.\
            query(self.entity).\
            filter_by(**kwargs)

    def save(self, entity):
        self.session.add(entity)
        self.session.commit()


class GuildChannelRepository(BaseRepository):
    def __init__(self, db_session):
        super().__init__(db_session, GuildChannel)

    def exists(self, guild_id):
        return self.find_by(guild_id=guild_id).first() != None

    def find_channel_id_by_guild_id(self, guild_id):
        return self.\
            query(GuildChannel.channel_id).\
            filter_by(guild_id=guild_id).\
            first()


class BirthdayRepository(BaseRepository):
    def __init__(self, db_session):
        super().__init__(db_session, Birthday)

    def exists(self, guild_id, user_id):
        return self.find_by(guild_id=guild_id, user_id=user_id).first() != None

    def find_user_id_by_guild_id(self, guild_id):
        return self.\
            query(Birthday.user_id).\
            filter_by(guild_id=guild_id)
