from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image,ImageTk
import mysql.connector
import os
import json

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

class graphic_win:
   def __init__(self,root):
        self.root=root
        self.root.geometry("1920x1080+0+0")
        self.root.title("Tailor Management System")
        self.root.state("zoomed")
        self.root.resizable(False,False)
#====================================================variables==================================
        self.search_entry_var=StringVar()

        lbl_main_title=Label(self.root,text="Graphical Measurement",font=("times new roman",20,"bold"),bg="black",fg="gold",bd=4,relief=RIDGE)
        lbl_main_title.place(x=0,y=0,width=1550,height=50)

        mainframe=Frame(self.root,bd=13,relief=RIDGE)
        mainframe.place(x=0,y=50,width=1534,height=788)
        
        lbl_search=Label(mainframe,text="SEARCH BY",font=("times new roman",12,"bold"),bg="red",fg="white")
        lbl_search.place(x=550,y=20)

        search_entry=ttk.Entry(mainframe,textvariable=self.search_entry_var,font=("times new roman",13,"bold"),width=15)
        search_entry.place(x=650,y=20)

        search_btn=Button(mainframe,text="SHOW",command=self.showbtn,font=("times new roman",10,"bold"),bd=4,bg="cyan",fg="black",width=15,activebackground="cyan",activeforeground="black",cursor="hand2")
        search_btn.place(x=800,y=18)

        imggshirt_path=resource_path(r"photos\gshirt.png")
        imggshirt=Image.open(imggshirt_path)
        imggshirt=imggshirt.resize((300,300),Image.ANTIALIAS)
        self.imggshirt_demo=ImageTk.PhotoImage(imggshirt)
        imggshirt_lbl=Label(self.root,image=self.imggshirt_demo,bd=0,relief=RIDGE)
        imggshirt_lbl.place(x=590,y=160,width=300,height=300)

        imggpant_path=resource_path(r"photos\gpant.png")
        imggpant=Image.open(imggpant_path)
        imggpant=imggpant.resize((200,350),Image.ANTIALIAS)
        self.imggpant_demo=ImageTk.PhotoImage(imggpant)
        imggpant_lbl=Label(self.root,image=self.imggpant_demo,bd=0,relief=RIDGE)
        imggpant_lbl.place(x=640,y=450,width=200,height=350)

        imgdown_path=resource_path(r"photos\down.png")
        imgdown=Image.open(imgdown_path)
        imgdown=imgdown.resize((550,750),Image.ANTIALIAS)
        self.imgdown_demo=ImageTk.PhotoImage(imgdown)
        imgdown_lbl=Label(self.root,image=self.imgdown_demo,bd=0,relief=RIDGE)
        imgdown_lbl.place(x=15,y=65,width=550,height=750)

        imgup_path=resource_path(r"photos\up.png")
        imgup=Image.open(imgup_path)
        imgup=imgup.resize((550,750),Image.ANTIALIAS)
        self.imgup_demo=ImageTk.PhotoImage(imgup)
        imgdown_lbl=Label(self.root,image=self.imgup_demo,bd=0,relief=RIDGE)
        imgdown_lbl.place(x=940,y=70,width=550,height=750)



   def showbtn(self):
          if self.search_entry_var.get()=="":
             messagebox.showerror("Error","Please enter exist customer name...!",parent=self.root)
          else:
            conn=get_connection()
            mycursor=conn.cursor()
            query=("select Name from measurement where Name=%s")
            val=(self.search_entry_var.get(),)
            mycursor.execute(query,val)
            row=mycursor.fetchone()

            if row==None:
               messagebox.showerror("Error","This name customer dosn't exit...!",parent=self.root)
            else:
               conn.commit()
               conn.close()
               shirtshowframe=Frame(self.root,bd=4,relief=RIDGE,padx=2)
               shirtshowframe.place(x=150,y=160,width=400,height=250)

               pantshowframe=Frame(self.root,bd=4,relief=RIDGE,padx=2)
               pantshowframe.place(x=880,y=530,width=400,height=250)

               lblshirt=Label(shirtshowframe,text="SHIRT MEASUREMENT",font=("times new roman",12,"bold"))
               lblshirt.place(x=110,y=0)

               lblpant=Label(pantshowframe,text="PANT MEASUREMENT",font=("times new roman",12,"bold"))
               lblpant.place(x=110,y=0)

               lbl_name=Label(shirtshowframe,text="Name:",font=("times new roman",12,"bold"))
               lbl_name.place(x=120,y=28)

               lbl=Label(shirtshowframe,text=row,font=("times new roman",12,"bold"))
               lbl.place(x=170,y=28)

               lbl_namepant=Label(pantshowframe,text="Name:",font=("times new roman",12,"bold"))
               lbl_namepant.place(x=120,y=28)

               lbl_namepant=Label(pantshowframe,text=row,font=("times new roman",12,"bold"))
               lbl_namepant.place(x=170,y=28)
            """#==============================================fetch type of shirt====================================
            conn=mysql.connector.connect(
                                               host="localhost",
                                               user="root",
                                               password="OnkarA@060105",
                                               database="sarthtailor"
                                               )
            mycursor=conn.cursor()
            query=("select Type_Of_Shirt from addcustomer where Name=%s")
            val=(self.search_entry_var.get(),)
            mycursor.execute(query,val)
            row=mycursor.fetchone()

            lbl_gender=Label(shirtshowframe,text="Type Of Shirt:",font=("times new roman",12,"bold"))
            lbl_gender.place(x=120,y=50)

            lbl1=Label(shirtshowframe,text=row,font=("times new roman",12,"bold"))
            lbl1.place(x=220,y=50)
#====================================================design of shirt==============================
            conn=mysql.connector.connect(
                                               host="localhost",
                                               user="root",
                                               password="OnkarA@060105",
                                               database="sarthtailor"
                                               )
            mycursor=conn.cursor()
            query=("select Design_Of_Shirt from addcustomer where Name=%s")
            val=(self.search_entry_var.get(),)
            mycursor.execute(query,val)
            row=mycursor.fetchone()

            lbl_gender=Label(shirtshowframe,text="Design Of Shirt:",font=("times new roman",12,"bold"))
            lbl_gender.place(x=120,y=70)

            lbl1=Label(shirtshowframe,text=row,font=("times new roman",12,"bold"))
            lbl1.place(x=220,y=70)"""
