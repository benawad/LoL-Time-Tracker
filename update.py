import requests
from datetime import *
import time


def get_match_id(text):
    loc1 = text.find('[')
    loc2 = text.find(']')
    return text[loc1 + 1:loc2]


def get_champion(id, api):
    r = requests.get('https://na.api.pvp.net/api/lol/static-data/na/v1.2/champion/' + str(id) + '?api_key=' + api)
    data = r.json()
    return data['name']


def get_id(summoner, api):
    r = requests.get('https://na.api.pvp.net/api/lol/na/v1.4/summoner/by-name/' + summoner + '?api_key=' + api)
    return str(r.json()[summoner]['id'])


def update(summoner, api, storage_file):
    try:
        games_file = open(storage_file, 'r+')
    except:
        writeFile = open(storage_file, 'w')
        writeFile.close()
        games_file = open(storage_file, 'r+')

    summoner_id = get_id(summoner, api)

    lol_games = requests.get(
        'https://na.api.pvp.net/api/lol/na/v1.3/game/by-summoner/' + summoner_id + '/recent?api_key=' + api)
    last_10 = lol_games.json()

    lines = games_file.readlines()

    games = []
    ids = []
    is_update = False

    for line in lines:
        ids.append(get_match_id(line))

    for match in last_10['games']:
        matchid = str(match['gameId'])
        if matchid in ids:
            pass
        else:
            game_page = requests.get('https://na.api.pvp.net/api/lol/na/v2.2/match/' + matchid + '?api_key=' + api)
            game_info = game_page.json()
            is_update = True
            s_game = ''

            # match id
            s_game += '[' + matchid + ']'
            # match duration
            s_game += ' Duration: ' + str(float(game_info['matchDuration'] / 60))

            s_game += ' Happened: ' + str(date.fromtimestamp(match['createDate'] / 1000.0))

            s_game += ' (' + str(game_info['matchDuration']) + ') {' + str(
                date.fromtimestamp(match['createDate'] / 1000.0).day) + '}'

            games.append(s_game)

            time.sleep(5)

    for game in games:
        games_file.write(game + '\n')

    games_file.close()
    return is_update