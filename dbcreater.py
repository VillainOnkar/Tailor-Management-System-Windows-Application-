import mysql.connector
from mysql.connector import Error
import json
import os
from tkinter import ttk, messagebox
import tkinter as tk
from tkinter import messagebox
from pricemanager import get_sarth_base_folder

import sys, shutil

"""def get_drive_auth_folder():
    folder = os.path.join(os.getcwd(), "DriveAuth")

    if not os.path.exists(folder):
        os.makedirs(folder)

    return folder"""
"""ef get_drive_auth_folder():
    folder = os.path.join(
        os.getenv("LOCALAPPDATA"),
        "SarthTailorShop",
        "DriveAuth"
    )

    os.makedirs(folder, exist_ok=True)

    # ensure writable (extra safety)
    try:
        if not os.access(folder, os.W_OK):
            os.chmod(folder, 0o777)
    except:
        pass

    return folder"""



"""def extract_json_files():
     
    exe चलने पर → JSON फाइलें DriveAuth में कॉपी कर देता है
  
    target = get_drive_auth_folder()

    # .exe और .py दोनों के लिए base path detect
    base = sys._MEIPASS if hasattr(sys, "_MEIPASS") else os.getcwd()

    files = ["config.json"]   # चाहो तो future में और json add कर सकते हो

    for f in files:
        src = os.path.join(base, f)
        dst = os.path.join(target, f)

        if os.path.exists(src) and not os.path.exists(dst):
            shutil.copy(src, dst)

    return os.path.join(target, "config.json")"""

from tkinter import filedialog, messagebox
APP_FOLDER_NAME = "SarthTailorShop"

BASE_PATH_FILE = os.path.join(
    os.getenv("LOCALAPPDATA"),
    APP_FOLDER_NAME,
    "base_path.json"
)

"""def get_sarth_base_folder():
    # Agar pehle se user ne path select kiya hai
    if os.path.exists(BASE_PATH_FILE):
        with open(BASE_PATH_FILE, "r") as f:
            return json.load(f)["base_path"]

    # FIRST TIME RUN → user se folder select karvao
    temp_root = Tk()
    temp_root.withdraw()

    messagebox.showinfo(
        "Select Folder",
        "Please select a folder where Sarth Tailor Shop data will be stored"
    )

    base_path = filedialog.askdirectory(title="Select Folder for SarthTailorShop")
    temp_root.destroy()

    if not base_path:
        sys.exit("Folder not selected")

    # Save selected path
    os.makedirs(os.path.dirname(BASE_PATH_FILE), exist_ok=True)
    with open(BASE_PATH_FILE, "w") as f:
        json.dump({"base_path": base_path}, f, indent=4)

    return base_path"""

def extract_google_files():
    import sys, shutil

    base_path = get_sarth_base_folder()
    extract_folder = os.path.join(
        base_path,
        APP_FOLDER_NAME,
        "DriveAuth"
    )

    os.makedirs(extract_folder, exist_ok=True)

    if hasattr(sys, "_MEIPASS"):
        src_base = sys._MEIPASS
    else:
        src_base = os.getcwd()

    files = ["client_secrets.json", "my_drive_token.json", "config.json"]

    for file in files:
        src = os.path.join(src_base, file)
        dst = os.path.join(extract_folder, file)

        if os.path.exists(src) and not os.path.exists(dst):
            shutil.copy(src, dst)

    return extract_folder




DATABASE_NAME = "villaindb"
CONFIG_FILE = "config.json"



# -------------------------------------------------------------------
# LOAD CONFIG
# -------------------------------------------------------------------
"""def load_config():
    config_path = extract_json_files()   # <-- AUTO EXTRACT + CORRECT PATH

    # अगर config.json exist नहीं करता → नया बनाओ
    if not os.path.exists(config_path):
        default_config = {
            "host": "localhost",
            "user": "root",
            "password": "",
            "database": DATABASE_NAME
        }
        with open(config_path, "w") as f:
            json.dump(default_config, f, indent=4)

    # config return करो
    with open(config_path, "r") as f:
        return json.load(f)"""

def load_config():
    auth_folder = extract_google_files()
    config_path = os.path.join(auth_folder, "config.json")

    if not os.path.exists(config_path):
        default_config = {
            "host": "localhost",
            "user": "root",
            "password": "",
            "database": DATABASE_NAME
        }
        with open(config_path, "w") as f:
            json.dump(default_config, f, indent=4)

    with open(config_path, "r") as f:
        return json.load(f)





