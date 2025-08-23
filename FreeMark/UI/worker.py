import tkinter as tk
from tkinter.ttk import Progressbar
from tkinter import messagebox
import threading
import queue
import os
from ..tools.errors import BadOptionError
from FreeMark.tools.watermarker import WaterMarker
from FreeMark.UI.remaining_time import RemainingTime
from FreeMark.UI.theme_manager import ThemeManager

class Worker(tk.Frame):
    """
    Worker gui elements, does all the actual work to the images with the
    watermarker class and contains progressbar and startbutton
    """
    def __init__(self, file_selector, options_pane, master=None, theme=None):
        super().__init__(master)
        self.theme = theme or ThemeManager()
        self.running = False
        self.image_que = queue.Queue()
        self.file_selector = file_selector
        self.option_pane = options_pane
        self.watermarker = WaterMarker
        self.progress_var = tk.IntVar()
        self.file_count = tk.IntVar()
        self.counter_frame = tk.Frame(self, bg=self.theme.current['bg'])
        self.progress_bar = Progressbar(self, orient="horizontal", mode="determinate", length=600)
        self.time_tracker = RemainingTime(self.counter_frame, theme=self.theme)
        self.button_frame = tk.Frame(self, bg=self.theme.current['bg'])
        self.start_button = tk.Button(self.button_frame, text="Start", command=self.apply_watermarks, width=10, bg=self.theme.current['button_bg'], fg=self.theme.current['button_fg'], font=('Segoe UI', 11, 'bold'), relief=tk.FLAT, bd=0, highlightthickness=0)
        self.stop_button = tk.Button(self.button_frame, text="Stop", command=self.stop_work, width=10, bg=self.theme.current['button_bg'], fg=self.theme.current['button_fg'], font=('Segoe UI', 11, 'bold'), relief=tk.FLAT, bd=0, highlightthickness=0)
        self.theme.style_frame(self)
        self.create_widgets()

    def create_widgets(self):
        self.counter_frame.pack()
        self.time_tracker.pack(side=tk.LEFT, padx=(0, 10))
        progress_label = tk.Label(self.counter_frame, textvariable=self.progress_var, bg=self.theme.current['bg'], fg=self.theme.current['fg'], font=('Segoe UI', 11))
        slash_label = tk.Label(self.counter_frame, text="/", bg=self.theme.current['bg'], fg=self.theme.current['fg'], font=('Segoe UI', 11))
        count_label = tk.Label(self.counter_frame, textvariable=self.file_count, bg=self.theme.current['bg'], fg=self.theme.current['fg'], font=('Segoe UI', 11))
        progress_label.pack(side=tk.LEFT)
        slash_label.pack(side=tk.LEFT)
        count_label.pack(side=tk.LEFT)
        self.progress_bar.pack()
        self.stop_button.config(state=tk.DISABLED)
        self.start_button.pack(side=tk.LEFT, padx=15)
        self.stop_button.pack(side=tk.LEFT)
        self.button_frame.pack(pady=10)

    def fill_que(self):
        """
        Fill the worker que from the files in file selector,
        and prepare te progress bar
        """
        files = self.file_selector.get_file_paths()
        self.file_count.set(len(files))
        self.progress_bar.configure(maximum=len(files))
        self.time_tracker.set_max(len(files))
        for file in files:
            self.image_que.put(file)

    def is_existing_files(self):
        """
        Check if there's existing files which will be overwritten by the
        watermarker
        :return: True/False
        """
        out = self.option_pane.get_output_path()
        for _file in self.file_selector.get_file_paths():
            if os.path.isfile(self.option_pane.create_output_path(_file, out)):
                return True
        return False

    def apply_watermarks(self):
        """
        Fill the que, then prepare the watermarker
        before spawning workers
        """
        if len(self.file_selector.files) < 1:
            messagebox.showerror('Nothing to mark',
                                 'Please choose one or more files '
                                 'to mark.')
            return

        if self.is_existing_files():
            kwargs = {"title": "Overwrite files?",
                      "message": "Files already exists, want to overwrite?"}
            overwrite = messagebox.askyesno(**kwargs)
        else:
            # Shouldn't matter since there's no files.
            overwrite = False

        try:
            self.watermarker = WaterMarker(self.option_pane.get_watermark_path(),
                                           overwrite=overwrite)
        except Exception as e:
            self.handle_error(e)
            return

        self.stop_button.config(state=tk.NORMAL)
        self.start_button.config(state=tk.DISABLED)
        self.fill_que()
        self.start_work()

    def start_work(self):
        """
        The baby factory, spawns worker thread to apply the watermark to
        the images.
        Also locks the buttons and output selector
        """
        try:
            kwargs = {"pos": self.option_pane.get_watermark_pos(),
                      "padding": self.option_pane.get_padding(),
                      "scale": self.option_pane.should_scale(),
                      "opacity": self.option_pane.get_opacity()}
            output = self.option_pane.get_output_path()
            print(output)
        except BadOptionError as e:
            self.handle_error(e)
            return
        self.running = True
        self.option_pane.output_selector.lock()
        thread = threading.Thread(target=self.work,
                                  kwargs=kwargs, args=(output, ))
        self.time_tracker.start()
        thread.start()

    def reset(self):
        """
        Reset the worker, emptying queue, resetting vars and buttons and stuff.
        """
        self.image_que = queue.Queue()
        self.watermarker = WaterMarker
        self.progress_var.set(0)
        self.progress_bar.stop()
        self.time_tracker.stop()
        self.file_count.set(0)
        self.start_button.config(state=NORMAL)
        self.stop_button.config(state=DISABLED)
        self.option_pane.output_selector.unlock()

    def handle_error(self, e):
        """
        Handle an error, showing the callback to the user.
        Is meant to be primarily used with BadOption error with a custom text.
        :param e: Error object.
        """
        self.reset()
        messagebox.showerror("Error", str(e))

    def work(self, outpath, **kwargs):
        """
        Work instructions for the child workers
        keep grabbing a new image path and then apply free_mark with
        the watermarker, using option pane to create paths.
        Controls progress bar and timer_tracker as well
        """
        while self.running:
            try:
                input_path = self.image_que.get(block=False)
            except queue.Empty:
                self.start_button.config(state=NORMAL)
                self.stop_button.config(state=DISABLED)
                self.option_pane.output_selector.unlock()
                self.progress_var.set(0)
                self.file_count.set(0)
                self.running = False
                return
            try:
                self.watermarker.apply_watermark(input_path,
                                                 self.option_pane.create_output_path(input_path, outpath),
                                                 **kwargs)
            except BadOptionError as e:
                self.handle_error(e)
                print("Bad config, stopping\n", e)
                return
            except Exception as e:
                print("Error!\n", type(e), "\n", e)
            self.progress_bar.step(amount=1)
            self.time_tracker.step()
            self.progress_var.set(self.progress_var.get()+1)

        self.reset()

    def stop_work(self):
        self.running = False
