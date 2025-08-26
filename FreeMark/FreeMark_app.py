from tkinter import *

from FreeMark.UI.file_selector import FileSelector
from FreeMark.UI.options_pane import OptionsPane
from FreeMark.UI.worker import Worker


class FreeMarkApp(Frame):
    """
    Top most frame of the application, represents the 'app'
    brings together all the other major pieces, which in turn brings together 
    the smaller pieces
    """
    def __init__(self, master=None):
        Frame.__init__(self, master, bg='#2b2d35')
        self.master = master
        self.master.configure(bg='#2b2d35')
        self.create_widgets()

    def create_widgets(self):
        """Create the GUI elements"""
        options_frame = Frame(self.master, bg='#2b2d35')
        file_selector = FileSelector(options_frame, bg='#2b2d35')
        options_pane = OptionsPane(options_frame, bg='#2b2d35')

        file_selector.pack(side=LEFT, padx=(2, 5))
        options_pane.pack(side=RIGHT, fill=Y, pady=10)

        options_frame.pack()

        worker = Worker(file_selector, options_pane, bg='#2b2d35')
        worker.pack()
