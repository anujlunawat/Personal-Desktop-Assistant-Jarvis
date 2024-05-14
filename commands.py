from libs import *
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--start-maximized")

pygame.init()

chatStr = str()
currentSite = str()
browser = str()

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
try:
    engine.setProperty("voice", voices[2].id)
except:
    engine.setProperty("voice", voices[0].id)

# engine.setProperty("rate", 200)
# engine.setProperty("volume", 1.0)


def speak(audio: str, rate=150) -> None:

    """
    Speak the "audio" string passed to the function.
    rate is the speed with which it speaks
    """
    rate=175
    try:
        engine.setProperty("rate", rate)
        engine.say(audio)
        engine.runAndWait()
    except Exception as e:
        print(e)

def greet():
    """
    Greets the user according to the time.
    Asks about what the user wants help with.

    """
    hour = int(datetime.datetime.now().hour)

    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")

    speak("I am Jarvis, Sir. How may I help you today")


def takeCommand(lang='en-in', **kwargs):
    """
    Listens to the command from the user through the microphone.
    """

    r = sr.Recognizer()
    # self.pause_threshold >= self.non_speaking_duration >= 0
    # r.non_speaking_duration = 0.5
    r.pause_threshold = 1
    r.energy_threshold = 300

    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

        try:
            kwargs["mic_button"].configure(text_color=kwargs["reset_clr"])
            # kwargs["mic_button"].configure(image=kwargs["mic_img"])
            kwargs["root"].update()
        except: pass
        try:
            # profanity filter has been set to 1.
            # Will only show the first character and replace the rest with asterisks
            # can even use "hi-in" for hindi
            print("Recognizing...")
            query = r.recognize_google(audio_data=audio, language=lang)
            return query
        except:
            return False


def searchInSite(text, browser, site):
    """
    searches for given topic in the site
    """

    search = text[text.index('search') + 7:] if 'search for' not in text else text[text.index('search for') + 11:]

    # these are the sites you can search on. Currently the list is short
    element = {"youtube": [by[0], 'search_query'], "google": [by[0], 'q'], "wikipedia": [by[0], "search"]}

    if site in element.keys():
        try:
            ele = browser.find_element(element[site][0], element[site][1])
            ele.clear()
            ele.send_keys(search)
            browser.implicitly_wait(7)
            ele.submit()
            noError = True
        except Exception:
            print("Couldn't find element")
            speak("Could not complete request!")
            noError = False


def url(text):
    # for site in sites.keys():
    # if ((f'Open {site}'.casefold() in text) or ( f'on {site}'.casefold() in text) or (f'in {site}' in text)) and ((".com" in text.casefold())):
    #     return site

    text = text.replace('dot', '.')
    domain = [domain for domain in vars.domain_names if domain in ''.join(text.split())]

    if ((f'Open'.lower() in text) or (f'on'.lower() in text) or (f'in'.lower() in text)) and domain:
        h = 'open' if 'open' in text else ('on' if 'on' in text else ('in' if 'in' in text else False))
        site = text[text.find(h) + len(h): text.find(domain[0])]
        site = ''.join(site.split())
        # print(f"https://{site}{domain[0]}")
        return True, f"https://{site}{domain[0]}", site

    return False, str(), str()

def is_window_open(browser):
    try: return browser.window_handles
    except: return False


def tryTillEnd(say=True):
    var = False
    while not var:
        var = takeCommand()
        if (not var) and say:
            r = (choice(cannotHearResponse))
            print(r)
            speak(r)
    return var

def back(browser):
    try:
        browser.back()
    except:
        return False


def forward(browser):
    try:
        browser.forward()
    except:
        return False


def clickLink(browser, site):
    element = {"youtube": [by[1], 'video-title'], "google": [by[2], 'LC20lb']}
    try:
        ele = browser.find_element(element[site][0], element[site][1])
        ele.click()
    except Exception as e:
        print(f'{e = }')
        speak("Some error occured!")
        print("Some error occured!")


def open_AI(prompt):
    print("On it, Sir...")
    speak("On it, Sir...", rate=185)

    file_name = openAI.chat_with_gpt(prompt)

    # dir_ = f"{os.getcwd()}\{file_loc}"
    speak(f"Prompt in file: {prompt}", rate=160)

    os.system(fr"notepad.exe {file_name}")


def chat_AI(prompt):
    global chatStr
    chatStr += f"\n{USER}: {prompt}\nJarvis: "
    output = openAI.chat_with_gpt(chatStr, False)
    chatStr += f"{output}\n"
    print(f"Jarvis: {output}")
    # speak(output, rate=180)
    return output


def news(text):
    api = newsapi.NewsApiClient(api_key=NEWS_API_KEY)
    response = openAI.chat_with_gpt(f"{vars.s} {text}", file=False)
    country_code, k_word, category = tuple(map(str.strip, response.split(',')))
    # print(f'\n{response = }\n{country_code = }\n{k_word = }\n{category = }')

    if country_code.lower() not in vars.countryCodes:
        country_code = 'False'
    try:
        if country_code != 'False' and len(country_code.strip()) == 2:
            if category != 'False':
                if k_word != 'False':
                    news_ = api.get_top_headlines(q=k_word, country=country_code.lower(), category=category)

                else:
                    news_ = api.get_top_headlines(country=country_code.lower(), category=category)

            elif k_word != 'False':
                news_ = api.get_top_headlines(q=k_word, country=country_code.lower())

            else:
                news_ = api.get_top_headlines(country=country_code.lower())

        else:
            if category != 'False':
                if k_word != 'False':
                    news_ = api.get_top_headlines(q=k_word, category=category)
                else:
                    news_ = api.get_top_headlines(category=category)

            elif k_word != 'False':
                news_ = api.get_top_headlines(q=k_word)

            else:
                print("Invalid parameters")
                # speak("Invalid parameters", rate=175)
                return False
    except:
        print("Something went wrong")
        # speak("Something went wrong", rate=175)
        time.sleep(2)
        return False
    if news_["status"] == 'ok' and news_["totalResults"] > 0:
        return news_
    else:
        # speak("No news today")
        return False


def join_(string, op):
    return ''.join(string.split(op))


def song_download(text):
    speak("Starting the download...")
    song_name = text[14:]
    song_loc = songDownload.ultimateSongDownload(song_name.lower())
    speak(" song download complete")