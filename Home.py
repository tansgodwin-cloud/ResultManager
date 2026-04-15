import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
# --- CÁC HÀM XỬ LÝ KHI BẤM NÚT ---
def unfinished():
    messagebox.showinfo("Thông báo", "Chức năng này đang được viết, hãy đợi nhé!")

def logout():
    cua_so.destroy()
    #gọi file login
    ten_file = "login.py"
    subprocess.Popen([sys.executable, ten_file])

# Tạo trang chủ
cua_so = tk.Tk()
cua_so.title("Trang Chủ - Quản lý sinh viên")
cua_so.geometry("400x300")

tk.Label(cua_so, text="Chào mừng bạn đã đăng nhập thành công!", font=("Arial", 14)).pack(pady=20)
tk.Button(cua_so, text="Xem Điểm Sinh Viên", command=unfinished).pack(pady=10)

# Nút này sẽ gọi hàm dang_xuat ở trên
tk.Button(cua_so, text="Đăng Xuất", fg="black", command=logout).pack(pady=20)

cua_so.mainloop()