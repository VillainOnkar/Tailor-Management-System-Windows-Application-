from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image,ImageTk
import mysql.connector
from time import strftime
from datetime import datetime
from addcustomer import customer
from measurement import measurement_win
from graphicview import graphic_win
from billingsystem import bill_win
from pricemanager import ProductControl
from sms import sms_win
import os
import sys
import json
import datetime
import threading
import subprocess
import shutil
from tkinter import filedialog, messagebox, StringVar

# PyDrive imports (Google Drive)
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

APP_FOLDER_NAME = "SarthTailorShop"

BASE_PATH_FILE = os.path.join(
    os.getenv("LOCALAPPDATA"),
    APP_FOLDER_NAME,
    "base_path.json"
)



# ==========================
# GOOGLE AUTH FILE EXTRACTOR
# ==========================


# ==========================
# GOOGLE AUTH FILE EXTRACTOR
# ==========================


"""def extract_google_files():
    extract_folder = os.path.join(os.getcwd(), "DriveAuth")

    # Folder auto create
    os.makedirs(extract_folder, exist_ok=True)

    # जब .exe चलता है → JSON फाइलें यहीं से मिलती हैं
    if hasattr(sys, "_MEIPASS"):
        base = sys._MEIPASS
    else:
        base = os.getcwd()

    # अब तीनों JSON file extract होंगे
    files = ["client_secrets.json", "my_drive_token.json", "config.json"]

    for file in files:
        src = os.path.join(base, file)
        dst = os.path.join(extract_folder, file)

        # अगर फाइल EXE में है और बाहर नहीं है → बाहर निकालो
        if os.path.exists(src) and not os.path.exists(dst):
            shutil.copy(src, dst)
            print("Extracted →", file)

    return extract_folder"""
def get_sarth_base_folder():
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

    return base_path



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






def get_connection():
    CONFIG_FILE = os.path.join(extract_google_files(), "config.json")
    with open(CONFIG_FILE, "r") as f:
        config = json.load(f)

    return mysql.connector.connect(
        host=config["host"],
        user=config["user"],
        password=config["password"],
        database=config["database"]   # yeh now tailor_db hoga
    )

def resource_path(relative_path):
    import sys, os
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)



 

class Tailorsoftware:
   def __init__(self,root):
        self.root=root
        self.root.geometry("1920x1080+0+0")
        self.root.title("Tailor Management System")
        self.root.state("zoomed")
        self.root.resizable(False,False)

        
#==========================================Photos==============================
        img_main_path=resource_path(r"photos\main.jpg")
        img_main=Image.open(img_main_path)
        img_main=img_main.resize((1550,140),Image.ANTIALIAS)
        self.img_main_demo=ImageTk.PhotoImage(img_main)
        lbl_img_main=Label(self.root,image=self.img_main_demo,bd=4,relief=RIDGE)
        lbl_img_main.place(x=200,y=0,width=1335,height=140)

        img_logo_path=resource_path(r"photos\logo.jpeg")
        img_logo=Image.open(img_logo_path)
        img_logo=img_logo.resize((230,140),Image.ANTIALIAS)
        self.logodemo=ImageTk.PhotoImage(img_logo)
        lbl_img_logo=Label(self.root,image=self.logodemo,bd=4,relief=RIDGE)
        lbl_img_logo.place(x=0,y=0,width=230,height=140)

        lbl_main_title=Label(self.root,text="SARTH TAILOR",font=("times new roman",40,"bold"),bg="black",fg="gold",bd=4,relief=RIDGE)
        lbl_main_title.place(x=0,y=140,width=1550,height=50)

        img_setting_path=resource_path(r"photos\setting.png")
        img_setting=Image.open(img_setting_path)
        img_setting=img_setting.resize((50,40),Image.ANTIALIAS)
        self.settingdemo=ImageTk.PhotoImage(img_setting)
        lbl_img_setting=Button(lbl_main_title,image=self.settingdemo,command=self.settingframe,bd=0,relief=RIDGE,bg="black",activebackground="black",cursor="hand2")
        lbl_img_setting.place(x=1450,y=0,width=50,height=40)

        def time():
            string=strftime("%I:%M:%S %p %d-%m-%Y")
            lbl.config(text=string)
            lbl.after(1000,time)

        lbl=Label(lbl_main_title,font=("times new roman",16,"bold"),bg="black",fg="gold")
        lbl.place(x=10,y=0,width=230,height=40)
        time()    

