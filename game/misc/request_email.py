"""
request_email.py
requests the user's email address for bug reports.
"""
import tkinter as tk
import os

MESSAGE = '''you can enter your email
address here, and if the game crahses,
it should be reported to me,
and I can get back to you and \ntry and get it fixed!\n
(it is completely optional,\npress \'skip\' to continue)
if you dont get it, it means you didnt enter the correct email address.
contact me at <michaelveenstra12@gmail.com> for help if you do that

you should recieve a confirmation email :)
oh yeah, I wont sell it to anyone either'''

try:
    FILE = os.path.join((os.environ['USERPROFILE'] if os.name ==
                         'nt' else os.environ['']), '.stickman_new_world', 'useremail')
except KeyError:
    wrong_os()


def main():
    print('hi')
    variables = {}

    if os.path.exists(FILE):
        return

    root = tk.Tk()
    root.title('email address')
    root.geometry('250x270')
    root.protocol('WM_DELETE_WINDOW', lambda: exit(variables))

    entry = tk.Entry(root, text='email:')
    entry.place(anchor='center', relx=0.5, rely=0.5)
    entry.pack(fill=None, expand=True)

    label = tk.Label(root, text=MESSAGE)
    label.pack(fill=None, expand=True)

    skip = tk.Button(root, text='skip', command=lambda: exit(variables))
    skip.place(x=220, y=100)
    skip.pack()

    done = tk.Button(root, text='done',
                     command=lambda: get_text(entry, variables))
    done.place(x=200, y=100)
    done.pack()

    while True:
        print('hi')
        if variables.get('quit'):
            return

        elif variables.get('entry_data'):
            remember(variables)
            send_confirm(variables)
            root.destroy()

        root.update()


def get_text(entry, variables):
    print(entry.get())
    variables['entry_data'] = entry.get()


def exit(v):
    v['quit'] = True


def remember(item):
    with open(FILE, 'w') as openfile:
        openfile.write(item['entry_data'])
    exit(item)


def send_confirm(items):
    import smtplib
    import bugreport
    from cryptography.fernet import Fernet

    sender = 'bugreporter.smr@gmail.com'
    reciever = [items['entry_data']]
    message = f'''To: <{reciever}>
From: <{sender}>
Subject: confirmation email


Hi! if you are recieving this email, it means you have successfully
gotten your email address to me. Since you didn't give your password,
you shouldnt have any troubles. I will only use this when I have a very important
thing to tell you, or if the game crashes on your computer, I will be alerted
and try to fix the problem and tell you about it as well. Thanks!

-sincerely, Michael Gill (creater of stickman\'s new world)
'''
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    a = Fernet(bugreport.HIUEFWILEIURFHE).decrypt(
        bugreport.FYUKYFVKFYVHUFL).decode()
    server.ehlo()
    server.login(sender, a)
    server.sendmail(sender, reciever, message)
    server.close()


try:
    main()

except Exception as e:
    import bugreport
    bugreport.default_smr(e, 'in request_email')
