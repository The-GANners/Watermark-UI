import tkinter as tk
from tkinter import filedialog
from FreeMark.tools.errors import BadOptionError
from FreeMark.tools.config import Config
from FreeMark.UI.theme_manager import ThemeManager

class WatermarkSelector(tk.Frame):
    """
    GUI element letting the user choose the free_mark to be applied
    """
    def __init__(self, master=None, theme=None):
        super().__init__(master)
        self.master = master
        self.theme = theme or ThemeManager()
        self.config = Config('options.ini')
        self.watermark_path = tk.StringVar()
        self.watermark_path.set(self.config.get_config()["watermark_location"])
        self.theme.style_frame(self)
        self.create_widgets()

    def create_widgets(self):
        label = tk.Label(self, text="Watermark source")
        self.theme.style_label(label)
        label.pack(anchor=tk.W, pady=(8, 0))
        entry = tk.Entry(self, width=50, textvariable=self.watermark_path)
        self.theme.style_entry(entry)
        entry.pack(side=tk.LEFT, padx=4, pady=4)
        choose_btn = tk.Button(self, text="Choose watermark", command=self.set_path)
        self.theme.style_button(choose_btn)
        choose_btn.pack(side=tk.LEFT, padx=10)

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