#=================================farme========================================
        main_frame=Frame(self.root,bd=4,relief=RIDGE)
        main_frame.place(x=0,y=190,width=1550,height=620)

        # menu
        lbl_menu=Label(main_frame,text="MENU",font=("times new roman",20,"bold"),bg="black",fg="gold",bd=4,relief=RIDGE)
        lbl_menu.place(x=0,y=0,width=230,height=44)

#==============================btn frame======================================
        btn_frame=Frame( main_frame,bd=4,relief=RIDGE)
        btn_frame.place(x=230,y=0,width=1300,height=44)

        btn_addcustomer=Button(btn_frame,text="Add Customer",command=self.addcustomer_btn,width=19,font=("times new roman",14,"bold"),bg="black",fg="gold",bd=4,activebackground="black",activeforeground="gold",cursor="hand2")
        btn_addcustomer.grid(row=0,column=0,pady=1)

        btn_measurement=Button(btn_frame,text="Measurement",command=self.measurement_btn,width=19,font=("times new roman",14,"bold"),bg="black",fg="gold",bd=4,activebackground="black",activeforeground="gold",cursor="hand2")
        btn_measurement.grid(row=0,column=1,pady=1)

        btn_graphicalmeasurement=Button(btn_frame,command=self.graphicviewbtn,text="Graphical Measurement",width=19,font=("times new roman",14,"bold"),bg="black",fg="gold",bd=4,activebackground="black",activeforeground="gold",cursor="hand2")
        btn_graphicalmeasurement.grid(row=0,column=2,pady=1)

        btn_Bill=Button(btn_frame,text="Bill",command=self.billbtn2,width=19,font=("times new roman",14,"bold"),bg="black",fg="gold",bd=4,activebackground="black",activeforeground="gold",cursor="hand2")
        btn_Bill.grid(row=0,column=3,pady=1)

        btn_pricemanager=Button(btn_frame,text="Price Manager",command=self.pricemanagerbtn,width=19,font=("times new roman",14,"bold"),bg="black",fg="gold",bd=4,activebackground="black",activeforeground="gold",cursor="hand2")
        btn_pricemanager.grid(row=0,column=4,pady=1)

        btn_message=Button(btn_frame,text="Message",command=self.smsbtn,width=15,font=("times new roman",14,"bold"),bg="black",fg="gold",bd=4,activebackground="black",activeforeground="gold",cursor="hand2")
        btn_message.grid(row=0,column=5,pady=1)
 
        btn_logout=Button(self.root,text="Logout",command=self.logout_btn,width=10,font=("times new roman",10,"bold"),bg="red",fg="black",activebackground="red",activeforeground="black",cursor="hand2")
        btn_logout.place(x=735,y=810)

