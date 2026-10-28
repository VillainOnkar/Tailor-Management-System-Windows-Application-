from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image,ImageTk
import mysql.connector
import os,random
from docx import Document
from docx.shared import Inches
import tempfile
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
#from fpdf import FPDF
from tkcalendar import DateEntry
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


 


class bill_win:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1525x535+0+262")
        self.root.title("Dashboard")
        self.root.resizable(False,False)
         

#=========================================================variables==============================================================
        self.receiptno_var=StringVar()
        self.cname_var=StringVar()
        self.cphone_var=StringVar()
        self.submitdate_var=StringVar()
        self.category_var=StringVar()
        self.price_var=IntVar()
        self.qty_var=IntVar()
        self.total_var=StringVar()
        self.billno_var=StringVar()
#==============================================================================================================================

        lbl_main_title=Label(self.root,text="BILLING SYSTEM",font=("times new roman",18,"bold"),bg="black",fg="gold",bd=4,relief=RIDGE)
        lbl_main_title.place(x=0,y=0,width=1524,height=50)

        self.mainframe=Frame(self.root,bd=10,relief=RIDGE)
        self.mainframe.place(x=0,y=50,width=1524,height=485)

        billimg1_path=resource_path(r"photos\billimg1.png")
        billimg1=Image.open(billimg1_path)
        billimg1=billimg1.resize((200,465),Image.ANTIALIAS)
        self.billimg1_demo=ImageTk.PhotoImage(billimg1)
        billimg1_lbl=Label(self.mainframe,image=self.billimg1_demo,bd=0,relief=RIDGE)
        billimg1_lbl.place(x=0,y=0,width=200,height=465)

        billimg2_path=resource_path(r"photos\billimg2.png")
        billimg2=Image.open(billimg2_path)
        billimg2=billimg2.resize((200,465),Image.ANTIALIAS)
        self.billimg2_demo=ImageTk.PhotoImage(billimg2)
        billimg2_lbl=Label(self.mainframe,image=self.billimg2_demo,bd=0,relief=RIDGE)
        billimg2_lbl.place(x=1300,y=0,width=200,height=465)

        
        billimg3_path=resource_path(r"photos\billimg3.png")
        billimg3=Image.open(billimg3_path)
        billimg3=billimg3.resize((400,465),Image.ANTIALIAS)
        self.billimg3_demo=ImageTk.PhotoImage(billimg3)
        billimg3_lbl=Label(self.mainframe,image=self.billimg3_demo,bd=0,relief=RIDGE)
        billimg3_lbl.place(x=510,y=0,width=400,height=465)


        qrimg_path=resource_path(r"photos\qrimg.png")
        qrimg=Image.open(qrimg_path)
        qrimg=qrimg.resize((150,150),Image.ANTIALIAS)
        self.qrimg_demo=ImageTk.PhotoImage(qrimg)
        
    

        leftframe=Frame(self.mainframe,bd=4,relief=GROOVE,bg="white")
        leftframe.place(x=170,y=5,width=400,height=453)
#============================================================info frame==================================================================
        infoframe=LabelFrame(leftframe,text="Information",font=("times new roman",10,"bold"),bd=4,bg="white",relief=GROOVE,fg="red")
        infoframe.place(x=5,y=0,width=380,height=170)

        
        self.lbl_receiptno=Label(infoframe,text="Receipt No:",font=("times new roman",12,"bold"),bg="white",fg="red")
        self.lbl_receiptno.grid(row=0,column=0,padx=5,pady=5,sticky=W)
        self.receiptno_entry= ttk.Entry(infoframe,textvariable=self.receiptno_var,font=("times new roman",12,"bold"),width=20)
        self.receiptno_entry.grid(row=0,column=1,padx=5,pady=5,sticky=W)

        
        self.lbl_custname=Label(infoframe,text="Name:",font=("times new roman",12,"bold"),bg="white",fg="red")
        self.lbl_custname.grid(row=1,column=0,padx=5,pady=5,sticky=W)
        self.custname_entry= ttk.Entry(infoframe,textvariable=self.cname_var,font=("times new roman",12,"bold"),width=20)
        self.custname_entry.grid(row=1,column=1,padx=5,pady=5,sticky=W)

        self.lbl_phone=Label(infoframe,text="Phone No:",font=("times new roman",12,"bold"),bg="white",fg="red")
        self.lbl_phone.grid(row=2,column=0,padx=5,pady=5,sticky=W)
        self.phone_entry= ttk.Entry(infoframe,textvariable=self.cphone_var,font=("times new roman",12,"bold"),width=20)
        self.phone_entry.grid(row=2,column=1,padx=5,pady=5,sticky=W)

        self.lbl_submittedadate=Label(infoframe,text="Submit Date:",font=("times new roman",12,"bold"),bg="white",fg="red")
        self.lbl_submittedadate.grid(row=3,column=0,padx=5,pady=5,sticky=W)
        self.submittedadate_entry=DateEntry(infoframe,textvariable=self.submitdate_var,font=("times new roman",12,"bold"),width=18,date_pattern="dd-mm-yyyy")
        self.submittedadate_entry.grid(row=3,column=1,padx=5,pady=5,sticky=W)

        fetchbtn=Button(infoframe,text="Fetch",command=self.fetchbtn,font=("times new roman",10,"bold"),width=10,bd=4,bg="black",fg="gold",activebackground="black",activeforeground="gold",cursor="hand2")
        fetchbtn.grid(row=0,column=3,padx=5,pady=5,sticky=W)
       
