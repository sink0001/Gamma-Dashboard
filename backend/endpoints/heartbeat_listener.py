from flask import Blueprint, session
from backend.coordinators.Cache_handler import Cache_handler

heart_beat_listener = Blueprint("heart_beat_listener", __name__)


@heart_beat_listener.route("/heartbeat", methods=["POST"])
def let_session_live():
    '''
    If the heartbeat is received update the time to live for the redis key
    that is the session id to extend its lifetime if the session dies the
    key will die naturally and redis wont be clogged up
    '''
    cache_handler = Cache_handler()
    session_id = session["session_id"]
    heartbeat_interval = 60

    if cache_handler.check_key_presence(session_id):
        cache_handler.set_key_time_to_live(session_id, heartbeat_interval+1)
    return ""