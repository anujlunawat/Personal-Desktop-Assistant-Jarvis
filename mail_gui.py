import threading
import customtkinter
from PIL import Image
import eMail
import openAI
from commands import takeCommand, speak
import db
import time
sender_mail = False
def start_mail(body:str) -> None:
    """
    Opens a window to compose and send an email.
    """
    win = customtkinter.CTkToplevel()
    win.geometry("500x450")
    win.wm_attributes("-topmost", True)

    tick_img = customtkinter.CTkImage(
        light_image=Image.open(r"assets\GUI\mail top level\tick.png"),
        dark_image=Image.open(r"assets\GUI\mail top level\tick.png"),
        size=(25, 25)
    )
    mic_img = customtkinter.CTkImage(Image.open(r"assets\GUI\mail top level\mic.png"))

    def ValidateEmail():
        global sender_mail
        sm = db.retrieve(sender_mail_entry.get())
        if sm:
            if eMail.isValid(sm[0]):
                sender_mail = sm[0]
                img_label.configure(image=tick_img)
        elif eMail.isValid(sender_mail_entry.get()):
            sender_mail = sender_mail_entry.get()
            img_label.configure(image=tick_img)
        else:
            # img_label.configure(text='')
            img_label.configure(image='')
            sender_mail = False
        win.update()

    def takeCommandCopy():
        global body
        message = takeCommand()
        if 'send' ==  message.lower() or 'send it' == message.lower():
            send_mail()

        else:
            time.sleep(.5)
            speak("Working on it...")
            body = send_to_gpt(message)
            mail_contents_label.configure(text=body)

    def entry1_enter():
        global body
        message = entry1.get()
        if 'send' == message.lower() or 'send it' == message.lower():
            send_mail()

        else:
            entry1.delete(0, customtkinter.END)
            time.sleep(.5)
            speak("Working on it...")
            body = send_to_gpt(message)
            mail_contents_label.configure(text=body)

    def send_to_gpt(message):
        return openAI.chat_with_gpt(f"make changes: {message}: {body}", file=False)

    def send_mail():
        global sender_mail
        subject = [line[9:] for line in body.split('\n') if "Subject" in line][0]
        main_body = body[len(subject)+10:]
        if sender_mail:
            if eMail.send_email(sender_mail, subject, main_body):
                speak("Email sent successfully", rate=175)
                print("Email sent successfully")
                win.destroy()
            else:
                speak("Email could not be sent ")
                print("Email could not be sent ")
                win.destroy()
        else:
            speak("Invalid Email Address!")
            print("Invalid Email Address!")

    customtkinter.CTkLabel(win, height=35, text="Mail", font=(customtkinter.CTkFont("arial rounded mt bold"), 20)).place(x=224, y=5)

    label1 = customtkinter.CTkLabel(
        win,
        height=35,
        text="To:",
        font=(customtkinter.CTkFont("arial rounded mt bold"), 20)
    )
    label1.place(x=17, y=51)

    sender_mail_entry = customtkinter.CTkEntry(win, width=235, height=35, placeholder_text="Sender's email address", )
    sender_mail_entry.place(x=63, y=51)
    sender_mail_entry.bind("<KeyRelease>", lambda x: ValidateEmail())

    img_label = customtkinter.CTkLabel(
        master=win,
        text="",
        # text_color="green",
        font = ("Arial", 20, "bold"),
        height=35,
        width=35)
    img_label.place(x=320, y=51)

    mail_contents_frame = customtkinter.CTkScrollableFrame(win, width=480, height=294)
    mail_contents_frame.place(x=0, y=91)

    mail_contents_label = customtkinter.CTkLabel(
        master=mail_contents_frame,
        width=500,
        height=294,
        bg_color='black',
        # bg_color="#314894",
        text=body,
        font=(customtkinter.CTkFont("arial rounded mt bold"), 20),
        text_color='white',
        anchor='nw',
        wraplength=460,
        justify='left',
        padx=10,
        pady=10
    )
    mail_contents_label.pack(fill="both")

    entry1 = customtkinter.CTkEntry(win, width=322, height=35, placeholder_text="any changes?", )
    entry1.place(x=10, y=402)
    entry1.bind("<Return>", lambda x: entry1_enter())

    mic_button = customtkinter.CTkButton(
        master=win,
        image=mic_img,
        text="",
        border_width=2,
        width=60,
        height=35,
        border_color="white",
        command=takeCommandCopy
    )
    mic_button.place(x=344, y=402)

    send_button = customtkinter.CTkButton(
        master=win,
        width=60,
        height=35,
        text="Send",
        border_color="white",
        font=(customtkinter.CTkFont("arial rounded mt bold"), 16),
        border_width=2,
        command=send_mail)
    send_button.place(x=421, y=402)

    win.wait_window(window=win)
