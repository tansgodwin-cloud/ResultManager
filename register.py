import customtkinter as ctk
from tkinter import messagebox
import csv
import os


class RegisterFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#18181b")  # Màu nền Xám than đồng bộ
        self.controller = controller

        # --- KHUNG GIAO DIỆN CHÍNH ---
        khung_chinh = ctk.CTkFrame(self, fg_color="#27272a", corner_radius=15, border_width=1, border_color="#3f3f46")
        khung_chinh.pack(fill="both", expand=True, padx=40, pady=20)

        ctk.CTkLabel(khung_chinh, text="TẠO TÀI KHOẢN MỚI", font=("Arial", 22, "bold"), text_color="#60a5fa").pack(
            pady=(20, 5))
        ctk.CTkLabel(khung_chinh, text="Vui lòng điền đầy đủ thông tin bên dưới", font=("Arial", 13),
                     text_color="#9ca3af").pack(pady=(0, 20))

        # --- HÀM TẠO Ô NHẬP LIỆU CHO NHANH ---
        def tao_o_nhap(tieu_de, an_chu=False, placeholder=""):
            ctk.CTkLabel(khung_chinh, text=tieu_de, font=("Arial", 13, "bold"), text_color="#d1d5db").pack(anchor="w",
                                                                                                           padx=40)
            o_nhap = ctk.CTkEntry(khung_chinh, font=("Arial", 14), width=320, height=35,
                                  fg_color="#18181b", border_color="#3f3f46", text_color="white",
                                  placeholder_text=placeholder, placeholder_text_color="#4b5563",
                                  show="*" if an_chu else "")
            o_nhap.pack(pady=(5, 12))
            return o_nhap

        self.txt_user = tao_o_nhap("Tên đăng nhập (Mã SV):")
        self.txt_pass = tao_o_nhap("Mật khẩu:", an_chu=True)
        self.txt_pass2 = tao_o_nhap("Xác nhận mật khẩu:", an_chu=True)
        self.txt_email = tao_o_nhap("Địa chỉ Email:", placeholder="VD: gaysech@uhl.edu.vn")

        ctk.CTkLabel(khung_chinh, text="Số điện thoại:", font=("Arial", 13, "bold"), text_color="#d1d5db").pack(
            anchor="w", padx=40)
        self.txt_phone = ctk.CTkEntry(khung_chinh, font=("Arial", 14), width=320, height=35, fg_color="#18181b",
                                      border_color="#3f3f46", text_color="white")
        self.txt_phone.pack(pady=(5, 20))

        # --- NÚT BẤM ĐĂNG KÝ ---
        btn_dang_ky = ctk.CTkButton(khung_chinh, text="ĐĂNG KÝ", font=("Arial", 15, "bold"),
                                    fg_color="#10b981", hover_color="#059669", text_color="white",
                                    height=40, width=320, command=self.xu_ly_dang_ky)
        btn_dang_ky.pack(pady=(0, 15))

        # --- QUAY LẠI ĐĂNG NHẬP (Xài Bộ Đàm, Đéo Xài Subprocess) ---
        khung_chuyen = ctk.CTkFrame(khung_chinh, fg_color="transparent")
        khung_chuyen.pack()
        btn_dang_nhap = ctk.CTkButton(khung_chuyen, text="Đã có tài khoản? Đăng nhập ngay", font=("Arial", 13, "bold","underline"),
                                      text_color="#60a5fa", fg_color="transparent", hover_color="#3f3f46",
                                      width=100, command=lambda: self.controller.show_frame("LoginFrame"))
        btn_dang_nhap.pack(side="left")

    # --- XỬ LÝ LOGIC ---
    def xu_ly_dang_ky(self):
        user = self.txt_user.get().strip()
        mat_khau = self.txt_pass.get()
        xac_nhan = self.txt_pass2.get()
        email = self.txt_email.get().strip()
        phone = self.txt_phone.get().strip()

        if not user or not mat_khau or not xac_nhan or not email or not phone:
            messagebox.showerror("Lỗi", "Vui lòng điền đầy đủ tất cả các trường thông tin!")
            return

        if mat_khau != xac_nhan:
            messagebox.showerror("Lỗi", "Xác nhận mật khẩu không khớp! Tay run à?")
            return

        # Đường dẫn tới account.csv
        thu_muc_hien_tai = os.path.dirname(os.path.abspath(__file__))
        duong_dan_csv = os.path.normpath(os.path.join(thu_muc_hien_tai, "..", "database", "../Database/account.csv"))
        os.makedirs(os.path.dirname(duong_dan_csv), exist_ok=True)

        # Kiểm tra trùng lặp
        if os.path.exists(duong_dan_csv):
            try:
                with open(duong_dan_csv, mode='r', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    for row in reader:
                        if len(row) > 0 and row[0].strip().lower() == user.lower():
                            messagebox.showwarning("Trùng lặp", f"Tên đăng nhập '{user}' đã có người lụm rồi ba!")
                            return
            except Exception:
                pass

        # Ghi vào file với 5 CỘT
        file_exists = os.path.exists(duong_dan_csv)
        try:
            with open(duong_dan_csv, mode='a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                if not file_exists:
                    # Ghi Header nếu file chưa tồn tại
                    writer.writerow(['Tài Khoản', 'Mật Khẩu', 'Vai Trò', 'Email', 'Số điện thoại'])

                # Mặc định Vai Trò là "User"
                writer.writerow([user, mat_khau, "User", email, phone])

            messagebox.showinfo("Thành công", "Đăng ký thành công! Chuyển về màn hình đăng nhập...")

            # Xóa trắng ô nhập liệu sau khi đăng ký xong
            for txt in (self.txt_user, self.txt_pass, self.txt_pass2, self.txt_email, self.txt_phone):
                txt.delete(0, 'end')

            self.controller.show_frame("LoginFrame")

        except Exception as e:
            messagebox.showerror("Lỗi hệ thống", f"Không thể lưu tài khoản. Lỗi: {e}")
