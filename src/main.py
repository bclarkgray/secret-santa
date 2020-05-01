'''
main script to generate secret santa pool, send emails to participant, flush the sent emails

can't cheat ! hehe

args :
-email: Gmail email
-pw: gmail pw

example :


 python main.py email=toto@popo.com pw=password
'''

import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

from lib.email_flush import Flush
from lib.santa_gen import Santa

import tkinter as tk

ss = Santa('', '')

def create_SS():
    global ss
    ss = Santa(emailLogin.get(),emailPass.get())
    ss.set_number(partScale.get())

    login.destroy()

def enter_participants():
    global ss

    names = []
    emails = {}
    for i in range (0, ss.nb_ppl):
        entry = nameEntries[i]
        names.append(entry.get())
        entry = emailEntries[i]
        emails[names[i]] = entry.get()
    
    ss.set_names(names)
    ss.set_emails(emails)
    ss.gen_secrets()
    ss.send_emails()


    flush_sent = Flush(ss.usr, ss.pw, ss.nb_ppl)

    flush_sent.connectImap()
    flush_sent.deleteSentMails()
    flush_sent.cleanTrash()
    flush_sent.logout()

    partEntry.destroy()

if __name__ == '__main__':
    login = tk.Tk()
    login.title('Secret Santa Login')

    tk.Label(login, text='Email Login:').grid(row=0)
    tk.Label(login, text='Email').grid(row=1)
    tk.Label(login, text='Password').grid(row=2)

    emailLogin = tk.Entry(login)
    emailPass = tk.Entry(login, show='*')
    emailLogin.grid(row=1, column=1)
    emailPass.grid(row=2, column=1)

    partScale = tk.Scale(login, from_=3, to_=25, orient=tk.HORIZONTAL)
    partScale.grid(row=3)

    valB = tk.Button(login, text='Validate', width=25, command=create_SS)
    valB.grid(row=4, column=1)

    login.mainloop()

    partEntry = tk.Tk()
    partEntry.title('Secret Santa Participant Entry')
    
    labels = []
    nameEntries = []
    emailEntries = []
    participants = []

    for i in range(0, ss.nb_ppl):
        #str = 'Participant ' + i
        tk.Label(partEntry, text='Participant #' + str(i+1) + ': Name:').grid(row=i, column=0)
        tk.Label(partEntry, text='Email:').grid(row=i, column=2)

        entry = tk.Entry(partEntry)
        entry.grid(row=i, column=1)
        nameEntries.append(entry)

        entry = tk.Entry(partEntry)
        entry.grid(row=i, column=3)
        emailEntries.append(entry)

    enterBtn = tk.Button(partEntry, text='Send Secret Santas!', width='25', command=enter_participants)
    enterBtn.grid(row=ss.nb_ppl+1)
    partEntry.mainloop()