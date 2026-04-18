import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from PIL import Image
import csv
import subprocess
import sys
import os


# Công cuj điều hướng
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
        self.realtime_id = None  # Biến quản lý vòng lặp chạy ngầm để chống lag

        ctk.set_appearance_mode("light")
        self.title("Trường Đại Học Hạ Long - Cổng thông tin")
        self.geometry("1100x650")  # Mở rộng chiều ngang để chứa đủ 3 cột
        self.configure(fg_color="#f4f4f4")

        self.tao_header()
        self.tao_thanh_dieu_huong()

        self.khung_noi_dung = ctk.CTkFrame(self, fg_color="white", corner_radius=15)
        self.khung_noi_dung.pack(fill="both", expand=True, padx=20, pady=20)

        self.hien_thi_trang_chu()

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

            # Thêm dấu # vào đầu dòng dưới đây để TẮT cái khung màu vàng
            # ToolTip(btn, tooltip_text)

        if self.current_user and self.current_user.strip() != "":
            self.btn_user = ctk.CTkButton(khung_menu, text=f"👤 {self.current_user} ▼",
                                          fg_color="#334a7a", text_color="white",
                                          hover_color="#1e2c4d", font=("Arial", 13, "bold"), corner_radius=15)
            self.btn_user.pack(side="right", padx=20, pady=8)

            self.btn_user.bind("<Enter>", self.hien_thi_dropdown)
            self.btn_user.bind("<Leave>", self.an_dropdown_delay)
        else:
            btn_dang_nhap = ctk.CTkButton(khung_menu, text="Đăng nhập", command=self.mo_file_dang_nhap,
                                          fg_color="#334a7a", text_color="white", hover_color="#1e2c4d",
                                          font=("Arial", 13, "bold"), corner_radius=15)
            btn_dang_nhap.pack(side="right", padx=20, pady=8)

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
            self.dropdown_frame.wm_geometry(f"230x150+{x}+{y}")
            self.dropdown_frame.attributes("-alpha", 0.9)

            khung = ctk.CTkFrame(self.dropdown_frame, fg_color="#1e2c4d", corner_radius=5)
            khung.pack(fill="both", expand=True)

            btn_doi_mk = ctk.CTkButton(khung, text="  Đổi mật khẩu", fg_color="transparent", hover_color="#5c72a6",
                                       command=self.doi_mat_khau, height=35, anchor="w")
            btn_doi_mk.pack(fill="x", pady=(10, 5), padx=5)

            btn_dang_xuat = ctk.CTkButton(khung, text="  Đăng xuất", fg_color="transparent", hover_color="#d9534f",
                                          command=self.dang_xuat, height=35, anchor="w")
            btn_dang_xuat.pack(fill="x", pady=(0, 10), padx=5)

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
        subprocess.Popen([sys.executable, "login.py"])
        self.destroy()

    def doi_mat_khau(self):
        messagebox.showinfo("Đổi mật khẩu", "Tính năng đổi mật khẩu đang cập nhật!")
        self.thuc_su_an_dropdown()

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
        """Xóa trắng nội dung và ngắt vòng lặp chạy ngầm nếu có"""
        if self.realtime_id:
            self.after_cancel(self.realtime_id)
            self.realtime_id = None

        for widget in self.khung_noi_dung.winfo_children():
            widget.destroy()

   #Giao diện chính bao gồm 3 cột thng tin
    def hien_thi_trang_chu(self):
        self.xoa_noi_dung_cu()

        # Thiết lập 3 cột bằng nhau
        self.khung_noi_dung.grid_columnconfigure((0, 1, 2), weight=1, uniform="col")
        self.khung_noi_dung.grid_rowconfigure(1, weight=1)  # Chiều cao tự giãn cho phần list

        # Tiêu đề của 3 cột
        ctk.CTkLabel(self.khung_noi_dung, text="TIN TỨC MỚI NHẤT", font=("Arial", 15, "bold"),
                     text_color="#1a3b5c").grid(row=0, column=0, pady=(15, 5), sticky="w", padx=10)
        ctk.CTkLabel(self.khung_noi_dung, text="THÔNG BÁO", font=("Arial", 15, "bold"), text_color="#1a3b5c").grid(
            row=0, column=1, pady=(15, 5), sticky="w", padx=10)
        ctk.CTkLabel(self.khung_noi_dung, text="VĂN BẢN, BIỂU MẪU", font=("Arial", 15, "bold"),
                     text_color="#1a3b5c").grid(row=0, column=2, pady=(15, 5), sticky="w", padx=10)

        # Cột 1: tin tức
        frame_tintuc = ctk.CTkScrollableFrame(self.khung_noi_dung, fg_color="transparent")
        frame_tintuc.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        danh_sach_tin = ["TB-không sử dụng CC NLNN thi trực tuyến", "Danh sách sinh viên đăng ký nhận bằng",
                         "Đăng ký nhận bằng trên sân khấu đợt 1 năm 2026"]
        for tin in danh_sach_tin:
            btn = ctk.CTkButton(frame_tintuc, text=f"➤ {tin}", fg_color="transparent", text_color="#333",
                                hover_color="#e0e0e0", anchor="w", font=("Arial", 12))
            btn.pack(fill="x", pady=2)

        # Cột 2: Thông báo lấy dữ liệu từ file CSV
        self.frame_thongbao = ctk.CTkScrollableFrame(self.khung_noi_dung, fg_color="#f8f9fa", border_width=1,
                                                     border_color="#dee2e6", corner_radius=5)
        self.frame_thongbao.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)

        # Gọi vòng lặp cập nhật thông báo
        self.cap_nhat_thong_bao_realtime()

        # Cột 3: Văn bản, biểu mẫu
        frame_vanban = ctk.CTkScrollableFrame(self.khung_noi_dung, fg_color="transparent")
        frame_vanban.grid(row=1, column=2, sticky="nsew", padx=5, pady=5)

        ctk.CTkLabel(frame_vanban, text="PHÒNG ĐÀO TẠO", font=("Arial", 13, "bold"), text_color="#8b0000",
                     anchor="w").pack(fill="x", pady=(5, 0))
        ctk.CTkButton(frame_vanban, text="Quy định đào tạo", fg_color="transparent", text_color="#333",
                      hover_color="#e0e0e0", anchor="w").pack(fill="x")
        ctk.CTkButton(frame_vanban, text="Sổ tay sinh viên", fg_color="transparent", text_color="#333",
                      hover_color="#e0e0e0", anchor="w").pack(fill="x")

        ctk.CTkLabel(frame_vanban, text="PHÒNG CÔNG TÁC SINH VIÊN", font=("Arial", 13, "bold"), text_color="#8b0000",
                     anchor="w").pack(fill="x", pady=(15, 0))
        ctk.CTkButton(frame_vanban, text="Quy định", fg_color="transparent", text_color="#333", hover_color="#e0e0e0",
                      anchor="w").pack(fill="x")
        ctk.CTkButton(frame_vanban, text="Biểu mẫu", fg_color="transparent", text_color="#333", hover_color="#e0e0e0",
                      anchor="w").pack(fill="x")

    def cap_nhat_thong_bao_realtime(self):
        """Hàm tự động quét file News.csv - Phiên bản 'Thám tử' chống lỗi tuyệt đối"""
        if not hasattr(self, 'frame_thongbao') or not self.frame_thongbao.winfo_exists():
            return

        thu_muc_hien_tai = os.path.dirname(os.path.abspath(__file__))
        # Dùng os.path.normpath để gộp đường dẫn cho chuẩn đẹp
        duong_dan_file = os.path.normpath(os.path.join(thu_muc_hien_tai, '..', 'database', 'News.csv'))

        # Xóa sạch khung cũ
        for widget in self.frame_thongbao.winfo_children():
            widget.destroy()

        # KIỂM TRA 1: FILE CÓ TỒN TẠI KHÔNG?
        if not os.path.exists(duong_dan_file):
            ctk.CTkLabel(self.frame_thongbao,
                         text=f"❌ MÁY TÍNH BÁO KHÔNG TÌM THẤY FILE!\nNó đang tìm tại đường dẫn này:\n{duong_dan_file}",
                         text_color="red", wraplength=250, font=("Arial", 12, "bold")).pack(pady=20)
        else:
            try:
                with open(duong_dan_file, mode='r', encoding='utf-8-sig') as file:
                    reader = csv.reader(file)
                    danh_sach_tb = [row for row in reader if len(row) > 0 and "".join(row).strip() != ""]

                    # KIỂM TRA 2: FILE CÓ DỮ LIỆU KHÔNG?
                    if len(danh_sach_tb) == 0:
                        ctk.CTkLabel(self.frame_thongbao, text="📭 TÌM THẤY FILE RỒI NHƯNG FILE ĐANG TRỐNG!",
                                     text_color="#856404", font=("Arial", 13, "bold")).pack(pady=30)
                    else:
                        # IN RA DỮ LIỆU (Bao gồm cả trường hợp quên gõ dấu phẩy)
                        for row in reversed(danh_sach_tb):
                            if len(row) >= 2:
                                thoi_gian = row[0].strip()
                                noi_dung = row[1].strip()
                            else:
                                # Nếu quên gõ dấu phẩy, nó vẫn sẽ in ra!
                                thoi_gian = "Mới nhất"
                                noi_dung = row[0].strip()

                            card = ctk.CTkFrame(self.frame_thongbao, fg_color="white", corner_radius=8, border_width=1,
                                                border_color="#e0e0e0")
                            card.pack(fill="x", pady=5, padx=5)

                            lbl_nd = ctk.CTkLabel(card, text=noi_dung, font=("Arial", 13, "bold"), text_color="#2b579a",
                                                  justify="left", wraplength=250)
                            lbl_nd.pack(anchor="w", padx=10, pady=(10, 0))

                            lbl_tg = ctk.CTkLabel(card, text=f"🕒 {thoi_gian}", font=("Arial", 11), text_color="gray")
                            lbl_tg.pack(anchor="e", padx=10, pady=(0, 10))

            except Exception as e:
                ctk.CTkLabel(self.frame_thongbao, text=f"❌ FILE BỊ LỖI ĐỊNH DẠNG:\n{e}", text_color="red",
                             wraplength=250).pack(pady=20)

        # Lặp lại chu kỳ cập nhật mỗi 3 giây
        self.realtime_id = self.after(3000, self.cap_nhat_thong_bao_realtime)

    # Các module khác
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
