from tkinter import *
from tkinter import filedialog

from FreeMark.tools.errors import BadOptionError
from FreeMark.tools.config import Config


class WatermarkSelector(Frame):
    def set_dark_ttk_style(self):
        from tkinter import ttk
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TEntry', fieldbackground='#23242a', foreground='white', bordercolor='#44475a', lightcolor='#44475a', darkcolor='#44475a')
        style.configure('TMenubutton', background='#44475a', foreground='white', bordercolor='#44475a', lightcolor='#44475a', darkcolor='#44475a')
        style.map('TEntry', focuscolor=[('!focus', '#44475a')])
        style.map('TMenubutton', focuscolor=[('!focus', '#44475a')])
    """
    GUI element letting the user choose the free_mark to be applied
    """
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.configure(bg='#2b2d35')
        self.config = Config('options.ini')

        self.watermark_path = StringVar()
        self.watermark_path.set(self.config.get_config()["watermark_location"])

        self.create_widgets()

    def create_widgets(self):
        self.set_dark_ttk_style()
        Label(self, text="Watermark source", font=14, bg='#2b2d35', fg='white').pack(anchor=W)
        from tkinter import ttk
        ttk.Entry(self, width=50, textvariable=self.watermark_path, style='TEntry').pack(side=LEFT)
        Button(self, text="Choose watermark",
               command=self.set_path, bg='#44475a', fg='white', activebackground='#6272a4', activeforeground='white').pack(side=LEFT, padx=10)

    def set_path(self):
        """Prompt the user, asking the to choose a file"""
        path = filedialog.askopenfilename()
        if len(path) == 0:
            # Don't do anything if the user chose nothing
            return

        self.watermark_path.set(path)
        self.config.get_config()["watermark_location"] = path
        self.config.save_config()

    def get_path(self):
        """
        Get the path to the currently selected free_mark
        :return: path to free_mark as string
        """
        path = self.watermark_path.get()
        if len(path) < 1:
            raise BadOptionError("Watermark not selected, please click the "
                                 "\"Choose watermark\" button")
        return path
