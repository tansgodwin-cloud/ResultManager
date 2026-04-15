import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk  # Import thư viện giao diện hiện đại
import subprocess
import sys
import csv
import os

# CÀI ĐẶT GIAO DIỆN MẶC ĐỊNH
ctk.set_appearance_mode("System")  # Chế độ Sáng/Tối theo hệ thống (Light/Dark)
ctk.set_default_color_theme("blue") # Theme màu chủ đạo

#hàm mở database
def kiem_tra_tren_csv(tai_khoan_nhap, mat_khau_nhap):
    """Mở file CSV, kiểm tra tài khoản và TRẢ VỀ VAI TRÒ của tài khoản đó."""
    ten_file = '../database/tai_khoan_cua_toi.csv'

    if not os.path.isfile(ten_file):
        return None  # Trả về None nếu không thấy file

    with open(ten_file, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader, None)

        for row in reader:
            if len(row) >= 3:
                if tai_khoan_nhap == row[0] and mat_khau_nhap == row[1]:
                    return row[2]
    return None
#HÀM chỉnh sửa login
def login():
    tk_hien_tai = entry_username.get()
    mk_hien_tai = entry_password.get()
    vai_tro_chon = role_var.get()

    vai_tro_thuc_te = kiem_tra_tren_csv(tk_hien_tai, mk_hien_tai)

    if vai_tro_thuc_te:
        if vai_tro_chon == "Admin":
            if vai_tro_thuc_te == "Admin":
                messagebox.showinfo("Thành công", "Đăng nhập quyền Quản lý thành công!")
                open_quan_ly()
            else:
                messagebox.showerror("Từ chối truy cập", "Tài khoản của bạn chỉ là Người dùng bình thường!")
        else:
            messagebox.showinfo("Thành công", "Đăng nhập thành công!")
            open_home()
    else:
        messagebox.showerror("Lỗi", "Sai tài khoản hoặc mật khẩu!")

def tao_tk():
    root.destroy()

def open_home():
    root.destroy()
    subprocess.Popen([sys.executable, "Home.py"])

def open_quan_ly():
    root.destroy()
    subprocess.Popen([sys.executable, "AccManage.py"])

def back_create(event=None):
    root.destroy()
    subprocess.Popen([sys.executable, "taotk.py"])

root = ctk.CTk() # Dùng CTk thay vì tk.Tk()
root.title("Đăng nhập hệ thống")
# Tăng kích thước cửa sổ lên một chút vì các nút hiện đại thường to hơn
root.geometry("400x380")

# Tiêu đề chính
lbl_login = ctk.CTkLabel(root, text="Đăng nhập", font=("Arial", 24, "bold"))
lbl_login.place(x=130, y=20)

# Ô nhập Tài khoản
user_name = ctk.CTkLabel(root, text="Username: ", font=("Arial", 13))
user_name.place(x=30, y=80)
# Thêm corner_radius để bo tròn ô nhập liệu
entry_username = ctk.CTkEntry(root, width=220, height=35, corner_radius=10)
entry_username.place(x=100, y=80)

# Ô nhập Mật khẩu
password = ctk.CTkLabel(root, text="Password: ", font=("Arial", 13))
password.place(x=30, y=130)
entry_password = ctk.CTkEntry(root, show="*", width=220, height=35, corner_radius=10)
entry_password.place(x=100, y=130)

# Chọn Vai trò
tk_role_lbl = ctk.CTkLabel(root, text="Vai trò:", font=("Arial", 13))
tk_role_lbl.place(x=30, y=178)

role_var = ctk.StringVar(value="User") # Dùng StringVar của ctk
radio_user = ctk.CTkRadioButton(root, text="Người dùng", variable=role_var, value="User")
radio_user.place(x=100, y=180)

radio_admin = ctk.CTkRadioButton(root, text="Quản lý", variable=role_var, value="Admin")
radio_admin.place(x=245, y=180)

# NÚT ĐĂNG NHẬP BO TRÒN
btn = ctk.CTkButton(
    root,
    text="Log In",
    command=login,
    width=220,
    height=40,
    corner_radius=20, # Bo tròn dạng viên thuốc
    font=("Arial", 15, "bold")
)
btn.place(x=90, y=240)

# Nút chuyển sang Đăng ký
sign_up = ctk.CTkLabel(
    root,
    text="Chưa có tài khoản? Đăng Ký ngay",
    text_color="#007bff",
    cursor="hand2",
    font=("Arial", 13, "underline")
)
sign_up.place(x=100, y=300)
# Ràng buộc sự kiện click chuột
sign_up.bind("<Button-1>", back_create)

root.mainloop()