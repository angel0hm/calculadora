import ttkbootstrap as ttk
import customtkinter as ctk
from ui import crear_ui
import tkinter as tk
from tkinter import font as tkfont
import os
import json

def main():
    ctk.set_appearance_mode("dark") 
    ctk.set_default_color_theme("dark-blue")  # Referencia, modificamos con tema.json

    root = ctk.CTk()    
    root.configure(fg_color="#f9f9f9")
    root.title("Calculadora")
    root.geometry("350x500")
    root.wm_attributes("-alpha", 0.99)

    crear_ui(root)
    root.mainloop()

if __name__ == "__main__":
    main()