#================================================ shop photo ==========================
        img_shop_path=resource_path(r"photos\shop.jpg")
        img_shop=Image.open(img_shop_path)
        img_shop=img_shop.resize((1301,568),Image.ANTIALIAS)
        self.shopdemo=ImageTk.PhotoImage(img_shop)
        lbl_img_shop=Label(self.root,image=self.shopdemo,bd=4,relief=RIDGE,bg="black")
        lbl_img_shop.place(x=233,y=239,width=1301,height=568)

        sideframe=Frame(main_frame,bd=4,bg="black",relief=RIDGE)
        sideframe.place(x=0,y=45,width=230,height=568)

         
        img_tool_path=resource_path(r"photos\tool2.png")
        img_tool=Image.open(img_tool_path)
        img_tool=img_tool.resize((220,200),Image.ANTIALIAS)
        self.img_tool_demo=ImageTk.PhotoImage(img_tool)
        lbl_img_tool=Label(sideframe,image=self.img_tool_demo,bd=0,bg="black")
        lbl_img_tool.place(x=0,y=0,width=220,height=200)

        img_katri_path=resource_path(r"photos\katri.png")
        img_katri=Image.open(img_katri_path)
        img_katri=img_katri.resize((220,150),Image.ANTIALIAS)
        self.img_katri_demo=ImageTk.PhotoImage(img_katri)
        lbl_img_katri=Label(sideframe,image=self.img_katri_demo,bd=0,bg="black")
        lbl_img_katri.place(x=0,y=410,width=220,height=150)


        img_suit_path=resource_path(r"photos\neadle.png")
        img_suit=Image.open(img_suit_path)
        img_suit=img_suit.resize((220,200),Image.ANTIALIAS)
        self.img_suit_demo=ImageTk.PhotoImage(img_suit)
        lbl_img_suit=Label(sideframe,image=self.img_suit_demo,bd=0,bg="black")
        lbl_img_suit.place(x=0,y=168,width=220,height=250)

        

        # Customer count label
        self.lbl_count = Label(lbl_main_title, font=("times new roman", 16, "bold"), bg="black", fg="gold")
        self.lbl_count.place(x=1200,y=0,width=230,height=40)

        # Call function to update count
        self.update_customer_count()
        #setup_database()
        #self.auto_backup_to_drive()

   def update_customer_count(self):
        conn = get_connection()
        mycursor = conn.cursor()
        mycursor.execute("SELECT COUNT(Reference_No) FROM addcustomer")
        total = mycursor.fetchone()[0]
        conn.close()
        
        self.lbl_count.config(text=f"Total Customers: {total}")
        self.root.after(5000,self.update_customer_count)

   def settingframe(self):
       if hasattr(self, 'settingfrm') and self.setting_frame_open:
            self.settingfrm.destroy()
            self.setting_frame_open = False
       else:
            self.settingfrm=Frame(self.root,bd=4,relief=RIDGE,bg="darkgreen")
            self.settingfrm.place(x=1354,y=200,width=178,height=100)
            self.setting_frame_open = True

            #btn_backupstatus=Button(self.settingfrm,text="Backup Status",command=self.update_backup_status,width=14,font=("times new roman",14,"bold"),bg="black",fg="gold",bd=4,activebackground="black",activeforeground="gold",cursor="hand2")
            #btn_backupstatus.grid(row=0,column=0,pady=1)

            btn_databackup=Button(self.settingfrm,text="Backup Data",command=self.auto_backup_to_drive,width=14,font=("times new roman",14,"bold"),bg="black",fg="gold",bd=4,activebackground="black",activeforeground="gold",cursor="hand2")
            btn_databackup.grid(row=1,column=0,pady=1)
 
            btn_restorebackup=Button(self.settingfrm,text="Restore Data",command=self.restore_backup,width=14,font=("times new roman",14,"bold"),bg="black",fg="gold",bd=4,activebackground="black",activeforeground="gold",cursor="hand2")
            btn_restorebackup.grid(row=2,column=0,pady=1)


    # ----------------------
    # DB credential helper
    # ----------------------
   """def get_db_credentials(self):
    # config.json EXE और .py दोनों में सही path से load होगा
        # ALWAYS load config.json from extracted DriveAuth folder
        auth_folder = extract_google_files()
        config_path = os.path.join(auth_folder, "config.json")

        with open(config_path, "r") as f:
            config = json.load(f)

        # ----------------------------------------
        # AUTO-DETECT MYSQLDUMP & MYSQL
        # ----------------------------------------
        mysqldump_path = shutil.which("mysqldump")
        mysql_path = shutil.which("mysql")

        # Common MySQL Install Paths (Backup search)
        common_paths = [
            r"C:\Program Files\MySQL\MySQL Server 8.0\bin",
            r"C:\Program Files\MySQL\MySQL Server 5.7\bin",
            r"C:\Program Files (x86)\MySQL\MySQL Server 8.0\bin",
            r"C:\Program Files (x86)\MySQL\MySQL Server 5.7\bin",
        ]

        if mysqldump_path is None:
            for p in common_paths:
                test = os.path.join(p, "mysqldump.exe")
                if os.path.exists(test):
                    mysqldump_path = test
                    break

        if mysql_path is None:
            for p in common_paths:
                test = os.path.join(p, "mysql.exe")
                if os.path.exists(test):
                    mysql_path = test
                    break

        # If still not found → show error
        if mysqldump_path is None:
            messagebox.showerror(
                "MySQL Tools Missing",
                "mysqldump.exe not found!\n\n"
                "Please add MySQL/bin folder to PATH."
            )
            return None

        if mysql_path is None:
            messagebox.showerror(
                "MySQL Tools Missing",
                "mysql.exe not found!\n\n"
                "Please add MySQL/bin folder to PATH."
            )
            return None

        # Final return
        return {
            "host": config["host"],
            "user": config["user"],
            "password": config["password"],
            "database": config["database"],

            "mysqldump_path": mysqldump_path,
            "mysql_path": mysql_path
        }"""
   
   def get_db_credentials(self):
    # Load DriveAuth folder from AppData
    auth_folder = extract_google_files()  
    config_path = os.path.join(auth_folder, "config.json")

    # Read config.json safely
    with open(config_path, "r") as f:
        config = json.load(f)

    # ----------------------------------------
    # AUTO-DETECT MYSQLDUMP & MYSQL
    # ----------------------------------------
    mysqldump_path = shutil.which("mysqldump")
    mysql_path = shutil.which("mysql")

    # Common install locations of MySQL
    common_paths = [
        r"C:\Program Files\MySQL\MySQL Server 8.0\bin",
        r"C:\Program Files\MySQL\MySQL Server 5.7\bin",
        r"C:\Program Files (x86)\MySQL\MySQL Server 8.0\bin",
        r"C:\Program Files (x86)\MySQL\MySQL Server 5.7\bin",
    ]

    if mysqldump_path is None:
        for p in common_paths:
            test = os.path.join(p, "mysqldump.exe")
            if os.path.exists(test):
                mysqldump_path = test
                break

    if mysql_path is None:
        for p in common_paths:
            test = os.path.join(p, "mysql.exe")
            if os.path.exists(test):
                mysql_path = test
                break

    # Still not found?
    if mysqldump_path is None:
        messagebox.showerror(
            "MySQL Tools Missing",
            "mysqldump.exe not found!\n\nPlease add MySQL/bin folder to PATH."
        )
        return None

    if mysql_path is None:
        messagebox.showerror(
            "MySQL Tools Missing",
            "mysql.exe not found!\n\nPlease add MySQL/bin folder to PATH."
        )
        return None

    # Final return dictionary
    return {
        "host": config["host"],
        "user": config["user"],
        "password": config["password"],
        "database": config["database"],
        "mysqldump_path": mysqldump_path,
        "mysql_path": mysql_path
    }



