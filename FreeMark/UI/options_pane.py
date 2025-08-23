import tkinter as tk
from FreeMark.UI.ouput_selector import OutputSelector
from FreeMark.UI.watermark_selector import WatermarkSelector
from FreeMark.UI.watermark_options import WatermarkOptions
from FreeMark.UI.theme_manager import ThemeManager

class OptionsPane(tk.Frame):
    """
    Frame for holding all the options elements, is also used as an interface
    to supply the worker with settings and services
    """
    def __init__(self, master=None, theme=None):
        super().__init__(master)
        self.theme = theme or ThemeManager()
        self.theme.style_frame(self)
        self.output_selector = OutputSelector(self, theme=self.theme)
        self.watermark_selector = WatermarkSelector(self, theme=self.theme)
        self.watermark_options = WatermarkOptions(self, theme=self.theme)
        self.create_widgets()

    def create_widgets(self):
        pady = 8
        self.label = tk.Label(self, text="Settings")
        self.theme.style_label(self.label)
        self.label.pack(anchor=tk.N, pady=(pady, 0))
        self.watermark_selector.pack(fill=tk.X, pady=pady, anchor=tk.N)
        self.watermark_options.pack(fill=tk.X, pady=pady, anchor=tk.N)
        self.output_selector.pack(fill=tk.X, anchor=tk.N)

    def get_watermark_path(self):
        """
        Get path to the currently selected free_mark
        :return: path to free_mark as string
        """
        return self.watermark_selector.get_path()

    def get_output_path(self):
        return self.output_selector.get_dir()

    def create_output_path(self, input_path, output_path):
        return self.output_selector.get_output_path(input_path, output_path)

    def get_watermark_pos(self):
        return self.watermark_options.position.get()

    def get_padding(self):
        return (int(self.watermark_options.padx.get()), self.watermark_options.unit_x.get()), \
               (int(self.watermark_options.pady.get()), self.watermark_options.unit_y.get())

    def get_opacity(self):
        return self.watermark_options.opacity.get()/100

    def should_scale(self):
        return self.watermark_options.scale_watermark.get()
