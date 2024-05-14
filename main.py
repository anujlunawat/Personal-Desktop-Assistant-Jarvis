import os
import random
import threading
import time

import customtkinter
from mail_gui import start_mail
import db
import playMusic
from commands import *

browser, bg_listening = str(), True


def speakThread(text):
    """
   Start a new thread to speak the provided text, using pyttsx3

   Args:
   text (str): The text to be spoken.

   """
    thread = threading.Thread(target=speak, args=(text,), daemon=True)
    thread.start()
    # thread.join() #ig no need for this statement


def start(text):
    """
    Process user input and perform various actions accordingly.

    Args:
    text (str): The user input text.
    """
    text = text.lower()
    global browser, bg_listening
    chat = True
    site, URL, wSite = url(text)
    global currentSite
    currentSite = wSite if site != False else currentSite

    # assign names to email addresses
    # useful when sending emails
    if 'set' == text.lower():
        chat = False
        reply = "This hot word allows you to save email address with nick names"
        msg_on_frame(reply)
        speakThread(reply)
        time.sleep(.7)
        speakThread("Enter the email address and the name you want to associate it with")
        top_level_login("Name", "Email")
        # vars.eMails.update(creds)
        msg_on_frame("Wonderful! You can now send email to this person just by naming them", )
        speak("Wonderful! You can now send email to this person just by naming them")

    # go back in the browser(driver)
    elif 'go back' in text:
        chat = False
        back(browser)
    # go forward in the browser(driver)
    elif 'go forward' in text:
        chat = False
        forward(browser)

    # open new site in new a tab (instead of another window)
    if site:
        chat = False
        if is_window_open(browser):
            browser.switch_to.new_window("tab")
            browser.get(URL)
        else:
            browser = wd.Chrome(options=options)
            browser.get(URL)

    # maximize window (if presence of driver/browser)
    if ('maximise' in text) or ('full screen' in text) or ('fullscreen' in text):
        try:
            browser.fullscreen_window()
            chat = False
        except:
            pass
    # minimize window (if presence of driver/browser)
    elif ('minimise' in text) or ('back ground' in text) or ('background' in text):
        try:
            browser.minimize_window()
            chat = False
        except:
            pass

    # search for given topic in the website driver/browser is currently assigned to
    if 'search'.lower() in text:
        chat = False
        try:
            searchInSite(text, browser, currentSite)
        except:
            pass

    # if the driver/browser is running flawlessly
    # i.e. no error raised when performing operations on driver/browser (selenium Chrome webdriver)
    if noError:
        for _ in ['video', 'link', 'the']:
            for t in ['play', 'click', 'select', 'start']:
                if (f'{t} {_}' in text) or (f'{t} the {_}' in text) or (f"{t} the first {_}" in text):
                    chat = False
                    clickLink(browser, currentSite)

    # close tab/window (if open)
    if [True for a in ['close', 'exit'] for b in ['the', 'this', ''] for c in
        ['tab', 'window', 'site', 'page', 'browser'] if ' '.join(f"{a} {b} {c}".split()) in text.lower()]:
        try:
            windowHandles = browser.window_handles
            if len(windowHandles) > 1:
                windowHandles.remove(browser.current_window_handle)
                browser.close()
                browser.switch_to.window(windowHandles[-1])

            else:
                browser.quit()
                speak("Window closed.")
                chat = False
        except:
            chat = False
            msg_on_frame("No window is open")
            speak("No window is open")

    # exit
    elif 'exit' == text:
        speak("Good Bye!")
        root.destroy()
        time.sleep(1)
        sys.exit(0)

    # play music
    elif ("play" in text and "song" in text) or "play music" in text or 'start music' in text:
        song = [s for s in vars.songs if ''.join(text.split()[2:]) in ''.join(s[:-4].lower().split())]
        song = vars.songs[randint(0, len(vars.songs) - 1)] if not len(song) else song[0]

        msg_on_frame(f"Currently playing: {song[:-4]}")
        speak(f"Playing a song...")

        threading.Thread(target=playMusic.music_gui, daemon=True, args=(song,)).start()

    # locate places on google maps
    elif text.lower().startswith("locate"):
        loc = text.lower()[7:]

        # open a new tab if browser window is already open
        if is_window_open(browser):
            browser.switch_to.new_window("tab")
        # create a new Chrome driver and search for give loc (if browser/driver not already open)
        else:
            browser = wd.Chrome(options=options)
        browser.get(f"https://www.google.com/maps/search/?api=1&query={loc}")

    elif 'alarm' in text:
        n = re.findall(r'\d+', text)
        current_dir = os.getcwd()
        try:
            if 'past' in text:
                hour = n[1]
                minutes = n[0]
            else:
                hour = n[0]
                minutes = n[1]
        except:
            speak("couldn't complete request")
        print(f"{hour = }, {minutes = }")
        if len(minutes)<2:
            minutes = '0'+str(minutes)
        command = fr'schtasks /create /tn "AlarmTask{random.randint(0,1000)}" /tr r"start {current_dir}\assets\sounds\alarm.wav" /sc once /st {hour}:{minutes}'
        print(command)
        subprocess.run(command, shell=True)
        msg_on_frame(f"Alarm set for {hour}:{minutes}")
        speak("Alarm set successfully")

    # stop listening in background
    elif "stop listening" == text.lower():
        bg_listening = False

    # start listening in background
    elif "start listening" == text.lower():
        bg_listening = True

    # weather details
    elif "weather" in text:
        if [s for s in list(("what is today's weather", "how is today's weather", 'what is the weather today',
                             'how is the weather today')) if s in text]:
            result = weather.weather("pune")
        else:
            try:
                loc = ' '.join(text.lower().split()[text.lower().split().index("weather") + 2:])
                result = weather.weather(loc)
            except:
                msg_on_frame("Unable to provide information")
                speak("Unable to provide information")

        msg_on_frame(result)
        speak(result, rate=160)

    # check the time
    elif "the time" in text:
        strftime = datetime.datetime.now().strftime("%H:%M:%S")
        msg_on_frame(f"The time is {strftime}")
        speak(f'The time is {strftime}')

    # check the date
    elif "date" in text and 'today' in text:
        date = f'Today is {calendar.month_name[datetime.date.today().month]} {datetime.date.today().day}, {datetime.date.today().year}'
        msg_on_frame(date)
        speak(date)

    # check the day
    elif "day" in text and 'today' in text:
        day = f"It is {calendar.day_name[datetime.datetime.now().weekday()]} today."
        msg_on_frame(day)
        speak(day)

    # download a song
    elif 'download song' in text:
        song_download(text)

    # open an app
    elif (('open' in text and '.com' not in text.lower()) and (everythingApps.check_app(
            ' '.join(text.lower().split()[text.lower().split().index("open") + 1:]).rstrip("app").strip()))):
        app = ' '.join(text.lower().split()[text.lower().split().index("open") + 1:]).rstrip("app").strip()
        # print(f"\nIn OPEN, {app = }\n")
        if everythingApps.openApp(app):
            speak(f"OPENING {app}")
        else:
            speak("App cannot be opened. My bad!")

    # close an app
    elif ('close' in text and ".com" not in text.lower()) and (everythingApps.check_app(
            ' '.join(text.lower().split()[text.lower().split().index("close") + 1:]).rstrip("app").strip())):
        app = ' '.join(text.lower().split()[text.lower().split().index("close") + 1:]).rstrip("app").strip()
        # print(f"\nIn CLOSE, {app = }\n")
        if everythingApps.closeApp(app):
            speak(f"CLOSING {app}")
        else:
            speak("Cannot close app")

    # clear the chat between the user and AI (Jarvis)
    elif "clear chat" in text or "clear our chat" in text:

        global chatStr
        chatStr = str()
        db.delete_chats_data()
        msg_on_frame("Chat history deleted")
        time.sleep(.4)
        speak("chat history deleted")

    # display news
    elif "news" in text.lower():
        news_ = news(text)
        if news_:
            top_level_news(news_)
        else:
            msg_on_frame("No news today")
            speak("No news today!")

    # roll 2 dice
    elif [phrase for phrase in vars.rollTwoDices if phrase in text.lower()]:
        msg_on_frame(f"They came up {nums[random.randint(1, 6)]} and {nums[random.randint(1, 6)]}")

    # send emails
    elif text.startswith(("send an email", "send a mail", "write an email", "write a mail")):
        thread1 = threading.Thread(target=start_mail, args=(openAI.chat_with_gpt(
            text + ". NOTE: use the given data only. do not provide any other information that is not given",
            file=False),), daemon=True)
        thread1.start()

    # generate images
    elif "generate an image" in text.lower() or "generate image" in text.lower():
        image_prompt = text[len("generate an image"):]
        speak("hold up, i'm generating the image")
        image_url = image_generation.generate_image(image_prompt)

        # download the image and display it
        filename = fr"generatedImage{random.randint(0, 1000)}.png"
        filepath = fr"assets\generated_images\{filename}"
        urllib.request.urlretrieve(image_url, filepath)

        img = Image.open(filepath)
        img.show()

    # chat with the AI
    elif chat:
        # if ("save it" in text.lower()) or  ("save" in text.lower() and "file" in text.lower()):
        if [phrase for phrase in vars.saveFile if phrase.lower() in text.lower()]:
            prompt = text.lower().split('save')[0].strip().rstrip('and')
            open_AI(prompt)
        else:
            output = chat_AI(text)
            db.chats()
            db.add_chats(text, output)
            msg_on_frame(output)
            speakThread(output)
            # speak(output, rate=180)


