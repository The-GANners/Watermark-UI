import tkinter as tk
from FreeMark.UI.file_selector import FileSelector
from FreeMark.UI.options_pane import OptionsPane
from FreeMark.UI.worker import Worker
from FreeMark.UI.theme_manager import ThemeManager


class FreeMarkApp(tk.Frame):
    """
    Top most frame of the application, represents the 'app'
    brings together all the other major pieces, which in turn brings together 
    the smaller pieces
    """
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.theme = ThemeManager()
        self.theme.current = self.theme.DARK
        self.master.configure(bg=self.theme.current['bg'])
        self.create_widgets()

    def create_widgets(self):
        # Create listbox for files
        options_frame = tk.Frame(self.master, bg=self.theme.current['bg'])
        file_selector = FileSelector(options_frame, theme=self.theme)
        options_pane = OptionsPane(options_frame, theme=self.theme)
        file_selector.pack(side=tk.LEFT, padx=(2, 5))
        options_pane.pack(side=tk.RIGHT, fill=tk.Y, pady=10)
        options_frame.pack()
        worker = Worker(file_selector, options_pane)
        worker.pack()
