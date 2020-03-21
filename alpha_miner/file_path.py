import tkinter as tk
from tkinter import filedialog

def get_file_path():
  root = tk.Tk()
  root.withdraw()

  file_path = filedialog.askopenfilename()

  
  return file_path
