import os
import pygubu
import tkinter as tk
import tkinter.ttk as ttk


PROJECT_PATH = os.path.dirname(__file__)
PROJECT_UI = os.path.join(PROJECT_PATH, "simpleGUI.ui")


class SimpleguiApp:
    def __init__(self, parent):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        self.mainwindow = builder.get_object('background', parent)
        builder.connect_callbacks(self)

    def run(self):
        self.mainwindow.mainloop()


if __name__ == '__main__':
    root = tk.Tk()
    root.title('Tytul')
    app = SimpleguiApp(root)
    app.run()
