from tkinter import*
from tkinter import ttk
from PIL import Image,ImageTk
from tkinter import messagebox
import mysql.connector
from Home import Tailorsoftware,extract_google_files
from dbcreater import setup_database

def resource_path(relative_path):
    import sys, os
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


# Fixed credentials
FIXED_USERNAME = "admin"
FIXED_PASSWORD = "admin123"
SECURITY_QUESTION = "Your Birth Place"
SECURITY_ANSWER = "Mumbai"

# ================= Database Connection Function =================
def get_connection():
    import json
    import os

     # ALWAYS load config.json from extracted DriveAuth folder
    auth_folder = extract_google_files()
    config_path = os.path.join(auth_folder, "config.json")

    with open(config_path, "r") as f:
        config = json.load(f)

    return mysql.connector.connect(
        host=config["host"],
        user=config["user"],
        password=config["password"],
        database=config["database"]
    )


def main():
    setup_database()
    win=Tk()
    app=login_form(win)
    win.mainloop()

 
class login_form():
    def __init__(self,root):
        self.root=root
        self.root.title("Login Page")
        self.root.geometry("1920x1080+0+0")
        #self.root.resizable(False,False)
    # Main Background photo
        img_bg_path=resource_path(r"photos\bg.jpg")
        img_bg=Image.open(img_bg_path)
        img_bg=img_bg.resize((1900,1060),Image.ANTIALIAS)
        self.main_bg=ImageTk.PhotoImage(img_bg)
        lbl_main_bg=Label(self.root,image=self.main_bg)
        lbl_main_bg.place(x=0,y=0)

    # Main Frame
        main_frame=Frame(self.root,bg="black")
        main_frame.place(x=610,y=170,width=340,height=450)
   
    # login Icon
        img1_path=resource_path(r"photos\login.webp")
        img1=Image.open(img1_path)
        img1=img1.resize((100,100),Image.ANTIALIAS)
        self.photoimg1=ImageTk.PhotoImage(img1)
        lblimg=Label(image=self.photoimg1,bg="black",borderwidth=0,)
        lblimg.place(x=730,y=175,width=100,height=100)

        lbl_started=Label(main_frame,text="Get Started",font=("times new roman",20,"bold"),bg="black",fg="white")
        lbl_started.place(x=95,y=100)

    # NameIcon
        img_name_path=resource_path(r"photos\login.webp")
        img_name=Image.open(img_name_path)
        img_name=img_name.resize((25,25),Image.ANTIALIAS)
        self.img_photo2=ImageTk.PhotoImage(img_name)
        lbl_image2=Label(main_frame,image=self.img_photo2,bg="black",borderwidth=0)
        lbl_image2.place(x=55,y=150)

    # passwordLogo
        img_password_path=resource_path(r"photos\password.png")
        img_password=Image.open(img_password_path)
        img_password=img_password.resize((25,25),Image.ANTIALIAS)
        self.img_photo3=ImageTk.PhotoImage(img_password)
        lbl_image3=Label(main_frame,image=self.img_photo3,bg="black",borderwidth=0)
        lbl_image3.place(x=55,y=210)
    # Labels Name
        lbl_name=Label(main_frame,text="UserName/Gmail:",font=("times new roman",13,"bold"),bg="black",fg="white")
        lbl_name.place(x=80,y=150)

        self.entry_name=ttk.Entry(main_frame,font=("times new roman",10))
        self.entry_name.place(x=60,y=180,width=230)

    # label password
        lbl_password=Label(main_frame,text="Password:",font=("times new roman",13,"bold"),bg="black",fg="white")
        lbl_password.place(x=80,y=210)

        self.entry_password=ttk.Entry(main_frame,font=("times new roman",10),show="*")
        self.entry_password.place(x=60,y=240,width=230)
    
    # Login button
        btn_login=Button(main_frame,command=self.login_accept,text="Login",font=("times new roman",15,"bold"),bg="red",fg="white",activebackground="red",activeforeground="white",cursor="hand2")
        btn_login.place(x=140,y=280)

        forgot_password=Button(main_frame,text="Forgot Password?",command=self.forgot_password,font=("times new roman",10,"bold"),bg="black",fg="white",activebackground="black",activeforeground="white",cursor="hand2",)
        forgot_password.place(x=60,y=350)
      


    def login_accept(self):

        username = self.entry_name.get()
        password = self.entry_password.get()

        if username == "" or password == "":
            messagebox.showerror("Error", "All Fields Are Required", parent=self.root)
            return

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM login WHERE username=%s", (username,))
        row = cursor.fetchone()
        conn.close()
    
        if row is None:
            messagebox.showerror("Error", "Invalid Username", parent=self.root)
        elif row[0] == password:
            open_main = messagebox.askyesno("Sarth Tailor Shop",
                                            "Access Only Admin. Open Sarth Tailor Shop?",
                                            parent=self.root)
            if open_main: 
                self.new_window = Toplevel(self.root)
                self.app = Tailorsoftware(self.new_window)               
        else:
            messagebox.showerror("Error", "Incorrect Password", parent=self.root)
        self.entry_name.delete(0,END)
        self.entry_password.delete(0,END) 
        

