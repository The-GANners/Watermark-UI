from tkinter import *
# tkinter OptionMenu is hella ugly so use ttk
from tkinter.ttk import OptionMenu


class WatermarkOptions(Frame):

    def set_dark_ttk_style(self):
        from tkinter import ttk
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TMenubutton', background='#44475a', foreground='white', bordercolor='#44475a', 
                       lightcolor='#44475a', darkcolor='#44475a', arrowcolor='white')
        style.map('TMenubutton', 
                 background=[('active', '#6272a4'), ('pressed', '#6272a4')],
                 foreground=[('active', 'white'), ('pressed', 'white')],
                 arrowcolor=[('active', 'white'), ('pressed', 'white')])

    def __init__(self, master=None):
        super().__init__(master)
        self.configure(bg='#2b2d35')

        self.position = StringVar()
        self.position.set("SE")

        self.padx = StringVar()
        self.pady = StringVar()
        self.unit_x = StringVar()
        self.unit_y = StringVar()
        self.padx.set(20)
        self.pady.set(5)
        # ttk is super weird and demands that the first option is left blank
        self.unit_options = ["", "px", "%"]
        self.unit_x.set(self.unit_options[1])
        self.unit_y.set(self.unit_options[1])

        self.scale_watermark = BooleanVar()
        self.scale_watermark.set(True)

        self.opacity = IntVar()
        self.opacity.set(100)

        self.create_widgets()

    def create_widgets(self):
      self.set_dark_ttk_style()
      padx = 5
      pady = 5
      Label(self, text="Watermark options", font=14, bg='#2b2d35', fg='white').pack(anchor=W)

      # --------- Position options ---------
      pos_options = Frame(self, bg='#2b2d35')
      Label(pos_options, text="Position", bg='#2b2d35', fg='white').pack(anchor=W)

      # -- Padding --
      validate = (self.register(self.validate_int), '%P')
      padding_frame = Frame(pos_options, bg='#2b2d35')
      # Horizontal padding
      Label(padding_frame, text="Pad x", bg='#2b2d35', fg='white').grid(column=0, row=0)
      Entry(padding_frame, textvariable=self.padx, validate="key", width=5,
          validatecommand=validate, bg='#23242a', fg='white', insertbackground='white',
          highlightbackground='#2b2d35', highlightcolor='#6272a4', highlightthickness=1).grid(column=1, row=0, padx=padx)
      OptionMenu(padding_frame, self.unit_x,
             *self.unit_options).grid(column=3, row=0)

      # Vertical padding
      Label(padding_frame, text="Pad y", bg='#2b2d35', fg='white').grid(column=0, row=1)
      Entry(padding_frame, textvariable=self.pady, validate="key", width=5,
          validatecommand=validate, bg='#23242a', fg='white', insertbackground='white',
          highlightbackground='#2b2d35', highlightcolor='#6272a4', highlightthickness=1).grid(column=1, row=1,
                               padx=padx, pady=pady)
      OptionMenu(padding_frame, self.unit_y,
             *self.unit_options).grid(column=3, row=1)

      padding_frame.pack(side=LEFT)

      pos_frame = Frame(pos_options, bg='#2b2d35')
      radio_pad = 5
      # -- Position --
      Radiobutton(pos_frame, text="Top left", variable=self.position,
              value="NW", bg='#2b2d35', fg='white', selectcolor='#44475a', activebackground='#2b2d35', activeforeground='white').grid(column=0, row=0, sticky=W,
                         padx=radio_pad, pady=radio_pad)

      Radiobutton(pos_frame, text="Top right", variable=self.position,
              value="NE", bg='#2b2d35', fg='white', selectcolor='#44475a', activebackground='#2b2d35', activeforeground='white').grid(column=1, row=0, sticky=W,
                         padx=radio_pad, pady=radio_pad)

      Radiobutton(pos_frame, text="Bottom left", variable=self.position,
              value="SW", bg='#2b2d35', fg='white', selectcolor='#44475a', activebackground='#2b2d35', activeforeground='white').grid(column=0, row=1,
                         padx=radio_pad, pady=radio_pad)

      Radiobutton(pos_frame, text="Bottom right", variable=self.position,
              value="SE", bg='#2b2d35', fg='white', selectcolor='#44475a', activebackground='#2b2d35', activeforeground='white').grid(column=1, row=1,
                         padx=radio_pad, pady=radio_pad)
      pos_frame.pack(side=LEFT, padx=30)

      pos_options.pack(anchor=W)

      # ---------- Opacity options ---------
      Label(self, text="Opacity and size", bg='#2b2d35', fg='white').pack(anchor=W)
      opacity_frame = Frame(self, bg='#2b2d35')
      Label(opacity_frame, text="Opacity", bg='#2b2d35', fg='white').pack(side=LEFT, anchor=S)

      Scale(opacity_frame, from_=0, to=100, orient=HORIZONTAL,
          variable=self.opacity, bg='#2b2d35', fg='white', troughcolor='#23242a', 
          activebackground='#6272a4', highlightbackground='#2b2d35').pack(side=LEFT, anchor=N, padx=5)

      Entry(opacity_frame, textvariable=self.opacity, width=4,
          validate="key", validatecommand=validate, bg='#23242a', fg='white', insertbackground='white',
          highlightbackground='#2b2d35', highlightcolor='#6272a4', highlightthickness=1).pack(side=LEFT,
                             anchor=S, pady=3)

      Label(opacity_frame, text="%", bg='#2b2d35', fg='white').pack(side=LEFT, anchor=S, pady=3)
      opacity_frame.pack(anchor=W)

      # ----------- Size options -----------
      Checkbutton(self, text="Auto resize watermark",
            variable=self.scale_watermark,
            onvalue=True, offvalue=False, bg='#2b2d35', fg='white', selectcolor='#44475a', 
            activebackground='#2b2d35', activeforeground='white').pack(anchor=W, pady=(5, 0))

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
