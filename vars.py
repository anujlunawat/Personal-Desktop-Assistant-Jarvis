# used to get the list of songs in the Music dir
from os import listdir, getenv
from os.path import isfile, join
# used in by variable
from selenium.webdriver.common.by import By

# name of the user
USER = "Anuj"

# list of all the songs in the Music dir
mypath = fr"C:\Users\{getenv('username')}\Music\\"
songs = [f for f in listdir(mypath) if isfile(join(mypath, f))]

# noError variable used if any error raised when performing operations on driver (selenium webdriver)
noError = True

# search by element
by = [By.NAME, By.ID, By.CLASS_NAME]

# name of sites currently accesible
sites = {"youtube": "https://www.youtube.com", "google": "https://www.google.com",
             "wikipedia": "https://www.wikipedia.com",
             "instagram": "https://www.instagram.com", "geeksforgeeks": "https://www.geeksforgeeks.org",
             "facebook": "https://www.facebook.com"}

# weather parameters from weather.py
weather_parameters = ['weather'],# 'temperature', 'sky', 'region', 'country', 'local_Time', 'time', 'local_Date', 'date', 'wind_Speed', 'humidity', 'air_Quality']

# tryTillEnd() function
cannotHearResponse = ["I couldn't hear you. Please speak again!", "I was onto something else. What were you saying meanwhile?", "Could you please repeat?", "Did you say something?", "It's so quiet around here. I can hear you breathe", "Hey! I'm listening", "Hey, could you hit the replay button? I missed what you said."]

# used in fetching important points of prompt for news
s = f""" Reply to these 3 points as in one word as instructed, separated by commas
1. State the 2-letter ISO 3166-1 code of the country in the prompt below, if country name present, else reply with 'False'.
2. State the keyword or a phrase, from the prompt below. If no keyword or phrase, reply 'False'. The keywords should not be a country.
3. Any category, such as entertainment, health, science, sports, technology, in the prompt below. If no such category present, reply "False"
prompt:
"""

# nums
nums = {1:'One', 2:'Two', 3:'Three', 4:'Four', 5:'Five', 6:'Six'}

# roll two dices
rollTwoDices = [f'{w1} {w2} {w3}' for w1 in ["role", "roll"] for w2 in ["two", "to", "too"] for w3 in ["dices", "dice", "dies"]]

# save file
# could have done stg like: f"save{w1}{w2}{w3}{w4}".strip()
saveFile = [' '.join(f"save {w1} {w2} {w3} {w4}".split()) for w1 in ['it', 'this', 'that', 'the'] for w2 in ['in', ''] for w3 in ['a', 'the', 'new', 'a new', ''] for w4 in ['file', '']]

# country codes
a = "aearataubebgbrcachcncocuczdeegfrgbgrhkhuidieilinitjpkrltlvmamxmyngnlnonzphplptrorsrusasesgsiskthtrtwuausveza"
countryCodes = list(map(lambda x, y: x+y, a[::2], a[1::2]))

# gTLD domain names
domain_names = ['.com',
 '.net',
 '.org',
 '.io',
 '.co',
 '.ai',
 '.co.uk',
 '.ca',
 '.dev',
 '.me',
 '.de',
 '.app',
 '.in',
 '.is',
 '.eu',
 '.gg',
 '.to',
 '.ph',
 '.nl',
 '.id',
 '.inc',
 '.website',
 '.xyz',
 '.club',
 '.online',
 '.info',
 '.store',
 '.best',
 '.live',
 '.us',
 '.tech',
 '.pw',
 '.pro',
 '.uk',
 '.tv',
 '.cx',
 '.mx',
 '.fm',
 '.cc',
 '.world',
 '.space',
 '.vip',
 '.life',
 '.shop',
 '.host',
 '.fun',
 '.biz',
 '.icu',
 '.design',
 '.art']

sender_mail = False