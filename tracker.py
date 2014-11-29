from update import update
from twilio.rest import TwilioRestClient
from datetime import date
import time

account_sid = "ACe55c9f31f8281a9005adf51931c1998a"
auth_token = ''
client = TwilioRestClient(account_sid, auth_token)
lol_api_key = ''

SUMMONER_NAME = ''
SCREEN_TIME = 2
SCREEN_TIME_SEC = SCREEN_TIME * 60 * 60
TWILIO_PHONE_NUMBER = ''
YOUR_PHONE_NUMBER = ''
STORAGE_FILE = SUMMONER_NAME + '_games.txt'

def get_dur(text):
    loc1 = text.find('(')
    loc2 = text.find(')')
    return text[loc1+1:loc2]


def get_date(text):
    loc1 = text.find('{')
    loc2 = text.find('}')
    return text[loc1+1:loc2]


def get_time():
    games_today = []
    games_file = open(STORAGE_FILE, 'r')
    game_data = games_file.readlines()
    games_file.close()

    for game in game_data:
        if get_date(game) == str(date.today().day):
            games_today.append(get_dur(game))

    total = 0
    for game in games_today:
        total += int(game)

    return total


while True:
    new_game = update(SUMMONER_NAME, lol_api_key, STORAGE_FILE)
    if new_game:
        time_left = SCREEN_TIME_SEC - get_time()
        if time_left < 0:
            exact = float(abs(time_left)) / float(60)
            seconds = int((exact - int(exact)) * 60)
            minutes = int(exact)
            text = "You are " + str(minutes) + " minutes and " + str(seconds) + " seconds over your " + str(SCREEN_TIME) + ' hour screen time.'
            message = client.sms.messages.create(body=text, to=YOUR_PHONE_NUMBER, from_=TWILIO_PHONE_NUMBER)
            print "Text sent!"

    time.sleep(2*60)