import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image
import csv
import os


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
                         background="#27272a", fg="white", relief="solid", borderwidth=1, font=("Arial", 10))
        label.pack(ipadx=5, ipady=3)

    def hide_tooltip(self, event=None):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None


class HomeFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#18181b")
        self.controller = controller

        self.current_user = None
        self.dropdown_frame = None
        self.hide_id = None

        # Cảm biến Realtime cho các file CSV
        self.news_realtime_id = None
        self.grades_realtime_id = None
        self.thoi_gian_sua_file_diem_cu = 0
        self.thoi_gian_sua_news_cu = 0

        # Độ lại Style cho cái bảng điểm Tkinter gốc
        self.style_bang_diem()
        self.dung_giao_dien()

    def style_bang_diem(self):
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#27272a", foreground="#d1d5db",
                        fieldbackground="#27272a", borderwidth=0, rowheight=30)
        style.map('Treeview', background=[('selected', '#3b82f6')])
        style.configure("Treeview.Heading", background="#1f2937", foreground="#60a5fa",
                        font=("Arial", 11, "bold"), borderwidth=1)

    def dung_giao_dien(self):
        for widget in self.winfo_children():
            widget.destroy()

        self.tao_header()
        self.tao_thanh_dieu_huong()

        self.khung_noi_dung = ctk.CTkFrame(self, fg_color="#27272a", corner_radius=15)
        self.khung_noi_dung.pack(fill="both", expand=True, padx=20, pady=20)

        self.hien_thi_trang_chu()

    def load_data_va_giao_dien(self, username):
        self.current_user = username
        self.dung_giao_dien()

    def tao_header(self):
        self.khung_header = ctk.CTkFrame(self, fg_color="#18181b", corner_radius=0, cursor="hand2")
        self.khung_header.pack(fill="x")
        self.khung_header.bind("<Button-1>", lambda e: self.hien_thi_trang_chu())

        try:
            img_data = Image.open("logo.png")
            self.logo_img = ctk.CTkImage(light_image=img_data, dark_image=img_data, size=(80, 80))
            lbl_logo = ctk.CTkLabel(self.khung_header, image=self.logo_img, text="")
            lbl_logo.pack(side="left", padx=20, pady=10)
        except:
            lbl_logo = ctk.CTkLabel(self.khung_header, text="[LOGO]", font=("Arial", 20, "bold"), text_color="#60a5fa")
            lbl_logo.pack(side="left", padx=20, pady=10)

        lbl_ten_truong = ctk.CTkLabel(self.khung_header, text="TRƯỜNG ĐẠI HỌC HẠ LONG\nHọc Để Thành Công",
                                      font=("Arial", 18, "bold"), text_color="#60a5fa", justify="left")
        lbl_ten_truong.pack(side="left", pady=10)

    def tao_thanh_dieu_huong(self):
        self.khung_menu = ctk.CTkFrame(self, fg_color="#1f2937", corner_radius=0)
        self.khung_menu.pack(fill="x")

        # THÊM NÚT XEM ĐIỂM Ở ĐÂY NÈ BRUH
        danh_sach_nut = [
            ("Trang chủ", self.hien_thi_trang_chu, "Quay về màn hình chính"),
            ("Xem điểm", self.hien_thi_diem, "Bảng điểm sinh viên realtime"),
            ("Đăng kí", self.chuyen_trang_dang_ky, "Tạo tài khoản mới"),
            ("Thông tin cá nhân", self.hien_thi_thong_tin, "Xem hồ sơ sinh viên"),
            ("Đánh giá", self.hien_thi_danh_gia, "Hệ thống đánh giá rèn luyện"),
            ("Liên hệ", self.hien_thi_dich_vu, "Hỗ trợ & Liên hệ")
        ]

        for text, command, tooltip_text in danh_sach_nut:
            btn = ctk.CTkButton(self.khung_menu, text=text, command=command,
                                fg_color="transparent", text_color="#d1d5db",
                                hover_color="#374151", font=("Arial", 13, "bold"), corner_radius=8)
            btn.pack(side="left", padx=10, pady=8)

        if self.current_user and self.current_user.strip() != "":
            self.btn_user = ctk.CTkButton(self.khung_menu, text=f"👤 {self.current_user} ▼",
                                          fg_color="#10b981", text_color="white",
                                          hover_color="#059669", font=("Arial", 13, "bold"), corner_radius=15)
            self.btn_user.pack(side="right", padx=20, pady=8)
            self.btn_user.bind("<Enter>", self.hien_thi_dropdown)
            self.btn_user.bind("<Leave>", self.an_dropdown_delay)
        else:
            btn_dang_nhap = ctk.CTkButton(self.khung_menu, text="Đăng nhập", command=self.mo_file_dang_nhap,
                                          fg_color="#3b82f6", text_color="white", hover_color="#2563eb",
                                          font=("Arial", 13, "bold"), corner_radius=15)
            btn_dang_nhap.pack(side="right", padx=20, pady=8)

    # --- XỬ LÝ DROPDOWN MENU ---
    def hien_thi_dropdown(self, event=None):
        if self.hide_id: self.after_cancel(self.hide_id); self.hide_id = None
        if self.dropdown_frame is None:
            self.update_idletasks()
            x = self.btn_user.winfo_rootx()
            y = self.btn_user.winfo_rooty() + self.btn_user.winfo_height()
            self.dropdown_frame = tk.Toplevel(self)
            self.dropdown_frame.wm_overrideredirect(True)
            self.dropdown_frame.wm_geometry(f"230x150+{x}+{y}")
            self.dropdown_frame.attributes("-alpha", 0.95)
            khung = ctk.CTkFrame(self.dropdown_frame, fg_color="#1f2937", corner_radius=5)
            khung.pack(fill="both", expand=True)
            ctk.CTkButton(khung, text="  Đổi mật khẩu", fg_color="transparent", hover_color="#374151",
                          text_color="#d1d5db", command=self.doi_mat_khau, height=35, anchor="w").pack(fill="x",
                                                                                                       pady=(10, 5),
                                                                                                       padx=5)
            ctk.CTkButton(khung, text="  Đăng xuất", fg_color="transparent", hover_color="#ef4444", text_color="white",
                          command=self.dang_xuat, height=35, anchor="w").pack(fill="x", pady=(0, 10), padx=5)
            self.dropdown_frame.bind("<Enter>", self.vao_dropdown)
            self.dropdown_frame.bind("<Leave>", self.an_dropdown_delay)

    def vao_dropdown(self, event=None):
        if self.hide_id: self.after_cancel(self.hide_id); self.hide_id = None

    def an_dropdown_delay(self, event=None):
        self.hide_id = self.after(500, self.thuc_su_an_dropdown)

    def thuc_su_an_dropdown(self):
        if self.dropdown_frame: self.dropdown_frame.destroy(); self.dropdown_frame = None

    # --- CHUYỂN TRANG ---
    def dang_xuat(self):
        self.thuc_su_an_dropdown()
        self.xoa_noi_dung_cu()
        self.current_user = None
        self.controller.show_frame("LoginFrame")

    def chuyen_trang_dang_ky(self):
        self.controller.show_frame("RegisterFrame")

    def mo_file_dang_nhap(self):
        self.controller.show_frame("LoginFrame")

    # --- HÀM DỌN RÁC (NGẮT REALTIME KHI CHUYỂN TAB) ---
    def xoa_noi_dung_cu(self):
        if self.news_realtime_id: self.after_cancel(self.news_realtime_id); self.news_realtime_id = None
        if self.grades_realtime_id: self.after_cancel(self.grades_realtime_id); self.grades_realtime_id = None

        if self.khung_noi_dung:
            for widget in self.khung_noi_dung.winfo_children():
                widget.destroy()

    # MODULE XEM ĐIỂM SINH VIÊN
    def hien_thi_diem(self):
        self.xoa_noi_dung_cu()
        if self.current_user in ["Khách", "Sinh viên khách", "", None]:
            ctk.CTkLabel(self.khung_noi_dung, text="🔒 YÊU CẦU ĐĂNG NHẬP", font=("Arial", 22, "bold"),
                         text_color="#ef4444").pack(pady=(80, 10))
            ctk.CTkLabel(self.khung_noi_dung, text="Chỉ sinh viên nội bộ mới được xem điểm.", font=("Arial", 16),
                         text_color="#d1d5db").pack(pady=10)
            return

        self.khung_tong_ket = ctk.CTkFrame(self.khung_noi_dung, fg_color="#1f2937", corner_radius=10)
        self.khung_tong_ket.pack(fill="x", padx=10, pady=(10, 20))

        ctk.CTkLabel(self.khung_tong_ket, text=f"Mã sinh viên: {self.current_user}", font=("Arial", 16, "bold"),
                     text_color="#10b981").grid(row=0, column=0, padx=20, pady=10, sticky="w")
        self.lbl_tbc_he10 = ctk.CTkLabel(self.khung_tong_ket, text="TBC học tập (Hệ 10): 0.00",
                                         font=("Arial", 14, "bold"), text_color="#ef4444")
        self.lbl_tbc_he10.grid(row=0, column=1, padx=40, pady=10, sticky="w")
        self.lbl_tbc_he4 = ctk.CTkLabel(self.khung_tong_ket, text="TBC học tập (Hệ 4): 0.00",
                                        font=("Arial", 14, "bold"), text_color="#ef4444")
        self.lbl_tbc_he4.grid(row=0, column=2, padx=40, pady=10, sticky="w")
        self.lbl_tin_chi = ctk.CTkLabel(self.khung_tong_ket, text="Số tín chỉ tích lũy: 0", font=("Arial", 14, "bold"),
                                        text_color="#f59e0b")
        self.lbl_tin_chi.grid(row=1, column=0, padx=20, pady=10, sticky="w")

        ctk.CTkLabel(self.khung_noi_dung, text="📑 BẢNG ĐIỂM CHI TIẾT", font=("Arial", 16, "bold"), text_color="#60a5fa",
                     anchor="w").pack(fill="x", padx=10, pady=(0, 5))

        frame_table = ctk.CTkFrame(self.khung_noi_dung)
        frame_table.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        columns = ("stt", "ky_hieu", "ten_mon", "tin_chi", "diem_tp", "diem_thi", "tbchp", "he_4", "diem_chu",
                   "ghi_chu", "tu_chon")
        self.tree_diem = ttk.Treeview(frame_table, columns=columns, show="headings", height=15)

        vsb = ttk.Scrollbar(frame_table, orient="vertical", command=self.tree_diem.yview)
        vsb.pack(side="right", fill="y")
        self.tree_diem.configure(yscrollcommand=vsb.set)
        self.tree_diem.pack(side="left", fill="both", expand=True)

        headers = [("stt", "STT", 40), ("ky_hieu", "Ký hiệu", 80), ("ten_mon", "Tên học phần", 200),
                   ("tin_chi", "Số TC", 50), ("diem_tp", "Điểm TP", 180), ("diem_thi", "Điểm thi", 70),
                   ("tbchp", "TBCHP", 60), ("he_4", "Điểm số", 60), ("diem_chu", "Điểm chữ", 70),
                   ("ghi_chu", "Ghi chú", 70), ("tu_chon", "Tự chọn", 70)]

        for col, text, width in headers:
            self.tree_diem.heading(col, text=text)
            self.tree_diem.column(col, width=width, anchor="center" if col != "ten_mon" else "w")

        self.thoi_gian_sua_file_diem_cu = 0
        self.cap_nhat_diem_realtime()

    def cap_nhat_diem_realtime(self):
        if not hasattr(self, 'tree_diem') or not self.tree_diem.winfo_exists(): return

        thu_muc_hien_tai = os.path.dirname(os.path.abspath(__file__))
        duong_dan_file = os.path.normpath(os.path.join(thu_muc_hien_tai, '..', 'database', 'Subject.csv'))

        if not os.path.exists(duong_dan_file):
            self.grades_realtime_id = self.after(3000, self.cap_nhat_diem_realtime)
            return

        try:
            thoi_gian_sua_moi = os.path.getmtime(duong_dan_file)
            if thoi_gian_sua_moi == self.thoi_gian_sua_file_diem_cu:
                self.grades_realtime_id = self.after(2000, self.cap_nhat_diem_realtime)
                return

            self.thoi_gian_sua_file_diem_cu = thoi_gian_sua_moi

            for item in self.tree_diem.get_children():
                self.tree_diem.delete(item)

            tong_tc = 0
            tong_diem_he_10 = 0.0
            tong_diem_he_4 = 0.0
            stt = 1

            with open(duong_dan_file, mode='r', encoding='utf-8-sig') as file:
                reader = csv.reader(file)
                next(reader, None)
                for row in reader:
                    if len(row) >= 11 and row[0].strip() == self.current_user:
                        self.tree_diem.insert("", "end", values=(stt, *row[1:11]))
                        stt += 1
                        try:
                            tc = int(row[3].strip())
                            diem_10 = float(row[6].strip())
                            diem_4 = float(row[7].strip())
                            tong_tc += tc
                            tong_diem_he_10 += diem_10 * tc
                            tong_diem_he_4 += diem_4 * tc
                        except ValueError:
                            pass

            if tong_tc > 0:
                tbc_10 = tong_diem_he_10 / tong_tc
                tbc_4 = tong_diem_he_4 / tong_tc
                self.lbl_tbc_he10.configure(text=f"TBC học tập (Hệ 10): {tbc_10:.2f}")
                self.lbl_tbc_he4.configure(text=f"TBC học tập (Hệ 4): {tbc_4:.2f}")
                self.lbl_tin_chi.configure(text=f"Số tín chỉ tích lũy: {tong_tc}")
        except Exception:
            pass

        self.grades_realtime_id = self.after(2000, self.cap_nhat_diem_realtime)

    #Module trang chủ, tin realtime
    def hien_thi_trang_chu(self):
        self.xoa_noi_dung_cu()
        self.khung_noi_dung.grid_columnconfigure((0, 1, 2), weight=1, uniform="col")
        self.khung_noi_dung.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(self.khung_noi_dung, text="TIN TỨC MỚI NHẤT", font=("Arial", 15, "bold"),
                     text_color="#f3f4f6").grid(row=0, column=0, pady=(15, 5), sticky="w", padx=10)
        ctk.CTkLabel(self.khung_noi_dung, text="BẢNG TIN REALTIME", font=("Arial", 15, "bold"),
                     text_color="#10b981").grid(row=0, column=1, pady=(15, 5), sticky="w", padx=10)
        ctk.CTkLabel(self.khung_noi_dung, text="VĂN BẢN, BIỂU MẪU", font=("Arial", 15, "bold"),
                     text_color="#f3f4f6").grid(row=0, column=2, pady=(15, 5), sticky="w", padx=10)

        frame_tintuc = ctk.CTkScrollableFrame(self.khung_noi_dung, fg_color="transparent")
        frame_tintuc.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        for tin in ["TB-không sử dụng CC NLNN thi trực tuyến", "Danh sách sinh viên đăng ký nhận bằng",
                    "Đăng ký nhận bằng trên sân khấu đợt 1 năm 2026"]:
            ctk.CTkButton(frame_tintuc, text=f"➤ {tin}", fg_color="transparent", text_color="#9ca3af",
                          hover_color="#374151", anchor="w", font=("Arial", 12)).pack(fill="x", pady=2)

        self.frame_thongbao = ctk.CTkScrollableFrame(self.khung_noi_dung, fg_color="#1f2937", border_width=1,
                                                     border_color="#374151", corner_radius=5)
        self.frame_thongbao.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)

        self.thoi_gian_sua_news_cu = 0
        self.cap_nhat_thong_bao_realtime()

        frame_vanban = ctk.CTkScrollableFrame(self.khung_noi_dung, fg_color="transparent")
        frame_vanban.grid(row=1, column=2, sticky="nsew", padx=5, pady=5)
        ctk.CTkLabel(frame_vanban, text="PHÒNG ĐÀO TẠO", font=("Arial", 13, "bold"), text_color="#f87171",
                     anchor="w").pack(fill="x", pady=(5, 0))
        ctk.CTkButton(frame_vanban, text="Quy định đào tạo", fg_color="transparent", text_color="#9ca3af",
                      hover_color="#374151", anchor="w").pack(fill="x")
        ctk.CTkButton(frame_vanban, text="Sổ tay sinh viên", fg_color="transparent", text_color="#9ca3af",
                      hover_color="#374151", anchor="w").pack(fill="x")

    def cap_nhat_thong_bao_realtime(self):
        if not hasattr(self, 'frame_thongbao') or not self.frame_thongbao.winfo_exists(): return

        thu_muc_hien_tai = os.path.dirname(os.path.abspath(__file__))
        duong_dan_file = os.path.normpath(os.path.join(thu_muc_hien_tai, '..', 'database', 'Real_Time_info.csv'))

        if not os.path.exists(duong_dan_file):
            self.news_realtime_id = self.after(3000, self.cap_nhat_thong_bao_realtime)
            return

        try:
            thoi_gian_moi = os.path.getmtime(duong_dan_file)
            if thoi_gian_moi == self.thoi_gian_sua_news_cu:
                self.news_realtime_id = self.after(2000, self.cap_nhat_thong_bao_realtime)
                return

            self.thoi_gian_sua_news_cu = thoi_gian_moi
            for widget in self.frame_thongbao.winfo_children(): widget.destroy()

            with open(duong_dan_file, mode='r', encoding='utf-8-sig') as file:
                reader = csv.reader(file)
                danh_sach_tb = [row for row in reader if len(row) > 0 and "".join(row).strip() != ""]

                if not danh_sach_tb:
                    ctk.CTkLabel(self.frame_thongbao, text="Hiện chưa có tin tức gì mới.", text_color="#9ca3af",
                                 font=("Arial", 13, "italic")).pack(pady=20)
                else:
                    for row in reversed(danh_sach_tb):
                        thoi_gian = row[0].strip() if len(row) >= 2 else "Vừa xong"
                        noi_dung = row[1].strip() if len(row) >= 2 else row[0].strip()
                        card = ctk.CTkFrame(self.frame_thongbao, fg_color="#27272a", corner_radius=8, border_width=1,
                                            border_color="#374151")
                        card.pack(fill="x", pady=5, padx=5)
                        ctk.CTkLabel(card, text=noi_dung, font=("Arial", 13, "bold"), text_color="#60a5fa",
                                     justify="left", wraplength=250).pack(anchor="w", padx=10, pady=(10, 0))
                        ctk.CTkLabel(card, text=f"🕒 {thoi_gian}", font=("Arial", 11), text_color="#9ca3af").pack(
                            anchor="e", padx=10, pady=(0, 10))
        except Exception:
            pass
        self.news_realtime_id = self.after(2000, self.cap_nhat_thong_bao_realtime)

    #module đánh giá
    def hien_thi_danh_gia(self):
        self.xoa_noi_dung_cu()
        if self.current_user in ["Khách", "Sinh viên khách", "", None]:
            ctk.CTkLabel(self.khung_noi_dung, text="🔒 YÊU CẦU ĐĂNG NHẬP", font=("Arial", 22, "bold"),
                         text_color="#ef4444").pack(pady=(80, 10))
            return

        thu_muc_hien_tai = os.path.dirname(os.path.abspath(__file__))
        file_rate = os.path.normpath(os.path.join(thu_muc_hien_tai, "..", "database", "Rate.csv"))
        da_danh_gia = False

        if os.path.exists(file_rate):
            try:
                with open(file_rate, "r", encoding="utf-8") as f:
                    for row in csv.reader(f):
                        if len(row) > 0 and row[0] == self.current_user:
                            da_danh_gia = True;
                            break
            except Exception:
                pass

        if da_danh_gia:
            ctk.CTkLabel(self.khung_noi_dung, text="⛔ ĐÃ ĐÁNH GIÁ", font=("Arial", 24, "bold"),
                         text_color="#ef4444").pack(pady=(80, 10))
            ctk.CTkLabel(self.khung_noi_dung,
                         text="Tài khoản này đã nộp điểm rèn luyện cho kỳ này.\nVui lòng chờ đến đợt đánh giá tiếp theo!",
                         font=("Arial", 16), text_color="#d1d5db").pack(pady=10)
            return

        ctk.CTkLabel(self.khung_noi_dung, text="ĐÁNH GIÁ ĐIỂM RÈN LUYỆN", font=("Arial", 24, "bold"),
                     text_color="#60a5fa").pack(pady=(30, 5))
        form_frame = ctk.CTkFrame(self.khung_noi_dung, fg_color="#1f2937", corner_radius=10)
        form_frame.pack(fill="both", expand=True, padx=80, pady=10)

        self.danh_sach_tieu_chi = [("1. Ý thức", 20), ("2. Chấp hành", 25), ("3. Hoạt động", 20), ("4. Phẩm chất", 25),
                                   ("5. Cán bộ", 10)]
        self.cac_o_nhap_diem = {}

        for tc, d_max in self.danh_sach_tieu_chi:
            dong = ctk.CTkFrame(form_frame, fg_color="transparent")
            dong.pack(fill="x", padx=30, pady=15)
            ctk.CTkLabel(dong, text=f"{tc} (Max: {d_max})", font=("Arial", 15, "bold"), text_color="white").pack(
                side="left")
            o_nhap = ctk.CTkEntry(dong, width=60, justify="center", fg_color="#374151", text_color="white",
                                  border_color="#4b5563")
            o_nhap.insert(0, "0")
            o_nhap.pack(side="right", padx=(0, 10))
            self.cac_o_nhap_diem[tc] = o_nhap

        ctk.CTkButton(self.khung_noi_dung, text="Gửi đánh giá", fg_color="#3b82f6", hover_color="#2563eb",
                      command=self.xu_ly_luu_danh_gia).pack(pady=30)

    def xu_ly_luu_danh_gia(self):
        tong_diem = 0
        ket_qua_tung_muc = []
        for tc, d_max in self.danh_sach_tieu_chi:
            gia_tri = self.cac_o_nhap_diem[tc].get().strip()
            if not gia_tri:
                messagebox.showerror("Lỗi", f"Chưa nhập điểm cho mục '{tc}'!");
                return
            try:
                diem = int(gia_tri)
                if diem < 0 or diem > d_max:
                    messagebox.showerror("Lỗi", f"Mục '{tc}' chỉ được nhập từ 0 đến {d_max} thôi.");
                    return
                tong_diem += diem;
                ket_qua_tung_muc.append(diem)
            except ValueError:
                messagebox.showerror("Lỗi", f"Mục '{tc}' phải nhập số chứ!");
                return

        thu_muc_hien_tai = os.path.dirname(os.path.abspath(__file__))
        file_rate = os.path.normpath(os.path.join(thu_muc_hien_tai, "..", "database", "Rate.csv"))
        os.makedirs(os.path.dirname(file_rate), exist_ok=True)

        file_exists = os.path.exists(file_rate)
        try:
            with open(file_rate, mode='a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                if not file_exists:
                    writer.writerow(
                        ["Tài Khoản", "Ý thức", "Chấp hành", "Hoạt động", "Phẩm chất", "Cán bộ", "Tổng điểm"])
                writer.writerow([self.current_user] + ket_qua_tung_muc + [tong_diem])

            messagebox.showinfo("Thành công", f"Nộp bài thành công!\nTổng điểm rèn luyện: {tong_diem}/100")
            self.hien_thi_danh_gia()
        except Exception as e:
            messagebox.showerror("Lỗi DB", f"Không thể lưu điểm: {e}")

    #Module đổi pass
    def doi_mat_khau(self):
        self.thuc_su_an_dropdown()
        if self.current_user in ["Khách", "Sinh viên khách", "", None]:
            messagebox.showwarning("Từ chối", "Tài khoản Khách không thể đổi mật khẩu!")
            return

        cua_so_doi_mk = ctk.CTkToplevel(self)
        cua_so_doi_mk.title("Bảo mật tài khoản")
        cua_so_doi_mk.geometry("450x380")
        cua_so_doi_mk.attributes("-topmost", True)
        cua_so_doi_mk.grab_set()
        cua_so_doi_mk.configure(fg_color="#18181b")

        container = ctk.CTkFrame(cua_so_doi_mk, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=20, pady=20)

        def xoa_container():
            for widget in container.winfo_children(): widget.destroy()

        def buoc_1_nhap_email():
            xoa_container()
            ctk.CTkLabel(container, text="BƯỚC 1: XÁC THỰC EMAIL", font=("Arial", 18, "bold"),
                         text_color="#60a5fa").pack(pady=(10, 20))
            txt_email = ctk.CTkEntry(container, font=("Arial", 14), width=350, height=40, fg_color="#27272a",
                                     text_color="white", border_color="#3f3f46")
            txt_email.pack(pady=(5, 20))
            ctk.CTkButton(container, text="Nhận mã OTP", font=("Arial", 15, "bold"), fg_color="#3b82f6",
                          hover_color="#2563eb", height=40, width=200,
                          command=lambda: [messagebox.showinfo("Chế độ Demo", "Mã OTP là 1111", parent=cua_so_doi_mk),
                                           buoc_2_nhap_otp()]).pack()

        def buoc_2_nhap_otp():
            xoa_container()
            ctk.CTkLabel(container, text="BƯỚC 2: NHẬP MÃ OTP", font=("Arial", 18, "bold"), text_color="#60a5fa").pack(
                pady=(10, 20))
            txt_otp = ctk.CTkEntry(container, font=("Arial", 22, "bold"), justify="center", width=200, height=45,
                                   fg_color="#27272a", text_color="white", border_color="#3f3f46")
            txt_otp.pack(pady=(10, 20))
            khung_nut = ctk.CTkFrame(container, fg_color="transparent")
            khung_nut.pack()
            ctk.CTkButton(khung_nut, text="Quay lại", font=("Arial", 14), fg_color="#4b5563", hover_color="#374151",
                          height=40, width=120, command=buoc_1_nhap_email).pack(side="left", padx=10)
            ctk.CTkButton(khung_nut, text="Xác nhận", font=("Arial", 15, "bold"), fg_color="#10b981",
                          hover_color="#059669", height=40, width=120,
                          command=lambda: buoc_3_tao_mk_moi() if txt_otp.get().strip() == "1111" else messagebox.showerror(
                              "Lỗi", "Mã OTP sai!", parent=cua_so_doi_mk)).pack(side="left", padx=10)

        def buoc_3_tao_mk_moi():
            xoa_container()
            ctk.CTkLabel(container, text="BƯỚC 3: TẠO MẬT KHẨU MỚI", font=("Arial", 18, "bold"),
                         text_color="#10b981").pack(pady=(10, 20))
            txt_mk_moi = ctk.CTkEntry(container, font=("Arial", 14), show="*", width=350, height=35, fg_color="#27272a",
                                      text_color="white", border_color="#3f3f46")
            txt_mk_moi.pack(pady=(0, 10))
            txt_xac_nhan = ctk.CTkEntry(container, font=("Arial", 14), show="*", width=350, height=35,
                                        fg_color="#27272a", text_color="white", border_color="#3f3f46")
            txt_xac_nhan.pack(pady=(0, 20))

            def xu_ly_luu_mk():
                if not txt_mk_moi.get() or txt_mk_moi.get() != txt_xac_nhan.get():
                    messagebox.showerror("Lỗi", "Mật khẩu trống hoặc không khớp!", parent=cua_so_doi_mk);
                    return

                thu_muc_hien_tai = os.path.dirname(os.path.abspath(__file__))
                file_tk = os.path.normpath(os.path.join(thu_muc_hien_tai, "..", "database", "account.csv"))
                du_lieu = []
                try:
                    with open(file_tk, "r", encoding="utf-8") as f:
                        for row in csv.reader(f):
                            if len(row) >= 2 and row[0] == self.current_user: row[1] = txt_mk_moi.get()
                            du_lieu.append(row)
                    with open(file_tk, "w", newline="", encoding="utf-8") as f:
                        csv.writer(f).writerows(du_lieu)
                    messagebox.showinfo("Xong", "Đổi MK thành công. Vui lòng đăng nhập lại.", parent=cua_so_doi_mk)
                    cua_so_doi_mk.destroy();
                    self.dang_xuat()
                except Exception as e:
                    messagebox.showerror("Lỗi", f"Lỗi DB: {e}", parent=cua_so_doi_mk)

            ctk.CTkButton(container, text="Lưu mật khẩu", font=("Arial", 15, "bold"), fg_color="#ef4444",
                          hover_color="#dc2626", height=40, width=200, command=xu_ly_luu_mk).pack()

        buoc_1_nhap_email()

    def hien_thi_thong_tin(self):
        self.xoa_noi_dung_cu()
        ctk.CTkLabel(self.khung_noi_dung, text="MODULE THÔNG TIN CÁ NHÂN", font=("Arial", 22, "bold"),
                     text_color="white").pack(pady=30)

    def hien_thi_dich_vu(self):
        self.xoa_noi_dung_cu()
        ctk.CTkLabel(self.khung_noi_dung, text="THÔNG TIN LIÊN HỆ", font=("Arial", 24, "bold"),
                     text_color="#60a5fa").pack(pady=30)
        info_frame = ctk.CTkFrame(self.khung_noi_dung, fg_color="#1f2937", corner_radius=10)
        info_frame.pack(fill="x", padx=150, pady=10)
        for i, d in [("Điện thoại:", "0960 694 201"), ("Email:", "gaysech69@uhl.edu.vn"), ("Web:", "uhl.edu.vn")]:
            dong = ctk.CTkFrame(info_frame, fg_color="transparent")
            dong.pack(fill="x", padx=40, pady=15)
            ctk.CTkLabel(dong, text=i, font=("Arial", 16, "bold"), text_color="#93c5fd").pack(side="left")
            ctk.CTkLabel(dong, text=d, font=("Arial", 16), text_color="white").pack(side="right")