#==============================================================product frame================================================================
        productframe=LabelFrame(leftframe,text="Product",font=("times new roman",10,"bold"),bd=4,bg="white",relief=GROOVE,fg="red")
        productframe.place(x=5,y=170,width=380,height=170)

        self.lbl_Category=Label(productframe,text="Category:",font=("times new roman",12,"bold"),bg="white",fg="red")
        self.lbl_Category.grid(row=0,column=0,padx=5,pady=5,sticky=W)

        conn=get_connection()
        mycursor=conn.cursor()
        mycursor.execute("select product_name from products")
        rows=mycursor.fetchall()
        self.Category_combobox= ttk.Combobox(productframe,textvariable=self.category_var,font=("times new roman",12,"bold"),width=18,state="readonly")
        self.Category_combobox["values"]=rows
        self.Category_combobox.grid(row=0,column=1,padx=5,pady=5,sticky=W)
        self.Category_combobox.bind("<<ComboboxSelected>>",self.categories)

        self.lbl_price=Label(productframe,text="Price:",font=("times new roman",12,"bold"),bg="white",fg="red")
        self.lbl_price.grid(row=1,column=0,padx=5,pady=5,sticky=W)
        self.price_entry= ttk.Entry(productframe,textvariable=self.price_var,font=("times new roman",12,"bold"),width=20)
        self.price_entry.grid(row=1,column=1,padx=5,pady=5,sticky=W)

        self.lbl_qty=Label(productframe,text="QTY:",font=("times new roman",12,"bold"),bg="white",fg="red")
        self.lbl_qty.grid(row=2,column=0,padx=5,pady=5,sticky=W)
        self.qty_entry= ttk.Entry(productframe,textvariable=self.qty_var,font=("times new roman",12,"bold"),width=20)
        self.qty_entry.grid(row=2,column=1,padx=5,pady=5,sticky=W)

        self.lbl_total=Label(productframe,text="Total Amount:",font=("times new roman",12,"bold"),bg="white",fg="red")
        self.lbl_total.grid(row=3,column=0,padx=5,pady=5,sticky=W)
        self.total_entry= ttk.Entry(productframe,textvariable=self.total_var,font=("times new roman",12,"bold"),width=20)
        self.total_entry.grid(row=3,column=1,padx=5,pady=5,sticky=W)


        self.addcartbtn1=Button(leftframe,text="ADD CART",command=self.addcartbtn,font=("times new roman",10,"bold"),width=10,bd=4,bg="orangered",fg="black",activebackground="orangered",activeforeground="black",cursor="hand2")
        self.addcartbtn1.place(x=100,y=350)

        self.genbillbtn=Button(leftframe,text="Generate Bill",command=self.gen_bill,font=("times new roman",10,"bold"),width=10,bd=4,bg="orangered",fg="black",activebackground="orangered",activeforeground="black",cursor="hand2")
        self.genbillbtn.place(x=200,y=350)

        billimg4_path=resource_path(r"photos\billimg4.png")
        billimg4=Image.open(billimg4_path)
        billimg4=billimg4.resize((220,65),Image.ANTIALIAS)
        self.billimg4_demo=ImageTk.PhotoImage(billimg4)
        billimg4_lbl=Label(leftframe,image=self.billimg4_demo,bd=0,relief=RIDGE,bg="white")
        billimg4_lbl.place(x=80,y=380,width=220,height=65)
        
