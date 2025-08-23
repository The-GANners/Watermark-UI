import tkinter as tk
from tkinter import filedialog, messagebox
import os
import re
from ..tools.errors import BadOptionError
from FreeMark.UI.theme_manager import ThemeManager

NONE = 0
PRE = 1
SUFFIX = 2

class OutputSelector(tk.Frame):
    """
    Class for selecting output destination and generating paths
    """
    def __init__(self, master=None, theme=None):
        super().__init__(master)
        self.theme = theme or ThemeManager()
        self.fix = tk.StringVar()
        self.fix_position = tk.IntVar()
        self.output_dir = tk.StringVar()
        self.output_dir.set("Choose output folder")
        self.validate_pattern = re.compile(r'[<|>*:?"/\\]')
        self.entry_frame = tk.Frame(self)
        self.fix_frame = tk.Frame(self)
        self.radio_frame = tk.Frame(self.fix_frame)
        self.theme.style_frame(self)
        self.theme.style_frame(self.entry_frame)
        self.theme.style_frame(self.fix_frame)
        self.theme.style_frame(self.radio_frame)
        self.create_widgets()

    def create_widgets(self):
        label = tk.Label(self, text="Output options")
        self.theme.style_label(label)
        label.pack(anchor=tk.W, pady=(8, 0))
        entry = tk.Entry(self.entry_frame, width=50, textvariable=self.output_dir)
        self.theme.style_entry(entry)
        entry.pack(side=tk.LEFT, padx=4, pady=4)
        choose_btn = tk.Button(self.entry_frame, text="Choose folder", command=self.choose_dir)
        self.theme.style_button(choose_btn)
        choose_btn.pack(side=tk.LEFT, padx=10)
        self.entry_frame.pack(fill=tk.X, pady=5)
        rename_label = tk.Label(self, text="Rename files")
        self.theme.style_label(rename_label)
        rename_label.pack(anchor=tk.W, pady=(8, 0))
        fix_label = tk.Label(self.fix_frame, text="Fix: ")
        self.theme.style_label(fix_label)
        fix_label.pack(side=tk.LEFT)
        validate = (self.register(self.validate_fix), '%P')
        fix_entry = tk.Entry(self.fix_frame, width=30, validate="key", validatecommand=validate, textvariable=self.fix)
        self.theme.style_entry(fix_entry)
        fix_entry.pack(side=tk.LEFT, padx=5)
        postfix_radio = tk.Radiobutton(self.radio_frame, text="Postfix", variable=self.fix_position, value=SUFFIX)
        prefix_radio = tk.Radiobutton(self.radio_frame, text="Prefix", variable=self.fix_position, value=PRE)
        none_radio = tk.Radiobutton(self.radio_frame, text="None", variable=self.fix_position, value=NONE)
        for radio in [postfix_radio, prefix_radio, none_radio]:
            radio.configure(bg=self.theme.current['bg'], fg=self.theme.current['fg'], selectcolor=self.theme.current['accent'], font=('Segoe UI', 10))
            radio.pack(side=tk.RIGHT, padx=4)
        self.radio_frame.pack(anchor=tk.CENTER)
        self.fix_frame.pack(fill=tk.X)

    def lock(self):
        """
        Lock down the output selector so the user doesn't mess with it
        while it's running
        """
        for child in (self.fix_frame.winfo_children()
                      + self.radio_frame.winfo_children()
                      + self.entry_frame.winfo_children()):
            try:
                child.config(state=tk.DISABLED)
            except tk.TclError:
                pass

    def unlock(self):
        """
        Opposite of lock
        """
        for child in (self.fix_frame.winfo_children()
                      + self.radio_frame.winfo_children()
                      + self.entry_frame.winfo_children()):
            try:
                child.config(state=tk.NORMAL)
            except tk.TclError:
                pass

    def validate_fix(self, fix_change):
        assert type(fix_change) == str, "Path must be a string"

        if re.search(self.validate_pattern, fix_change):
            return False

        return True

    def choose_dir(self):
        """
        Prompts the user to choose a folder.
        Bound to button next to folder entry
        """
        self.output_dir.set(filedialog.askdirectory())

    def get_dir(self):
        """
        Returns the currently selected dir
        """
        out_path = self.output_dir.get().rstrip().lstrip()

        if out_path.strip() == "":
            raise BadOptionError("Missing output location, please click the "
                                 "\"Choose Folder\" button")

        if not os.path.isabs(out_path):
            raise BadOptionError("Invalid output location, please click the "
                                 "\"Choose Folder\" button")

        if os.path.isdir(out_path):
            return out_path

        if messagebox.askyesno("Create folder",
                               "Folder doesn't exist, create it?"):
            try:
                os.makedirs(out_path)
            except OSError:
                raise BadOptionError("Invalid character in folder name.")
            return out_path
        else:
            raise BadOptionError("Output location doesn't exist.")

    def rename_file(self, filename, abs_path=False):
        """
        extract file name and apply suffix or prefix
        :param filename: file name or path
        :param abs_path: kwarg, true if filename isn't a filename but a path
        :return: 
        """
        if abs_path:
            filename = os.path.split(filename)[-1]

        if self.fix_position.get() == NONE:
            return filename
        elif self.fix_position.get() == PRE:
            return "{}_{}".format(self.fix.get(), filename)
        elif self.fix_position.get() == SUFFIX:
            filename = filename.rsplit('.', maxsplit=1)
            return "{}_{}.{}".format(filename[0], self.fix.get(), filename[1])

    def get_output_path(self, input_path, output_path):
        """
        Get output path from an input path
        :param input_path: path to original image
        :return: path to image destination
        """
        filename = self.rename_file(input_path, abs_path=True)
        return os.path.join(output_path, filename)
