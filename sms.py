from tkinter import *
import requests
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image,ImageTk
import mysql.connector
import threading
import requests
import json
import os
import sys, os, shutil
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
from tkinter import filedialog, messagebox
APP_FOLDER_NAME = "SarthTailorShop"

BASE_PATH_FILE = os.path.join(
    os.getenv("LOCALAPPDATA"),
    APP_FOLDER_NAME,
    "base_path.json"
)

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
 


class sms_win:
    def __init__(self,root):
        self.root=root
        self.root.geometry("700x400+470+300")
        self.root.title("Messager")
        self.root.resizable(False,False)
        
        self.phone_var=StringVar()
        self.message_var=StringVar()
        self.serverurl_var=StringVar()
        self.stop_sending = False  # Stop flag

        # ========= Database Connection =========
        try:
            self.conn=get_connection()
            self.cursor = self.conn.cursor()
        except Exception as e:
            messagebox.showerror("Database Error", f"Database connection failed:\n{e}")
            return  # agar DB fail hua to aage code na chale

        # ========= Main Frame =========
        self.mainframe = Frame(self.root, bd=5, relief=GROOVE)
        self.mainframe.place(x=0, y=0, width=698, height=398)

        smsimg1_path=resource_path(r"photos\smsimg1.png")
        smsimg1=Image.open(smsimg1_path)
        smsimg1=smsimg1.resize((150,100),Image.ANTIALIAS)
        self.smsimg1_demo=ImageTk.PhotoImage(smsimg1)
        smsimg1_lbl=Button(self.mainframe,command=self.serverlink,image=self.smsimg1_demo,bd=0,relief=RIDGE)
        smsimg1_lbl.pack(side=TOP)

        smsimg2_path=resource_path(r"photos\billimg1.png")
        smsimg2=Image.open(smsimg2_path)
        smsimg2=smsimg2.resize((200,389),Image.ANTIALIAS)
        self.smsimg2_demo=ImageTk.PhotoImage(smsimg2)
        smsimg2_lbl=Label(self.mainframe,image=self.smsimg2_demo,bd=0,relief=RIDGE)
        smsimg2_lbl.place(x=0,y=0,width=200,height=389)

        smsimg3_path=resource_path(r"photos\billimg2.png")
        smsimg3=Image.open(smsimg3_path)
        smsimg3=smsimg3.resize((200,389),Image.ANTIALIAS)
        self.smsimg3_demo=ImageTk.PhotoImage(smsimg3)
        smsimg3_lbl=Label(self.mainframe,image=self.smsimg3_demo,bd=0,relief=RIDGE)
        smsimg3_lbl.place(x=485,y=0,width=200,height=389)


        # ========= Phone Input =========
        Label(self.mainframe, text="Phone No:(+91)", font=("times new roman", 12, "bold")).place(x=220, y=130)
        ttk.Entry(self.mainframe, textvariable=self.phone_var, font=("times new roman", 12, "bold"), width=30).place(x=220, y=160)

        # ========= Message Box =========
        Label(self.mainframe, text="Message:", font=("times new roman", 12, "bold")).place(x=220, y=200)
        self.textentry = Text(self.mainframe, font=("times new roman", 12, "bold"), width=30, height=5)
        self.textentry.place(x=220, y=230)
        self.textentry.insert(END, "Hello! This is a test SMS")

        # ========= Buttons =========
        self.sendbtn=Button(self.mainframe, text="SEND", command=self.send_sms_gui,font=("times new roman", 12, "bold"), width=10, bg="green",fg="white",activebackground="green",activeforeground="white",cursor="hand2")
        self.sendbtn.place(x=295,y=340)

        self.sendallbtn=Button(self.mainframe, text="SEND TO ALL", command=self.start_send_all_thread,font=("times new roman", 12, "bold"), width=12, bg="blue",fg="white",activebackground="blue",activeforeground="white",cursor="hand2")
        self.sendallbtn.place(x=480, y=240)

        self.stopsendingbtn=Button(self.mainframe, text="STOP SENDING", command=self.stop_sending_messages,font=("times new roman",11, "bold"), width=12, bg="red",fg="white",activebackground="red",activeforeground="white",cursor="hand2")
        self.stopsendingbtn.place(x=480, y=285)

        # ========= Progress Bar =========
        self.progress = ttk.Progressbar(self.mainframe, orient=HORIZONTAL, length=400, mode='determinate')
        self.progress.place(x=220, y=420)

        self.status_lbl = Label(self.mainframe, text="", font=("times new roman", 11, "bold"), fg="purple")
        self.status_lbl.place(x=220, y=445)

   # ---- Function to send SMS ----
    """def send_sms(self, number, message):
        
        url = "https://www.fast2sms.com/dev/bulkV2"

        headers = {
            "authorization": "Fq7URU4lRd5MmmMtXuxWOh1LGaj8ZtSDy5pyTigNEI3a90psNDe0S3yzLmGF",  # your API key
        }

        payload = {
            "sender_id": "TXTIND",     # default sender id
            "message": message,        # your SMS content
            "language": "english",     # or 'unicode' for Hindi
            "route": "q",             # 'v3' for transactional messages
            "numbers": number          # single or multiple comma-separated numbers
        }

        try:
            # ✅ send POST requestcr
            response = requests.post(url, data=payload, headers=headers)
            print(response.text)  # debugging

            if response.status_code == 200 and "Message sent successfully" in response.text:
                messagebox.showinfo("Success", "✅ SMS Sent Successfully!", parent=self.root)
            else:
                messagebox.showerror("Failed", f"❌ Failed: {response.text}", parent=self.root)
        except Exception as e:
            messagebox.showerror("Error", f"❌ Error: {str(e)}", parent=self.root)"""