#====================================================================receipt area============================================

        searchframe=Frame(self.mainframe,bd=2)
        searchframe.place(x=850,y=0,width=480,height=40)

        self.lbl_billno=Label(searchframe,text="Bill Number:",font=("times new roman",12,"bold"),bg="red",fg="white")
        self.lbl_billno.grid(row=0,column=0,sticky=W,padx=1)

        self.searchentry=ttk.Entry(searchframe,textvariable=self.billno_var,font=("times new roman",10,"bold"),width=24)
        self.searchentry.grid(row=0,column=1,sticky=W,padx=5,pady=2)

        self.searchbtn=Button(searchframe,text="SEARCH",command=self.searchbill,font=("times new roman",10,"bold"),bg="orangered",fg="white",activebackground="orangered",activeforeground="white",cursor="hand2",width=15)
        self.searchbtn.grid(row=0,column=2,sticky=W,padx=5,pady=2)

   
#======================================================================treeview===============================================
        rightbillframe=LabelFrame(self.mainframe,text="Bill Area",font=("times new roman",12,"bold"),bg="white",fg="red")
        rightbillframe.place(x=850,y=30,width=480,height=430)

        self.lbl_receipt=Label(rightbillframe,text="Bill Receipt",font=("times new roman",18,"bold"),bg="white",fg="red",bd=4,relief=RIDGE)
        self.lbl_receipt.place(x=0,y=0,width=475,height=40)

        rightbillframe2=Label(rightbillframe,bg="white",fg="red",bd=4)
        rightbillframe2.place(x=0,y=40,width=475,height=368)

        scrolly=Scrollbar(rightbillframe2,orient=VERTICAL)
        self.textarea=Text(rightbillframe2,yscrollcommand=scrolly.set,bg="white",fg="blue",font=("times new roman",12,"bold"))
        scrolly.pack(side=RIGHT,fill=Y)
        scrolly.config(command=self.textarea.yview)
        self.textarea.pack(fill=BOTH,expand=1)
#===========================================================bill btn frame====================================================

        btnframe=Frame(self.mainframe,bd=4,relief=RIDGE,bg="darkgreen")
        btnframe.place(x=1340,y=250,width=143,height=124)

        self.savebillbtn=Button(btnframe,text="Save Bill",command=self.savebill,font=("times new roman",12,"bold"),width=14,bg="lime",fg="white",cursor="hand2",activebackground="lime",activeforeground="white",pady=4)
        self.savebillbtn.grid(row=1,column=0)

        self.printbillbtn=Button(btnframe,text="Print Bill",command=self.printbtn1,font=("times new roman",12,"bold"),width=14,bg="purple",fg="white",cursor="hand2",activebackground="purple",activeforeground="white",pady=4)
        self.printbillbtn.grid(row=2,column=0)

        self.clearbtn=Button(btnframe,text="Clear",command=self.clearbtn2,font=("times new roman",12,"bold"),width=14,bg="red",fg="white",cursor="hand2",activebackground="red",activeforeground="white",pady=4)
        self.clearbtn.grid(row=3,column=0)

        self.list1=[]
        self.welcome()