#========================================Sh_Length===========================================================
            conn=get_connection()
            mycursor=conn.cursor()
            query=("select Sh_Length from measurement where Name=%s")
            val=(self.search_entry_var.get(),)
            mycursor.execute(query,val)
            row=mycursor.fetchone()

            lbl_gender=Label(shirtshowframe,text="Sh_Length:",font=("times new roman",12,"bold"))
            lbl_gender.place(x=50,y=100)

            lbl1=Label(shirtshowframe,text=row,font=("times new roman",12,"bold"))
            lbl1.place(x=135,y=100)
#========================================Sh_Chest===========================================================
            conn=get_connection()
            mycursor=conn.cursor()
            query=("select Sh_Chest from measurement where Name=%s")
            val=(self.search_entry_var.get(),)
            mycursor.execute(query,val)
            row=mycursor.fetchone()

            lbl_gender=Label(shirtshowframe,text="Sh_Chest:",font=("times new roman",12,"bold"))
            lbl_gender.place(x=250,y=100)

            lbl1=Label(shirtshowframe,text=row,font=("times new roman",12,"bold"))
            lbl1.place(x=325,y=100)
#========================================Sh_Stomach===========================================================
            conn=get_connection()
            mycursor=conn.cursor()
            query=("select Sh_Stomach from measurement where Name=%s")
            val=(self.search_entry_var.get(),)
            mycursor.execute(query,val)
            row=mycursor.fetchone()

            lbl_gender=Label(shirtshowframe,text="Sh_Stomach:",font=("times new roman",12,"bold"))
            lbl_gender.place(x=50,y=125)

            lbl1=Label(shirtshowframe,text=row,font=("times new roman",12,"bold"))
            lbl1.place(x=140,y=125)
