"""
This module defines functions and utilities for a music player GUI using custom tkinter components and pygame for audio playback.

It includes functionality for playing music, controlling playback (play, pause, next, previous, shuffle, repeat), updating the GUI elements based on the current state of the music playback, and allowing seeking within the currently playing track.

Functions:
    - on_close(win): Function to handle closing of the music player window.
    - secs_to_mins(num1): Converts seconds to a string in the format 'MM:SS'.
    - timestamp_update(current_timestamp): Updates the current timestamp (time elapsed) of the playing track.
    - pos_update(): Updates the position (time elapsed) of the playing track.
    - seek(): Handles seeking within the currently playing track.
    - play_music(song): Plays the specified music file.
    - music_gui(song): Creates and manages the music player GUI window.

Variables:
    - pygame.init(): Initializes the pygame module for audio playback.
    - my_song: Reference to the pygame music player.
    - pos: Current position (time elapsed) within the playing track.
    - seek_paused: Flag indicating whether seeking is paused.
    - shuffle_on: Flag indicating whether shuffle mode is enabled.
    - playing: Flag indicating whether music is currently playing.
    - repeat: Flag indicating whether repeat mode is enabled.
    - nextsong: Path to the next song to be played.
    - seq: List of songs in the playback sequence.
    - song_len: Length of the currently playing song.
    - curr_song: Currently playing song.
    - b: Reference to the play/pause button.
    - p_img: Image for the play/pause button.
    - song_len_var: Variable to store the length of the currently playing song.
    - w: Function to update the title of the music player window.
    - progress_var: Variable to store the progress of the currently playing track.
"""

import threading
import time
import customtkinter
import tkinter as tk
from PIL import Image
from vars import songs, mypath
import pygame
from random import choice

pygame.init()
my_song = pygame.mixer.music
pos = 0
seek_paused = False
shuffle_on = False
playing = True
repeat = False
# queue = songs
nextsong = None
seq: list[str] = list()
song_len = float()
curr_song = None
b, p_img = None, None
song_len_var = None
w = None
progress_var = None


def on_close(win):
    """
    Function to handle the closing event of the music player window.

    Parameters:
        win (Tkinter.Toplevel): The music player window to be closed.
    """
    my_song.unload()
    win.destroy()