# -------------------------------------------------------------------
# SAVE CONFIG
# -------------------------------------------------------------------
def save_config(config):
    auth_folder = extract_google_files()
    config_path = os.path.join(auth_folder, "config.json")

    with open(config_path, "w") as f:
        json.dump(config, f, indent=4)



# -------------------------------------------------------------------
# TEST CONNECTION USING PASSWORD
# -------------------------------------------------------------------
def test_connection(password):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password=password
        )
        conn.close()
        return True
    except:
        return False


# -------------------------------------------------------------------
# ONE TIME PASSWORD GUI
# -------------------------------------------------------------------
def ask_password_window():
    win = tk.Tk()
    win.title("Database Setup")
    win.geometry("350x160+600+300")
    win.resizable(False, False)
    win.config(bg="#0e0e0e")

    tk.Label(win, text="Enter MySQL Root Password", font=("times new roman", 18, "bold"),
                      fg="gold", bg="#0e0e0e").pack(pady=10),

    pwd_entry = tk.Entry(win, show="*", font=("Arial", 12))
    pwd_entry.pack(pady=5)
   

    def save_and_connect():
        pwd = pwd_entry.get()

        if pwd == "":
            messagebox.showerror("Error", "Password cannot be empty")
            return

        if test_connection(pwd):
            config = load_config()
            config["password"] = pwd
            save_config(config)

            messagebox.showinfo("Success", "Database Connected Successfully!")
            win.destroy()

        else:
            messagebox.showerror("Error", "Wrong Password! Try Again")
    
    tk.Button(win, text="Connect", command=save_and_connect,bg="gold",fg="black",activebackground="gold",activeforeground="black",cursor="hand2").pack(pady=10)

    win.mainloop()


# -------------------------------------------------------------------
# 1) CONNECT WITHOUT DATABASE (CREATE DATABASE)
# -------------------------------------------------------------------
def create_root_connection():
    config = load_config()

    if config["password"] == "":
        ask_password_window()
        config = load_config()

    return mysql.connector.connect(
        host=config["host"],
        user=config["user"],
        password=config["password"]
    )


# -------------------------------------------------------------------
# 2) CONNECT WITH DATABASE
# -------------------------------------------------------------------
def create_db_connection():
    config = load_config()

    return mysql.connector.connect(
        host=config["host"],
        user=config["user"],
        password=config["password"],
        database=DATABASE_NAME
    )


# -------------------------------------------------------------------
# 3) CREATE DATABASE IF NOT EXISTS
# -------------------------------------------------------------------
def create_database():
    try:
        conn = create_root_connection()
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DATABASE_NAME}")
        conn.commit()
        cursor.close()
        conn.close()
    except Error as e:
        print("Database Create Error:", e)


# -------------------------------------------------------------------
# 4) CREATE TABLES
# -------------------------------------------------------------------
def create_tables():
    try:
        conn = create_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS addcustomer (
                Reference_No VARCHAR(50) PRIMARY KEY,
                Name VARCHAR(50),
                Delivery VARCHAR(45),
                Address VARCHAR(45),
                Phone VARCHAR(10),
                Shirt_Quantity VARCHAR(45),
                Pant_Quantity VARCHAR(45),
                Type_Of_Shirt VARCHAR(45),
                Design_Of_Shirt VARCHAR(45),
                Receiving_Date VARCHAR(45),
                Submitted_Date VARCHAR(45),
                Payment VARCHAR(45)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS login (
                username VARCHAR(100) PRIMARY KEY,
                password VARCHAR(45),
                security_question VARCHAR(255),
                security_answer VARCHAR(255)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS measurement (
                Name VARCHAR(50),
                Shirt_Cutting VARCHAR(45),
                Pant_Cutting VARCHAR(45),
                Sh_Length VARCHAR(45),
                Sh_Chest VARCHAR(45),
                Sh_Stomach VARCHAR(45),
                Sh_Shoulder VARCHAR(45),
                Sh_Sleeves VARCHAR(45),
                Sh_Neck VARCHAR(45),
                Sh_Cup VARCHAR(45),
                Sh_Front VARCHAR(45),
                Length VARCHAR(45),
                Waist VARCHAR(45),
                Seat VARCHAR(45),
                Thigh VARCHAR(45),
                Knee VARCHAR(45),
                Bottom VARCHAR(45)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                product_name VARCHAR(50) PRIMARY KEY,
                price INT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS gatewayurl (
                url VARCHAR(255)
            )
        """)


        conn.commit()
        cursor.close()
        conn.close()

    except Error as e:
        print("Table Creation Error:", e)


# -------------------------------------------------------------------
# 5) MAIN FUNCTION
# -------------------------------------------------------------------
def setup_database():
    create_database()
    create_tables()

