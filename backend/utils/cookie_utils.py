import zlib
import base64


def decode_session_cookie(cookie):
    try:
        payload = cookie[1:]
        data = payload.split(".")[0]
        data = base64.urlsafe_b64decode(data)
        data = zlib.decompress(data)
        return data.decode("utf-8")
    
    except Exception as e:
        return "[Decoding error: are you sure this was a Flask session cookie? {}]".format(e)