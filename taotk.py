import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import subprocess
import sys
import csv
import os

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

def kiem_tra_ton_tai(tai_khoan_moi):
    ten_file = '../database/tai_khoan_cua_toi.csv'

    if not os.path.isfile(ten_file):
        return False

    with open(ten_file, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader, None)
        for row in reader:
            if len(row) >= 1:
                if tai_khoan_moi == row[0]:
                    return True
    return False

def luu_tai_khoan(tai_khoan, mat_khau):
    ten_file = '../database/tai_khoan_cua_toi.csv'
    file_da_ton_tai = os.path.isfile(ten_file)
    with open(ten_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        if not file_da_ton_tai:
            writer.writerow(['Tên đăng nhập', 'Mật khẩu', 'Vai trò'])
        writer.writerow([tai_khoan, mat_khau, 'User'])

def xu_ly_dang_ky():
    u = user_name.get()
    p = password.get()
    c = confirm.get()

    if u == "" or p == "" or c == "":
        messagebox.showwarning("Thông báo", "Vui lòng điền đầy đủ thông tin!")
        return

    if p != c:
        messagebox.showerror("Lỗi", "Mật khẩu xác nhận không khớp!")
        return

    if kiem_tra_ton_tai(u):
        messagebox.showerror("Lỗi", f"Tên đăng nhập '{u}' đã tồn tại!\nVui lòng chọn tên khác.")
        return

    luu_tai_khoan(u, p)

    messagebox.showinfo("Thành công", f"Tạo tài khoản thành công!\nVui lòng đăng nhập để tiếp tục.")
    quay_lai_dang_nhap()

def quay_lai_dang_nhap(event=None):
    root.destroy()
    subprocess.Popen([sys.executable, "login.py"])

root = ctk.CTk()
root.title("Hệ thống - Tạo tài khoản")
root.geometry("450x500")

frame = ctk.CTkFrame(master=root, width=350, height=420, corner_radius=15)
frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

lbl_register = ctk.CTkLabel(master=frame, text="ĐĂNG KÝ", font=("Arial", 24, "bold"))
lbl_register.place(x=120, y=30)

user_name = ctk.CTkEntry(master=frame, placeholder_text="Tên đăng nhập", width=250, height=40, corner_radius=10)
user_name.place(x=50, y=90)

password = ctk.CTkEntry(master=frame, placeholder_text="Mật khẩu", show="*", width=250, height=40, corner_radius=10)
password.place(x=50, y=150)

confirm = ctk.CTkEntry(master=frame, placeholder_text="Xác nhận mật khẩu", show="*", width=250, height=40, corner_radius=10)
confirm.place(x=50, y=210)

create_acc = ctk.CTkButton(master=frame, text="TẠO TÀI KHOẢN", command=xu_ly_dang_ky, width=250, height=40, corner_radius=10, fg_color="#2FA572", hover_color="#107C41", font=("Arial", 15, "bold"))
create_acc.place(x=50, y=280)

back_btn = ctk.CTkLabel(master=frame, text="Đã có tài khoản? Đăng nhập ngay", text_color="#007bff", cursor="hand2", font=("Arial", 12, "underline"))
back_btn.place(x=75, y=340)
back_btn.bind("<Button-1>", quay_lai_dang_nhap)

root.mainloop()