#=============================================================================================================================================================
    def welcome(self):
        self.textarea.delete(1.0,END)
        self.textarea.image_create(END, image=self.qrimg_demo,padx=150)
        self.textarea.insert(END,"\t WELCOME TO SARTH TAILOR SHOP")
        self.textarea.insert(END,f"\n Receipt Number:{self.receiptno_var.get()}",)
        self.textarea.insert(END,f"\n Customer Name: {self.cname_var.get()}")
        self.textarea.insert(END,f"\n Mobile Number:{self.cphone_var.get()}")
        self.textarea.insert(END,f"\n Submitted Date:{self.submitdate_var.get()}")

        self.textarea.insert(END,"\n=================================================")
        self.textarea.insert(END,f"\n PRODUCTS\t\tQTY\t\tPRICE")
        self.textarea.insert(END,"\n=================================================\n")

    def addcartbtn(self):
        Tax=1
        self.m=self.price_var.get()*self.qty_var.get()
        self.list1.append(self.m)
        if self.category_var.get()=="Select Option":
            messagebox.showerror("Error","Pleaae Select the Product Name...!",parent=self.root)
        else:
            self.textarea.insert(END,f"\n {self.category_var.get()}\t\t{self.qty_var.get()}\t\t{self.m}")
            self.total_var.set(str("Rs.%.2f"%(sum(self.list1))))

    def gen_bill(self):
        if self.category_var.get()=="":
            messagebox.showerror("Error","Please Add To Cart Product",parent=self.root)
        else:
            text=self.textarea.get(10.0,(10.0+float(len(self.list1))))
            self.welcome()
            self.textarea.insert(END,text)
            self.textarea.insert(END,"\n\n=================================================")
            self.textarea.insert(END,f"\n \tTotal Amount:{self.total_var.get()}")
            self.textarea.insert(END,"\n=================================================\n")
            #self.textarea.insert(END,"\n=================================================\n")
            #self.textarea.insert(END,"\t\t\tAt Post Dhotri \n\t\tTaluka South Solapur District Solapur,\n\t\t\tMothi Ves\n\t\t\tContact:\n\t\t8888357708 \t   7028441334")
            #self.textarea.insert(END,"\n=================================================\n")
            self.textarea.tag_config("italic", font=("Times New Roman", 10, "italic","bold"))
            self.textarea.insert(END, "\t\tAt Post Dhotri \n\tTaluka South Solapur District Solapur,\n\t\tMothi Ves\n\t\tContact:\n\t8888357708  7028441334", "italic")

     
    """def savebill(self):
        if self.receiptno_var.get() == "":
            messagebox.showerror("Error", "Please Enter The Receipt No...!", parent=self.root)
            return

        op = messagebox.askyesno("Save Bill", "Do you want to save the bill?", parent=self.root)
        if op > 0:
            try:
                import os
                from docx import Document
                from docx.shared import Inches, Pt
                from docx.enum.text import WD_ALIGN_PARAGRAPH

                # ✅ Folder create karo agar nahi hai
                if not os.path.exists("bills_word"):
                    os.mkdir("bills_word")

                # ✅ Bill text fetch karo (textarea se)
                self.billdata = self.textarea.get(1.0, "end-1c")

                # ✅ Word file initialize
                doc = Document()
                section = doc.sections[0]
                section.page_width = Inches(3.14)     # 80 mm
                section.page_height = Inches(8.0)
                section.left_margin = Inches(0.2)
                section.right_margin = Inches(0.2)
                section.top_margin = Inches(0.2)
                section.bottom_margin = Inches(0.2)

                # ✅ QR image center me add karo
                try:
                    qr_para = doc.add_paragraph()
                    run = qr_para.add_run()
                    run.add_picture(resource_path(r"photos/qrimg.png"), width=Inches(1.3))
                    qr_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
                except Exception as e:
                    print("QR image not found:", e)

                # ✅ Thoda gap
                #doc.add_paragraph("")

                # ✅ Fixed-width font (alignment maintain rahe)
                para = doc.add_paragraph()
                run = para.add_run(self.billdata)
                run.font.name = "Courier New"   # Monospaced font
                run.font.size = Pt(6)           # 80 mm ke liye perfect
                para.alignment = WD_ALIGN_PARAGRAPH.LEFT
                para.paragraph_format.line_spacing = 1.0
                para.paragraph_format.space_after = Pt(0)

                # ✅ Save file
                file_path = f"bills_word/{self.receiptno_var.get()}.docx"
                doc.save(file_path)

                messagebox.showinfo(
                    "Saved",
                    f"Bill saved successfully!\n\nFile: {file_path}",
                    parent=self.root
                )

            except Exception as e:
                messagebox.showerror("Error", f"Error while saving file:\n{e}", parent=self.root)"""
    def savebill(self):
        import os
        from docx import Document
        from docx.shared import Inches, Pt
        from docx.enum.text import WD_ALIGN_PARAGRAPH
        from tkinter import messagebox

        # Receipt check
        if self.receiptno_var.get() == "":
            messagebox.showerror(
                "Error",
                "Please Enter The Receipt No...!",
                parent=self.root
            )
            return

        if not messagebox.askyesno(
            "Save Bill",
            "Do you want to save the bill?",
            parent=self.root
        ):
            return

        try:
            # -----------------------------------------
            # SAFE Bills Folder (Documents)
            # -----------------------------------------
            base_path = get_sarth_base_folder()
            bills_folder = os.path.join(base_path,APP_FOLDER_NAME,"Bills")
            os.makedirs(bills_folder, exist_ok=True)

            # -----------------------------------------
            # Bill text
            # -----------------------------------------
            self.billdata = self.textarea.get(1.0, "end-1c")

            # -----------------------------------------
            # Word Document
            # -----------------------------------------
            doc = Document()
            section = doc.sections[0]
            section.page_width = Inches(3.14)
            section.page_height = Inches(8.0)
            section.left_margin = Inches(0.2)
            section.right_margin = Inches(0.2)
            section.top_margin = Inches(0.2)
            section.bottom_margin = Inches(0.2)

            # QR Image
            try:
                qr_para = doc.add_paragraph()
                run = qr_para.add_run()
                run.add_picture(
                    resource_path("photos/qrimg.png"),
                    width=Inches(1.3)
                )
                qr_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            except:
                pass

            # Bill Text (Monospace)
            para = doc.add_paragraph()
            run = para.add_run(self.billdata)
            run.font.name = "Courier New"
            run.font.size = Pt(6)
            para.alignment = WD_ALIGN_PARAGRAPH.LEFT

            # -----------------------------------------
            # Save File
            # -----------------------------------------
            file_path = os.path.join(
                bills_folder,
                f"{self.receiptno_var.get()}.docx"
            )

            doc.save(file_path)

            messagebox.showinfo(
                "Saved",
                f"Bill saved successfully!\n\n{file_path}",
                parent=self.root
            )

        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Error while saving bill:\n{e}",
                parent=self.root
            )

         
    
    def printbtn1(self):
         
        try:
            from docx import Document
            from docx.shared import Inches, Pt
            from docx.enum.text import WD_ALIGN_PARAGRAPH
            import tempfile
            import os

            # ✅ Temporary Word document create karo
            doc = Document()
            section = doc.sections[0]
            section.page_width = Inches(3.14)     # 80 mm
            section.page_height = Inches(8.0)
            section.left_margin = Inches(0.2)
            section.right_margin = Inches(0.2)
            section.top_margin = Inches(0.2)
            section.bottom_margin = Inches(0.2)

            # ✅ QR image center me add karo
            try:
                qr_para = doc.add_paragraph()
                run = qr_para.add_run()
                run.add_picture(resource_path("photos/qrimg.png"), width=Inches(1.3))
                qr_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            except Exception as e:
                print("QR image missing:", e)

            # ✅ Thoda gap
            #doc.add_paragraph("")

            # ✅ Bill text add karo (alignment maintain rahe)
            bill_text = self.textarea.get(1.0, "end-1c")
            para = doc.add_paragraph()
            run = para.add_run(bill_text)
            run.font.name = "Courier New"   # Monospaced font for perfect spacing
            run.font.size = Pt(6)
            para.alignment = WD_ALIGN_PARAGRAPH.LEFT
            para.paragraph_format.line_spacing = 1.0
            para.paragraph_format.space_after = Pt(0)

            # ✅ Temporary file me save karo
            temp_path = tempfile.mktemp(".docx")
            doc.save(temp_path)

            # ✅ Print command
            os.startfile(temp_path, "print")

        except Exception as e:
            messagebox.showerror("Error", f"Error while printing:\n{e}", parent=self.root)


        """try:
            from docx import Document
            from docx.shared import Inches
            import tempfile
            import os

            # Temporary Word document with both QR image and text
            doc = Document()
             
            # ✅ Add QR image
            try:
                doc.add_picture("E:/Tailor management system/photos/qrimg.png", width=Inches(1.5))
            except Exception as e:
                print("QR image missing:", e)

            # ✅ Add bill text
            bill_text = self.textarea.get(1.0, "end-1c")
            doc.add_paragraph(bill_text)

            # ✅ Save temporary Word file
            temp_path = tempfile.mktemp(".docx")
            doc.save(temp_path)

            # ✅ Open/print
            os.startfile(temp_path, "print")

        except Exception as e:
            messagebox.showerror("Error", f"Error while printing:\n{e}", parent=self.root)"""


    
    

    """def searchbill(self):
        found = "no"
        bill_no = self.billno_var.get().strip()

        if bill_no == "":
            messagebox.showerror("Error", "Please enter Bill No!", parent=self.root)
            return

        for i in os.listdir("bills_word/"):
            if i.split(".")[0] == bill_no:
                try:
                    # ✅ Word file open using python-docx
                    doc = Document(f"bills_word/{i}")
                    self.textarea.delete(1.0, END)

                    # ✅ QR Image dubara show kare
                    self.textarea.image_create(END, image=self.qrimg_demo, padx=150)

                    # ✅ File ke text paragraphs read kare
                    for para in doc.paragraphs:
                        self.textarea.insert(END, para.text + "\n")

                    found = "yes"
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to open file:\n{e}", parent=self.root)
                break

        if found == "no":
            messagebox.showerror("Error", "Invalid Bill No or File Not Found!", parent=self.root)"""
    def searchbill(self):
        import os
        from docx import Document
        from tkinter import messagebox, END

        bill_no = self.billno_var.get().strip()

        if bill_no == "":
            messagebox.showerror(
                "Error",
                "Please enter Bill No!",
                parent=self.root
            )
            return

        # -----------------------------------------
        # SAFE Bills Folder (Documents)
        # -----------------------------------------
        base_path = get_sarth_base_folder()
        bills_folder = os.path.join(base_path,APP_FOLDER_NAME,"Bills")
        os.makedirs(bills_folder, exist_ok=True)

        if not os.path.exists(bills_folder):
            messagebox.showerror(
                "Error",
                "No bills found yet!",
                parent=self.root
            )
            return

        bill_file = os.path.join(
            bills_folder,
            f"{bill_no}.docx"
        )

        if not os.path.exists(bill_file):
            messagebox.showerror(
                "Error",
                "Invalid Bill No or File Not Found!",
                parent=self.root
            )
            return

        try:
            doc = Document(bill_file)

            self.textarea.delete(1.0, END)

            # QR image dubara show
            try:
                self.textarea.image_create(
                    END,
                    image=self.qrimg_demo,
                    padx=150
                )
            except:
                pass

            for para in doc.paragraphs:
                self.textarea.insert(END, para.text + "\n")

        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Failed to open file:\n{e}",
                parent=self.root
            )


    def clearbtn2(self):
        self.textarea.delete(1.0,END)
        self.receiptno_var.set("")
        self.cname_var.set("")
        self.cphone_var.set("")
        self.submitdate_var.set("")
        self.category_var.set("Select Option")
        self.price_var.set(0)
        self.qty_var.set(1)
        self.total_var.set(0)
        self.billno_var.set("")
        self.welcome()

            