#
#
#
#
#
#
#
#
#
#
def hey_jarvis():
    """
    Function for continuous listening for "hey Jarvis" command
    """
    print("inside hey_jarvis")
    r = sr.Recognizer()
    # r.pause_threshold = 1
    # with sr.Microphone() as mic:
    # r.adjust_for_ambient_noise(mic, duration=.5)
    # r.listen_in_background()
    with sr.Microphone() as mic:
        r.adjust_for_ambient_noise(mic, duration=.2)
    global bg_listening
    while bg_listening:
        # print("listening.........")
        with sr.Microphone() as mic:
            # r.adjust_for_ambient_noise(mic, duration=.2)
            print('listening....')
            audio = r.listen(mic)
            print('recognizing....')
            try:
                text = r.recognize_google(audio)
                text = text.lower()
            except:
                continue
            if 'hey jarvis' in text:
                print("Hello there mf")
                take_command_mic()


def take_command_mic(event=True):
    """
    Function to handle microphone command.

    Gets called when the mic button is clicked or "hey jarvis" is spoken and detected by hey_jarvis() command
    """
    global message, mic_org_clr
    # global mic_img_red, mic_img_black
    mic_button.configure(text_color="red")
    # mic_button.configure(image=mic_img_red)
    root.update()
    # playsound(r"C:\Users\Mohit\OneDrive\Desktop\Jarvis\assets\sounds\mic_on.mp3")
    text = takeCommand(root=root, mic_button=mic_button, reset_clr=mic_org_clr)
    # text = takeCommand(root=root, mic_button=mic_button, reset_clr=mic_org_clr, mic_img = mic_img_black)
    # mic_button.configure(text_color="")
    # root.update()
    # playsound(r"C:\Users\Mohit\OneDrive\Desktop\Jarvis\assets\sounds\mic_off.mp3")
    if text:
        message = text
        msg_on_frame(text.capitalize(), value="You")
        start(text)
    else:
        speak("Sorry, I couldn't hear. Could You Try Again!!")


