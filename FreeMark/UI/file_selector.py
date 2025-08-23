import tkinter as tk
from tkinter import filedialog, messagebox
import os
from FreeMark.UI.theme_manager import ThemeManager

class FileSelector(tk.Frame):
    """
    GUI element for selecting images to apply free_mark to
    """
    def __init__(self, master=None, theme=None):
        super().__init__(master)
        self.master = master
        self.theme = theme or ThemeManager()
        self.base_dir = tk.StringVar()
        self.files = []
        self.button_frame = tk.Frame(self)
        self.folder_frame = tk.Frame(self)
        self.files_view = tk.Listbox(self, width=65, height=20, bg=self.theme.current['entry_bg'], fg=self.theme.current['entry_fg'], font=('Segoe UI', 11), highlightthickness=0, bd=0, selectbackground=self.theme.current['accent'])
        self.folder_entry = tk.Entry(self.folder_frame, width=58, textvariable=self.base_dir)
        self.theme.style_entry(self.folder_entry)
        self.theme.style_frame(self)
        self.theme.style_frame(self.button_frame)
        self.theme.style_frame(self.folder_frame)
        self.create_widgets()

    def create_widgets(self):
        pad_y = 8
        pad_x = 12
        self.label = tk.Label(self, text="Images")
        self.theme.style_label(self.label)
        self.label.pack(pady=(pad_y, 0))
        self.files_view.pack(pady=pad_y, padx=pad_x, fill='both', expand=True)
        folder_label = tk.Label(self.folder_frame, text="Folder:")
        self.theme.style_label(folder_label)
        folder_label.pack(side=tk.LEFT)
        self.folder_entry.pack(side=tk.RIGHT, pady=pad_y)
        self.folder_frame.pack(fill='x', padx=pad_x)
        choose_folder_btn = tk.Button(self.button_frame, text="Choose folder", command=self.fill_list)
        self.theme.style_button(choose_folder_btn)
        choose_folder_btn.pack(side=tk.LEFT, padx=pad_x)
        choose_files_btn = tk.Button(self.button_frame, text="Choose file(s)", command=self.select_files)
        self.theme.style_button(choose_files_btn)
        choose_files_btn.pack(side=tk.LEFT)
        clear_files_btn = tk.Button(self.button_frame, text="Clear files", command=self.clear_files)
        self.theme.style_button(clear_files_btn)
        clear_files_btn.pack(side=tk.RIGHT)
        remove_file_btn = tk.Button(self.button_frame, text="Remove file", command=self.remove_item)
        self.theme.style_button(remove_file_btn)
        remove_file_btn.pack(side=tk.RIGHT, padx=pad_x)
        self.button_frame.pack(pady=pad_y, fill='x')

    def remove_item(self):
        self.files_view.delete(tk.ANCHOR)
        self.files = self.files_view.get(0, tk.END)

    def prompt_directory(self):
        self.base_dir.set(filedialog.askdirectory())

    def select_files(self):
        file_types = [('Images', '*.jpg;*.jpeg;*.png;*.bmp;*.tiff')]
        files = filedialog.askopenfilenames(title="Select images", filetypes=file_types)
        for _file in files:
            if _file not in self.files:
                self.files.append(_file)
        self.refresh_list()

    def refresh_list(self):
        self.files_view.delete(0, tk.END)
        for _file in self.files:
            self.files_view.insert(tk.END, _file)

    def clear_files(self):
        self.files = []
        self.refresh_list()
        self.base_dir.set('')

    def refresh_files(self):
        self.files = []
        types = ['.png', '.jpg', '.jpeg', '.bmp', '.tiff']
        try:
            for _file in os.listdir(self.base_dir.get()):
                if os.path.isfile(os.path.join(self.base_dir.get(), _file)):
                    for _type in types:
                        if _file.endswith(_type) and _file not in self.files:
                            self.files.append(_file)
                            break
        except FileNotFoundError:
            messagebox.showerror("Error", "Directory not found")
            return
        self.refresh_list()

    def fill_list(self):
        self.prompt_directory()
        self.refresh_files()

    def get_files(self):
        return self.files

    def get_file_paths(self):
        return [os.path.join(self.base_dir.get(), file) for file in self.get_files()]