#=============================================================================================================================================================

    def categories(self,event=""):
        try:
            conn = get_connection()
            mycursor = conn.cursor()
            query = "SELECT price FROM products WHERE product_name = %s"
            val = (self.Category_combobox.get(),)
            mycursor.execute(query, val)
            row = mycursor.fetchone()

            if row:
                self.price_var.set(row[0])  # price ko set karo
                self.qty_var.set(1)
            else:
                messagebox.showerror("Error", "Price not found for selected product.", parent=self.root)

            conn.close()

        except Exception as e:
            messagebox.showerror("Error", f"Something went wrong: {str(e)}", parent=self.root)

#=================================================================fetch button==========================================================
    def fetchbtn(self):
        if self.receiptno_var.get()=="":
            messagebox.showerror("Error","Please Enter The Exit Receipt No...!",parent=self.root)
        else:
            conn=get_connection()
            mycursor=conn.cursor()
            query=("select Name from addcustomer where Reference_No=%s")
            val=(self.receiptno_var.get(),)
            mycursor.execute(query,val)
            row=mycursor.fetchone()

            if row==None:
               messagebox.showerror("Error","This Receipt No Customer Not Exist...!",parent=self.root)
            else:
               conn.commit()
               conn.close()
               self.fetchframe=Frame(self.mainframe,bd=4,relief=RIDGE,padx=2,bg="white")
               self.fetchframe.place(x=580,y=5,width=250,height=280)

               lbl_name=Label(self.fetchframe,text="Name:",font=("times new roman",12,"bold"),bg="white",fg="red")
               lbl_name.place(x=10,y=28)

               lbl_name=Label(self.fetchframe,text=row,font=("times new roman",12,"bold"),bg="white",fg="red")
               lbl_name.place(x=65,y=28)
