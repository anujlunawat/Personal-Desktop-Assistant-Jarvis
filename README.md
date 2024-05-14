# Jarvis: Personal Desktop Assistant

![Jarvis Logo](https://github.com/anujlunawat/Personal-Desktop-Assistant-Jarvis/blob/main/assets/GUI/Main%20Window/Jarvis_main.png)


Jarvis is an AI assistant designed to perform various tasks such as web browsing, playing music, sending emails, and much more, all through voice commands. It uses Python and integrates with libraries like `selenium`, `pyttsx3`, and `speech_recognition`.

## Features
- Background Listening: Just say "Hey Jarvis" and it is ready to take your command. WALLAH!
- Voice-controlled browsing: You can open websites, search for topics, navigate backward and forward, and even maximize or minimize the browser window using voice commands.
- Music Player: Play your favorite songs by simply asking Jarvis to play music (dedicated front-end for music player controls). Can even shuffle and repeat tracks, play previour or next music.
-  Weather Updates: Get real-time weather updates for any location just by asking Jarvis. Provides local time of that location, wind speed, humidity, temperature, air quality index and much more related info.
- News Reader: Stay updated with the latest news by having Jarvis read out news articles for you, on any provided topic and/or country and/or category.
- Task Scheduler: Set alarms using Jarvis to remind you of important events.
- Application launcher: Open/Close applications. No need to say the full names of apps; matches for the closest name in the appnames
- Locate on Google Maps: Suggests places for a fine dine-out, or grocery shopping near you, or locate the Taj Mahal or  locate anything you wish.
- Chatbot Interaction: You can engage in conversations with Jarvis. You can ask questions, seek advice, or engage in casual conversation.
- Search on sites: Search for given topics on pre-defined sites. Sites Youtube, Google, Wikipedia are supported as of not.
- Download Song: Download a song by telling the name of the song
- Image Generation: Generates and downloads images on the spoken topic
- Set: Assign a name to an email address. So the next time you want to send them an email, you just need to type the assigned name (remember, it's case sensitive)
- <details>
  <summary>Email Sender: Jarvis can send emails on your behalf. Just tell it what to write and who to send it to.</summary>
  
  Checks if the email valid really exists. If so, displays a tick.
</details>

 

## Installation

1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Ensure you have the necessary drivers (e.g., Chrome driver for browsing).

## Usage

1. Run `main.py` to start Jarvis.
2. Say "Hey Jarvis" to activate voice commands, then issue commands like "Open Google", "Play music", or "Send an email".

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

