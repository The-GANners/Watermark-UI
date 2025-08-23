import tkinter as tk
from tkinter.ttk import OptionMenu
from FreeMark.UI.theme_manager import ThemeManager

class WatermarkOptions(tk.Frame):
    def __init__(self, master=None, theme=None):
        super().__init__(master)
        self.theme = theme or ThemeManager()
        self.position = tk.StringVar()
        self.position.set("SE")
        self.padx = tk.StringVar()
        self.pady = tk.StringVar()
        self.unit_x = tk.StringVar()
        self.unit_y = tk.StringVar()
        self.padx.set(20)
        self.pady.set(5)
        self.unit_options = ["", "px", "%"]
        self.unit_x.set(self.unit_options[1])
        self.unit_y.set(self.unit_options[1])
        self.scale_watermark = tk.BooleanVar()
        self.scale_watermark.set(True)
        self.opacity = tk.IntVar()
        self.opacity.set(100)
        self.theme.style_frame(self)
        self.create_widgets()

    def create_widgets(self):
        padx = 5
        pady = 5
        label = tk.Label(self, text="Watermark options")
        self.theme.style_label(label)
        label.pack(anchor=tk.W, pady=(8, 0))
        pos_options = tk.Frame(self)
        self.theme.style_frame(pos_options)
        pos_label = tk.Label(pos_options, text="Position")
        self.theme.style_label(pos_label)
        pos_label.pack(anchor=tk.W)

        # -- Padding --
        validate = (self.register(self.validate_int), '%P')
        padding_frame = tk.Frame(pos_options)
        self.theme.style_frame(padding_frame)
        pad_x_label = tk.Label(padding_frame, text="Pad x")
        self.theme.style_label(pad_x_label)
        pad_x_label.grid(column=0, row=0)
        pad_x_entry = tk.Entry(padding_frame, textvariable=self.padx, validate="key", width=5, validatecommand=(self.register(self.validate_int), '%P'))
        self.theme.style_entry(pad_x_entry)
        pad_x_entry.grid(column=1, row=0, padx=padx)
        pad_x_unit = OptionMenu(padding_frame, self.unit_x, *self.unit_options)
        pad_x_unit.grid(column=3, row=0)
        pad_y_label = tk.Label(padding_frame, text="Pad y")
        self.theme.style_label(pad_y_label)
        pad_y_label.grid(column=0, row=1)
        pad_y_entry = tk.Entry(padding_frame, textvariable=self.pady, validate="key", width=5, validatecommand=(self.register(self.validate_int), '%P'))
        self.theme.style_entry(pad_y_entry)
        pad_y_entry.grid(column=1, row=1, padx=padx, pady=pady)
        pad_y_unit = OptionMenu(padding_frame, self.unit_y, *self.unit_options)
        pad_y_unit.grid(column=3, row=1)
        padding_frame.pack(side=tk.LEFT)
        pos_frame = tk.Frame(pos_options)
        self.theme.style_frame(pos_frame)
        radio_pad = 5
        radios = [
            ("Top left", "NW", 0, 0),
            ("Top right", "NE", 1, 0),
            ("Bottom left", "SW", 0, 1),
            ("Bottom right", "SE", 1, 1)
        ]
        for text, value, col, row in radios:
            radio = tk.Radiobutton(pos_frame, text=text, variable=self.position, value=value)
            radio.configure(bg=self.theme.current['bg'], fg=self.theme.current['fg'], selectcolor=self.theme.current['accent'], font=('Segoe UI', 10))
            radio.grid(column=col, row=row, sticky=tk.W, padx=radio_pad, pady=radio_pad)
        pos_frame.pack(side=tk.LEFT, padx=30)
        pos_options.pack(anchor=tk.W)
        opacity_label = tk.Label(self, text="Opacity and size")
        self.theme.style_label(opacity_label)
        opacity_label.pack(anchor=tk.W, pady=(8, 0))
        opacity_frame = tk.Frame(self)
        self.theme.style_frame(opacity_frame)
        op_label = tk.Label(opacity_frame, text="Opacity")
        self.theme.style_label(op_label)
        op_label.pack(side=tk.LEFT, anchor=tk.S)
        op_scale = tk.Scale(opacity_frame, from_=0, to=100, orient=tk.HORIZONTAL, variable=self.opacity)
        op_scale.configure(bg=self.theme.current['bg'], fg=self.theme.current['fg'], troughcolor=self.theme.current['accent'])
        op_scale.pack(side=tk.LEFT, anchor=tk.N, padx=5)
        op_entry = tk.Entry(opacity_frame, textvariable=self.opacity, width=4, validate="key", validatecommand=(self.register(self.validate_int), '%P'))
        self.theme.style_entry(op_entry)
        op_entry.pack(side=tk.LEFT, anchor=tk.S, pady=3)
        percent_label = tk.Label(opacity_frame, text="%")
        self.theme.style_label(percent_label)
        percent_label.pack(side=tk.LEFT, anchor=tk.S, pady=3)
        opacity_frame.pack(anchor=tk.W)
        resize_check = tk.Checkbutton(self, text="Auto resize watermark", variable=self.scale_watermark, onvalue=True, offvalue=False)
        resize_check.configure(bg=self.theme.current['bg'], fg=self.theme.current['fg'], selectcolor=self.theme.current['accent'], font=('Segoe UI', 10))
        resize_check.pack(anchor=tk.W, pady=(5, 0))

    @staticmethod
    def validate_int(number):
        try:
            int(number)
        except ValueError:
            if len(number.strip()) == 0:
                # Allow the field to be empty
                return True
            return False
        else:
            return True