#==============================================phone ====================================
            conn=get_connection()
            mycursor=conn.cursor()
            query=("select Phone from addcustomer where Reference_No=%s")
            val=(self.receiptno_var.get(),)
            mycursor.execute(query,val)
            row=mycursor.fetchone()

            lbl_gender=Label(self.fetchframe,text="Phone No:",font=("times new roman",12,"bold"),bg="white",fg="red")
            lbl_gender.place(x=10,y=60)

            lbl1=Label(self.fetchframe,text=row,font=("times new roman",12,"bold"),bg="white",fg="red")
            lbl1.place(x=90,y=60)
#=====================================================================submitted date========================================================
            conn=get_connection()
            mycursor=conn.cursor()
            query=("select Submitted_Date from addcustomer where Reference_No=%s")
            val=(self.receiptno_var.get(),)
            mycursor.execute(query,val)
            row=mycursor.fetchone()

            lbl_gender=Label(self.fetchframe,text="Submit Date:",font=("times new roman",12,"bold"),bg="white",fg="red")
            lbl_gender.place(x=10,y=92)

            lbl1=Label(self.fetchframe,text=row,font=("times new roman",12,"bold"),bg="white",fg="red")
            lbl1.place(x=110,y=92)
        
#=====================================================================type of shirt========================================================
            conn=get_connection()
            mycursor=conn.cursor()
            query=("select Type_Of_Shirt from addcustomer where Reference_No=%s")
            val=(self.receiptno_var.get(),)
            mycursor.execute(query,val)
            row=mycursor.fetchone()

            lbl_gender=Label(self.fetchframe,text="Type of Shirt:",font=("times new roman",12,"bold"),bg="white",fg="red")
            lbl_gender.place(x=10,y=124)

            lbl1=Label(self.fetchframe,text=row,font=("times new roman",12,"bold"),bg="white",fg="red")
            lbl1.place(x=115,y=124)
