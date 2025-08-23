# theme_manager.py
# Handles light/dark mode and color schemes for FreeMark UI

import tkinter as tk

class ThemeManager:
    LIGHT = {
        'bg': '#f5f6fa',
        'fg': '#222f3e',
        'accent': '#00a8ff',
        'button_bg': '#dff9fb',
        'button_fg': '#192a56',
        'entry_bg': '#ffffff',
        'entry_fg': '#222f3e',
    }
    DARK = {
        'bg': '#222f3e',
        'fg': '#f5f6fa',
        'accent': '#9c88ff',
        'button_bg': '#353b48',
        'button_fg': '#f5f6fa',
        'entry_bg': '#353b48',
        'entry_fg': '#f5f6fa',
    }

    def __init__(self):
        self.current = self.DARK

    def toggle(self):
        self.current = self.LIGHT if self.current == self.DARK else self.DARK

    def apply(self, widget, element='bg'):
        color = self.current.get(element, self.current['bg'])
        widget.configure(bg=color)

    def style_button(self, button):
        button.configure(bg=self.current['button_bg'], fg=self.current['button_fg'], relief=tk.FLAT, font=('Segoe UI', 11, 'bold'), bd=0, highlightthickness=0)

    def style_entry(self, entry):
        entry.configure(bg=self.current['entry_bg'], fg=self.current['entry_fg'], insertbackground=self.current['entry_fg'], font=('Segoe UI', 11))

    def style_label(self, label):
        label.configure(bg=self.current['bg'], fg=self.current['fg'], font=('Segoe UI', 12))

    def style_frame(self, frame):
        frame.configure(bg=self.current['bg'])

    def accent_color(self):
        return self.current['accent']
