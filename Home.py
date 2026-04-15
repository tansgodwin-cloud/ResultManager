import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from PIL import Image
import csv
import subprocess
import sys

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5
        self.tooltip_window = tk.Toplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)
        self.tooltip_window.wm_geometry(f"+{x}+{y}")

        label = tk.Label(self.tooltip_window, text=self.text, justify="left",
                         background="#ffffe0", relief="solid", borderwidth=1, font=("Arial", 10))
        label.pack(ipadx=5, ipady=3)

    def hide_tooltip(self, event=None):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None


# giao diện chính
class AppHome(ctk.CTk):
    def __init__(self, current_user=None):
        super().__init__()

        self.current_user = current_user
        self.dropdown_frame = None
        self.hide_id = None

        ctk.set_appearance_mode("light")
        self.title("Trường Đại Học Hạ Long - Hệ thống Quản lý")
        self.geometry("1000x600")
        self.configure(fg_color="#f4f4f4")

        self.thong_tin_csv = []
        self.doc_file_csv()

        self.tao_header()
        self.tao_thanh_dieu_huong()

        self.khung_noi_dung = ctk.CTkFrame(self, fg_color="white", corner_radius=15)
        self.khung_noi_dung.pack(fill="both", expand=True, padx=20, pady=20)

        self.hien_thi_trang_chu()

    def doc_file_csv(self):
        try:
            with open('tk.csv', mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                for row in reader:
                    self.thong_tin_csv.append(row)
        except FileNotFoundError:
            pass

    def tao_header(self):
        khung_header = ctk.CTkFrame(self, fg_color="white", corner_radius=0, cursor="hand2")
        khung_header.pack(fill="x")
        khung_header.bind("<Button-1>", lambda e: self.hien_thi_trang_chu())

        try:
            img_data = Image.open("logo.png")
            self.logo_img = ctk.CTkImage(light_image=img_data, dark_image=img_data, size=(80, 80))
            lbl_logo = ctk.CTkLabel(khung_header, image=self.logo_img, text="")
            lbl_logo.pack(side="left", padx=20, pady=10)
            lbl_logo.bind("<Button-1>", lambda e: self.hien_thi_trang_chu())
        except:
            lbl_logo = ctk.CTkLabel(khung_header, text="[LOGO]", font=("Arial", 20, "bold"), text_color="#42649b")
            lbl_logo.pack(side="left", padx=20, pady=10)

        lbl_ten_truong = ctk.CTkLabel(khung_header, text="TRƯỜNG ĐẠI HỌC HẠ LONG\nHọc Để Thành Công",
                                      font=("Arial", 18, "bold"), text_color="#42649b", justify="left")
        lbl_ten_truong.pack(side="left", pady=10)
        lbl_ten_truong.bind("<Button-1>", lambda e: self.hien_thi_trang_chu())

    def tao_thanh_dieu_huong(self):
        khung_menu = ctk.CTkFrame(self, fg_color="#5c72a6", corner_radius=0)
        khung_menu.pack(fill="x")

        danh_sach_nut = [
            ("Trang chủ", self.hien_thi_trang_chu, "Quay về màn hình chính"),
            ("Đăng kí", self.mo_file_dang_ki, "Tạo tài khoản mới (Chuyển trang)"),
            ("Thông tin cá nhân", self.hien_thi_thong_tin, "Xem hồ sơ sinh viên"),
            ("Đánh giá", self.hien_thi_danh_gia, "Hệ thống đánh giá rèn luyện"),
            ("Dịch vụ liên hệ", self.hien_thi_dich_vu, "Hỗ trợ & Liên hệ")
        ]

        for text, command, tooltip_text in danh_sach_nut:
            btn = ctk.CTkButton(khung_menu, text=text, command=command,
                                fg_color="transparent", text_color="white",
                                hover_color="#425585", font=("Arial", 13, "bold"), corner_radius=8)
            btn.pack(side="left", padx=10, pady=8)
            ToolTip(btn, tooltip_text)

        # nút đăng nhập tài khoản
        if self.current_user and self.current_user.strip() != "":
            # Chỉ hiển thị Tên người dùng trên thanh điều hướng
            self.btn_user = ctk.CTkButton(khung_menu, text=f"👤 {self.current_user} ▼",
                                          fg_color="#334a7a", text_color="white",
                                          hover_color="#1e2c4d", font=("Arial", 13, "bold"), corner_radius=15)
            self.btn_user.pack(side="right", padx=20, pady=8)

            # Ràng buộc sự kiện để mở Dropdown (chứa Đăng xuất & Đổi MK)
            self.btn_user.bind("<Enter>", self.hien_thi_dropdown)
            self.btn_user.bind("<Leave>", self.an_dropdown_delay)
        else:
            btn_dang_nhap = ctk.CTkButton(khung_menu, text="Đăng nhập", command=self.mo_file_dang_nhap,
                                          fg_color="#334a7a", text_color="white", hover_color="#1e2c4d",
                                          font=("Arial", 13, "bold"), corner_radius=15)
            btn_dang_nhap.pack(side="right", padx=20, pady=8)
            ToolTip(btn_dang_nhap, "Đăng nhập vào hệ thống")

    # dropdown menu chứa đăng nhập và đăng xuất
    def hien_thi_dropdown(self, event=None):
        if self.hide_id:
            self.after_cancel(self.hide_id)
            self.hide_id = None

        if self.dropdown_frame is None:
            self.update_idletasks()
            x = self.btn_user.winfo_rootx()
            y = self.btn_user.winfo_rooty() + self.btn_user.winfo_height()

            self.dropdown_frame = tk.Toplevel(self)
            self.dropdown_frame.wm_overrideredirect(True)
            self.dropdown_frame.wm_geometry(f"200x150+{x}+{y}")
            self.dropdown_frame.attributes("-alpha", 0.9)

            khung = ctk.CTkFrame(self.dropdown_frame, fg_color="#1e2c4d", corner_radius=5)
            khung.pack(fill="both", expand=True)

            # Nút 1: Đổi mật khẩu
            btn_doi_mk = ctk.CTkButton(khung, text="  Đổi mật khẩu", fg_color="transparent", hover_color="#5c72a6",
                                       command=self.doi_mat_khau, height=35, anchor="w")
            btn_doi_mk.pack(fill="x", pady=(8, 0), padx=5)

            # Nút 2: Đăng xuất
            btn_dang_xuat = ctk.CTkButton(khung, text="  Đăng xuất", fg_color="transparent", hover_color="#d9534f",
                                          command=self.dang_xuat, height=35, anchor="w")
            btn_dang_xuat.pack(fill="x", pady=(5, 8), padx=5)

            self.dropdown_frame.bind("<Enter>", self.vao_dropdown)
            self.dropdown_frame.bind("<Leave>", self.an_dropdown_delay)

    def vao_dropdown(self, event=None):
        if self.hide_id:
            self.after_cancel(self.hide_id)
            self.hide_id = None

    def an_dropdown_delay(self, event=None):
        self.hide_id = self.after(500, self.thuc_su_an_dropdown)

    def thuc_su_an_dropdown(self):
        if self.dropdown_frame:
            self.dropdown_frame.destroy()
            self.dropdown_frame = None

    def dang_xuat(self):
        # Mở lại trang login.py khi bấm đăng xuất
        subprocess.Popen([sys.executable, "login.py"])
        self.destroy()

    def doi_mat_khau(self):
        messagebox.showinfo("Đổi mật khẩu", "Tính năng đổi mật khẩu đang cập nhật!")
        self.thuc_su_an_dropdown()

    # Điều hướng module
    def mo_file_dang_ki(self):
        try:
            subprocess.Popen([sys.executable, "taotk.py"])
            self.destroy()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không mở được taotk.py: {e}")

    def mo_file_dang_nhap(self):
        try:
            subprocess.Popen([sys.executable, "login.py"])
            self.destroy()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không mở được login.py: {e}")

    def xoa_noi_dung_cu(self):
        for widget in self.khung_noi_dung.winfo_children():
            widget.destroy()

    def hien_thi_trang_chu(self):
        self.xoa_noi_dung_cu()
        ctk.CTkLabel(self.khung_noi_dung, text="CHÀO MỪNG ĐẾN VỚI TRANG CHỦ", font=("Arial", 22, "bold"),
                     text_color="#42649b").pack(pady=30)

        if self.thong_tin_csv:
            noi_dung_csv = "Dữ liệu từ tk.csv:\n\n"
            for row in self.thong_tin_csv:
                noi_dung_csv += " | ".join(row) + "\n"
            ctk.CTkLabel(self.khung_noi_dung, text=noi_dung_csv, font=("Arial", 14), justify="left").pack(pady=10)

    def hien_thi_thong_tin(self):
        self.xoa_noi_dung_cu()
        ctk.CTkLabel(self.khung_noi_dung, text="MODULE THÔNG TIN CÁ NHÂN", font=("Arial", 22, "bold")).pack(pady=30)

    def hien_thi_danh_gia(self):
        self.xoa_noi_dung_cu()
        ctk.CTkLabel(self.khung_noi_dung, text="MODULE ĐÁNH GIÁ", font=("Arial", 22, "bold")).pack(pady=30)

    def hien_thi_dich_vu(self):
        self.xoa_noi_dung_cu()
        ctk.CTkLabel(self.khung_noi_dung, text="MODULE DỊCH VỤ LIÊN HỆ", font=("Arial", 22, "bold")).pack(pady=30)


if __name__ == "__main__":
    nguoi_dung_hien_tai = sys.argv[1] if len(sys.argv) > 1 else None
    app = AppHome(current_user=nguoi_dung_hien_tai)
    app.mainloop()
