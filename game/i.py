import threading
import tkinter.messagebox
threading.Thread(
    target=lambda: tkinter.messagebox.showmessage('hi', 'hi')).start()
from queue import Queue
Q = Queue()


def p():
    print(Q.get())


t = threading.Thread(target=p)
t.start()
while True:
    Q.put(input('type to send a message to t: '))
