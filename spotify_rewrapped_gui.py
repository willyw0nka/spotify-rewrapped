"""This module contains the code corresponding to the basic GUI implemented for
Windows users."""
import tkinter as tk
from tkinter import Tk, W, E, N, filedialog, messagebox
from tkinter.ttk import Frame, Button, Entry, Label

import glob

from spotify_rewrapped import SpotifyRewrapped

class SpotifyRewrappedGUI(Frame):
    """SpotifyRewrappedGUI contains the code needed to render the GUI."""
    def __init__(self, root):
        super().__init__()
        self.root = root
        self.input_path = ''
        self.output_file = ''

        self.init_ui()

    def launch(self):       
        """Runs an instance of SpotifyRewrapped to generate the desired png.
        """
        SpotifyRewrapped(path=self.input_path, output=self.output_file)
        messagebox.showinfo(title='Spotify rewrapped',
                            message='Success!\n'
                            'You can check your results at {}'.format(self.output_file))

    def set_input_path(self):
        """Displays an askdirectory dialog and saves the result to allow
        calling SpotifyRewrapped.
        """
        self.input_path = filedialog.askdirectory()
        print(self.input_path)
        self.entry_input_path.configure(state='enabled')
        self.entry_input_path.delete(0, tk.END)
        self.entry_input_path.insert(0, self.input_path)
        self.entry_input_path.configure(state='disabled')

        self.listbox.configure(state='normal')
        for file in glob.glob(f'{self.input_path}/StreamingHistory[0-9].json'):
            print(file)
            self.listbox.insert(tk.END, file)
        self.listbox.configure(state='disabled')

    def set_output_path(self):
        """Displays an askdirectory dialog and saves the result to allow
        calling SpotifyRewrapped.
        """
        self.output_file = filedialog.askdirectory()
        self.output_file += '/spotify-rewrapped.png'
        print(self.output_file)
        self.entry_output_file.configure(state='enabled')
        self.entry_output_file.delete(0, tk.END)
        self.entry_output_file.insert(0, self.output_file)
        self.entry_output_file.configure(state='disabled')

    def init_ui(self):
        """Displays all the elements that are contained in the GUI.
        """

        self.master.title('Spotify rewrapped')

        self.columnconfigure(0, pad=3, weight=1)
        self.columnconfigure(1, pad=3, weight=1)
        self.columnconfigure(2, pad=3, weight=4)
        self.columnconfigure(3, pad=3, weight=1)

        self.rowconfigure(0, pad=3)
        self.rowconfigure(1, pad=3)
        self.rowconfigure(2, pad=3)
        self.rowconfigure(3, pad=3)
        self.rowconfigure(4, pad=3)
        self.rowconfigure(5, pad=3)

        current_row = 0
        Label(self, text='Spotify rewrapped').grid(row=current_row,
                                                   columnspan=4,
                                                   sticky=N)

        current_row = 1
        Label(self, text='Input path:').grid(row=current_row, column=0)
        self.entry_input_path = Entry(self, state='disabled')
        self.entry_input_path.grid(row=current_row, column=1, sticky=E+W)
        Button(self, text='...', command=self.set_input_path).grid(row=current_row,
                                                                   column=3)

        current_row = 2
        Label(self, text='Matched files').grid(row=current_row, column=0)

        current_row = 3
        self.listbox = tk.Listbox(self, state='disabled')
        self.listbox.grid(row=current_row, column=0, columnspan=4, sticky=E+W)

        current_row = 4
        Label(self, text='Output file:').grid(row=current_row, column=0)
        self.entry_output_file = Entry(self, state='disabled')
        self.entry_output_file.grid(row=current_row, column=1, sticky=E+W)
        Button(self, text='...', command=self.set_output_path).grid(row=current_row,
                                                                    column=3)

        current_row = 5
        Button(self, text='Generate', command=self.launch).grid(row=current_row,
                                                                column=0,
                                                                columnspan=2,
                                                                sticky=E+W)
        Button(self, text='Quit', command=self.root.destroy).grid(row=current_row,
                                                                  column=2,
                                                                  columnspan=2,
                                                                  sticky=E+W)

        self.pack()


def main():
    """Entrypoint.
    """
    root = Tk()
    SpotifyRewrappedGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