def top_level_news(news):
    """
    displays news
    """
    def open_news(url):
        global browser
        if is_window_open(browser):
            browser.switch_to.new_window("tab")
            browser.get(url)
        else:
            browser = wd.Chrome(options=options)
            browser.get(url)

    win = customtkinter.CTkToplevel(fg_color='#10204c')
    win.wm_attributes("-topmost", True)
    win.title("News")
    win.geometry("600x600")
    win.resizable(False, False)

    news_label = customtkinter.CTkLabel(win, fg_color='black', text_color='white', text='NEWS',
                                        font=("Segoe ui black", 25))
    news_label.pack(fill='x')

    frame_ = customtkinter.CTkScrollableFrame(win, width=600, height=560, fg_color='#081026')
    frame_.pack(fill='y', after=news_label)

    labels = list()
    for i in range(len(news['articles']) if len(news['articles']) < 10 else 10):
        labels.append(
            customtkinter.CTkLabel(frame_, justify=customtkinter.LEFT, text=f"{i + 1}. {news['articles'][i]['title']}",
                                   font=(customtkinter.CTkFont("sans serif collection"), 18), wraplength=560))

        if i == 0:
            labels[i].pack(anchor='w', side='top', padx=10, pady=7)
        else:
            labels[i].pack(after=labels[i - 1], anchor='w', padx=10, pady=7)

        try:
            labels[i].bind("<Button-1>",
                           lambda event, url_=news['articles'][i]['url']: threading.Thread(target=open_news,
                                                                                           daemon=True,
                                                                                           args=(url_,)).start())
            labels[i].bind()
        except: pass

    close_button = customtkinter.CTkButton(win, text="Close", command=win.destroy)
    close_button.pack(after=labels[-1], pady=10)

    win.wait_window(window=win)