#========================================Sh_shoulder===========================================================
            conn=get_connection()
            mycursor=conn.cursor()
            query=("select Sh_Shoulder from measurement where Name=%s")
            val=(self.search_entry_var.get(),)
            mycursor.execute(query,val)
            row=mycursor.fetchone()

            lbl_gender=Label(shirtshowframe,text="Sh_Shoulder:",font=("times new roman",12,"bold"))
            lbl_gender.place(x=250,y=125)

            lbl1=Label(shirtshowframe,text=row,font=("times new roman",12,"bold"))
            lbl1.place(x=345,y=125)
#========================================Sh_Sleeves===========================================================
            conn=get_connection()
            mycursor=conn.cursor()
            query=("select Sh_Sleeves from measurement where Name=%s")
            val=(self.search_entry_var.get(),)
            mycursor.execute(query,val)
            row=mycursor.fetchone()

            lbl_gender=Label(shirtshowframe,text="Sh_Sleeves:",font=("times new roman",12,"bold"))
            lbl_gender.place(x=50,y=150)

            lbl1=Label(shirtshowframe,text=row,font=("times new roman",12,"bold"))
            lbl1.place(x=140,y=150)
#========================================Sh_Neck===========================================================
            conn=get_connection()
            mycursor=conn.cursor()
            query=("select Sh_Neck from measurement where Name=%s")
            val=(self.search_entry_var.get(),)
            mycursor.execute(query,val)
            row=mycursor.fetchone()

            lbl_gender=Label(shirtshowframe,text="Sh_Neck:",font=("times new roman",12,"bold"))
            lbl_gender.place(x=250,y=150)

            lbl1=Label(shirtshowframe,text=row,font=("times new roman",12,"bold"))
            lbl1.place(x=320,y=150)
#========================================Sh_Cup===========================================================
            conn=get_connection()
            mycursor=conn.cursor()
            query=("select Sh_Cup from measurement where Name=%s")
            val=(self.search_entry_var.get(),)
            mycursor.execute(query,val)
            row=mycursor.fetchone()

            lbl_gender=Label(shirtshowframe,text="Sh_Cup:",font=("times new roman",12,"bold"))
            lbl_gender.place(x=50,y=175)

            lbl1=Label(shirtshowframe,text=row,font=("times new roman",12,"bold"))
            lbl1.place(x=115,y=175)
#========================================Sh_Front===========================================================
            conn=get_connection()
            mycursor=conn.cursor()
            query=("select Sh_Front from measurement where Name=%s")
            val=(self.search_entry_var.get(),)
            mycursor.execute(query,val)
            row=mycursor.fetchone()

            lbl_gender=Label(shirtshowframe,text="Sh_Front:",font=("times new roman",12,"bold"))
            lbl_gender.place(x=250,y=175)

            lbl1=Label(shirtshowframe,text=row,font=("times new roman",12,"bold"))
            lbl1.place(x=320,y=175)
            """#========================================Submitted date===========================================================
            conn=mysql.connector.connect(
                                               host="localhost",
                                               user="root",
                                               password="OnkarA@060105",
                                               database="sarthtailor"
                                               )
            mycursor=conn.cursor()
            query=("select Submitted_Date from addcustomer where Name=%s")
            val=(self.search_entry_var.get(),)
            mycursor.execute(query,val)
            row=mycursor.fetchone()

            lbl_gender=Label(shirtshowframe,text="Submitted Date:",font=("times new roman",12,"bold"))
            lbl_gender.place(x=120,y=210)

            lbl1=Label(shirtshowframe,text=row,font=("times new roman",12,"bold"))
            lbl1.place(x=230,y=210)"""
