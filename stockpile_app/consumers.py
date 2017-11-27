from channels import Channel, Group
from channels.sessions import channel_session
from channels.auth import channel_session_user, channel_session_user_from_http

# Connected to websocket.connect
@channel_session_user_from_http
def ws_add(message):
    message.reply_channel.send({"accept": True})
    # Add them to the right group
    Group("notif").add(message.reply_channel)

# Connected to websocket.disconnect
@channel_session_user_from_http
def ws_disconnect(message):
    Group("notif").discard(message.reply_channel)