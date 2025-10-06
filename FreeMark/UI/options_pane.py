from tkinter import *

from FreeMark.UI.ouput_selector import OutputSelector
from FreeMark.UI.watermark_selector import WatermarkSelector
from FreeMark.UI.watermark_options import WatermarkOptions


class OptionsPane(Frame):
    """
    Frame for holding all the options elements, is also used as an interface
    to supply the worker with settings and services
    """
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(bg='#2b2d35')

        self.output_selector = OutputSelector(self)
        self.watermark_selector = WatermarkSelector(self)
        self.watermark_options = WatermarkOptions(self)
        self.create_widgets()
        # NEW: react to mode change to toggle text style options
        try:
            self.watermark_selector.mode.trace('w', self._on_mode_change)
        except Exception:
            pass
        # Initialize visibility per current mode
        self._on_mode_change()

    def _on_mode_change(self, *args):
        mode = self.get_watermark_mode()
        if mode == "image":
            self.watermark_options.hide_text_style()
        else:
            self.watermark_options.show_text_style()

    def create_widgets(self):
        """Create the graphical element"""
        pady = 5
        Label(self, text="Settings", font=14, bg='#2b2d35', fg='white').pack(anchor=N)
        self.watermark_selector.pack(fill=X, pady=pady, anchor=N)
        self.watermark_options.pack(fill=X, pady=pady, anchor=N)
        self.output_selector.pack(fill=X, anchor=N)

    def get_watermark_path(self):
        """
        Get path to the currently selected free_mark
        :return: path to free_mark as string
        """
        return self.watermark_selector.get_path()

    # NEW: expose mode and text config
    def get_watermark_mode(self):
        return self.watermark_selector.get_mode()

    def get_text_value(self):
        return self.watermark_selector.get_text()

    def get_text_size(self):
        return int(self.watermark_options.text_size.get())

    def get_text_color(self):
        return self.watermark_options.text_color.get()

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
