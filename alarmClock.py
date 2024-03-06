from tkinter.ttk import *
from tkinter import *
from PIL import ImageTk, Image
from datetime import datetime, timedelta
from time import sleep
from pygame import mixer
from threading import Thread
from plyer import notification

bg_color = '#ffffff'
col1 = "#566FC6"
col2 = "#000000"
window = Tk()
window.title("")
window.geometry('400x250')
window.configure(bg=bg_color)

frame_line = Frame(window, width=600, height=5, bg=col1)
frame_line.grid(row=0, column=0)

frame_body = Frame(window, width=600, height=290, bg=bg_color)
frame_body.grid(row=1, column=0)

img = Image.open('clock.png')
img = img.resize((110, 110))  
img = ImageTk.PhotoImage(img)
app_image = Label(frame_body, height=110, image=img, bg=bg_color)
app_image.place(x=10, y=35)

name = Label(frame_body, text="Set Alarm", height=1, font=('Ivy 18 bold'), bg=bg_color)
name.place(x=132, y=10)

hour = Label(frame_body, text="hour", height=1, font=('Ivy 10 bold'), bg=bg_color, fg=col1)
hour.place(x=132, y=40)
comb_hour = Combobox(frame_body, width=2, font=('arial 15'))
comb_hour['values'] = ("00","01","02","03","04","05","06","07","08","09","10","11","12")
comb_hour.current(0)
comb_hour.place(x=135, y=58)

minute = Label(frame_body, text="min", height=1, font=('Ivy 10 bold'), bg=bg_color, fg=col1)
minute.place(x=182, y=40)
comb_minute = Combobox(frame_body, width=2, font=('arial 15'))
comb_minute['values'] = tuple("{:02d}".format(i) for i in range(60))
comb_minute.current(0)
comb_minute.place(x=184, y=58)

seconds = Label(frame_body, text="sec", height=1, font=('Ivy 10 bold'), bg=bg_color, fg=col1)
seconds.place(x=229, y=40)
comb_seconds = Combobox(frame_body, width=2, font=('arial 15'))
comb_seconds['values'] = tuple("{:02d}".format(i) for i in range(60))
comb_seconds.current(0)
comb_seconds.place(x=232, y=58)

amAndpm = Label(frame_body, text="period", height=1, font=('Ivy 10 bold'), bg=bg_color, fg=col1)
amAndpm.place(x=280, y=40)
comb_amAndpm = Combobox(frame_body, width=3, font=('arial 15'))
comb_amAndpm['values'] = ("AM","PM")
comb_amAndpm.current(0)
comb_amAndpm.place(x=283, y=58)

remaining_time_label = Label(frame_body, text="", font=('Ivy 10 bold'), bg=bg_color, fg=col1)
remaining_time_label.place(x=132, y=90)
alarm_running = False
def activate_alarm():
    global alarm_running
    alarm_running = True
    t = Thread(target=alarm)
    t.start()

def deactivate_alarm():
    global alarm_running
    print('Stop alarm:', selected.get() )
    mixer.music.stop()
    if selected.get() == 2 and int(comb_hour.get()) != 0:
        notification.notify(
            title='Alarm Deactivated',
            message='The alarm has been deactivated.',
            app_name='Alarm App'
        )
    alarm_running = False


selected = IntVar()
radio1 = Radiobutton(frame_body, font=('arial 10 bold'), value=1, text="On", bg=bg_color, command=activate_alarm, variable=selected)
radio1.place(x=127,y=130)

radio2 = Radiobutton(frame_body, font=('arial 10 bold'), value=2, text="Off", bg=bg_color, command=deactivate_alarm, variable=selected)
radio2.place(x=189,y=130)

def sound_alarm():
    mixer.music.load('alarm.mp3')
    mixer.music.play()
    selected.set(0)

def alarm():
    while alarm_running:
        global control
        control = selected.get()
        print(control)
        global alarm_hour
        alarm_hour = int(comb_hour.get())
        alarm_minutes = int(comb_minute.get())
        alarm_seconds = int(comb_seconds.get())
        alarm_period = comb_amAndpm.get().upper()
        
        now = datetime.now()
        
        hour = int(now.strftime("%I"))
        minutes = int(now.strftime("%M"))
        seconds = int(now.strftime("%S"))
        period = now.strftime("%p")

        if control == 1:
            if alarm_period == period:
                if alarm_hour == hour:
                    if alarm_minutes == minutes:
                        if alarm_seconds == seconds:
                            print("Alarm Time!")
                            sound_alarm()
        
        alarm_time = datetime(now.year, now.month, now.day, alarm_hour, alarm_minutes, alarm_seconds)
        if alarm_period == "PM" and hour < 12:
            alarm_time += timedelta(hours=12)
        elif alarm_period == "AM" and hour == 12:
            alarm_time -= timedelta(hours=12)
        
        if control == 1:
            if alarm_time < now:
                alarm_time += timedelta(days=1)
            remaining_seconds = (alarm_time - now).total_seconds()
            remaining_time_label.config(text=f"Remaining Time: {int(remaining_seconds) // 3600:02}:{int(remaining_seconds % 3600) // 60:02}:{int(remaining_seconds) % 60:02}")
        sleep(1)

mixer.init()

window.mainloop()
