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
        tk.Label(self.tooltip_window, text=self.text, justify="left", background="#27272a", fg="white", relief="solid",
                 borderwidth=1, font=("Arial", 10)).pack(ipadx=5, ipady=3)

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
        self.news_realtime_id = None
        self.grades_realtime_id = None
        self.thoi_gian_sua_file_diem_cu = 0
        self.thoi_gian_sua_news_cu = 0
        self.style_bang_diem()
        self.dung_giao_dien()

    def style_bang_diem(self):
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#27272a", foreground="#d1d5db", fieldbackground="#27272a",
                        borderwidth=0, rowheight=40, font=("Arial", 16))
        style.map('Treeview', background=[('selected', '#3b82f6')])
        style.configure("Treeview.Heading", background="#1f2937", foreground="#60a5fa", font=("Arial", 18, "bold"),
                        borderwidth=1)

        style.configure("LichThi.Treeview", background="#27272a", foreground="#d1d5db", fieldbackground="#27272a",
                        borderwidth=0, rowheight=40, font=("Arial", 16))
        style.map('LichThi.Treeview', background=[('selected', '#3b82f6')])
        style.configure("LichThi.Treeview.Heading", background="#1f2937", foreground="#60a5fa",
                        font=("Arial", 18, "bold"), borderwidth=1)

    def dung_giao_dien(self):
        for widget in self.winfo_children(): widget.destroy()
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
            ctk.CTkLabel(self.khung_header, image=self.logo_img, text="").pack(side="left", padx=20, pady=10)
        except:
            ctk.CTkLabel(self.khung_header, text="[LOGO]", font=("Arial", 20, "bold"), text_color="#60a5fa").pack(
                side="left", padx=20, pady=10)
        ctk.CTkLabel(self.khung_header, text="TRƯỜNG ĐẠI HỌC HẠ LONG\nHọc Để Thành Công", font=("Arial", 18, "bold"),
                     text_color="#60a5fa", justify="left").pack(side="left", pady=10)

    def tao_thanh_dieu_huong(self):
        self.khung_menu = ctk.CTkFrame(self, fg_color="#1f2937", corner_radius=0)
        self.khung_menu.pack(fill="x")
        danh_sach_nut = [
            ("Trang chủ", self.hien_thi_trang_chu),
            ("Xem điểm", self.hien_thi_diem),
            ("Đăng kí", self.chuyen_trang_dang_ky),
            ("Thông tin cá nhân", self.hien_thi_thong_tin),
            ("Đánh giá", self.hien_thi_danh_gia),
            ("Liên hệ", self.hien_thi_dich_vu)
        ]
        for text, command in danh_sach_nut:
            ctk.CTkButton(self.khung_menu, text=text, command=command, fg_color="transparent", text_color="#d1d5db",
                          hover_color="#374151", font=("Arial", 13, "bold"), corner_radius=8, cursor="hand2").pack(side="left", padx=10,
                                                                                                   pady=8)

        if self.current_user and self.current_user.strip() != "":
            self.btn_user = ctk.CTkButton(self.khung_menu, text=f"👤 {self.current_user} ▼", fg_color="#10b981",
                                          text_color="white", hover_color="#059669", font=("Arial", 13, "bold"),
                                          corner_radius=15, cursor="hand2")
            self.btn_user.pack(side="right", padx=20, pady=8)
            self.btn_user.bind("<Enter>", self.hien_thi_dropdown)
            self.btn_user.bind("<Leave>", self.an_dropdown_delay)
        else:
            ctk.CTkButton(self.khung_menu, text="Đăng nhập", command=self.mo_file_dang_nhap, fg_color="#3b82f6",
                          text_color="white", hover_color="#2563eb", font=("Arial", 13, "bold"), corner_radius=15, cursor="hand2").pack(
                side="right", padx=20, pady=8)

    def hien_thi_dropdown(self, event=None):
        if self.hide_id: self.after_cancel(self.hide_id); self.hide_id = None
        if self.dropdown_frame is None:
            self.update_idletasks()
            x = self.btn_user.winfo_rootx()
            y = self.btn_user.winfo_rooty() + self.btn_user.winfo_height()
            self.dropdown_frame = tk.Toplevel(self)
            self.dropdown_frame.wm_overrideredirect(True)
            self.dropdown_frame.wm_geometry(f"230x150+{x}+{y}")
            khung = ctk.CTkFrame(self.dropdown_frame, fg_color="#1f2937", corner_radius=5)
            khung.pack(fill="both", expand=True)
            ctk.CTkButton(khung, text="  Đổi mật khẩu", fg_color="transparent", hover_color="#374151",
                          text_color="#d1d5db", command=self.doi_mat_khau, height=35, anchor="w", cursor="hand2").pack(fill="x",
                                                                                                       pady=(10, 5),
                                                                                                       padx=5)
            ctk.CTkButton(khung, text="  Đăng xuất", fg_color="transparent", hover_color="#ef4444", text_color="white",
                          command=self.dang_xuat, height=35, anchor="w", cursor="hand2").pack(fill="x", pady=(0, 10), padx=5)
            self.dropdown_frame.bind("<Enter>", self.vao_dropdown)
            self.dropdown_frame.bind("<Leave>", self.an_dropdown_delay)

    def vao_dropdown(self, event=None):
        if self.hide_id: self.after_cancel(self.hide_id); self.hide_id = None

    def an_dropdown_delay(self, event=None):
        self.hide_id = self.after(500, self.thuc_su_an_dropdown)

    def thuc_su_an_dropdown(self):
        if self.dropdown_frame: self.dropdown_frame.destroy(); self.dropdown_frame = None

    def dang_xuat(self):
        self.thuc_su_an_dropdown()
        self.xoa_noi_dung_cu()
        self.current_user = None
        self.controller.show_frame("LoginFrame")

    def chuyen_trang_dang_ky(self):
        self.controller.show_frame("RegisterFrame")

    def mo_file_dang_nhap(self):
        self.controller.show_frame("LoginFrame")

    def xoa_noi_dung_cu(self):
        if self.news_realtime_id: self.after_cancel(self.news_realtime_id); self.news_realtime_id = None
        if self.grades_realtime_id: self.after_cancel(self.grades_realtime_id); self.grades_realtime_id = None
        if self.khung_noi_dung:
            for widget in self.khung_noi_dung.winfo_children(): widget.destroy()

    def hien_thi_diem(self):
        self.xoa_noi_dung_cu()
        if not self.current_user or self.current_user in ["Khách", "Sinh viên khách", ""]:
            ctk.CTkLabel(self.khung_noi_dung, text="YÊU CẦU ĐĂNG NHẬP", font=("Arial", 22, "bold"),
                         text_color="#ef4444").pack(pady=(80, 10))
            return
        self.khung_tong_ket = ctk.CTkFrame(self.khung_noi_dung, fg_color="#1f2937", corner_radius=10)
        self.khung_tong_ket.pack(fill="x", padx=10, pady=(10, 20))
        ctk.CTkLabel(self.khung_tong_ket, text=f"Mã sinh viên: {self.current_user}", font=("Arial", 16, "bold"),
                     text_color="#10b981").grid(row=0, column=0, padx=20, pady=10, sticky="w")
        self.lbl_tbc_he10 = ctk.CTkLabel(self.khung_tong_ket, text="TBC học tập (Hệ 10): 0.00",
                                         font=("Arial", 16, "bold"), text_color="#ef4444")
        self.lbl_tbc_he10.grid(row=0, column=1, padx=40, pady=10, sticky="w")
        self.lbl_tbc_he4 = ctk.CTkLabel(self.khung_tong_ket, text="TBC học tập (Hệ 4): 0.00",
                                        font=("Arial", 16, "bold"), text_color="#ef4444")
        self.lbl_tbc_he4.grid(row=0, column=2, padx=40, pady=10, sticky="w")
        self.lbl_tin_chi = ctk.CTkLabel(self.khung_tong_ket, text="Số tín chỉ tích lũy: 0", font=("Arial", 16, "bold"),
                                        text_color="#f59e0b")
        self.lbl_tin_chi.grid(row=1, column=0, padx=20, pady=10, sticky="w")

        ToolTip(self.lbl_tbc_he10, "Trung bình cộng điểm các môn học theo thang 10")
        ToolTip(self.lbl_tbc_he4, "Trung bình cộng điểm các môn học theo thang 4")
        ToolTip(self.lbl_tin_chi, "Tổng số tín chỉ của các môn học đã vượt qua")

        frame_table = ctk.CTkFrame(self.khung_noi_dung)
        frame_table.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.tree_diem = ttk.Treeview(frame_table,
                                      columns=("stt", "kh", "ten", "tc", "tp", "thi", "he10", "he4", "chu", "gc",
                                               "tuchon"), show="headings", height=15)
        vsb = ttk.Scrollbar(frame_table, orient="vertical", command=self.tree_diem.yview)
        vsb.pack(side="right", fill="y")
        self.tree_diem.configure(yscrollcommand=vsb.set)
        self.tree_diem.pack(side="left", fill="both", expand=True)

        for col, text, width in [("stt", "STT", 50), ("kh", "Ký hiệu", 90), ("ten", "Tên học phần", 250),
                                 ("tc", "Số TC", 70), ("tp", "Điểm TP", 120), ("thi", "Điểm thi", 90),
                                 ("he10", "TBCHP", 90), ("he4", "Điểm số", 90), ("chu", "Điểm chữ", 90),
                                 ("gc", "Ghi chú", 90), ("tuchon", "Tự chọn", 90)]:
            self.tree_diem.heading(col, text=text)
            self.tree_diem.column(col, width=width, anchor="w" if col == "ten" else "center")

        self.tree_diem.tag_configure("evenrow", background="#1f2937")
        self.tree_diem.tag_configure("oddrow", background="#27272a")

        self.thoi_gian_sua_file_diem_cu = 0
        self.cap_nhat_diem_realtime()

    def cap_nhat_diem_realtime(self):
        if not hasattr(self, 'tree_diem') or not self.tree_diem.winfo_exists(): return
        path = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'database', 'Subject.csv'))
        if not os.path.exists(path):
            self.grades_realtime_id = self.after(3000, self.cap_nhat_diem_realtime)
            return

        try:
            thoi_gian_moi = os.path.getmtime(path)
            if thoi_gian_moi == getattr(self, 'thoi_gian_sua_file_diem_cu', 0):
                self.grades_realtime_id = self.after(2000, self.cap_nhat_diem_realtime)
                return
            self.thoi_gian_sua_file_diem_cu = thoi_gian_moi
            for item in self.tree_diem.get_children(): self.tree_diem.delete(item)

            tong_tc = tong_diem_he_10 = tong_diem_he_4 = 0
            stt = 1
            with open(path, mode='r', encoding='utf-8-sig') as f:
                reader = csv.reader(f)
                next(reader, None)
                for row in reader:
                    if len(row) >= 11 and row[0].strip() == self.current_user:
                        tag = "evenrow" if stt % 2 == 0 else "oddrow"
                        self.tree_diem.insert("", "end", values=(stt, *row[1:11]), tags=(tag,))
                        stt += 1
                        try:
                            tc = int(row[3].strip())
                            tong_tc += tc
                            tong_diem_he_10 += float(row[6].strip()) * tc
                            tong_diem_he_4 += float(row[7].strip()) * tc
                        except ValueError:
                            pass

            if tong_tc > 0:
                self.lbl_tbc_he10.configure(text=f"TBC học tập (Hệ 10): {tong_diem_he_10 / tong_tc:.2f}")
                self.lbl_tbc_he4.configure(text=f"TBC học tập (Hệ 4): {tong_diem_he_4 / tong_tc:.2f}")
                self.lbl_tin_chi.configure(text=f"Số tín chỉ tích lũy: {tong_tc}")
        except Exception:
            pass
        self.grades_realtime_id = self.after(2000, self.cap_nhat_diem_realtime)

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
                    "Đăng ký nhận bằng đợt 1 năm 2026"]:
            ctk.CTkButton(frame_tintuc, text=f"➤ {tin}", fg_color="transparent", text_color="#9ca3af",
                          hover_color="#374151", anchor="w", font=("Arial", 12), cursor="hand2").pack(fill="x", pady=2)

        self.frame_thongbao = ctk.CTkScrollableFrame(self.khung_noi_dung, fg_color="#1f2937", border_width=1,
                                                     border_color="#374151", corner_radius=5)
        self.frame_thongbao.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
        self.thoi_gian_sua_news_cu = 0
        self.cap_nhat_thong_bao_realtime()

        frame_vanban = ctk.CTkScrollableFrame(self.khung_noi_dung, fg_color="transparent")
        frame_vanban.grid(row=1, column=2, sticky="nsew", padx=5, pady=5)
        ctk.CTkLabel(frame_vanban, text="PHÒNG ĐÀO TẠO", font=("Arial", 13, "bold"), text_color="#f87171",
                     anchor="w").pack(fill="x", pady=(5, 0))
        for vb in ["Quy định đào tạo", "Sổ tay sinh viên"]:
            ctk.CTkButton(frame_vanban, text=vb, fg_color="transparent", text_color="#9ca3af", hover_color="#374151",
                          anchor="w", cursor="hand2").pack(fill="x")

    def cap_nhat_thong_bao_realtime(self):
        if not hasattr(self, 'frame_thongbao') or not self.frame_thongbao.winfo_exists(): return
        path = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'database', 'Real_Time_info.csv'))
        if not os.path.exists(path):
            self.news_realtime_id = self.after(3000, self.cap_nhat_thong_bao_realtime)
            return
        try:
            thoi_gian_moi = os.path.getmtime(path)
            if thoi_gian_moi == self.thoi_gian_sua_news_cu:
                self.news_realtime_id = self.after(2000, self.cap_nhat_thong_bao_realtime)
                return
            self.thoi_gian_sua_news_cu = thoi_gian_moi
            for widget in self.frame_thongbao.winfo_children(): widget.destroy()

            with open(path, mode='r', encoding='utf-8-sig') as file:
                danh_sach_tb = [row for row in csv.reader(file) if len(row) > 0 and "".join(row).strip() != ""]
                if not danh_sach_tb:
                    ctk.CTkLabel(self.frame_thongbao, text="Chưa có tin mới.", text_color="#9ca3af").pack(pady=20)
                else:
                    for row in reversed(danh_sach_tb):
                        thoi_gian = row[0].strip() if len(row) >= 2 else "Vừa xong"
                        noi_dung = row[1].strip() if len(row) >= 2 else row[0].strip()
                        card = ctk.CTkFrame(self.frame_thongbao, fg_color="#27272a", corner_radius=8,
                                            border_color="#374151", border_width=1)
                        card.pack(fill="x", pady=5, padx=5)
                        ctk.CTkLabel(card, text=noi_dung, font=("Arial", 13, "bold"), text_color="#60a5fa",
                                     justify="left", wraplength=250).pack(anchor="w", padx=10, pady=(10, 0))
                        ctk.CTkLabel(card, text=f"{thoi_gian}", font=("Arial", 11), text_color="#9ca3af").pack(
                            anchor="e", padx=10, pady=(0, 10))
        except Exception:
            pass
        self.news_realtime_id = self.after(2000, self.cap_nhat_thong_bao_realtime)

    def hien_thi_danh_gia(self):
        self.xoa_noi_dung_cu()
        if not self.current_user or self.current_user in ["Khách", "Sinh viên khách", ""]:
            ctk.CTkLabel(self.khung_noi_dung, text="🔒 YÊU CẦU ĐĂNG NHẬP", font=("Arial", 22, "bold"),
                         text_color="#ef4444").pack(pady=(80, 10))
            return

        path = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "database", "../Database/Rate.csv"))
        da_danh_gia = False
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    for row in csv.reader(f):
                        if len(row) > 0 and row[0] == self.current_user:
                            da_danh_gia = True
                            break
            except Exception:
                pass

        if da_danh_gia:
            ctk.CTkLabel(self.khung_noi_dung, text="⛔ ĐÃ ĐÁNH GIÁ", font=("Arial", 24, "bold"),
                         text_color="#ef4444").pack(pady=(80, 10))
            return

        form_frame = ctk.CTkFrame(self.khung_noi_dung, fg_color="#1f2937", corner_radius=10)
        form_frame.pack(fill="both", expand=True, padx=80, pady=30)

        self.danh_sach_tieu_chi = [("1. Ý thức", 20), ("2. Chấp hành", 25), ("3. Hoạt động", 20), ("4. Phẩm chất", 25),
                                   ("5. Cán bộ", 10)]
        self.cac_o_nhap_diem = {}

        for tc, d_max in self.danh_sach_tieu_chi:
            dong = ctk.CTkFrame(form_frame, fg_color="transparent")
            dong.pack(fill="x", padx=30, pady=15)

            ctk.CTkLabel(dong, text=tc, font=("Arial", 15, "bold"), text_color="white").pack(side="left")

            ctk.CTkLabel(dong, text=f" / {d_max}", font=("Arial", 15, "bold"), text_color="#9ca3af").pack(side="right",
                                                                                                          padx=(5, 10))

            en = ctk.CTkEntry(dong, width=50, justify="center", fg_color="#374151", text_color="white",
                              border_color="#4b5563")
            en.insert(0, "0")
            en.pack(side="right")

            self.cac_o_nhap_diem[tc] = en

        ctk.CTkButton(self.khung_noi_dung, text="Gửi đánh giá", fg_color="#3b82f6", hover_color="#2563eb",
                      command=self.xu_ly_luu_danh_gia, cursor="hand2").pack(pady=30)

    def xu_ly_luu_danh_gia(self):
        tong = 0
        kq = []
        for tc, d_max in self.danh_sach_tieu_chi:
            try:
                diem = int(self.cac_o_nhap_diem[tc].get().strip())
                if diem < 0 or diem > d_max: messagebox.showerror("Lỗi", f"Mục '{tc}' từ 0 đến {d_max} thôi."); return
                tong += diem
                kq.append(diem)
            except ValueError:
                messagebox.showerror("Lỗi", "Nhập số nhé!");
                return
        path = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "database", "../Database/Rate.csv"))
        exists = os.path.exists(path)
        try:
            with open(path, mode='a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                if not exists: writer.writerow(
                    ["Tài Khoản", "Ý thức", "Chấp hành", "Hoạt động", "Phẩm chất", "Cán bộ", "Tổng"])
                writer.writerow([self.current_user] + kq + [tong])
            messagebox.showinfo("Thành công", f"Nộp thành công! Tổng: {tong}/100")
            self.hien_thi_danh_gia()
        except Exception as e:
            messagebox.showerror("Lỗi DB", str(e))

    def hien_thi_thong_tin(self):
        self.xoa_noi_dung_cu()
        if not self.current_user or self.current_user in ["Khách", "Sinh viên khách", ""]: return
        khung_menu_con = ctk.CTkFrame(self.khung_noi_dung, fg_color="transparent")
        khung_menu_con.pack(fill="x", padx=20, pady=(10, 0))
        self.combo_thong_tin = ctk.CTkOptionMenu(khung_menu_con, values=["Thông tin sinh viên", "Thông tin lịch học",
                                                                         "Lịch thi sinh viên"],
                                                 command=self.chuyen_tab_thong_tin, font=("Arial", 14, "bold"),
                                                 fg_color="#3b82f6", cursor="hand2")
        self.combo_thong_tin.pack(side="left")
        self.khung_hien_thi_dong = ctk.CTkFrame(self.khung_noi_dung, fg_color="#1f2937", corner_radius=10)
        self.khung_hien_thi_dong.pack(fill="both", expand=True, padx=20, pady=15)
        self.combo_thong_tin.set("Thông tin sinh viên")
        self.chuyen_tab_thong_tin("Thông tin sinh viên")

    def chuyen_tab_thong_tin(self, lua_chon):
        for w in self.khung_hien_thi_dong.winfo_children(): w.destroy()
        if lua_chon == "Thông tin sinh viên":
            self.render_thong_tin_sinh_vien()
        elif lua_chon == "Thông tin lịch học":
            self.render_lich_hoc_sinh_vien()
        elif lua_chon == "Lịch thi sinh viên":
            self.render_lich_thi_sinh_vien()

    def render_lich_hoc_sinh_vien(self):
        ctk.CTkLabel(self.khung_hien_thi_dong, text="LỊCH HỌC SINH VIÊN", font=("Arial", 20, "bold"),
                     text_color="#3b82f6").pack(pady=(10, 5))

        frame_table = ctk.CTkFrame(self.khung_hien_thi_dong, fg_color="transparent")
        frame_table.pack(fill="both", expand=True, padx=10, pady=10)
        cols = ("stt", "ten", "thu", "ca", "phong", "gv", "tuan")
        self.tree_lich_hoc = ttk.Treeview(frame_table, columns=cols, show="headings", height=12,
                                          style="LichThi.Treeview")

        vsb = ttk.Scrollbar(frame_table, orient="vertical", command=self.tree_lich_hoc.yview)
        vsb.pack(side="right", fill="y")
        self.tree_lich_hoc.configure(yscrollcommand=vsb.set)
        self.tree_lich_hoc.pack(side="left", fill="both", expand=True)

        self.tree_lich_hoc.tag_configure("evenrow", background="#1f2937")
        self.tree_lich_hoc.tag_configure("oddrow", background="#27272a")

        headers = [
            ("stt", "STT", 50),
            ("ten", "Tên học phần", 280),
            ("thu", "Thứ", 80),
            ("ca", "Ca học", 120),
            ("phong", "Phòng", 90),
            ("gv", "Giảng viên", 180),
            ("tuan", "Tuần học", 150)
        ]

        for c, t, w in headers:
            self.tree_lich_hoc.heading(c, text=t)
            self.tree_lich_hoc.column(c, width=w, anchor="w" if c in ["ten", "gv"] else "center")

        path = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "database", "ClassTime.csv"))

        if not os.path.exists(path):
            self.tree_lich_hoc.insert("", "end", values=("", "Không tìm thấy dữ liệu", "", "", "", "", ""))
            return

        try:
            stt = 1
            co_lich = False
            with open(path, "r", encoding="utf-8-sig") as f:
                reader = csv.reader(f)
                next(reader, None)
                for row in reader:
                    if len(row) >= 7 and row[0].strip() == self.current_user:
                        data_hien_thi = list(row[1:8])
                        while len(data_hien_thi) < 7:
                            data_hien_thi.append("")
                        tag = "evenrow" if stt % 2 == 0 else "oddrow"
                        self.tree_lich_hoc.insert("", "end", values=(stt, *data_hien_thi), tags=(tag,))
                        stt += 1
                        co_lich = True

            if not co_lich:
                self.tree_lich_hoc.insert("", "end", values=("", "Hiện chưa có thông tin lịch học", "", "", "", "", ""))

        except Exception as e:
            print(f"Lỗi đọc dữ liệu: {e}")

    def render_thong_tin_sinh_vien(self):
        path = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "database", "StudentInfo.csv"))
        info = None
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8-sig") as f:
                for row in csv.reader(f):
                    if len(row) >= 8 and row[0].strip() == self.current_user: info = row; break
        if info:
            khung = ctk.CTkFrame(self.khung_hien_thi_dong, fg_color="transparent")
            khung.pack(pady=10, padx=50, fill="both", expand=True)
            for i, lb in enumerate(
                    ["Mã SV:", "Họ và Tên:", "Ngày sinh:", "Giới tính:", "Lớp:", "Ngành học:", "Khóa:", "Quê quán:"]):
                ctk.CTkLabel(khung, text=lb, font=("Arial", 15, "bold"), text_color="#d1d5db").grid(row=i, column=0,
                                                                                                    sticky="e", padx=20,
                                                                                                    pady=12)
                ctk.CTkLabel(khung, text=info[i] if i < len(info) else "Trống", font=("Arial", 15),
                             text_color="white").grid(row=i, column=1, sticky="w", padx=20, pady=12)
        else:
            ctk.CTkLabel(self.khung_hien_thi_dong, text="CHƯA CÓ DỮ LIỆU", font=("Arial", 18, "bold"),
                         text_color="#ef4444").pack(pady=(40, 10))

    def render_lich_thi_sinh_vien(self):
        style = ttk.Style()
        style.configure("LichThi.Treeview", background="#27272a", foreground="#d1d5db", fieldbackground="#27272a",
                        borderwidth=0, rowheight=40, font=("Arial", 16))
        style.map('LichThi.Treeview', background=[('selected', '#3b82f6')])
        style.configure("LichThi.Treeview.Heading", background="#1f2937", foreground="#60a5fa",
                        font=("Arial", 18, "bold"), borderwidth=1)

        frame_table = ctk.CTkFrame(self.khung_hien_thi_dong, fg_color="transparent")
        frame_table.pack(fill="both", expand=True, padx=10, pady=10)

        self.tree_lich_thi = ttk.Treeview(frame_table,
                                          columns=("stt", "ten", "ngay", "ca", "gio", "lan", "dot", "sbd", "ten_phong",
                                                   "so_phong", "tp_thi", "hinh_thuc"), show="headings", height=12,
                                          style="LichThi.Treeview")

        vsb = ttk.Scrollbar(frame_table, orient="vertical", command=self.tree_lich_thi.yview)
        vsb.pack(side="right", fill="y")
        self.tree_lich_thi.configure(yscrollcommand=vsb.set)
        self.tree_lich_thi.pack(side="left", fill="both", expand=True)

        self.tree_lich_thi.tag_configure("evenrow", background="#1f2937")
        self.tree_lich_thi.tag_configure("oddrow", background="#27272a")

        for c, t, w in [("stt", "STT", 60), ("ten", "Tên HP", 280), ("ngay", "Ngày", 120), ("ca", "Ca", 70),
                        ("gio", "Giờ", 100), ("lan", "Lần", 70), ("dot", "Đợt", 70), ("sbd", "SBD", 70),
                        ("ten_phong", "Tên Phòng", 110), ("so_phong", "Số Phòng", 90), ("tp_thi", "TP thi", 100),
                        ("hinh_thuc", "Hình thức", 160)]:
            self.tree_lich_thi.heading(c, text=t)
            self.tree_lich_thi.column(c, width=w, anchor="w" if c == "ten" else "center")

        path = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "database", "Exam.csv"))
        try:
            with open(path, "r", encoding="utf-8-sig") as f:
                reader = csv.reader(f)
                next(reader, None)
                stt = 1
                for row in reader:
                    if len(row) >= 11 and row[0].strip() == self.current_user:
                        data_hien_thi = list(row[1:12])
                        while len(data_hien_thi) < 11:
                            data_hien_thi.append("")
                        tag = "evenrow" if stt % 2 == 0 else "oddrow"
                        self.tree_lich_thi.insert("", "end", values=(stt, *data_hien_thi), tags=(tag,))
                        stt += 1
        except Exception as e:
            print(f"Lỗi đọc file: {e}")

    def doi_mat_khau(self):
        self.thuc_su_an_dropdown()
        if not self.current_user: return
        win = ctk.CTkToplevel(self)
        win.title("Đổi Mật Khẩu")
        win.geometry("450x550")
        win.attributes("-topmost", True)
        win.grab_set()
        win.configure(fg_color="#18181b")

        con = ctk.CTkFrame(win, fg_color="transparent")
        con.pack(fill="both", expand=True, padx=20, pady=10)
        ctk.CTkLabel(con, text="TẠO MẬT KHẨU MỚI", font=("Arial", 18, "bold"), text_color="#10b981").pack(pady=(10, 10))

        ctk.CTkLabel(con, text="Số điện thoại:", text_color="#d1d5db", anchor="w").pack(fill="x", padx=10, pady=(10, 0))
        phone_entry = ctk.CTkEntry(con, width=300, fg_color="#27272a", placeholder_text="Nhập số điện thoại")
        phone_entry.pack(pady=(5, 10))

        ctk.CTkLabel(con, text="Email:", text_color="#d1d5db", anchor="w").pack(fill="x", padx=10, pady=(0, 0))
        email_entry = ctk.CTkEntry(con, width=300, fg_color="#27272a", placeholder_text="ví dụ: user@gmail.com")
        email_entry.pack(pady=(5, 10))

        ctk.CTkLabel(con, text="Mật khẩu mới:", text_color="#d1d5db", anchor="w").pack(fill="x", padx=10, pady=(0, 0))
        txt1 = ctk.CTkEntry(con, show="*", width=300, fg_color="#27272a", placeholder_text="Nhập mật khẩu mới")
        txt1.pack(pady=(5, 10))

        ctk.CTkLabel(con, text="Xác nhận mật khẩu:", text_color="#d1d5db", anchor="w").pack(fill="x", padx=10, pady=(0, 0))
        txt2 = ctk.CTkEntry(con, show="*", width=300, fg_color="#27272a", placeholder_text="Nhập lại mật khẩu mới")
        txt2.pack(pady=(5, 10))

        ctk.CTkLabel(con, text="Mã xác nhận SMS:", text_color="#d1d5db", anchor="w").pack(fill="x", padx=10, pady=(0, 0))
        sms_entry = ctk.CTkEntry(con, width=300, fg_color="#27272a", placeholder_text="Nhập mã (Demo: 1111)")
        sms_entry.pack(pady=(5, 10))

        def save():
            phone = phone_entry.get().strip()
            email = email_entry.get().strip()
            sms = sms_entry.get().strip()
            pw1 = txt1.get()
            pw2 = txt2.get()

            if not phone or not email or not sms or not pw1 or not pw2:
                from tkinter import messagebox
                messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin!", parent=win)
                return

            if pw1 != pw2:
                from tkinter import messagebox
                messagebox.showerror("Lỗi", "Mật khẩu xác nhận không khớp!", parent=win)
                return

            if sms != "1111":
                from tkinter import messagebox
                messagebox.showerror("Lỗi", "Mã SMS không hợp lệ (Demo: 1111)!", parent=win)
                return

            path = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "database", "account.csv"))
            data = []
            try:
                with open(path, "r", encoding="utf-8") as f:
                    for r in csv.reader(f):
                        if len(r) >= 2 and r[0] == self.current_user: r[1] = pw1
                        data.append(r)
                with open(path, "w", newline="", encoding="utf-8") as f:
                    csv.writer(f).writerows(data)
                
                from tkinter import messagebox
                messagebox.showinfo("Thành công", "Đổi mật khẩu thành công! Vui lòng đăng nhập lại.", parent=win)
                win.destroy()
                self.dang_xuat()
            except Exception as e:
                from tkinter import messagebox
                messagebox.showerror("Lỗi", f"Lỗi cập nhật mật khẩu: {e}", parent=win)

        btn_frame = ctk.CTkFrame(con, fg_color="transparent")
        btn_frame.pack(pady=20)
        
        ctk.CTkButton(btn_frame, text="Lưu", command=save, fg_color="#10b981", hover_color="#059669", cursor="hand2", width=120).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="Hủy", command=win.destroy, fg_color="#ef4444", hover_color="#dc2626", cursor="hand2", width=120).pack(side="left", padx=10)

    def hien_thi_dich_vu(self):
        self.xoa_noi_dung_cu()
        ctk.CTkLabel(self.khung_noi_dung, text="THÔNG TIN LIÊN HỆ PHÒNG ĐÀO TẠO", font=("Arial", 24, "bold"),
                     text_color="#f59e0b").pack(pady=(40, 10))
        ctk.CTkLabel(self.khung_noi_dung, text="Vui lòng liên hệ nếu sinh viên gặp vấn đề về học vụ hoặc hệ thống.",
                     font=("Arial", 15, "italic"), text_color="#9ca3af").pack(pady=(0, 30))

        info_frame = ctk.CTkFrame(self.khung_noi_dung, fg_color="#1f2937", corner_radius=15)
        info_frame.pack(fill="both", expand=True, padx=100, pady=10)

        thong_tin = [
            ("Địa chỉ trường:", "Số 258, Đường Chùa Náo, TP Hạ Long, Quảng Ninh"),
            ("Số điện thoại:", "0960 694 201"),
            ("Email hỗ trợ:", "phongdaotao@uhl.edu.vn")
        ]

        for tieu_de, noi_dung in thong_tin:
            dong = ctk.CTkFrame(info_frame, fg_color="transparent")
            dong.pack(fill="x", padx=40, pady=25)
            ctk.CTkLabel(dong, text=tieu_de, font=("Arial", 18, "bold"), text_color="#60a5fa", width=180,
                         anchor="w").pack(side="left")
            ctk.CTkLabel(dong, text=noi_dung, font=("Arial", 16), text_color="white", justify="left").pack(side="left",
                                                                                                           padx=20)