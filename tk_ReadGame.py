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

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
random.seed(time.clock())

class Game(object):
    def __init__(self):
        with open('words.pickle', 'rb') as pf:
            self.words = pickle.load(pf)

        self.voice = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0'
        self.speech_engine = pyttsx3.init()
        self.speech_engine.setProperty('voice', self.voice)
        self.correct_choices = 0
        self.wrong_choices = 0
        self.correct_index = 0

    def randomize_correct_index(self):
        random.seed(time.clock())
        self.correct_index = random.randrange(0, len(self.words))

    def get_choice_list(self):
        '''
        Generates a list of tuples randomly generated from the master word list
        :return: list of tuples [ ($word, index), ... ]
        '''
        word_option_indexes = [self.correct_index]
        start = self.correct_index - 20
        end = self.correct_index + 20
        if start < 0:
            start = 0
        if end > len(self.words):
            end = len(self.words)-1
        for _ in range(5):
            new_index = random.randrange(start, end)
            while new_index == self.correct_index:
                new_index = random.randrange(start, end)
            word_option_indexes.append(new_index)
        random.seed(time.clock())
        random.shuffle(word_option_indexes)
        word_options = [(self.words[index], index) for index in word_option_indexes]
        return word_options

    def is_choice_correct(self, index):
        return index == self.correct_index

    def tally_points(self, index):
        if index == self.correct_index:
            self.correct_choices += 1
        else:
            self.wrong_choices += 1

    def speak_selected_word(self, index):
        speech_string = 'The word you chose is, {}\n'.format(self.words[index])
        if self.is_choice_correct(index):
            speech_string += 'Great job, That is correct,'
        else:
            speech_string += 'Sorry, that is not correct, better luck next time.'
        self.speech_engine.say(speech_string)
        self.speech_engine.runAndWait()

    def speak_word_to_find(self):
        speech_string = 'Find and click on the word {}'.format(self.words[self.correct_index])
        self.speech_engine.say(speech_string)
        self.speech_engine.runAndWait()

    def get_word_to_find(self):
        return self.words[self.correct_index]

    def get_score_string(self):
        total_choices = self.correct_choices + self.wrong_choices
        if total_choices == 0:
            rv = '0.00%'
        else:
            rv = '{:.02f}%'.format((self.correct_choices/total_choices)*100)
        return rv
    def get_score(self):
        total = self.correct_choices + self.wrong_choices
        if total == 0:
            return 0.0
        else:
            return self.correct_choices / total

    def get_current_image(self):
        current_word = self.words[self.correct_index]
        url = 'https://www.google.com/search?q={}&tbm=isch'.format(current_word)
        print(current_word)
        imgSearchClnt = requests.get(url)
        imgSearchSoup = soup(imgSearchClnt.text, 'html.parser')
        imgSearchClnt.close()
        imgClient = requests.get(imgSearchSoup.img['src'])
        img = Image.open(BytesIO(imgClient.content))
        imgClient.close()
        if img is None:
            print('failed to get image')
        return img


class MainWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # self.geometry('900x500')
        self.game = Game()
        self.game.randomize_correct_index()
        self.scores = [0.0]
        self.midline = [0.5]
        self.font = tkFont.Font(family='helvetica',size=30)


        self.word_to_find_Label = tk.Label(self, text='Click the Right Word').pack()
        self.iamScoreLabel = tk.Label(self, text='SCORE').pack(side=tk.TOP, anchor=tk.NE)
        self.score_frame = tk.Frame(self, relief=tk.RAISED, bd=2, height=500, width=500, padx=50, pady=50)
        self.score_frame.pack(side=tk.RIGHT,fill=tk.Y)
        self.score_label = tk.Label(self.score_frame, text='0')
        self.score_label.pack()

        self.plot_fig = Figure(figsize=(5, 5), dpi=100)
        self.add_plot = self.plot_fig.add_subplot(111)
        self.add_plot.plot(self.scores)
        self.canvas = FigureCanvasTkAgg(self.plot_fig, self.score_frame)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        self.canvas._tkcanvas.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        self.image_Frame = tk.Frame(self, relief=tk.RAISED, bd=2)
        self.image_Frame.pack()
        self.image_Canvas = tk.Canvas(self.image_Frame)
        self.photo = ImageTk.PhotoImage(self.game.get_current_image().resize((200, 200)))
        print(self.photo)
        self.image_Canvas.pack()
        self.image_Canvas.create_image(10, 10, image=self.photo,anchor='nw')
        self.listen_to_word_button = tk.Button(self, text='Listen to word', command=self.game.speak_word_to_find)
        self.listen_to_word_button.pack()
        self.guess_buttons = []
        for word, index in self.game.get_choice_list():
            self.guess_buttons.append(tk.Button(self, text=word, pady=5, command=lambda c=index: self.b_click(c)))

        for b in self.guess_buttons:
            b.pack(expand=1, fill=tk.BOTH)

    def b_click(self, index):
        self.game.speak_selected_word(index)
        self.game.tally_points(index)
        self.regenerate_frame()

    def regenerate_frame(self):
        self.game.randomize_correct_index()

        for b in self.guess_buttons:
            b.pack_forget()
            b.destroy()

        self.guess_buttons = []
        for word, index in self.game.get_choice_list():
            self.guess_buttons.append(tk.Button(self, text=word, command=lambda c=index: self.b_click(c)))

        for b in self.guess_buttons:
            b.pack(expand=1, fill=tk.BOTH)

        self.update_Score_Frame()
        self.update_image_Canvas()

    def update_image_Canvas(self):
        self.image_Canvas.delete(tk.ALL)
        self.photo = ImageTk.PhotoImage(self.game.get_current_image().resize((200, 200)))
        self.image_Canvas.create_image(10, 10, image=self.photo, anchor='nw')

    def update_Score_Frame(self):
        self.score_label.pack_forget()
        self.score_label.destroy()
        self.scores.append(self.game.get_score())
        self.midline.append(0.5)
        if self.game.get_score() > 0.5:
            fg = 'Green'
        else:
            fg = 'Red'
        self.score_label = tk.Label(self.score_frame, text=self.game.get_score_string(), fg=fg)
        self.score_label.pack()

        # self.canvas_widget.pack_forget()
        # self.canvas_widget.destroy()

        self.add_plot.plot(self.scores)
        self.add_plot.plot(self.midline)
        # self.canvas = FigureCanvasTkAgg(self.plot_fig, self.score_frame)
        self.canvas.draw()


        # self.canvas_widget.update()
        # self.canvas_widget = self.canvas.get_tk_widget()
        # self.canvas_widget.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

app = MainWindow()
app.mainloop()