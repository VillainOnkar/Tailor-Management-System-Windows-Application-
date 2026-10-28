from tkinter import *
from tkinter import ttk, messagebox
import mysql.connector
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

class ProductControl:
    def __init__(self, root):
        self.root = root
        self.root.title("Product Price Control")
        self.root.geometry("500x350+600+300")
        self.root.config(bg="#0e0e0e")

        # ---------- Variables ----------
        self.product_var = StringVar()
        self.price_var = StringVar()

        # ---------- Title ----------
        title = Label(self.root, text="PRODUCT PRICE CONTROL",
                      font=("times new roman", 18, "bold"),
                      fg="gold", bg="#0e0e0e")
        title.pack(pady=20)

        # ---------- Product Name ----------
        lbl_name = Label(self.root, text="Product Name :",
                         font=("times new roman", 14), bg="#0e0e0e", fg="white")
        lbl_name.place(x=60, y=100)

        self.txt_name = Entry(self.root, textvariable=self.product_var,
                              font=("times new roman", 13),
                              bg="#1c1c1c", fg="gold", relief=FLAT, width=25)
        self.txt_name.place(x=220, y=100)

        # ---------- Product Price ----------
        lbl_price = Label(self.root, text="Product Price :",
                          font=("times new roman", 14), bg="#0e0e0e", fg="white")
        lbl_price.place(x=60, y=150)

        self.txt_price = Entry(self.root, textvariable=self.price_var,
                               font=("times new roman", 13),
                               bg="#1c1c1c", fg="gold", relief=FLAT, width=25)
        self.txt_price.place(x=220, y=150)

        # ---------- Buttons ----------
        style = ttk.Style()
        style.configure("Gold.TButton", font=("times new roman", 12, "bold"),
                        foreground="black", background="gold")

        btn_add = ttk.Button(self.root, text="ADD PRODUCT", style="Gold.TButton", command=self.add_product,cursor="hand2")
        btn_add.place(x=40, y=230, width=130, height=35)

        btn_update = ttk.Button(self.root, text="UPDATE PRICE", style="Gold.TButton", command=self.update_price,cursor="hand2")
        btn_update.place(x=185, y=230, width=130, height=35)

        btn_delete = ttk.Button(self.root, text="DELETE PRODUCT", style="Gold.TButton", command=self.delete_product,cursor="hand2")
        btn_delete.place(x=330, y=230, width=155, height=35)

        btn_reset = ttk.Button(self.root, text="RESET", style="Gold.TButton", command=self.reset_fields,cursor="hand2")
        btn_reset.place(x=200, y=280, width=100, height=35)

    # ---------- Add Product ----------
    def add_product(self):
        if self.product_var.get() == "" or self.price_var.get() == "":
            messagebox.showerror("Error", "All fields are required", parent=self.root)
            return

        conn = get_connection()
        mycursor = conn.cursor()
        mycursor.execute("INSERT INTO products (product_name, price) VALUES (%s, %s)",
                         (self.product_var.get(), self.price_var.get()))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Product added successfully!", parent=self.root)
        self.reset_fields()

    # ---------- Update Price ----------
    def update_price(self):
        if self.product_var.get() == "" or self.price_var.get() == "":
            messagebox.showerror("Error", "Both fields required", parent=self.root)
            return

        conn = get_connection()
        mycursor = conn.cursor()
        mycursor.execute("UPDATE products SET price=%s WHERE product_name=%s",
                         (self.price_var.get(), self.product_var.get()))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Price updated successfully!", parent=self.root)
        self.reset_fields()

    # ---------- Delete Product ----------
    def delete_product(self):
        if self.product_var.get() == "":
            messagebox.showerror("Error", "Enter product name to delete", parent=self.root)
            return

        confirm = messagebox.askyesno("Confirm", "Are you sure to delete this product?", parent=self.root)
        if confirm:
            conn = get_connection()
            mycursor = conn.cursor()
            mycursor.execute("DELETE FROM products WHERE product_name=%s", (self.product_var.get(),))
            conn.commit()
            conn.close()
            messagebox.showinfo("Deleted", "Product deleted successfully!", parent=self.root)
            self.reset_fields()

    # ---------- Reset ----------
    def reset_fields(self):
        self.product_var.set("")
        self.price_var.set("")


# ---------- Run ----------
if __name__ == "__main__":
    root = Tk()
    obj = ProductControl(root)
    root.mainloop()