# --------------------------------------

    def send_sms(self, number, message):
        try:
            # ---- Fetch URL from Database ----
            self.cursor.execute("SELECT url FROM gatewayurl LIMIT 1")
            result = self.cursor.fetchone()

            if result is None:
                messagebox.showerror("Error", "❌ No Server URL found in database!", parent=self.root)
                return

            SIMPLE_GATEWAY_URL = result[0]   # URL fetched

        except Exception as e:
            messagebox.showerror("Error", f"❌ Failed to fetch URL from DB:\n{e}", parent=self.root)
            return

        # ---- JSON Payload ----
        payload_data = {
            "phone": str(number),
            "message": str(message)
        }

        headers = {
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(SIMPLE_GATEWAY_URL, json=payload_data, headers=headers)
            response_text = response.text
            print(f"Server Response: {response_text}")

            if response.status_code == 200 and ("success" in response_text or "SENT" in response_text):
                #messagebox.showinfo("Success", f"SMS Sent Successfully to {number}", parent=self.root)
                return True
            else:
                print("Failed response:", response_text)
                return False

        except requests.exceptions.ConnectionError:
            messagebox.showerror("Error", "❌ Connection Error: Unable to reach server!", parent=self.root)
            return False

        except Exception as e:
            messagebox.showerror("Error", f"Unexpected Error: {e}", parent=self.root)
            return False

        
    # ---- Function linked to Button ----
    def send_sms_gui(self):
        number = self.phone_var.get().strip()
        msg = self.textentry.get("1.0", END).strip()

        if not number or not msg:
            messagebox.showwarning("Input Error", "⚠️ Please enter number and message!", parent=self.root)
            return

        # Send SMS and get result
        success = self.send_sms(number, msg)
        if success:
            messagebox.showinfo("Success",f"SMS Sent Successfully to {number}", parent=self.root)
        else:
            messagebox.showerror("Error",f"Something went wrong message not sent to this{number}", parent=self.root)



    # ---------------- THREAD STARTER ----------------
    def start_send_all_thread(self):
        self.stop_sending = False
        thread = threading.Thread(target=self.send_to_all)
        thread.start()

    # ---------------- STOP FUNCTION ----------------
    def stop_sending_messages(self):
        self.stop_sending = True
        self.status_lbl.config(text="🛑 Sending stopped by user.")
        messagebox.showinfo("Stopped", "🚫 Message sending has been stopped!", parent=self.root)

    # ---------------- SEND TO ALL ----------------
    def update_progress(self, count, total):
        self.progress["value"] = count
        percent = int((count / total) * 100)
        self.status_lbl.config(text=f"Sending {count}/{total} messages... ({percent}%)")


    def show_popup_once(self, title, message):
        """Show only one popup per send process."""
        if not self.popup_shown:
            self.popup_shown = True
            messagebox.showinfo(title, message, parent=self.root)


    def send_to_all(self):
        msg = self.textentry.get("1.0", END).strip()
        self.popup_shown = False    # Reset popup lock
        error_found = False

        # Check empty message
        if not msg:
            self.show_popup_once("Error", "Message box is empty!")
            return

        try:
            # Fetch numbers
            self.cursor.execute("SELECT phone FROM addcustomer")
            numbers = self.cursor.fetchall()

            if not numbers:
                self.show_popup_once("Info", "No customers found in database!")
                return

            total = len(numbers)
            count = 0

            # UI start state
            self.progress.config(maximum=total, value=0)
            self.status_lbl.config(text=f"Sending messages... (0/{total})")

            # Send loop
            all_results = []

            for num in numbers:
                try:
                    success = self.send_sms(num[0], msg)
                    all_results.append((num[0], success))
                    if not success:
                        error_found = True
                except:
                    all_results.append((num[0], False))
                    error_found = True

            count += 1
            self.update_progress(count, total)

            # -------------------------
            # FINAL SINGLE POPUP WITH STATUS
            # -------------------------
            popup_text = ""
            for number, success in all_results:
                status = "Sent ✅" if success else "Failed ❌"
                popup_text += f"{number}: {status}\n"

            self.show_popup_once("SMS Report", popup_text)

            # Reset progress
            self.progress.config(value=0)

        except Exception as e:
            self.show_popup_once("Error", f"Error: {e}")


    
    def serverlink(self):
        self.root2=Toplevel()
        self.root2.geometry("700x200+470+400")
        self.root2.title("Server")
        self.root2.resizable(False,False)

        self.serverlinkmainframe= Frame(self.root2, bd=5,relief=GROOVE)
        self.serverlinkmainframe.place(x=0, y=0, width=698, height=198)

        #server link
        serverimg2_path=resource_path(r"photos\server.png")
        serverimg2=Image.open(serverimg2_path)
        serverimg2=serverimg2.resize((690,220),Image.ANTIALIAS)
        self.serverimg2_demo=ImageTk.PhotoImage(serverimg2)
        serverimg2_lbl=Label(self.serverlinkmainframe,image=self.serverimg2_demo,bd=0,relief=RIDGE)
        serverimg2_lbl.place(x=0,y=0,width=690,height=220)

        self.lblurl=Label(self.serverlinkmainframe, text="SERVER URL:", font=("times new roman", 12, "bold"))
        self.lblurl.place(x=200, y=50)
        conn=get_connection()
        mycursor=conn.cursor()
        mycursor.execute("SELECT url FROM gatewayurl")
        rows=mycursor.fetchall()
        self.entryurl=ttk.Entry(self.serverlinkmainframe,textvariable=self.serverurl_var,font=("times new roman", 12, "bold"), width=40)
        self.entryurl.place(x=200, y=80)
        if rows:
            last_url = rows[-1][0]    # सबसे आखिरी वाला URL
            self.serverurl_var.set(last_url)
        

        serverbtn=Button(self.serverlinkmainframe,text="START SERVER",command=self.update_server_url,font=("times new roman",12,"bold"),bg="green",fg="white",activebackground="green",activeforeground="white",cursor="hand2")
        serverbtn.place(x=280,y=130)


    def update_server_url(self):
        new_url = self.serverurl_var.get().strip()

        if not new_url:
            messagebox.showerror("Error", "Please enter new server URL", parent=self.root2)
            return

        try:
            conn=get_connection()
            cursor = conn.cursor()

            # Update URL - assuming only one row exists
            cursor.execute("UPDATE gatewayurl SET url = %s", (new_url,))
            conn.commit()
            conn.close()

            messagebox.showinfo("Success","✔️ Connection Established\n\nThe server is now active and ready to use.",parent=self.root2)


        except Exception as e:
            messagebox.showerror("Database Error", f"Error: {e}", parent=self.root2)





            

if __name__=="__main__":
    root=Tk()
    app=sms_win(root)
    root.mainloop()

 