# ----------------------
# Create local backup and upload to Google Drive
# ----------------------
   def auto_backup_to_drive(self):
        creds = self.get_db_credentials()
        host = creds["host"]; user = creds["user"]; password = creds["password"]; db = creds["database"]
        mysqldump_bin = creds["mysqldump_path"]

        # ensure backups folder exists
        base_path = get_sarth_base_folder()
        backup_folder = os.path.join(base_path,APP_FOLDER_NAME,"Backups")
        os.makedirs(backup_folder, exist_ok=True)


        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"sarthtailor_backup_{timestamp}.sql"
        backup_path = os.path.join(backup_folder, filename)

        # We explicitly list tables to EXCLUDE gatewayurl
        tables = ["addcustomer", "login", "measurement", "products"]

        cmd = [mysqldump_bin, f"--host={host}", f"--user={user}", f"--password={password}", db] + tables

        try:
            # create local SQL dump
            with open(backup_path, "wb") as out:
                proc = subprocess.run(cmd, stdout=out, stderr=subprocess.PIPE)
            if proc.returncode != 0:
                err = proc.stderr.decode(errors="ignore")
                #self.backup_status.set("Local backup failed")
                messagebox.showerror("Backup Failed", f"mysqldump error:\n{err}", parent=self.root)
                return

            # Upload to Google Drive
            try:
                # TOKEN SETTINGS: टोकन फ़ाइल का पथ सेट करें
                #token_file_path = os.path.join(os.path.dirname(__file__), "my_drive_token.json")
                auth_folder = extract_google_files()
                client_secret = os.path.join(auth_folder, "client_secrets.json")
                token_file_path = os.path.join(auth_folder, "my_drive_token.json")


                
                gauth = GoogleAuth()
                
                # PyDrive को क्लाइंट सीक्रेट्स फ़ाइल और टोकन सेव फ़ाइल दोनों बता रहा है
                gauth.DEFAULT_SETTINGS['client_config_file'] = client_secret
                gauth.DEFAULT_SETTINGS['save_credentials'] = True
                gauth.DEFAULT_SETTINGS['save_credentials_backend'] = 'file'
                gauth.DEFAULT_SETTINGS['save_credentials_file'] = token_file_path # इस नाम से सेव होगा
                
                gauth.LocalWebserverAuth() # पहली बार प्रमाणीकरण यहाँ होगा
                drive = GoogleDrive(gauth)

                gfile = drive.CreateFile({'title': filename})
                gfile.SetContentFile(backup_path)
                gfile.Upload()
                #self.backup_status.set(f"Backup OK: {filename}")
                messagebox.showinfo("Backup", "Backup created & uploaded to Google Drive.", parent=self.root)
            except Exception as e:
                #self.backup_status.set("Upload failed")
                messagebox.showerror("Upload Failed", f"Google Drive upload error:\n{e}", parent=self.root)

        except FileNotFoundError:
            messagebox.showerror("Error", "mysqldump not found. Provide correct path in get_db_credentials().", parent=self.root)
        except Exception as e:
            messagebox.showerror("Unexpected Error", f"{e}", parent=self.root)