#====================================================pantshow frame===============================================
#========================================Length===========================================================
            conn=get_connection()
            mycursor=conn.cursor()
            query=("select Length from measurement where Name=%s")
            val=(self.search_entry_var.get(),)
            mycursor.execute(query,val)
            row=mycursor.fetchone()

            lbl_gender=Label(pantshowframe,text="Length:",font=("times new roman",12,"bold"))
            lbl_gender.place(x=50,y=100)

            lbl1=Label(pantshowframe,text=row,font=("times new roman",12,"bold"))
            lbl1.place(x=105,y=100)
#========================================Weist===========================================================
            conn=get_connection()
            mycursor=conn.cursor()
            query=("select Waist from measurement where Name=%s")
            val=(self.search_entry_var.get(),)
            mycursor.execute(query,val)
            row=mycursor.fetchone()

            lbl_gender=Label(pantshowframe,text="Waist:",font=("times new roman",12,"bold"))
            lbl_gender.place(x=250,y=100)

            lbl1=Label(pantshowframe,text=row,font=("times new roman",12,"bold"))
            lbl1.place(x=300,y=100)
#========================================Seat===========================================================
            conn=get_connection()
            mycursor=conn.cursor()
            query=("select Seat from measurement where Name=%s")
            val=(self.search_entry_var.get(),)
            mycursor.execute(query,val)
            row=mycursor.fetchone()

            lbl_gender=Label(pantshowframe,text="Seat:",font=("times new roman",12,"bold"))
            lbl_gender.place(x=50,y=125)

            lbl1=Label(pantshowframe,text=row,font=("times new roman",12,"bold"))
            lbl1.place(x=90,y=125)
#========================================Thigh===========================================================
            conn=get_connection()
            mycursor=conn.cursor()
            query=("select Thigh from measurement where Name=%s")
            val=(self.search_entry_var.get(),)
            mycursor.execute(query,val)
            row=mycursor.fetchone()

            lbl_gender=Label(pantshowframe,text="Thigh:",font=("times new roman",12,"bold"))
            lbl_gender.place(x=250,y=125)

            lbl1=Label(pantshowframe,text=row,font=("times new roman",12,"bold"))
            lbl1.place(x=300,y=125)
#========================================Knee===========================================================
            conn=get_connection()
            mycursor=conn.cursor()
            query=("select Knee from measurement where Name=%s")
            val=(self.search_entry_var.get(),)
            mycursor.execute(query,val)
            row=mycursor.fetchone()

            lbl_gender=Label(pantshowframe,text="Knee:",font=("times new roman",12,"bold"))
            lbl_gender.place(x=50,y=150)

            lbl1=Label(pantshowframe,text=row,font=("times new roman",12,"bold"))
            lbl1.place(x=95,y=150)
#========================================Bottom===========================================================
            conn=get_connection()
            mycursor=conn.cursor()
            query=("select Bottom from measurement where Name=%s")
            val=(self.search_entry_var.get(),)
            mycursor.execute(query,val)
            row=mycursor.fetchone()

            lbl_gender=Label(pantshowframe,text="Bottom:",font=("times new roman",12,"bold"))
            lbl_gender.place(x=250,y=150)

            lbl1=Label(pantshowframe,text=row,font=("times new roman",12,"bold"))
            lbl1.place(x=310,y=150)
            """#========================================Submitted date===========================================================
            conn=mysql.connector.connect(
                                               host="localhost",
                                               user="root",
                                               password="OnkarA@060105",
                                               database="sarthtailor"
                                               )
            mycursor=conn.cursor()
            query=("select Submitted_Date from addcustomer where Name=%s")
            val=(self.search_entry_var.get(),)
            mycursor.execute(query,val)
            row=mycursor.fetchone()

            lbl_gender=Label(pantshowframe,text="Submitted Date:",font=("times new roman",12,"bold"))
            lbl_gender.place(x=120,y=210)

            lbl1=Label(pantshowframe,text=row,font=("times new roman",12,"bold"))
            lbl1.place(x=230,y=210)"""



if __name__=="__main__":
    root=Tk()
    app=graphic_win(root)
    root.mainloop()