#=====================================================================shirt quantity========================================================
            conn=get_connection()
            mycursor=conn.cursor()
            query=("select Shirt_Quantity from addcustomer where Reference_No=%s")
            val=(self.receiptno_var.get(),)
            mycursor.execute(query,val)
            row=mycursor.fetchone()

            lbl_gender=Label(self.fetchframe,text="Shirt Quantity:",font=("times new roman",12,"bold"),bg="white",fg="red")
            lbl_gender.place(x=10,y=156)

            lbl1=Label(self.fetchframe,text=row,font=("times new roman",12,"bold"),bg="white",fg="red")
            lbl1.place(x=120,y=156)
#=====================================================================pant quantity========================================================
            conn=get_connection()
            mycursor=conn.cursor()
            query=("select Pant_Quantity from addcustomer where Reference_No=%s")
            val=(self.receiptno_var.get(),)
            mycursor.execute(query,val)
            row=mycursor.fetchone()

            lbl_gender=Label(self.fetchframe,text="Pant Quantity:",font=("times new roman",12,"bold"),bg="white",fg="red")
            lbl_gender.place(x=10,y=188)

            lbl1=Label(self.fetchframe,text=row,font=("times new roman",12,"bold"),bg="white",fg="red")
            lbl1.place(x=120,y=188)

#=====================================================================Advanced Amount========================================================
            conn=get_connection()
            mycursor=conn.cursor()
            query=("select Payment from addcustomer where Reference_No=%s")
            val=(self.receiptno_var.get(),)
            mycursor.execute(query,val)
            row=mycursor.fetchone()

            lbl_gender=Label(self.fetchframe,text="Advance Amount:",font=("times new roman",12,"bold"),bg="white",fg="red")
            lbl_gender.place(x=10,y=220)

            lbl1=Label(self.fetchframe,text=row,font=("times new roman",12,"bold"),bg="white",fg="red")
            lbl1.place(x=140,y=220)



        
        
     

        

     





if __name__=="__main__":
    root=Tk()
    app=bill_win(root)
    root.mainloop()