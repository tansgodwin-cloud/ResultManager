import customtkinter as ctk
from tkinter import messagebox
import csv
import os


class LoginFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#18181b")
        self.controller = controller

        lbl_login = ctk.CTkLabel(self, text="Đăng nhập hệ thống", font=("Arial", 24, "bold"), text_color="#60a5fa")
        lbl_login.place(x=85, y=20)

        user_name = ctk.CTkLabel(self, text="Username: ", font=("Arial", 13), text_color="#d1d5db")
        user_name.place(x=30, y=80)
        self.entry_username = ctk.CTkEntry(self, width=250, height=35, corner_radius=10, fg_color="#27272a",
                                           border_color="#3f3f46", text_color="white")
        self.entry_username.place(x=100, y=80)

        password = ctk.CTkLabel(self, text="Password: ", font=("Arial", 13), text_color="#d1d5db")
        password.place(x=30, y=130)
        self.entry_password = ctk.CTkEntry(self, show="*", width=250, height=35, corner_radius=10, fg_color="#27272a",
                                           border_color="#3f3f46", text_color="white")
        self.entry_password.place(x=100, y=130)

        tk_role_lbl = ctk.CTkLabel(self, text="Vai trò:", font=("Arial", 13), text_color="#d1d5db")
        tk_role_lbl.place(x=30, y=178)

        self.role_var = ctk.StringVar(value="User")
        radio_user = ctk.CTkRadioButton(self, text="Người dùng", variable=self.role_var, value="User",
                                        text_color="white")
        radio_user.place(x=100, y=180)

        radio_admin = ctk.CTkRadioButton(self, text="Quản lý", variable=self.role_var, value="Admin",
                                         text_color="white")
        radio_admin.place(x=250, y=180)

        btn = ctk.CTkButton(self, text="Đăng nhập", command=self.xu_ly_login, width=250, height=40, corner_radius=20,
                            font=("Arial", 15, "bold"), fg_color="#3b82f6", hover_color="#2563eb")
        btn.place(x=95, y=240)

        sign_up = ctk.CTkLabel(self, text="Chưa có tài khoản? Đăng ký ngay", text_color="#60a5fa", cursor="hand2",
                               font=("Arial", 13, "bold", "underline"))
        sign_up.place(x=110, y=300)
        sign_up.bind("<Button-1>", lambda event: self.controller.show_frame("RegisterFrame"))

    def kiem_tra_tren_csv(self, tai_khoan_nhap, mat_khau_nhap):
        # Đã fix lại đường dẫn cho đỡ ngáo
        thu_muc_hien_tai = os.path.dirname(os.path.abspath(__file__))
        ten_file = os.path.normpath(os.path.join(thu_muc_hien_tai, "..", "database", "account.csv"))

        if not os.path.isfile(ten_file):
            messagebox.showerror("Lỗi hệ thống", f"Không tìm thấy database!\n{ten_file}")
            return None

        with open(ten_file, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader, None)
            for row in reader:
                if len(row) >= 3:
                    csv_user = row[0].strip()
                    csv_pass = row[1].strip()
                    csv_role = row[2].strip()

                    if tai_khoan_nhap == csv_user and mat_khau_nhap == csv_pass:
                        return csv_role
        return None

    def xu_ly_login(self):
        tk_hien_tai = self.entry_username.get().strip()
        mk_hien_tai = self.entry_password.get().strip()
        vai_tro_chon = self.role_var.get()

        if not tk_hien_tai or not mk_hien_tai:
            messagebox.showwarning("Cảnh báo", "Vui Lòng Điền Đầy Đủ Thông Tin!")
            return

        vai_tro_thuc_te = self.kiem_tra_tren_csv(tk_hien_tai, mk_hien_tai)

        if vai_tro_thuc_te:
            if vai_tro_chon == "Admin":
                if vai_tro_thuc_te == "Admin":
                    messagebox.showinfo("Thành công",
                                        f"Đăng nhập quyền Quản trị thành công!\nXin chào Sếp {tk_hien_tai}.")

                    admin_frame = self.controller.frames["AdminFrame"]
                    admin_frame.load_data_va_giao_dien(tk_hien_tai)

                    self.controller.show_frame("AdminFrame")

                    self.entry_username.delete(0, ctk.END)
                    self.entry_password.delete(0, ctk.END)
                else:
                    messagebox.showerror("Từ chối truy cập", "Tài khoản của bạn không có quyền Quản trị!")
            else:
                # ĐÂY NÀY BRUH!!! KHÚC CODE BỊ MÀY THIẾN MẤT LÀ Ở ĐÂY NÀY!
                messagebox.showinfo("Thành công", f"Đăng nhập tài khoản thành công!")

                home_frame = self.controller.frames["HomeFrame"]
                home_frame.load_data_va_giao_dien(tk_hien_tai)

                self.controller.show_frame("HomeFrame")

                self.entry_username.delete(0, ctk.END)
                self.entry_password.delete(0, ctk.END)
        else:
            messagebox.showerror("Lỗi", "Sai mật khẩu hoặc tài khoản!")