# =================================================reset function ======================================================
    def reset_password(self, username, correct_answer):
        new_password = self.new_password_entry.get()
        answer = self.entry_security_answer.get()

        if new_password == "" or answer == "":
            messagebox.showerror("Error", "All Fields Are Required", parent=self.root2)
        elif answer != correct_answer:
            messagebox.showerror("Error", "Incorrect Security Answer", parent=self.root2)
        else:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE login SET password=%s WHERE username=%s",
                           (new_password, username))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Password has been reset permanently.", parent=self.root2)
            self.root2.destroy()
# =================================================forget password ======================================================
    def forgot_password(self):
        username = self.entry_name.get()
        if username == "":
            messagebox.showerror("Error", "Enter Username", parent=self.root)
            return

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT security_question, security_answer FROM login WHERE username=%s", (username,))
        row = cursor.fetchone()
        conn.close()

        if row is None:
            messagebox.showerror("Error", "Invalid Username", parent=self.root)
            return

        question, answer = row

        self.root2 = Toplevel(self.root)
        self.root2.title("Forget Password")
        self.root2.geometry("340x450+610+170")
        self.root2.resizable(False,False)

        lbl = Label(self.root2, text="Forget Password",
                    font=("times new roman", 20, "bold"), fg="red")
        lbl.pack(side=TOP, pady=10)

        main_frame = Frame(self.root2, bd=4, relief=RIDGE, bg="orangered")
        main_frame.place(x=5, y=50, width=330, height=395)

        lbl_securityQ = Label(main_frame,text=f"Security Question:{question}",
                              font=("times new roman", 12, "bold"),bg="orangered")
        lbl_securityQ.place(x=20, y=50)

        self.entry_security_answer = ttk.Entry(main_frame,
                                               width=35,
                                               font=("times new roman", 10, "bold"))
        self.entry_security_answer.place(x=20, y=80, width=250)

        lbl_new_password = Label(main_frame, text="New Password",
                                 font=("times new roman", 12, "bold"), bg="orangered")
        lbl_new_password.place(x=20, y=130)

        self.new_password_entry = ttk.Entry(main_frame,
                                            width=35,
                                            font=("times new roman", 10, "bold"))
        self.new_password_entry.place(x=20, y=160, width=250)

        reset_btn = Button(main_frame, text="RESET",
                           command=lambda: self.reset_password(username, answer),
                           font=("times new roman", 12, "bold"),
                           bg="lime", fg="black",
                           activebackground="lime", activeforeground="white",
                           cursor="hand2")
        reset_btn.place(x=130, y=220)
     


    def return_login_page(self):
        self.root.destroy()
     
 
 
if __name__ == "__main__":
    main()

 