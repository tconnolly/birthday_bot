def strip_id_wrapper(id):
    """Trim the Discord channel ID formatting <#123456789>/<@123456789>."""
    return id[2:-1]


def wrap_user_id(user_id):
    """Wrap user ID for mention in Discord message."""
    return f'<@{user_id}>'


def wrap_channel_id(channel_id):
    """Wrap channel ID for mention in Discord message."""
    return f'<#{channel_id}>'