# ----------------------
# Restore - choose latest from Drive or local file
# ----------------------
   def restore_backup(self):
        # Warn user
        proceed = messagebox.askyesno("Confirm Restore", "Restoring will overwrite current database. Continue?", parent=self.root)
        if not proceed:
            return

        choice = messagebox.askyesno("Restore Source", "Restore latest backup from Google Drive?\n\nYes = Drive (automatic)\nNo = Choose local .sql file", parent=self.root)
        creds = self.get_db_credentials()
        mysql_bin = creds["mysql_path"]
        host = creds["host"]; user = creds["user"]; password = creds["password"]; db = creds["database"]

        if choice:
            # Restore latest from Drive
            try:
                # TOKEN SETTINGS: टोकन फ़ाइल का पथ सेट करें (वही पथ जो backup में उपयोग हुआ है)
                #token_file_path = os.path.join(os.path.dirname(__file__), "my_drive_token.json")
                auth_folder = extract_google_files()
                client_secret = os.path.join(auth_folder, "client_secrets.json")
                token_file_path = os.path.join(auth_folder, "my_drive_token.json")


                gauth = GoogleAuth()
                
                # PyDrive को क्लाइंट सीक्रेट्स फ़ाइल और टोकन सेव फ़ाइल दोनों बता रहा है
                gauth.DEFAULT_SETTINGS['client_config_file'] =  client_secret
                gauth.DEFAULT_SETTINGS['save_credentials'] = True
                gauth.DEFAULT_SETTINGS['save_credentials_backend'] = 'file'
                gauth.DEFAULT_SETTINGS['save_credentials_file'] = token_file_path
                
                gauth.LocalWebserverAuth()
                drive = GoogleDrive(gauth)

                # list files with our backup prefix
                file_list = drive.ListFile({'q': "title contains 'sarthtailor_backup_' and trashed=false"}).GetList()
                if not file_list:
                    messagebox.showerror("No Backup", "No backup files found on Google Drive.", parent=self.root)
                    return

                # choose latest by createdDate
                latest = max(file_list, key=lambda f: f['createdDate'])
                base_path = get_sarth_base_folder()
                download_folder = os.path.join(base_path,APP_FOLDER_NAME,"Backups")
                os.makedirs(download_folder, exist_ok=True)
                download_path = os.path.join(download_folder, latest['title'])
                latest.GetContentFile(download_path)

                # import into MySQL
                with open(download_path, "rb") as inp:
                    proc = subprocess.run([mysql_bin, f"--host={host}", f"--user={user}", f"--password={password}", db], stdin=inp, stderr=subprocess.PIPE)
                if proc.returncode == 0:
                    messagebox.showinfo("Restore", "Database restored from Drive backup.", parent=self.root)
                    #self.update_backup_status()
                else:
                    err = proc.stderr.decode(errors="ignore")
                    messagebox.showerror("Restore Failed", f"mysql import error:\n{err}", parent=self.root)

            except Exception as e:
                messagebox.showerror("Restore Failed", f"{e}", parent=self.root)

        else:
            # Let user pick local .sql file
            file_path = filedialog.askopenfilename(title="Select SQL file to restore", filetypes=[("SQL Files","*.sql"),("All Files","*.*")], parent=self.root)
            if not file_path:
                return
            try:
                with open(file_path, "rb") as inp:
                    proc = subprocess.run([mysql_bin, f"--host={host}", f"--user={user}", f"--password={password}", db], stdin=inp, stderr=subprocess.PIPE)
                if proc.returncode == 0:
                    messagebox.showinfo("Restore", "Database restored from local backup.", parent=self.root)
                    #self.update_backup_status()
                else:
                    err = proc.stderr.decode(errors="ignore")
                    messagebox.showerror("Restore Failed", f"mysql import error:\n{err}", parent=self.root)
            except FileNotFoundError:
                messagebox.showerror("Error", "mysql client not found. Provide correct path in get_db_credentials().", parent=self.root)
            except Exception as e:
                messagebox.showerror("Restore Error", f"{e}", parent=self.root)

