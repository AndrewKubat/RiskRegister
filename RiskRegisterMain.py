
import RiskRegisterCSV
import RiskRegisterSQL  # Assuming you have similar functions for SQL
from tkinter import Tk, IntVar, filedialog
import customtkinter as ct
from customtkinter import *
import os
import configparser
import base64
import sqlite3

global sql_boolean
global label_file
global csv_boolean
global file_name

sql_boolean = True
csv_boolean = False
csv_file_path = ""  # Path to the selected CSV file

##Author: Andrew Kubat, Alexander Roberts
##Purpose: Main portion of the Risk Register Automated Management System (RRAMS). This file will run all necessary code


##This module runs and determines what other modules will be run.


##This module is used to generate the initial GUI

##This module is used to determine GUI navigation

# Function to swap between SQL and CSV mode
def mode_Swap():
    RR_mode = mode_toggle.get()
    global sql_boolean, csv_boolean
    if RR_mode:
        sql_boolean = False
        csv_boolean = True
        print("I'm in CSV mode")
    else:
        sql_boolean = True
        csv_boolean = False
        print("I'm in SQL mode")
    save_config()

# Function to change between light and dark mode
def mode_style_change():
    cur_mode = style_toggle_slider.get()
    if cur_mode:
        ct.set_appearance_mode("Dark")
    else:
        ct.set_appearance_mode("Light")
    save_config()

# Function to save configuration settings
def save_config():
    config = configparser.RawConfigParser()
    config.read("config.ini")
    config.set('General', 'style_toggle_slider', str(style_toggle_slider.get()))
    config.set('General', 'mode_toggle_val', str(mode_toggle.get()))
    config.set('General', 'csv_file_path', csv_file_path)
    with open("config.ini", "w") as configFile:
        config.write(configFile)

# Function to load configuration settings
def load_config():
    config = configparser.ConfigParser()
    config.read("config.ini")
    if 'General' in config:
        style_toggle_slider.set(int(config['General']['style_toggle_slider']))
        mode_style_change()
        mode_toggle.set(int(config['General']['mode_toggle_val']))
        mode_Swap()
        global csv_file_path
        csv_file_path = config['General'].get('csv_file_path', '')

# Function to create initial configuration file
def create_config(style):
    if not os.path.exists('config.ini'):
        config = configparser.ConfigParser()
        testpass = "password123"
        encoded_pass = base64.b64encode(testpass.encode("utf-8")).decode("utf-8")  # Encode and decode the password
        config['Database'] = {'db_name': 'tempName', 'db_host': 'tempName', 'db_pass': encoded_pass, 'db_port': '5432'}
        config['General'] = {'style_toggle_slider': str(style), 'mode_toggle_val': '1', 'csv_file_path': ''}
        with open("config.ini", "w") as configFile:
            config.write(configFile)

# Function to debug password decoding
def debug_pass():
    config = configparser.ConfigParser()
    config.read("config.ini")
    encoded_pass = config.get('Database', 'db_pass')
    decoded_pass = base64.b64decode(encoded_pass).decode("utf-8")
    print("Decoded Password:", decoded_pass)

# Function to handle file selection
def select_file():
    global csv_file_path
    fileDir = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if fileDir:
        csv_file_path = fileDir
        filename = os.path.basename(fileDir)
        label_file.configure(text="Selected File: " + filename)
        save_config()
        print("CSV file selected:", csv_file_path)

# Main function to initialize the GUI
def main():
    def on_close():
        uiRoot.quit()  # Quit the main loop when the main dashboard is closed

    system_default = ct.get_appearance_mode()  # Check current appearance mode

    uiRoot = CTk()
    uiRoot.geometry("600x400")
    uiRoot.title("Risk Register")

    global mode_toggle, style_toggle_slider
    mode_toggle = IntVar(uiRoot)
    style_toggle_slider = IntVar(uiRoot)

    if os.path.exists('config.ini'):
        load_config()
    else:
        style_toggle_slider.set(1 if system_default == "Dark" else 0)  # Set the initial value based on current appearance mode
        mode_toggle.set(1)
        create_config(style_toggle_slider.get())

    sql_CSV_toggle = CTkSwitch(uiRoot, text="SQL/CSV", variable=mode_toggle, onvalue=1, offvalue=0, command=mode_Swap)
    sql_CSV_toggle.pack(pady=0, padx=20, anchor="nw", side="left")  # Positioned on the left side

    style_toggle = CTkSwitch(uiRoot, text="Light/Dark Mode toggle", variable=style_toggle_slider, onvalue=1, offvalue=0, command=lambda: mode_style_change())
    style_toggle.pack(pady=0, padx=10, anchor="ne", side="right")  # Positioned on the right side

    label_file = CTkLabel(uiRoot, text="No CSV file Selected")
    label_file.pack(pady=0, padx=1)  # Positioned on the right side
    uiRoot.protocol("WM_DELETE_WINDOW", on_close)
    file_name = "Click me to choose your file"

    button = CTkButton(uiRoot, text=file_name, command=select_file)
    button.pack(pady=90)

    uiRoot.mainloop()
    button.pack(pady=10)
    debug_pass()

if __name__ == "__main__":
    main()