

import tkinter as tk
from tkinter import Text, filedialog, messagebox, simpledialog, font
import re

class TextEditor:
    """
    A class that represents the text editor application.

    Attributes:
        root (tk.Tk): The root window of the Tkinter application.
        text_area (Text): The text area widget for editing text.
        line_numbers (tk.Text): The line numbers widget.
        status_bar (tk.Label): The status bar widget.

    Methods:
        update_status_bar(event=None): Updates the status bar with the current line and column number.
        create_menu(): Creates the menu bar with File, Edit, Format, and View menus.
        cut_text(): Cuts the selected text.
        copy_text(): Copies the selected text.
        paste_text(): Pastes the text from the clipboard.
        new_file(): Clears the text area for a new file.
        open_file(): Opens a file and displays its content in the text area.
        save_file(): Saves the content of the text area to a file.
        exit_editor(): Exits the text editor.
        find_text(): Finds and highlights the specified text.
        replace_text(): Replaces the specified text with the replacement text.
        undo_text(): Undoes the last action.
        redo_text(): Redoes the last undone action.
        choose_font(): Changes the font of the text area.
        toggle_dark_mode(): Toggles between dark mode and light mode.
        on_key_release(event=None): Updates line numbers, highlights syntax, and updates status bar on key release.
        update_line_numbers(event=None): Updates the line numbers in the line numbers widget.
        highlight_syntax(): Highlights syntax for keywords.
    """
    def __init__(self, root):
        """
        Initializes the TextEditor class.

        Args:
            root (tk.Tk): The root window of the Tkinter application.
        """
        self.root = root
        self.root.title("Text Editor")
        self.root.geometry("800x600")
        
        self.root.title("Text Editor")
        self.root.geometry("800x600")

        self.text_area = Text(self.root, wrap='word', font=("Calibri", 12), undo=True)
        self.text_area.pack(fill='both', expand=1)

        self.line_numbers = tk.Text(self.root, width=4, padx=3, takefocus=0, border=0,
                                    background='lightgrey', state='disabled', wrap='none')
        self.line_numbers.pack(side='left', fill='y')
        self.text_area.pack(side='right', fill='both', expand=True)

        self.status_bar = tk.Label(self.root, text="Line 1, Column 1", anchor='w')
        self.status_bar.pack(side='bottom', fill='x')

        self.text_area.bind('<KeyRelease>', self.on_key_release)
        self.text_area.bind('<Button-1>', self.update_status_bar)
        self.text_area.bind('<Motion>', self.update_status_bar)

        self.create_menu()
        self.update_status_bar()

    def update_status_bar(self, event=None):
        """
        Updates the status bar with the current line and column number.

        Args:
            event (tk.Event, optional): The event that triggered the update. Defaults to None.
        """
        row, col = self.text_area.index(tk.INSERT).split('.')
        self.status_bar.config(text=f"Line {row}, Column {col}")

    def create_menu(self):
        """
        Creates the menu bar with File, Edit, Format, and View menus.
        """
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.exit_editor)

        edit_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Edit", menu=edit_menu)
        
        edit_menu.add_command(label="Cut", command=self.cut_text)
        edit_menu.add_command(label="Copy", command=self.copy_text)
        edit_menu.add_command(label="Paste", command=self.paste_text)
        edit_menu.add_separator()
        edit_menu.add_command(label="Find", command=self.find_text)
        edit_menu.add_command(label="Replace", command=self.replace_text)
        edit_menu.add_separator()
        edit_menu.add_command(label="Undo", command=self.undo_text)
        edit_menu.add_command(label="Redo", command=self.redo_text)

        format_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Format", menu=format_menu)
        
        format_menu.add_command(label="Font", command=self.choose_font)
        
        view_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="View", menu=view_menu)
        
        view_menu.add_command(label="Toggle Dark Mode", command=self.toggle_dark_mode)

    def cut_text(self):
        """
        Cuts the selected text.
        """
        self.text_area.event_generate("<<Cut>>")

    def copy_text(self):
        """
        Copies the selected text.
        """
        self.text_area.event_generate("<<Copy>>")

    def paste_text(self):
        """
        Pastes the text from the clipboard.
        """
        self.text_area.event_generate("<<Paste>>")

    def new_file(self):
        """
        Clears the text area for a new file.
        """
        self.text_area.delete(1.0, tk.END)
        self.update_status_bar()

    def open_file(self):
        """
        Opens a file and displays its content in the text area.
        """
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, content)
            self.update_status_bar()

    def save_file(self):
        """
        Saves the content of the text area to a file.
        """
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text files", "*.txt"),
                                                            ("All files", "*.*")])
        if file_path:
            with open(file_path, 'w') as file:
                content = self.text_area.get(1.0, tk.END)
                file.write(content)

    def exit_editor(self):
        """
        Exits the text editor.
        """
        if messagebox.askokcancel("Quit", "Do you really want to quit?"):
            self.root.destroy()

    def find_text(self):
        """
        Finds and highlights the specified text.
        """
        find_string = simpledialog.askstring("Find", "Enter text to find:")
        self.text_area.tag_remove('found', '1.0', tk.END)
        if find_string:
            idx = '1.0'
            while 1:
                idx = self.text_area.search(find_string, idx, nocase=1, stopindex=tk.END)
                if not idx: break
                lastidx = f"{idx}+{len(find_string)}c"
                self.text_area.tag_add('found', idx, lastidx)
                idx = lastidx
            self.text_area.tag_config('found', foreground='red', background='yellow')

    def replace_text(self):
        """
        Replaces the specified text with the replacement text.
        """
        find_string = simpledialog.askstring("Find", "Enter text to replace:")
        replace_string = simpledialog.askstring("Replace", "Enter replacement text:")
        content = self.text_area.get(1.0, tk.END)
        new_content = content.replace(find_string, replace_string)
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(1.0, new_content)

    def undo_text(self):
        """
        Undoes the last action.
        """
        try:
            self.text_area.edit_undo()
        except:
            pass

    def redo_text(self):
        """
        Redoes the last undone action.
        """
        try:
            self.text_area.edit_redo()
        except:
            pass

    def choose_font(self):
        """
        Changes the font of the text area.
        """
        font_family = simpledialog.askstring("Font", "Enter font family (e.g., Arial):")
        font_size = simpledialog.askinteger("Font", "Enter font size:")
        if font_family and font_size:
            new_font = font.Font(family=font_family, size=font_size)
            self.text_area.config(font=new_font)

    def toggle_dark_mode(self):
        """
        Toggles between dark mode and light mode.
        """
        current_bg = self.text_area.cget('background')
        if current_bg == 'white':
            self.text_area.config(background='black', foreground='white', insertbackground='white')
            self.line_numbers.config(background='black', foreground='white')
        else:
            self.text_area.config(background='white', foreground='black', insertbackground='black')
            self.line_numbers.config(background='lightgrey', foreground='black')

    def on_key_release(self, event=None):
        """
        Updates line numbers, highlights syntax, and updates status bar on key release.

        Args:
            event (tk.Event, optional): The event that triggered the update. Defaults to None.
        """
        self.update_line_numbers()
        self.highlight_syntax()
        self.update_status_bar()

    def update_line_numbers(self, event=None):
        """
        Updates the line numbers in the line numbers widget.

        Args:
            event (tk.Event, optional): The event that triggered the update. Defaults to None.
        """
        self.line_numbers.config(state='normal')
        self.line_numbers.delete(1.0, tk.END)
        row, col = self.text_area.index(tk.END).split('.')
        line_numbers = "\n".join(str(i) for i in range(1, int(row)))
        self.line_numbers.insert(1.0, line_numbers)
        self.line_numbers.config(state='disabled')

    def highlight_syntax(self):
        """
        Highlights syntax for keywords.
        """
        keywords = ['def', 'class', 'if', 'else', 'elif', 'while', 'for', 'import', 'from', 'return']
        text_content = self.text_area.get(1.0, tk.END)
        for keyword in keywords:
            start_index = '1.0'
            while True:
                start_index = self.text_area.search(r'\b' + keyword + r'\b', start_index, stopindex=tk.END)
                if not start_index:
                    break
                end_index = f"{start_index}+{len(keyword)}c"
                self.text_area.tag_add(keyword, start_index, end_index)
                self.text_area.tag_config(keyword, foreground='blue')
                start_index = end_index

if __name__ == "__main__":
    root = tk.Tk()
    editor = TextEditor(root)
    root.mainloop()