def send_command():
    """
    function to get the command typed by the user the entry.
    Then, clears the entry
    sends the command to msg_on_frame() to get displayed
    sends the command to send_message_to_start()
    """
    global message
    message = entry.get()
    entry.delete(0, customtkinter.END)
    # Process the message here (print for now)
    # print(f"You entered: {message}")
    msg_on_frame(message, value="You")
    send_message_to_start(message)


def entry_enter(event):
    """
    called when <Enter> is pressed in the entry
    sends the command to msg_on_frame() and send_message_to_start()
    """
    global message
    message = entry.get()
    entry.delete(0, customtkinter.END)
    # print(f"You entered: {message}")
    msg_on_frame(message, value="You")
    send_message_to_start(message)


def send_message_to_start(message):
    """
    Creates a thread to send message to start() function

    Args:
    message (str): Message to be processed.
    """
    try:
        thread2 = threading.Thread(target=start, args=(message,), daemon=True)
        thread2.start()
    except Exception as e:
        print(e)


def msg_on_frame(message, value="Jarvis"):
    """
    Function to display message on the frame.

    Args:
    message (str): Message to be displayed.
    value (str, optional): Value. Defaults to "Jarvis".
    """

    global prev_msg_label
    msg = tk.StringVar(value=f"{value}: " + message.capitalize())
    msg_label = customtkinter.CTkLabel(
        frame,
        font=(customtkinter.CTkFont("arial rounded mt bold"), 16, "bold"),
        textvariable=msg,
        justify="left",
        # width = 50,
        height=30,
        fg_color="dark blue" if value == 'Jarvis' else "#807f7f",
        corner_radius=12,
        wraplength=280
    )
    if not prev_msg_label:
        prev_msg_label.append([msg_label, 0, 0])
        msg_label.grid(ipadx=15, pady=9, padx=5, sticky='W', row=0, column=0)
    else:
        msg_label.grid(ipadx=15, pady=9, padx=5, column=0, row=prev_msg_label[-1][1] + 1, sticky='W')
        prev_msg_label.append([msg_label, prev_msg_label[-1][1] + 1, 0])
    frame.update()


def top_level_login(*args):
    """
    Function to display top-level login window.
    Used to assign names to email addresses in the start() function (use 'set')
    Args:
    *args: Variable length arguments.
    """

    creds = dict()

    def credentials():
        for ind, e in enumerate(entries):
            creds[args[ind]] = e.get()
        db.emails_db()
        if not db.add(creds["Name"], creds["Email"]):
            msg_on_frame("Error! Name not unique. Could not set the given name.")
            speak("Error! Name not unique. Could not set the given name.")
        win.destroy()

    win = customtkinter.CTkToplevel()
    win.wm_attributes("-topmost", True)
    win.title("Login Credentials")
    win.geometry("300x300")
    labels, entries = list(), list()
    row, col = 0, 0
    for text in args:
        label = customtkinter.CTkLabel(win, text=text, )
        label.grid(padx=10, pady=5, row=row, column=col)
        labels.append(label)
        col += 1

        if 'password' in text.lower():
            eNtRy = customtkinter.CTkEntry(win, placeholder_text=text, show='*')
        else:
            eNtRy = customtkinter.CTkEntry(win, placeholder_text=text)
        eNtRy.grid(padx=5, row=row, column=col)
        entries.append(eNtRy)
        row, col = row + 1, 0
    button = customtkinter.CTkButton(win, text="Submit", command=credentials)
    button.grid(pady=10, row=row + 2, column=col + 1)
    win.wait_window(window=win)


