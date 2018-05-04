
import tkinter as tk
import tkinter.font as tkFont
import pyttsx3
import pickle
import random
import time
import requests
from bs4 import BeautifulSoup as soup
from PIL import Image, ImageTk
from io import BytesIO


def get_current_image(search):
    url = 'https://www.google.com/search?q={}&tbm=isch'.format(search)
    imgSearchClnt = requests.get(url)
    imgSearchSoup = soup(imgSearchClnt.text, 'html.parser')
    imgSearchClnt.close()
    imgClient = requests.get(imgSearchSoup.img['src'])
    img = Image.open(BytesIO(imgClient.content))
    imgClient.close()
    if img is None:
        print('failed to get image')
    return img


root = tk.Tk()
root.title("display image")
im= get_current_image('elephant')
photo=ImageTk.PhotoImage(im)
frm = tk.Frame(root)
frm.pack(side='top', fill='both', expand='yes')
cv = tk.Canvas(frm)
cv.pack(side='top', fill='both', expand='yes')
cv.create_image(20, 20, image=photo, anchor='nw')
root.mainloop()