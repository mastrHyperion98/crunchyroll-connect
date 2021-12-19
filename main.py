"""
Created by: Steven Smith (aka mastr_hyperion98)

This is the main script used for examples and testing the request calls. 

"""
import time
import json

from crunchyroll_connect.server import CrunchyrollServer
from ffpyplayer.player import MediaPlayer

if __name__ == "__main__":

    creds = None
    with open('creds.json') as f:
        creds = json.load(f)

    server = CrunchyrollServer()

    server.start_session()
    response = server.login(creds['account'], creds['password'])
    steins_gate_id = server.get_series_id('Re:Zero')

    collection = server.get_collections(steins_gate_id)
    episodes = server.get_episodes(collection[-1].collection_id)
    episode_id = episodes[0].media_id
    stream_data = server.get_stream(episode_id)
    url = stream_data['streams'][0]['url']

    """
    player = MediaPlayer(url)
    while 1:
        frame, val = player.get_frame()
        if val == 'eof':
            break
        elif frame is None:
            time.sleep(0.01)
        else:
            img, t = frame
            print(val, t, img.get_pixel_format(), img.get_buffer_size())
            time.sleep(val)
    """

    #logout = server.logout()
    print(url)
    server.close()
