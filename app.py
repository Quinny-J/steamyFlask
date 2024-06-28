# I'm still learning python. 
# Don't judge me harshly :)
# Made by @Quinny-J
# 27/06/2024

# if you have it installed but get an error run the last line in term
# pip install requests
# python -m pip install requests

# References 
# Flask - https://flask.palletsprojects.com/en/3.0.x/
# Steam API - https://developer.valvesoftware.com/wiki/Steam_Web_API#GetPlayerSummaries_.28v0001.29
# Requests LIB - https://requests.readthedocs.io/en/latest/
# Discord Webhook Lib - https://pypi.org/project/discord-webhook/#basic-webhook

# Import Libs
import requests

from flask import Flask, request

from discord_webhook import DiscordWebhook

app = Flask(__name__)

# Class is being used to store multiple vars in a catagory in this case strings
class statusColors:
    OKCYAN = '\033[96m' # Python likes ANSI :)
    WARN = '\033[91m'
    WHITE = '\033[0m'

# Class is being used to store multiple vars in a catagory in this case fstrings
class statusMsg:
    UI = f'\033[0m[{statusColors.OKCYAN}UI{statusColors.WHITE}]'
    OK = f'\033[0m[{statusColors.OKCYAN}OK{statusColors.WHITE}]'
    WARN = f'\033[0m[{statusColors.WARN}WARN{statusColors.WHITE}]'

# Define our function
# get_player_summaries(api_key, steam_id) Returns Games/Player Summary
def get_player_summaries(api_key, steam_id):
    base_url = "https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/"
    params = {
        "key": api_key,
        "steamids": steam_id
    }

    # Make a request with the params provided to the func
    response = requests.get(base_url, params=params)
    
    # Check for 200.ok which means success if not something is wrong
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"{statusMsg.WARN} Failed to fetch data. Status code: {response.status_code}")
        return None    

# GET 127.0.0.1:5000/grab/?api_key=APIKEY&steam_id=STEAMID
@app.route('/grab/', methods=['GET'])
def do_steam():

    # set the api key for steams api
    api_key = request.args.get('api_key')
    # set the steam id to scrape data from
    steam_id = request.args.get('steam_id')

    class steamStuff:
        steamData = get_player_summaries(api_key,steam_id)

    class steamUser:
        player_info = steamStuff.steamData.get("response", {}).get("players", [{}])[0] 
        avatar = player_info.get("avatar", "")
        avatarMed = player_info.get("avatarmedium", "")
        profileurl = player_info.get("profileurl", "")
        personaname = player_info.get("personaname", "")
        country = player_info.get("loccountrycode", "")

    
    # Set Webhook url and message to send
    webhook = DiscordWebhook(url="https://discord.com/api/webhooks/1256163384974381110/pMr3eppqjchqHt6pIyBMwag9g_jhoAJUqwbYBXJGw2SbBJY4AEfv-phY8Y8lmSLafamq", content="We have a request for " + steam_id)
    # Make the request we can also return the response for debugging
    response = webhook.execute()

    if response.status_code == 200:
        print(f"{statusMsg.OK} Webhook Sent")
    else:
        print(f"{statusMsg.WARN} Webhook Failed")
    
    # Debugging purpose to see if everything was being scraped
    print(f"{statusMsg.OK} Avatar: {steamUser.avatar}")
    print(f"{statusMsg.OK} AvatarMedUrl: {steamUser.avatarMed}")
    print(f"{statusMsg.OK} Profile URL: {steamUser.profileurl}")
    print(f"{statusMsg.OK} Personaname: {steamUser.personaname}")
    print(f"{statusMsg.OK} Base Location: {steamUser.country}")

    # Return some html to display on the browser end
    return f"""
    <h1>Information Grabbed</h1>
    <img src="{steamUser.avatarMed}">
    <br>
    <p><font color=green>Hello</font>,
    We have found <font color=gold>{steamUser.personaname}</font> who is located at <font color=red>{steamUser.country}</font>
    <br>
    <a href="{steamUser.profileurl}"> View Profile </a>
    </p>
    <hr>
    <h2>Raw Response</h2>
    <p><code>{steamUser.player_info}</code>
    <footer>github.com/quinny-j</footer>
    """
