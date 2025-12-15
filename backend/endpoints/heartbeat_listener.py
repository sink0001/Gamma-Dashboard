from flask import Blueprint, request

heart_beat_listener = Blueprint("heart_beat_listener", __name__)


@heart_beat_listener.route("/heartbeat", methods=["POST"])
def let_session_live():
    '''
    Decode the requests content using the decode_session_cookie() function
    in backend.utils.cookie_utils and then extend the redis key that matches
    that cookies id by heartbeat interval + 1 second
    '''
    data = request.get_json()
    return ""