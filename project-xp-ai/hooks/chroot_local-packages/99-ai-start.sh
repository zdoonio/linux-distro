#!/usr/bin/env python3
import sys, subprocess, tkinter as tk
from pathlib import Path

def ask():
    root=tk.Tk();root.title("AI Assistant")
    root.geometry('400x200')
    txt=tk.Text(root);txt.pack(expand=True,fill='both')
    def send(e=None):
        q=entry.get(); entry.delete(0,'end');
        # placeholder: echo back
        txt.insert('end',f'You: {q}\n');
        txt.insert('end',f'AI: Echo – {q}\n')
    entry=tk.Entry(root);entry.pack(fill='x')
    entry.bind('<Return>',send)
    root.mainloop()
if __name__=='__main__':
    ask()