# ----------------------
# Update UI to show last local backup filename (if any)
# ----------------------
   """def update_backup_status(self):
        try:
            backup_folder = os.path.join(os.path.dirname(__file__), "backups")
            if not os.path.exists(backup_folder):
                self.backup_status.set("No backups yet")
                return
            files = [f for f in os.listdir(backup_folder) if f.startswith("sarthtailor_backup_") and f.endswith(".sql")]
            if not files:
                self.backup_status.set("No backups yet")
                return
            last = max(files)   # lexicographically latest -> matches timestamp format
            self.backup_status.set(f"Last backup: {last}")
        except Exception:
            self.backup_status.set("Error reading backups")"""

# ----------------------
# Scheduler helper to run backup every 24 hours
# ----------------------
#  ... आपकी TailorSoftware क्लास के अंदर ...

    # यह फ़ंक्शन अब केवल बैकअप चलाता है और खुद को अगले 24 घंटे के लिए शेड्यूल करता है
   def schedule_daily_backup(self):
        try:
            # बैकअप को एक अलग थ्रेड में चलाएं ताकि GUI फ्रीज न हो
            threading.Thread(target=self.auto_backup_to_drive, daemon=True).start()
        finally:
            # 24 घंटे (86400 सेकंड) बाद फिर से शेड्यूल करें
            threading.Timer(86400, self.schedule_daily_backup).start()


   def start_daily_scheduler(self, target_hour=10, target_minute=0):
         
        now = datetime.datetime.now()
        
        target_time = now.replace(hour=target_hour, minute=target_minute, second=0, microsecond=0)
                 
        if now > target_time:
            target_time += datetime.timedelta(days=1)
        
        delay_seconds = (target_time - now).total_seconds()
                
        print(f"Daily backup scheduled to start at {target_time.strftime('%I:%M %p')} (in {datetime.timedelta(seconds=delay_seconds)})")
        
        threading.Timer(delay_seconds, self.schedule_daily_backup).start()


   def addcustomer_btn(self):
        self.new_window=Toplevel(self.root)
        self.app=customer(self.new_window)

   def measurement_btn(self):
       self.new_window=Toplevel(self.root)
       self.app=measurement_win(self.new_window)

   def graphicviewbtn(self):
       self.new_window=Toplevel(self.root)
       self.app=graphic_win(self.new_window)
   
   def billbtn2(self):
       self.new_window=Toplevel(self.root)
       self.app=bill_win(self.new_window)

   def smsbtn(self):
       self.new_window=Toplevel(self.root)
       self.app=sms_win(self.new_window)
   
   def pricemanagerbtn(self):
       self.new_window=Toplevel(self.root)
       self.app=ProductControl(self.new_window)
       

   def logout_btn(self):
        self.root.destroy()





if __name__=="__main__":
    root=Tk()
    app=Tailorsoftware(root)
    app.start_daily_scheduler(target_hour=10, target_minute=0)
    root.mainloop()