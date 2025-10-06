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
        # NEW: watermark mode and text
        self.mode = StringVar()
        self.mode.set("image")  # "image" | "text"
        self.text_value = StringVar()
        self.text_value.set("Sample Watermark")

        # NEW: references for toggling
        self.image_source_frame = None
        self.text_frame = None

        self.create_widgets()

    def create_widgets(self):
        self.set_dark_ttk_style()
        # NEW: Mode toggle
        mode_frame = Frame(self, bg='#2b2d35')
        Label(mode_frame, text="Watermark mode", font=14, bg='#2b2d35', fg='white').pack(anchor=W)
        Radiobutton(mode_frame, text="Image", variable=self.mode, value="image",
                    bg='#2b2d35', fg='white', selectcolor='#44475a',
                    activebackground='#2b2d35', activeforeground='white',
                    command=self.on_mode_change  # NEW
                    ).pack(side=LEFT, padx=5)
        Radiobutton(mode_frame, text="Text", variable=self.mode, value="text",
                    bg='#2b2d35', fg='white', selectcolor='#44475a',
                    activebackground='#2b2d35', activeforeground='white',
                    command=self.on_mode_change  # NEW
                    ).pack(side=LEFT, padx=5)
        mode_frame.pack(anchor=W, pady=(0, 6))

        # NEW: Group watermark source into its own frame for easy hide/show
        self.image_source_frame = Frame(self, bg='#2b2d35')
        Label(self.image_source_frame, text="Watermark source", font=14, bg='#2b2d35', fg='white').pack(anchor=W)
        from tkinter import ttk
        row = Frame(self.image_source_frame, bg='#2b2d35')
        ttk.Entry(row, width=50, textvariable=self.watermark_path, style='TEntry').pack(side=LEFT)
        Button(row, text="Choose watermark",
               command=self.set_path, bg='#44475a', fg='white',
               activebackground='#6272a4', activeforeground='white').pack(side=LEFT, padx=10)
        row.pack(anchor=W)
        self.image_source_frame.pack(anchor=W)  # initial pack; will be toggled

        # NEW: Text input frame
        self.text_frame = Frame(self, bg='#2b2d35')
        Label(self.text_frame, text="Text watermark", bg='#2b2d35', fg='white').pack(side=LEFT)
        ttk.Entry(self.text_frame, width=40, textvariable=self.text_value, style='TEntry').pack(side=LEFT, padx=8)
        self.text_frame.pack(anchor=W, pady=(8, 0))

        # Initialize visibility
        self.on_mode_change()

    # FIX: re-add set_path handler used by the button
    def set_path(self):
        """Prompt the user to choose a watermark image file"""
        path = filedialog.askopenfilename()
        if len(path) == 0:
            return
        self.watermark_path.set(path)
        self.config.get_config()["watermark_location"] = path
        self.config.save_config()

    # NEW: toggle UI sections based on mode
    def on_mode_change(self):
        mode = self.mode.get()
        if mode == "image":
            # show image source, hide text input
            if self.image_source_frame is not None:
                self.image_source_frame.pack(anchor=W)
            if self.text_frame is not None:
                self.text_frame.pack_forget()
        else:
            # show text input, hide image source
            if self.image_source_frame is not None:
                self.image_source_frame.pack_forget()
            if self.text_frame is not None:
                self.text_frame.pack(anchor=W, pady=(8, 0))

    # NEW: getters for mode and text
    def get_mode(self):
        return self.mode.get()

    def get_text(self):
        txt = self.text_value.get().strip()
        if self.get_mode() == "text" and len(txt) == 0:
            raise BadOptionError('Watermark text is empty. Please enter text or switch to Image mode.')
        return txt

    def get_path(self):
        """
        Get the path to the currently selected free_mark
        :return: path to free_mark as string
        """
        if self.get_mode() == "text":
            # Image file path is irrelevant in text mode
            return ""
        path = self.watermark_path.get()
        if len(path) < 1:
            raise BadOptionError("Watermark not selected, please click the "
                                 "\"Choose watermark\" button")
        return path
