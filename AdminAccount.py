import tkinter as tk
from tkinter import messagebox
import csv
import os


# PHẦN XỬ LÝ DỮ LIỆU CHO ADMIN
def kiem_tra_ton_tai(tai_khoan_moi):
    # Lưu vào một file CSV hoàn toàn mới, tách biệt với user
    ten_file = '../database/admin_accounts.csv'

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


def luu_tai_khoan_admin(tai_khoan, mat_khau):
    ten_file = '../database/admin_accounts.csv'
    file_da_ton_tai = os.path.isfile(ten_file)

    with open(ten_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_da_ton_tai:
            writer.writerow(['Tài khoản Admin', 'Mật khẩu'])
        writer.writerow([tai_khoan, mat_khau])


# PHẦN XỬ LÝ GIAO DIỆN
def xu_ly_tao_admin():
    u = user_name.get()
    p = password.get()
    c = confirm.get()
    ma_bi_mat = secret_code.get()

    # Thêm một lớp bảo mật: Yêu cầu mã bí mật mới được tạo Admin
    if ma_bi_mat != "123456":
        messagebox.showerror("Cảnh báo bảo mật", "Mã cấp quyền không hợp lệ!")
        return

    if u == "" or p == "" or c == "":
        messagebox.showwarning("Thông báo", "Vui lòng điền đầy đủ thông tin!")
        return

    if p != c:
        messagebox.showerror("Lỗi", "Mật khẩu xác nhận không khớp!")
        return

    if kiem_tra_ton_tai(u):
        messagebox.showerror("Lỗi", f"Tài khoản Admin '{u}' đã tồn tại!")
        return

    luu_tai_khoan_admin(u, p)
    messagebox.showinfo("Thành công", f"Đã cấp quyền Quản trị cho '{u}'!\nVui lòng đóng cửa sổ này.")
    lam_moi_form()


def lam_moi_form():
    user_name.delete(0, tk.END)
    password.delete(0, tk.END)
    confirm.delete(0, tk.END)
    secret_code.delete(0, tk.END)


# THIẾT KẾ GIAO DIỆN (Tông màu Admin)
root = tk.Tk()
root.title("Công cụ Cấp quyền Quản trị")
root.geometry("380x450")
# Đổi màu nền để phân biệt với giao diện User
root.configure(bg="#2c3e50")

tk.Label(root, text="TẠO TÀI KHOẢN ADMIN", font=("Arial", 16, "bold"), fg="white", bg="#2c3e50").pack(pady=20)

# Ô nhập Mã bảo mật
tk.Label(root, text="Mã cấp quyền (Secret Code):", font=("Arial", 10), fg="#ecf0f1", bg="#2c3e50").pack(anchor="w",
                                                                                                        padx=40)
secret_code = tk.Entry(root, font=("Arial", 12), show="*")
secret_code.pack(fill="x", padx=40, pady=(0, 10))

# Ô nhập Tên đăng nhập
tk.Label(root, text="Tên đăng nhập Admin:", font=("Arial", 10), fg="#ecf0f1", bg="#2c3e50").pack(anchor="w", padx=40)
user_name = tk.Entry(root, font=("Arial", 12))
user_name.pack(fill="x", padx=40, pady=(0, 10))

# Ô nhập Mật khẩu
tk.Label(root, text="Mật khẩu:", font=("Arial", 10), fg="#ecf0f1", bg="#2c3e50").pack(anchor="w", padx=40)
password = tk.Entry(root, font=("Arial", 12), show="*")
password.pack(fill="x", padx=40, pady=(0, 10))

# Ô nhập Xác nhận mật khẩu
tk.Label(root, text="Xác nhận mật khẩu:", font=("Arial", 10), fg="#ecf0f1", bg="#2c3e50").pack(anchor="w", padx=40)
confirm = tk.Entry(root, font=("Arial", 12), show="*")
confirm.pack(fill="x", padx=40, pady=(0, 20))

# Nút Tạo tài khoản
create_acc = tk.Button(root, text="CẤP QUYỀN ADMIN", bg="#e74c3c", fg="white", font=("Arial", 10, "bold"),
                       command=xu_ly_tao_admin)
create_acc.pack(pady=15)

root.mainloop()