if __name__ == "__main__":
    # call the hey_jarvis() function to run continuously in the bg
    thread3 = threading.Thread(target=hey_jarvis, daemon=True)
    thread3.start()

    # press F4 to start mic
    keyboard.add_hotkey("F4", take_command_mic, suppress=True)

    prev_msg_label = list()

    root = customtkinter.CTk()
    # Set the geometry of the window
    root.geometry("400x530")
    # Set the title of the window
    root.title("Jarvis")
    # The widget under mouse cursor gets focused
    root.tk_focusFollowsMouse()
    # Set appearance mode
    customtkinter.set_appearance_mode("dark")  # Change to "light" or "system" if desired
    # Set default color theme (optional)
    # customtkinter.set_default_color_theme("blue")
    # Prevent window resizing
    root.resizable(False, False)

    # logo; goes at the top
    photo = customtkinter.CTkImage(
        light_image=Image.open(r'assets\GUI\Main Window\Jarvis_main.png'),
        dark_image=Image.open(r'assets\GUI\Main Window\Jarvis_main.png'),
        size=(400, 120)
    )
    logo = customtkinter.CTkLabel(
        root,
        height=120,
        width=400,
        image=photo,
        text="",
    )
    logo.pack()

    # frame for the message log
    # to get "Chats" written on top of the frame:
    # 1. uncomment line 501 and 502
    # 2. comment line 500
    frame = customtkinter.CTkScrollableFrame(
        root,
        380,
        345,
        # height 375,
        # label_text="Chats",
        border_width=2,
        corner_radius=0,
    )
    frame.place(y=120, x=0)

    # Entry field with placeholder text and click event binding
    entry = customtkinter.CTkEntry(
        height=35,
        master=root,
        width=315,
        placeholder_text="Type Here",
        font=("Arial", 16),
        border_width=1,
        border_color="white",
        # fg_color="#643B9F",
        # corner_radius=20
    )
    entry.place(y=475, x=10)
    # Bind Enter key press with entry_enter() function.
    # So, when Enter key is pressed, entry gets cleared and the message is stored
    entry.bind("<Return>", entry_enter)
    entry.focus()

    # Send button (use CTkButton).
    # Uncomment the line below to use the image
    # send_img = ImageTk.PhotoImage(Image.open("send.png"))
    send_button = customtkinter.CTkButton(
        master=root,
        text="Send",
        font=("Arial", 16),
        command=send_command,
        border_width=1,
        border_color="white",
        width=60,
        height=35,
        # bg_color="#643B9F",
        # hover_color="dark blue",
        hover=True
    )
    send_button.place(x=330, y=475)

    # Microphone button (use CTkButton with image)
    mic_img_white = customtkinter.CTkImage(
        light_image=Image.open(r"assets\GUI\Main Window\mic_white.png"),
        dark_image=Image.open(r"assets\GUI\Main Window\mic_white.png"),
        size=(25, 25)
    )
    mic_img_red = customtkinter.CTkImage(
        light_image=Image.open(r"assets\GUI\Main Window\mic_red.png"),
        dark_image=Image.open(r"assets\GUI\Main Window\mic_red.png"),
        size=(25, 25)
    )
    mic_button = customtkinter.CTkButton(
        master=root,
        text="🎙",
        border_width=1,
        font=("Arial", 25, "bold"),
        width=60,
        height=35,
        border_color="white",
        bg_color='transparent',
        command=take_command_mic,
        # text='',
        # image=mic_img_red,

    )
    mic_org_clr = mic_button.cget("text_color")[0]
    mic_button.place(y=435, x=330)

    root.update()
    threading.Thread(target=greet, daemon=True).start()
    root.mainloop()