def secs_to_mins(num1:float) -> str:
    """
    Converts seconds to a string representing minutes and seconds in the format 'MM:SS'.
    """
    mins, secs = int(num1 // 60), int(round(num1 % 60, 2))
    return f"{mins}:{secs if secs >= 10 else f'0{secs}'}"


def timestamp_update(current_timestamp):
    """
     Updates the current timestamp (time elapsed) of the playing track.

     Parameters:
         current_timestamp (Tkinter.StringVar): Variable to hold the current timestamp value.
     """
    while True:
        # current_timestamp.set(secs_to_mins(my_song.get_pos()/1000))
        current_timestamp.set(secs_to_mins(pos))
        time.sleep(.2)

def pos_update():
    """
    Updates the position (time elapsed) of the playing track.
    """
    global pos, song_len
    while True:
        if my_song.get_busy():
            pos += 1
            time.sleep(1)
        # if pos >= song_len-5:
            # print(f"{pos = }, {song_len = }")
        if pos >= song_len-1:
            # print("in song len vs pos", pos, song_len)
            play_music(nextsong)
            time.sleep(1)


def seek():
    """
    Handles seeking within the currently playing track.
    """
    global seek_paused, song_len
    while True:
        time_ref = (pos / song_len)
        if not seek_paused:
            progress_var.set(time_ref)
        time.sleep(1)


def play_music(song):
    """
    Plays the specified music file.

    Parameters:
        song (str): The path to the music file to be played.
    """
    # print("in play music")
    global song_len, nextsong, curr_song, pos, b, p_img, playing, num_of_song_played
    # unload the prev song
    my_song.unload()

    curr_song = song
    # path to the music file
    song_path = mypath + curr_song
    # load the music file
    my_song.load(song_path)
    # length of song (in seconds)

    song_len = pygame.mixer.Sound(song_path).get_length()
    print(f"{song_len = }")
    song_len_var.set(secs_to_mins(song_len))
    # append the current song to the sequence list
    seq.append(curr_song)

    if not repeat:
        if shuffle_on:
            nextsong = choice(songs)
            print("shuffle on", nextsong)
        else:
            nextsong = songs[songs.index(curr_song) + 1] if songs[songs.index(curr_song)] != songs[-1] else songs[0]
            print("shuffle off", nextsong)
        # nextsong = songs[songs.index(curr_song) + 1] if songs[songs.index(curr_song)] != songs[-1] else songs[0] if not shuffle_on else choice(songs)
    else:
        nextsong = curr_song
        print('repeat on', nextsong)

    b.configure(image=p_img)
    playing = True
    pos=0

    my_song.play()
    my_song.set_pos(0)

    w(curr_song)
    # my_song_queue(mypath + nextsong)


def music_gui(song):
    """
    Creates and manages the music player GUI window.

    Parameters:
        song (str): The path to the music file to be initially played in the GUI.
    """
    # queue = songs[songs.index(song)+1:]
    global w, song_len_var, progress_var
    win = customtkinter.CTkToplevel(fg_color='black')
    win.wm_attributes("-topmost", True)
    # win.title('music')
    win.title(song)
    win.geometry("450x100")
    win.resizable(False, False)
    w = win.title
    song_len_var = customtkinter.StringVar()
    current_timestamp = customtkinter.StringVar(value="0:00")
    # play_music(song, song_len_var, win)

    # win.update()

    # used as "variable" in progressbar (see below)
    progress_var = customtkinter.DoubleVar(value=0)
    #
    # threading.Thread(target=timestamp_update, daemon=True, args=(current_timestamp,)).start()
    # threading.Thread(target=seek, daemon=True, args=(progress_var,)).start()
    # threading.Thread(target=pos_update, daemon=True, args=(song_len, song_len_var, win)).start()

    file_loc = r'assets\GUI\music top level\\'
    play_img = customtkinter.CTkImage(light_image=Image.open(rf"{file_loc}play.png"), dark_image=Image.open(rf"{file_loc}play.png"), size=(30, 30))
    pause_img = customtkinter.CTkImage(light_image=Image.open(rf"{file_loc}pause.png"), dark_image=Image.open(rf"{file_loc}pause.png"), size=(30, 30))
    prev_img = customtkinter.CTkImage(light_image=Image.open(rf"{file_loc}prev.png"), dark_image=Image.open(rf"{file_loc}prev.png"), size=(30, 30))
    next_img = customtkinter.CTkImage(light_image=Image.open(rf"{file_loc}next.png"), dark_image=Image.open(rf"{file_loc}next.png"), size=(30, 30))
    shuffle_img = customtkinter.CTkImage(light_image=Image.open(rf"{file_loc}shuffle.png"), dark_image=Image.open(rf"{file_loc}shuffle.png"), size=(25, 25))
    repeat_img = customtkinter.CTkImage(light_image=Image.open(rf"{file_loc}repeat.png"), dark_image=Image.open(rf"{file_loc}repeat.png"), size=(25, 25))
    shuffle_on_img = customtkinter.CTkImage(light_image=Image.open(rf"{file_loc}shuffle_on.png"), dark_image=Image.open(rf"{file_loc}shuffle_on.png"), size=(25, 25))
    repeat_on_img = customtkinter.CTkImage(light_image=Image.open(rf"{file_loc}repeat_on.png"), dark_image=Image.open(rf"{file_loc}repeat_on.png"), size=(25, 25))

    # the x and y coordinates for placing the buttons
    x, y = 88, 15
    buttons = {'button_shuffle':None, 'button_prev':None, 'button_pause_play':None, 'button_next':None, 'button_repeat':None}

    for i, img, keys in zip(range(5),[shuffle_img, prev_img, pause_img, next_img, repeat_img], buttons.keys()):
        buttons[keys] = customtkinter.CTkButton(
            master=win,
            image=img,
            text='',
            font=("Arial", 30),
            width=35,
            height=35,
            border_width=0,
            # anchor='center',
            bg_color='transparent',
            fg_color='transparent',
            # hover=True,
            # hover_color='00FF00'
        )
        buttons[keys].place(x=x, y=y)
        x+=60

    def click_shuffle():
        """
        Toggles shuffle mode for music playback.
        """
        global shuffle_on, nextsong
        shuffle_on = not shuffle_on
        if shuffle_on:
            buttons["button_shuffle"].configure(image=shuffle_on_img)
            nextsong = choice(songs)
        else:
            buttons['button_shuffle'].configure(image=shuffle_img)
            try:
                nextsong = songs[songs.index(curr_song)+1]
            except:
                nextsong = songs[0]

    def click_prev():
        """
        Plays the previous track.
        """
        global pos
        if pos < 3:
            if seq.index(curr_song) != 0:
                play_music(seq[seq.index(curr_song) - 1])
                # my_song.unload()
                # my_song.load(mypath + queue[queue.index(song)-1])
                # my_song.play()
                # pos = 0
                # win.update()
        else:
            my_song.rewind()
            pos = 0

    def click_play_pause():
        """
        Toggles between playing and pausing the current track.
        """
        global playing
        playing = not playing
        if playing:
            my_song.unpause()
            buttons['button_pause_play'].configure(image=pause_img)
        else:
            my_song.pause()
            buttons['button_pause_play'].configure(image=play_img)

    def click_next():
        """
        Plays the next track in the playlist.
        """
        play_music(nextsong)

    def click_repeat():
        """
        Toggles repeat mode for music playback.
        """
        global repeat, nextsong
        repeat = not repeat
        if repeat:
            # my_song.
            buttons['button_repeat'].configure(image=repeat_on_img)
            nextsong = curr_song
        else:
            buttons['button_repeat'].configure(image=repeat_img)

    buttons['button_shuffle'].configure(command=click_shuffle)
    buttons['button_prev'].configure(command=click_prev)
    buttons['button_pause_play'].configure(command=click_play_pause)
    buttons['button_next'].configure(command=click_next)
    buttons['button_repeat'].configure(command=click_repeat)

    global b, p_img
    b = buttons['button_pause_play']
    p_img = pause_img

    # # button_shuffle.bind("<Enter>",lambda x: shuffle_img.configure(size=(27, 27)))
    # # button_shuffle.bind("<Leave>",lambda x: shuffle_img.configure(size=(25,25)))
    #
    # # button_prev.bind("<Enter>",lambda x: prev_img.configure(size=(33,33)))
    # # button_prev.bind("<Leave>",lambda x: prev_img.configure(size=(30,30)))
    #
    # # button_play_pause.bind("<Enter>",lambda x: current_play_pause_img.configure(size=(33,33)))
    # # button_play_pause.bind("<Leave>",lambda x: current_play_pause_img.configure(size=(30,30)))
    #
    # # button_next.bind("<Enter>",lambda x: next_img.configure(size=(33,33)))
    # # button_next.bind("<Leave>",lambda x: next_img.configure(size=(30,30)))
    #
    # # button_repeat.bind("<Enter>",lambda x: repeat_img.configure(size=(27, 27)))
    # # button_repeat.bind("<Leave>",lambda x: repeat_img.configure(size=(25,25)))

    def button_release():
        """
        Handles releasing the progress bar slider for seeking within a track.
        """
        global seek_paused, pos
        seek_rel = progress_var.get()
        pos = song_len * seek_rel
        my_song.set_pos(pos)
        seek_paused = False

    def button_click(event):
        """
        use the progress bar as a slider
        """
        global seek_paused
        # print(f"{event}, {event.x}, {event.y}")
        # print(f"{progressbar.winfo_width() = }")
        seek_paused = True
        progress_var.set(event.x / progressbar.winfo_width())

        if event == tk.EventType.Button:
            button_release()
        # print(f"{progressbar.winfo_width() = }")


    def progressbar_clr_change(event):
        """
        changes the color of the progressbar when cursor enters its widget
        resets to original color when cursor leaves the widget
        """
        # print(f"{event = }, {event.state = }, {event.type = }")
        if event.type == tk.EventType.Enter:
            progressbar.configure(progress_color='#4B006E')

        else:
            progressbar.configure(progress_color=progressbar_clr1)

    progressbar = customtkinter.CTkProgressBar(
        master=win,
        width=350,
        height=7,
        orientation='horizontal',
        # mode='determinate',
        variable=progress_var
        # determinate_speed=0.1
    )
    progressbar_clr1 = progressbar.cget("progress_color")[0]
    # progressbar.set(0)
    progressbar.place(x=50, y=70)

    progressbar.bind("<Button-1>", lambda event: button_click(event))
    progressbar.bind("<B1-Motion>", lambda event: button_click(event))
    progressbar.bind("<ButtonRelease-1>", lambda event: button_release())
    progressbar.bind("<Enter>", lambda event: progressbar_clr_change(event))
    progressbar.bind("<Leave>", lambda event: progressbar_clr_change(event))


    current_timestamp_label = customtkinter.CTkLabel(
        master=win,
        textvariable=current_timestamp,
        font=("spotify circular", 16),
        width=44,
        height=19
    )
    current_timestamp_label.place(x=5, y=64)

    totalsongtime_label = customtkinter.CTkLabel(
        master=win,
        textvariable=song_len_var,
        font=("spotify circular", 16),
        width=44,
        height=19
    )
    totalsongtime_label.place(x=400, y=64)

    play_music(song)
    threading.Thread(target=timestamp_update, daemon=True, args=(current_timestamp,)).start()
    threading.Thread(target=seek, daemon=True).start()
    threading.Thread(target=pos_update, daemon=True).start()

    win.protocol("WM_DELETE_WINDOW", lambda: on_close(win))
    # win.protocol("WM_DELETE_WINDOW", win.destroy)

    win.mainloop()


    # print("win destroyed")
    # my_song.stop()
    # print("song stopped")
    # my_song.unload()

# text = 'kaloli'
# song = [s for s in songs if ''.join(text.lower().split()) in ''.join(s[:-4].lower().split()) ]
# # song = [s for s in songs if ''.join(s[:-4].lower().split()) in ''.join(text.lower().split())]
# from random import randint
# song = songs[randint(0, len(songs) - 1)] if not len(song) else song[0]
#
# music_gui(song)