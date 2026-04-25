import customtkinter as ctk
from tkinter import messagebox
import csv
import os


class AdminFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#18181b")
        self.controller = controller
        self.current_admin = None

        self.user_dang_chon = ctk.StringVar(value="")

        self.dung_giao_dien()

    def load_data_va_giao_dien(self, username):
        self.current_admin = username
        self.user_dang_chon.set("")
        self.dung_giao_dien()

    def dung_giao_dien(self):
        for widget in self.winfo_children():
            widget.destroy()

        # --- HEADER ---
        khung_header = ctk.CTkFrame(self, fg_color="#27272a", corner_radius=0)
        khung_header.pack(fill="x", pady=(0, 10))

        ten_sep = self.current_admin if self.current_admin else "Ẩn danh"
        ctk.CTkLabel(khung_header, text=f"QUẢN LÝ TÀI KHOẢN - QUẢN TRỊ VIÊN: {ten_sep.upper()}",
                     font=("Arial", 20, "bold"), text_color="#ef4444").pack(side="left", padx=20, pady=15)

        btn_logout = ctk.CTkButton(khung_header, text="Đăng xuất", fg_color="#374151", hover_color="#1f2937",
                                   width=100, command=self.dang_xuat)
        btn_logout.pack(side="right", padx=20, pady=15)

        # --- CHIA 2 CỘT ---
        khung_chinh = ctk.CTkFrame(self, fg_color="transparent")
        khung_chinh.pack(fill="both", expand=True, padx=20, pady=10)

        # CỘT TRÁI: DANH SÁCH
        khung_trai = ctk.CTkFrame(khung_chinh, fg_color="#27272a", corner_radius=10)
        khung_trai.pack(side="left", fill="both", expand=True, padx=(0, 10))

        ctk.CTkLabel(khung_trai, text="DANH SÁCH NGƯỜI DÙNG", font=("Arial", 16, "bold"), text_color="#60a5fa").pack(
            pady=10)

        khung_head_bang = ctk.CTkFrame(khung_trai, fg_color="#1f2937", corner_radius=5)
        khung_head_bang.pack(fill="x", padx=10, pady=(0, 5))
        ctk.CTkLabel(khung_head_bang, text="Tài Khoản", width=120, font=("Arial", 13, "bold"),
                     text_color="#d1d5db").pack(side="left", padx=5)
        ctk.CTkLabel(khung_head_bang, text="Vai Trò", width=80, font=("Arial", 13, "bold"), text_color="#d1d5db").pack(
            side="left", padx=5)
        ctk.CTkLabel(khung_head_bang, text="Thao Tác", width=80, font=("Arial", 13, "bold"), text_color="#d1d5db").pack(
            side="right", padx=15)

        self.bang_danh_sach = ctk.CTkScrollableFrame(khung_trai, fg_color="#18181b")
        self.bang_danh_sach.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # CỘT PHẢI: ĐIỀU KHIỂN
        khung_phai = ctk.CTkFrame(khung_chinh, fg_color="#27272a", corner_radius=10, width=250)
        khung_phai.pack(side="right", fill="y")
        khung_phai.pack_propagate(False)

        ctk.CTkLabel(khung_phai, text="THAO TÁC", font=("Arial", 16, "bold"), text_color="#10b981").pack(pady=10)

        ctk.CTkLabel(khung_phai, text="Tài khoản đang chọn:", font=("Arial", 13), text_color="#9ca3af").pack(
            pady=(10, 0))
        lbl_muc_tieu = ctk.CTkLabel(khung_phai, textvariable=self.user_dang_chon, font=("Arial", 18, "bold"),
                                    text_color="#f59e0b")
        lbl_muc_tieu.pack(pady=(0, 20))

        btn_len_admin = ctk.CTkButton(khung_phai, text="Cấp quyền Admin", fg_color="#3b82f6", hover_color="#2563eb",
                                      font=("Arial", 14, "bold"), command=lambda: self.thay_doi_quyen("Admin"))
        btn_len_admin.pack(fill="x", padx=20, pady=10)

        btn_xuong_user = ctk.CTkButton(khung_phai, text="Chuyển thành User", fg_color="#f59e0b", hover_color="#d97706",
                                       font=("Arial", 14, "bold"), command=lambda: self.thay_doi_quyen("User"))
        btn_xuong_user.pack(fill="x", padx=20, pady=10)

        btn_xoa = ctk.CTkButton(khung_phai, text="Xóa tài khoản", fg_color="#ef4444", hover_color="#dc2626",
                                font=("Arial", 14, "bold"), command=self.xoa_tai_khoan)
        btn_xoa.pack(fill="x", padx=20, pady=40)

        self.load_danh_sach_tu_csv()

    # --- LOGIC ĐỌC DANH SÁCH ---
    def load_danh_sach_tu_csv(self):
        for widget in self.bang_danh_sach.winfo_children():
            widget.destroy()

        duong_dan_csv = self.lay_duong_dan()
        if not os.path.exists(duong_dan_csv):
            ctk.CTkLabel(self.bang_danh_sach, text="Hệ thống chưa có người dùng nào.", text_color="#9ca3af").pack(
                pady=20)
            return

        try:
            with open(duong_dan_csv, mode='r', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader, None)
                for row in reader:
                    if len(row) >= 3:
                        user = row[0].strip()
                        role = row[2].strip()

                        dong = ctk.CTkFrame(self.bang_danh_sach, fg_color="#27272a", corner_radius=5)
                        dong.pack(fill="x", pady=2)

                        ctk.CTkLabel(dong, text=user, width=120, anchor="w", text_color="white").pack(side="left",
                                                                                                      padx=10)

                        color_role = "#ef4444" if role == "Admin" else "#10b981"
                        ctk.CTkLabel(dong, text=role, width=80, text_color=color_role, font=("Arial", 12, "bold")).pack(
                            side="left", padx=5)

                        btn_chon = ctk.CTkButton(dong, text="Chọn", width=60, height=24, fg_color="#4b5563",
                                                 hover_color="#374151",
                                                 command=lambda u=user: self.user_dang_chon.set(u))
                        btn_chon.pack(side="right", padx=10, pady=5)
        except Exception as e:
            ctk.CTkLabel(self.bang_danh_sach, text=f"Lỗi đọc dữ liệu: {e}", text_color="red").pack()

    # --- LOGIC XỬ LÝ DATABASE ---
    def lay_duong_dan(self):
        thu_muc_hien_tai = os.path.dirname(os.path.abspath(__file__))
        return os.path.normpath(os.path.join(thu_muc_hien_tai, "..", "database", "account.csv"))

    def thay_doi_quyen(self, quyen_moi):
        muc_tieu = self.user_dang_chon.get()
        if not muc_tieu:
            messagebox.showwarning("Nhắc nhở", "Vui lòng chọn một tài khoản từ danh sách để thao tác!")
            return

        if muc_tieu == self.current_admin:
            messagebox.showerror("Từ chối thao tác", "Bạn không thể tự thay đổi quyền của chính mình!")
            return

        duong_dan = self.lay_duong_dan()
        du_lieu = []
        thanh_cong = False
        try:
            with open(duong_dan, "r", encoding="utf-8") as f:
                for row in csv.reader(f):
                    if len(row) >= 3 and row[0] == muc_tieu:
                        if row[2] == quyen_moi:
                            messagebox.showinfo("Thông báo",
                                                f"Tài khoản '{muc_tieu}' hiện tại đã có quyền {quyen_moi}.")
                            return
                        row[2] = quyen_moi
                        thanh_cong = True
                    du_lieu.append(row)

            if thanh_cong:
                with open(duong_dan, "w", newline="", encoding="utf-8") as f:
                    csv.writer(f).writerows(du_lieu)
                messagebox.showinfo("Thành công", f"Đã cập nhật quyền {quyen_moi} cho tài khoản '{muc_tieu}'.")
                self.load_danh_sach_tu_csv()
        except Exception as e:
            messagebox.showerror("Lỗi cơ sở dữ liệu", f"Không thể cập nhật dữ liệu: {e}")

    def xoa_tai_khoan(self):
        muc_tieu = self.user_dang_chon.get()
        if not muc_tieu:
            messagebox.showwarning("Nhắc nhở", "Vui lòng chọn tài khoản cần xóa!")
            return

        if muc_tieu == self.current_admin:
            messagebox.showerror("Từ chối thao tác", "Bạn không thể tự xóa tài khoản của chính mình!")
            return

        xac_nhan = messagebox.askyesno("Xác nhận xóa",
                                       f"Bạn có chắc chắn muốn xóa vĩnh viễn tài khoản '{muc_tieu}' không?\nThao tác này không thể hoàn tác.")
        if not xac_nhan: return

        duong_dan = self.lay_duong_dan()
        du_lieu = []
        try:
            with open(duong_dan, "r", encoding="utf-8") as f:
                for row in csv.reader(f):
                    if len(row) > 0 and row[0] != muc_tieu:
                        du_lieu.append(row)

            with open(duong_dan, "w", newline="", encoding="utf-8") as f:
                csv.writer(f).writerows(du_lieu)

            messagebox.showinfo("Thành công", f"Đã xóa tài khoản '{muc_tieu}' khỏi hệ thống.")
            self.user_dang_chon.set("")
            self.load_danh_sach_tu_csv()
        except Exception as e:
            messagebox.showerror("Lỗi cơ sở dữ liệu", f"Không thể xóa dữ liệu: {e}")

    def dang_xuat(self):
        self.current_admin = None
        self.user_dang_chon.set("")
        self.controller.show_frame("LoginFrame")import tkinter as tk
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
