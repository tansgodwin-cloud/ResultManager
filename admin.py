import customtkinter as ctk
from tkinter import ttk, messagebox
import csv
import os

class AdminFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#0f1115")
        self.controller = controller
        self.current_admin = None
        self.user_dang_chon = ctk.StringVar(value="")
        self.dung_giao_dien()

    def load_data_va_giao_dien(self, username):
        self.current_admin = username
        self.user_dang_chon.set("")
        self.dung_giao_dien()

    def dung_giao_dien(self):
        current_tab = None
        if hasattr(self, "tabview"):
            try:
                current_tab = self.tabview.get()
            except Exception:
                pass

        for widget in self.winfo_children():
            widget.destroy()

        khung_header = ctk.CTkFrame(self, fg_color="#1a1d24", corner_radius=0, height=60)
        khung_header.pack(fill="x")
        khung_header.pack_propagate(False)

        ten_sep = self.current_admin if self.current_admin else "Ẩn danh"
        ctk.CTkLabel(khung_header, text=f"QUẢN TRỊ HỆ THỐNG - {ten_sep.upper()}",
                     font=("Segoe UI", 22, "bold"), text_color="#38bdf8").pack(side="left", padx=20)

        btn_logout = ctk.CTkButton(khung_header, text="Đăng xuất", fg_color="#ef4444", hover_color="#b91c1c",
                                   font=("Segoe UI", 13, "bold"), width=100, height=32, corner_radius=6, cursor="hand2",
                                   command=self.dang_xuat)
        btn_logout.pack(side="right", padx=20)

        self.tabview = ctk.CTkTabview(self, fg_color="#14161b", segmented_button_fg_color="#1a1d24",
                                      segmented_button_selected_color="#0ea5e9",
                                      segmented_button_selected_hover_color="#0284c7",
                                      text_color="#94a3b8")
        self.tabview.pack(fill="both", expand=True, padx=20, pady=20)

        self.tab_acc = self.tabview.add("Quản lý Tài khoản")
        self.tab_grade = self.tabview.add("Quản lý Điểm")
        self.tab_schedule = self.tabview.add("Quản lý Lịch Học")

        self.setup_tab_taikhoan()
        self.setup_tab_diem()
        self.setup_tab_lichhoc()

        if current_tab:
            try:
                self.tabview.set(current_tab)
            except Exception:
                pass

    def setup_tab_taikhoan(self):
        khung_chinh = ctk.CTkFrame(self.tab_acc, fg_color="transparent")
        khung_chinh.pack(fill="both", expand=True, pady=(10, 0))

        khung_trai = ctk.CTkFrame(khung_chinh, fg_color="#1a1d24", corner_radius=12)
        khung_trai.pack(side="left", fill="both", expand=True, padx=(0, 20))

        khung_title = ctk.CTkFrame(khung_trai, fg_color="transparent")
        khung_title.pack(fill="x", padx=20, pady=(20, 10))
        ctk.CTkLabel(khung_title, text="DANH SÁCH NGƯỜI DÙNG", font=("Segoe UI", 18, "bold"), text_color="#e2e8f0").pack(side="left")

        khung_head_bang = ctk.CTkFrame(khung_trai, fg_color="#272a33", corner_radius=8, height=40)
        khung_head_bang.pack(fill="x", padx=20, pady=(0, 10))
        khung_head_bang.pack_propagate(False)
        
        ctk.CTkLabel(khung_head_bang, text="Tài Khoản", width=150, font=("Segoe UI", 14, "bold"), text_color="#cbd5e1", anchor="w").pack(side="left", padx=20)
        ctk.CTkLabel(khung_head_bang, text="Vai Trò", width=100, font=("Segoe UI", 14, "bold"), text_color="#cbd5e1").pack(side="left")
        ctk.CTkLabel(khung_head_bang, text="Thao Tác", width=100, font=("Segoe UI", 14, "bold"), text_color="#cbd5e1").pack(side="right", padx=20)

        self.bang_danh_sach = ctk.CTkScrollableFrame(khung_trai, fg_color="transparent")
        self.bang_danh_sach.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        khung_phai = ctk.CTkFrame(khung_chinh, fg_color="#1a1d24", corner_radius=12, width=300)
        khung_phai.pack(side="right", fill="y")
        khung_phai.pack_propagate(False)

        ctk.CTkLabel(khung_phai, text="BẢNG ĐIỀU KHIỂN", font=("Segoe UI", 18, "bold"), text_color="#e2e8f0").pack(pady=(20, 30))
        
        info_frame = ctk.CTkFrame(khung_phai, fg_color="#272a33", corner_radius=8)
        info_frame.pack(fill="x", padx=20, pady=(0, 30))
        
        ctk.CTkLabel(info_frame, text="Tài khoản đang chọn", font=("Segoe UI", 12), text_color="#94a3b8").pack(pady=(15, 5))
        lbl_muc_tieu = ctk.CTkLabel(info_frame, textvariable=self.user_dang_chon, font=("Segoe UI", 20, "bold"), text_color="#fbbf24")
        lbl_muc_tieu.pack(pady=(0, 15))

        btn_admin = ctk.CTkButton(khung_phai, text="Cấp quyền Admin", fg_color="#059669", hover_color="#047857",
                                  font=("Segoe UI", 14, "bold"), height=35, cursor="hand2", command=lambda: self.thay_doi_quyen("Admin"))
        btn_admin.pack(fill="x", padx=20, pady=(0, 15))
        
        btn_user = ctk.CTkButton(khung_phai, text="Chuyển thành User", fg_color="#d97706", hover_color="#b45309",
                                 font=("Segoe UI", 14, "bold"), height=35, cursor="hand2", command=lambda: self.thay_doi_quyen("User"))
        btn_user.pack(fill="x", padx=20, pady=(0, 15))
        
        btn_del = ctk.CTkButton(khung_phai, text="Xóa tài khoản", fg_color="#dc2626", hover_color="#991b1b",
                                font=("Segoe UI", 14, "bold"), height=35, cursor="hand2", command=self.xoa_tai_khoan)
        btn_del.pack(fill="x", padx=20, pady=(40, 0))

        self.load_acc_list()

    def load_acc_list(self):
        for widget in self.bang_danh_sach.winfo_children(): widget.destroy()
        duong_dan_csv = self.lay_path_acc()
        if not os.path.exists(duong_dan_csv): return

        try:
            with open(duong_dan_csv, mode='r', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader, None)
                for row in reader:
                    if len(row) >= 3:
                        user = row[0].strip()
                        role = row[2].strip()
                        dong = ctk.CTkFrame(self.bang_danh_sach, fg_color="#272a33", corner_radius=8, height=45)
                        dong.pack(fill="x", pady=(0, 8))
                        dong.pack_propagate(False)
                        
                        ctk.CTkLabel(dong, text=user, width=150, anchor="w", font=("Segoe UI", 14), text_color="#f8fafc").pack(side="left", padx=20)
                        
                        color_role = "#fbbf24" if role == "Admin" else "#34d399"
                        ctk.CTkLabel(dong, text=role, width=100, text_color=color_role, font=("Segoe UI", 14, "bold")).pack(side="left")
                        
                        ctk.CTkButton(dong, text="Chọn", width=80, height=28, fg_color="#3b82f6", hover_color="#2563eb",
                                      font=("Segoe UI", 12, "bold"), corner_radius=6, cursor="hand2",
                                      command=lambda u=user: self.user_dang_chon.set(u)).pack(side="right", padx=20)
        except Exception:
            pass

    def lay_path_acc(self):
        return os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "database", "account.csv"))

    def thay_doi_quyen(self, quyen_moi):
        muc_tieu = self.user_dang_chon.get()
        if not muc_tieu:
            messagebox.showwarning("Nhắc nhở", "Ê, chọn một tài khoản từ danh sách đã chứ!")
            return
        if muc_tieu == self.current_admin:
            messagebox.showerror("Từ chối thao tác", "Định tự giáng chức mình à? Bớt rảnh đi cu!")
            return

        duong_dan = self.lay_path_acc()
        du_lieu = []
        try:
            with open(duong_dan, "r", encoding="utf-8") as f:
                for row in csv.reader(f):
                    if len(row) >= 3 and row[0] == muc_tieu: row[2] = quyen_moi
                    du_lieu.append(row)
            with open(duong_dan, "w", newline="", encoding="utf-8") as f:
                csv.writer(f).writerows(du_lieu)
            messagebox.showinfo("Thành công", f"Đã cập nhật quyền {quyen_moi} cho '{muc_tieu}'.")
            self.load_acc_list()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Toang DB rồi: {e}")

    def xoa_tai_khoan(self):
        muc_tieu = self.user_dang_chon.get()
        if not muc_tieu: return
        if muc_tieu == self.current_admin:
            messagebox.showerror("Từ chối", "Tự tay bóp dái à? Đéo cho xóa chính mình nhé!")
            return
        if not messagebox.askyesno("Xác nhận", f"Cho thanh niên '{muc_tieu}' này đăng xuất khỏi hệ thống luôn?"): return

        duong_dan = self.lay_path_acc()
        du_lieu = []
        try:
            with open(duong_dan, "r", encoding="utf-8") as f:
                for row in csv.reader(f):
                    if len(row) > 0 and row[0] != muc_tieu: du_lieu.append(row)
            with open(duong_dan, "w", newline="", encoding="utf-8") as f:
                csv.writer(f).writerows(du_lieu)
            self.user_dang_chon.set("")
            self.load_acc_list()
            messagebox.showinfo("Thành công", f"Đã tiễn '{muc_tieu}' ra chuồng gà.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi cmnr: {e}")

    def dang_xuat(self):
        self.current_admin = None
        self.user_dang_chon.set("")
        self.controller.show_frame("LoginFrame")

    def setup_tab_diem(self):
        khung_top = ctk.CTkFrame(self.tab_grade, fg_color="transparent")
        khung_top.pack(fill="x", pady=(10, 15))

        khung_tim_kiem = ctk.CTkFrame(khung_top, fg_color="#1a1d24", corner_radius=10, height=60)
        khung_tim_kiem.pack(side="left", fill="x", expand=True)
        khung_tim_kiem.pack_propagate(False)

        ctk.CTkLabel(khung_tim_kiem, text="Tìm Sinh Viên:", font=("Segoe UI", 13, "bold"), text_color="#cbd5e1").pack(side="left", padx=(20, 10))
        
        self.entry_tim_kiem = ctk.CTkEntry(khung_tim_kiem, width=280, height=35, placeholder_text="Nhập mã SV cần tìm...",
                                           font=("Segoe UI", 13), fg_color="#272a33", text_color="#f8fafc", border_width=1, border_color="#3f3f46")
        self.entry_tim_kiem.pack(side="left", padx=10)

        ctk.CTkButton(khung_tim_kiem, text="Tìm kiếm", fg_color="#0ea5e9", hover_color="#0284c7", 
                      font=("Segoe UI", 13, "bold"), height=35, width=120, cursor="hand2", command=self.tim_kiem_diem).pack(side="left", padx=10)
        ctk.CTkButton(khung_tim_kiem, text="Làm mới", fg_color="#475569", hover_color="#334155", 
                      font=("Segoe UI", 13, "bold"), height=35, width=120, cursor="hand2", command=self.hien_tat_ca_diem).pack(side="left")

        khung_chinh = ctk.CTkFrame(self.tab_grade, fg_color="transparent")
        khung_chinh.pack(fill="both", expand=True)

        khung_bang = ctk.CTkFrame(khung_chinh, fg_color="#1a1d24", corner_radius=12)
        khung_bang.pack(fill="both", expand=True, pady=(0, 20))

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#272a33", foreground="#f8fafc", fieldbackground="#272a33",
                        borderwidth=0, rowheight=40, font=("Segoe UI", 16))
        style.map('Treeview', background=[('selected', '#0ea5e9')])
        style.configure("Treeview.Heading", background="#1e293b", foreground="#38bdf8", font=("Segoe UI", 18, "bold"),
                        borderwidth=0, padding=10)

        cols = ("msv", "kh", "ten", "tc", "tp", "thi", "he10", "he4", "chu", "gc", "tuchon")
        self.tree_grade = ttk.Treeview(khung_bang, columns=cols, show="headings")

        self.tree_grade.tag_configure("evenrow", background="#1e293b")
        self.tree_grade.tag_configure("oddrow", background="#272a33")

        vsb = ttk.Scrollbar(khung_bang, orient="vertical", command=self.tree_grade.yview)
        vsb.pack(side="right", fill="y", pady=10, padx=(0, 10))
        self.tree_grade.configure(yscrollcommand=vsb.set)
        self.tree_grade.pack(fill="both", expand=True, padx=(10, 0), pady=10)

        heads = [("msv", "Mã SV", 120), ("kh", "Môn", 100), ("ten", "Tên Môn Học", 250), ("tc", "TC", 70),
                 ("tp", "Quá Trình", 120), ("thi", "Cuối Kỳ", 120), ("he10", "Hệ 10", 100), ("he4", "Hệ 4", 100),
                 ("chu", "Chữ", 80), ("gc", "Ghi chú", 120), ("tuchon", "Tự chọn", 100)]
        for c, h, w in heads:
            self.tree_grade.heading(c, text=h)
            self.tree_grade.column(c, width=w, anchor="center")

        self.tree_grade.bind("<<TreeviewSelect>>", self.on_grade_select)

        khung_nhap = ctk.CTkFrame(khung_chinh, fg_color="#1a1d24", corner_radius=12)
        khung_nhap.pack(fill="x")

        khung_form = ctk.CTkFrame(khung_nhap, fg_color="transparent")
        khung_form.pack(side="left", padx=20, pady=20)

        self.inputs = {}
        fields = [("Mã SV:", "msv", 0, 0), ("Mã Môn:", "kh", 0, 2), ("Tên Môn Học:", "ten", 0, 4),
                  ("Tín Chỉ:", "tc", 1, 0), ("Quá Trình:", "tp", 1, 2), ("Cuối Kỳ:", "thi", 1, 4),
                  ("Hệ 10 (Auto):", "he10", 2, 0), ("Hệ 4 (Auto):", "he4", 2, 2), ("Điểm Chữ (Auto):", "chu", 2, 4),
                  ("Ghi Chú:", "gc", 3, 0), ("Tự Chọn:", "tuchon", 3, 2)]

        for lb, key, r, c in fields:
            ctk.CTkLabel(khung_form, text=lb, font=("Segoe UI", 14, "bold"), text_color="#cbd5e1").grid(row=r, column=c, padx=(15, 5), pady=8, sticky="e")
            en = ctk.CTkEntry(khung_form, width=180, height=35, font=("Segoe UI", 14), fg_color="#272a33", 
                              border_color="#3f3f46", text_color="#f8fafc", corner_radius=6)
            en.grid(row=r, column=c + 1, padx=5, pady=8, sticky="w")
            
            if key in ["he10", "he4", "chu"]:
                en.configure(state="disabled", fg_color="#1e293b", text_color="#94a3b8")
                
            self.inputs[key] = en

        khung_nut = ctk.CTkFrame(khung_nhap, fg_color="transparent")
        khung_nut.pack(side="right", padx=30, pady=20)
        
        ctk.CTkButton(khung_nut, text="Thêm Mới", fg_color="#059669", hover_color="#047857", 
                      font=("Segoe UI", 13, "bold"), height=40, width=140, cursor="hand2", command=self.them_diem).pack(pady=(0, 10))
        ctk.CTkButton(khung_nut, text="Cập Nhật", fg_color="#0ea5e9", hover_color="#0284c7", 
                      font=("Segoe UI", 13, "bold"), height=40, width=140, cursor="hand2", command=self.sua_diem).pack(pady=10)
        ctk.CTkButton(khung_nut, text="Xóa Điểm", fg_color="#dc2626", hover_color="#991b1b", 
                      font=("Segoe UI", 13, "bold"), height=40, width=140, cursor="hand2", command=self.xoa_diem).pack(pady=10)
        ctk.CTkButton(khung_nut, text="Làm Mới Form", fg_color="#475569", hover_color="#334155", 
                      font=("Segoe UI", 13, "bold"), height=40, width=140, cursor="hand2", command=self.clear_inputs).pack(pady=(10, 0))

        self.load_grade_list()

    def tinh_diem_tu_dong(self, tp_str, thi_str):
        try:
            tp = float(tp_str)
            thi = float(thi_str)
            he10 = round((tp * 0.4) + (thi * 0.6), 2)
            if he10 >= 8.5: return he10, 4.0, "A"
            elif he10 >= 7.0: return he10, 3.0, "B"
            elif he10 >= 5.5: return he10, 2.0, "C"
            elif he10 >= 4.0: return he10, 1.0, "D"
            else: return he10, 0.0, "F"
        except ValueError:
            return 0.0, 0.0, "F"

    def tim_kiem_diem(self):
        tu_khoa = self.entry_tim_kiem.get().strip().lower()
        self.load_grade_list(tu_khoa)

    def hien_tat_ca_diem(self):
        self.entry_tim_kiem.delete(0, 'end')
        self.load_grade_list("")

    def lay_path_subject(self):
        return os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'database', 'Subject.csv'))

    def load_grade_list(self, tu_khoa=""):
        for item in self.tree_grade.get_children(): self.tree_grade.delete(item)
        path = self.lay_path_subject()
        if not os.path.exists(path): return
        try:
            with open(path, "r", encoding="utf-8-sig") as f:
                reader = csv.reader(f)
                next(reader, None)
                stt = 1
                for row in reader:
                    if len(row) >= 11:
                        if tu_khoa == "" or tu_khoa in row[0].strip().lower():
                            tag = "evenrow" if stt % 2 == 0 else "oddrow"
                            self.tree_grade.insert("", "end", values=row[:11], tags=(tag,))
                            stt += 1
        except Exception:
            pass

    def on_grade_select(self, event):
        selected = self.tree_grade.selection()
        if not selected: return
        val = self.tree_grade.item(selected[0])['values']
        keys = ["msv", "kh", "ten", "tc", "tp", "thi", "he10", "he4", "chu", "gc", "tuchon"]
        for i, k in enumerate(keys):
            tam_khoa = self.inputs[k].cget("state") == "disabled"
            if tam_khoa: self.inputs[k].configure(state="normal")
            
            self.inputs[k].delete(0, 'end')
            if i < len(val): self.inputs[k].insert(0, val[i])
            
            if tam_khoa: self.inputs[k].configure(state="disabled")

    def clear_inputs(self):
        for k, en in self.inputs.items(): 
            tam_khoa = en.cget("state") == "disabled"
            if tam_khoa: en.configure(state="normal")
            en.delete(0, 'end')
            if tam_khoa: en.configure(state="disabled")
            
        self.inputs["msv"].focus()
        for item in self.tree_grade.selection(): self.tree_grade.selection_remove(item)

    def them_diem(self):
        msv = self.inputs["msv"].get().strip()
        kh = self.inputs["kh"].get().strip()
        if not msv or not kh:
            messagebox.showwarning("Lỗi", "Bắt buộc nhập Mã SV và Mã Môn nhé bro!")
            return

        tp = self.inputs["tp"].get().strip()
        thi = self.inputs["thi"].get().strip()
        
        try:
            float(tp)
            float(thi)
        except ValueError:
            messagebox.showwarning("Lỗi", "Quá trình với Cuối kỳ phải là số, m định nhập chữ cái à?")
            return

        he10, he4, chu = self.tinh_diem_tu_dong(tp, thi)
        
        row_data = [msv, kh, self.inputs["ten"].get().strip(), self.inputs["tc"].get().strip(),
                    tp, thi, str(he10), str(he4), chu, 
                    self.inputs["gc"].get().strip(), self.inputs["tuchon"].get().strip()]

        path = self.lay_path_subject()
        exists = os.path.exists(path)
        try:
            with open(path, "a", newline="", encoding="utf-8-sig") as f:
                writer = csv.writer(f)
                if not exists: writer.writerow(
                    ["Mã SV", "Ký hiệu", "Tên học phần", "Tín chỉ", "Điểm TP", "Điểm thi", "TBCHP", "Điểm số",
                     "Điểm chữ", "Ghi chú", "Môn tự chọn"])
                writer.writerow(row_data)
            self.load_grade_list(self.entry_tim_kiem.get().strip().lower())
            self.clear_inputs()
            messagebox.showinfo("Thành công", f"Đã chốt sổ điểm cho {msv}.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Toang: {e}")

    def sua_diem(self):
        sel = self.tree_grade.selection()
        if not sel:
            messagebox.showwarning("Lỗi", "Chọn dòng nào trên bảng để sửa đi cu!");
            return

        old_msv = str(self.tree_grade.item(sel[0])['values'][0]).strip()
        old_kh = str(self.tree_grade.item(sel[0])['values'][1]).strip()
        
        tp = self.inputs["tp"].get().strip()
        thi = self.inputs["thi"].get().strip()
        try:
            float(tp)
            float(thi)
        except ValueError:
            messagebox.showwarning("Lỗi", "Điểm thì phải là số!")
            return

        he10, he4, chu = self.tinh_diem_tu_dong(tp, thi)
        
        new_row = [self.inputs["msv"].get().strip(), self.inputs["kh"].get().strip(), 
                   self.inputs["ten"].get().strip(), self.inputs["tc"].get().strip(),
                   tp, thi, str(he10), str(he4), chu, 
                   self.inputs["gc"].get().strip(), self.inputs["tuchon"].get().strip()]

        path = self.lay_path_subject()
        all_data = []
        try:
            with open(path, "r", encoding="utf-8-sig") as f:
                reader = list(csv.reader(f))
                header = reader[0]
                for r in reader[1:]:
                    if len(r) >= 2 and r[0].strip() == old_msv and r[1].strip() == old_kh:
                        all_data.append(new_row)
                    else:
                        all_data.append(r)
            with open(path, "w", newline="", encoding="utf-8-sig") as f:
                writer = csv.writer(f)
                writer.writerow(header)
                writer.writerows(all_data)
            self.load_grade_list(self.entry_tim_kiem.get().strip().lower())
            self.on_grade_select(None)
            messagebox.showinfo("Thành công", "Đã fix điểm thành công.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi cmnr: {e}")

    def xoa_diem(self):
        sel = self.tree_grade.selection()
        if not sel:
            messagebox.showwarning("Lỗi", "Chọn 1 dòng trên bảng để xóa!");
            return

        if not messagebox.askyesno("Xác nhận", "Chắc chắn muốn cho môn này đăng xuất khỏi thanh xuân của em nó chứ?"): return

        old_msv = str(self.tree_grade.item(sel[0])['values'][0]).strip()
        old_kh = str(self.tree_grade.item(sel[0])['values'][1]).strip()

        path = self.lay_path_subject()
        all_data = []
        try:
            with open(path, "r", encoding="utf-8-sig") as f:
                reader = list(csv.reader(f))
                header = reader[0]
                for r in reader[1:]:
                    if len(r) >= 2 and r[0].strip() == old_msv and r[1].strip() == old_kh: continue
                    all_data.append(r)
            with open(path, "w", newline="", encoding="utf-8-sig") as f:
                writer = csv.writer(f)
                writer.writerow(header)
                writer.writerows(all_data)
            self.load_grade_list(self.entry_tim_kiem.get().strip().lower())
            self.clear_inputs()
            messagebox.showinfo("Thành công", "Đã bay màu môn học!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi DB: {e}")

    # ================= QUẢN LÝ LỊCH HỌC (TÁCH RIÊNG NHÉ BA) =================
    def setup_tab_lichhoc(self):
        khung_top = ctk.CTkFrame(self.tab_schedule, fg_color="transparent")
        khung_top.pack(fill="x", pady=(10, 15))

        khung_tim_kiem = ctk.CTkFrame(khung_top, fg_color="#1a1d24", corner_radius=10, height=60)
        khung_tim_kiem.pack(side="left", fill="x", expand=True)
        khung_tim_kiem.pack_propagate(False)

        ctk.CTkLabel(khung_tim_kiem, text="Tìm Sinh Viên:", font=("Segoe UI", 13, "bold"), text_color="#cbd5e1").pack(side="left", padx=(20, 10))
        
        self.entry_tim_lich = ctk.CTkEntry(khung_tim_kiem, width=280, height=35, placeholder_text="Nhập mã SV cần tìm...",
                                           font=("Segoe UI", 13), fg_color="#272a33", text_color="#f8fafc", border_width=1, border_color="#3f3f46")
        self.entry_tim_lich.pack(side="left", padx=10)

        ctk.CTkButton(khung_tim_kiem, text="Tìm kiếm", fg_color="#0ea5e9", hover_color="#0284c7", 
                      font=("Segoe UI", 13, "bold"), height=35, width=120, cursor="hand2", command=self.tim_kiem_lich).pack(side="left", padx=10)
        ctk.CTkButton(khung_tim_kiem, text="Làm mới", fg_color="#475569", hover_color="#334155", 
                      font=("Segoe UI", 13, "bold"), height=35, width=120, cursor="hand2", command=self.hien_tat_ca_lich).pack(side="left")

        khung_chinh = ctk.CTkFrame(self.tab_schedule, fg_color="transparent")
        khung_chinh.pack(fill="both", expand=True)

        khung_bang = ctk.CTkFrame(khung_chinh, fg_color="#1a1d24", corner_radius=12)
        khung_bang.pack(fill="both", expand=True, pady=(0, 20))

        cols = ("msv", "ten", "thu", "ca", "phong", "gv", "tuan")
        self.tree_schedule = ttk.Treeview(khung_bang, columns=cols, show="headings")
        self.tree_schedule.tag_configure("evenrow", background="#1e293b")
        self.tree_schedule.tag_configure("oddrow", background="#272a33")

        vsb = ttk.Scrollbar(khung_bang, orient="vertical", command=self.tree_schedule.yview)
        vsb.pack(side="right", fill="y", pady=10, padx=(0, 10))
        self.tree_schedule.configure(yscrollcommand=vsb.set)
        self.tree_schedule.pack(fill="both", expand=True, padx=(10, 0), pady=10)

        heads = [("msv", "Mã SV", 120), ("ten", "Tên Môn Học", 250), ("thu", "Thứ", 80),
                 ("ca", "Ca Học", 120), ("phong", "Phòng", 100), ("gv", "Giảng Viên", 200), ("tuan", "Tuần Học", 150)]
        for c, h, w in heads:
            self.tree_schedule.heading(c, text=h)
            self.tree_schedule.column(c, width=w, anchor="center" if c not in ["ten", "gv"] else "w")

        self.tree_schedule.bind("<<TreeviewSelect>>", self.on_schedule_select)

        khung_nhap = ctk.CTkFrame(khung_chinh, fg_color="#1a1d24", corner_radius=12)
        khung_nhap.pack(fill="x")

        khung_form = ctk.CTkFrame(khung_nhap, fg_color="transparent")
        khung_form.pack(side="left", padx=20, pady=20)

        self.sched_inputs = {}
        fields = [("Mã SV:", "msv", 0, 0), ("Tên Môn Học:", "ten", 0, 2), ("Thứ:", "thu", 0, 4),
                  ("Ca Học:", "ca", 1, 0), ("Phòng:", "phong", 1, 2), ("Giảng Viên:", "gv", 1, 4),
                  ("Tuần Học:", "tuan", 2, 0)]

        for lb, key, r, c in fields:
            ctk.CTkLabel(khung_form, text=lb, font=("Segoe UI", 14, "bold"), text_color="#cbd5e1").grid(row=r, column=c, padx=(15, 5), pady=8, sticky="e")
            en = ctk.CTkEntry(khung_form, width=180, height=35, font=("Segoe UI", 14), fg_color="#272a33", 
                              border_color="#3f3f46", text_color="#f8fafc", corner_radius=6)
            en.grid(row=r, column=c + 1, padx=5, pady=8, sticky="w")
            self.sched_inputs[key] = en

        khung_nut = ctk.CTkFrame(khung_nhap, fg_color="transparent")
        khung_nut.pack(side="right", padx=30, pady=20)
        
        ctk.CTkButton(khung_nut, text="Thêm Mới", fg_color="#059669", hover_color="#047857", 
                      font=("Segoe UI", 13, "bold"), height=40, width=140, cursor="hand2", command=self.them_lich).pack(pady=(0, 10))
        ctk.CTkButton(khung_nut, text="Cập Nhật", fg_color="#0ea5e9", hover_color="#0284c7", 
                      font=("Segoe UI", 13, "bold"), height=40, width=140, cursor="hand2", command=self.sua_lich).pack(pady=10)
        ctk.CTkButton(khung_nut, text="Xóa Lịch", fg_color="#dc2626", hover_color="#991b1b", 
                      font=("Segoe UI", 13, "bold"), height=40, width=140, cursor="hand2", command=self.xoa_lich).pack(pady=10)
        ctk.CTkButton(khung_nut, text="Làm Mới Form", fg_color="#475569", hover_color="#334155", 
                      font=("Segoe UI", 13, "bold"), height=40, width=140, cursor="hand2", command=self.clear_sched_inputs).pack(pady=(10, 0))

        self.load_schedule_list()

    def lay_path_classtime(self):
        return os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'database', 'ClassTime.csv'))

    def tim_kiem_lich(self):
        tu_khoa = self.entry_tim_lich.get().strip().lower()
        self.load_schedule_list(tu_khoa)

    def hien_tat_ca_lich(self):
        self.entry_tim_lich.delete(0, 'end')
        self.load_schedule_list("")

    def load_schedule_list(self, tu_khoa=""):
        for item in self.tree_schedule.get_children(): self.tree_schedule.delete(item)
        path = self.lay_path_classtime()
        if not os.path.exists(path): return
        try:
            with open(path, "r", encoding="utf-8-sig") as f:
                reader = csv.reader(f)
                next(reader, None)
                stt = 1
                for row in reader:
                    if len(row) >= 7:
                        if tu_khoa == "" or tu_khoa in row[0].strip().lower():
                            tag = "evenrow" if stt % 2 == 0 else "oddrow"
                            self.tree_schedule.insert("", "end", values=row[:7], tags=(tag,))
                            stt += 1
        except Exception:
            pass

    def on_schedule_select(self, event):
        selected = self.tree_schedule.selection()
        if not selected: return
        val = self.tree_schedule.item(selected[0])['values']
        keys = ["msv", "ten", "thu", "ca", "phong", "gv", "tuan"]
        for i, k in enumerate(keys):
            self.sched_inputs[k].delete(0, 'end')
            if i < len(val): self.sched_inputs[k].insert(0, val[i])

    def clear_sched_inputs(self):
        for en in self.sched_inputs.values(): en.delete(0, 'end')
        self.sched_inputs["msv"].focus()
        for item in self.tree_schedule.selection(): self.tree_schedule.selection_remove(item)

    def them_lich(self):
        row_data = [self.sched_inputs[k].get().strip() for k in ["msv", "ten", "thu", "ca", "phong", "gv", "tuan"]]
        if not row_data[0] or not row_data[1]:
            messagebox.showwarning("Lỗi", "Tối thiểu phải có Mã SV và Tên Môn nhé cu!")
            return

        path = self.lay_path_classtime()
        exists = os.path.exists(path)
        try:
            with open(path, "a", newline="", encoding="utf-8-sig") as f:
                writer = csv.writer(f)
                if not exists: writer.writerow(["Mã SV", "Tên học phần", "Thứ", "Ca học", "Phòng", "Giảng viên", "Tuần học"])
                writer.writerow(row_data)
            self.load_schedule_list(self.entry_tim_lich.get().strip().lower())
            self.clear_sched_inputs()
            messagebox.showinfo("Thành công", "Đã chèn môn vào lịch học!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Toang: {e}")

    def sua_lich(self):
        sel = self.tree_schedule.selection()
        if not sel:
            messagebox.showwarning("Lỗi", "Chọn dòng nào trên bảng để sửa đi bro!");
            return

        old_msv = str(self.tree_schedule.item(sel[0])['values'][0]).strip()
        old_ten = str(self.tree_schedule.item(sel[0])['values'][1]).strip()
        new_row = [self.sched_inputs[k].get().strip() for k in ["msv", "ten", "thu", "ca", "phong", "gv", "tuan"]]

        path = self.lay_path_classtime()
        all_data = []
        try:
            with open(path, "r", encoding="utf-8-sig") as f:
                reader = list(csv.reader(f))
                header = reader[0]
                for r in reader[1:]:
                    if len(r) >= 2 and r[0].strip() == old_msv and r[1].strip() == old_ten:
                        all_data.append(new_row)
                    else:
                        all_data.append(r)
            with open(path, "w", newline="", encoding="utf-8-sig") as f:
                writer = csv.writer(f)
                writer.writerow(header)
                writer.writerows(all_data)
            self.load_schedule_list(self.entry_tim_lich.get().strip().lower())
            self.on_schedule_select(None)
            messagebox.showinfo("Thành công", "Cập nhật lịch mượt mà!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi: {e}")

    def xoa_lich(self):
        sel = self.tree_schedule.selection()
        if not sel:
            messagebox.showwarning("Lỗi", "Chọn 1 dòng để xóa đi má!");
            return

        if not messagebox.askyesno("Xác nhận", "Thích xóa môn trong lịch của nó không?"): return

        old_msv = str(self.tree_schedule.item(sel[0])['values'][0]).strip()
        old_ten = str(self.tree_schedule.item(sel[0])['values'][1]).strip()

        path = self.lay_path_classtime()
        all_data = []
        try:
            with open(path, "r", encoding="utf-8-sig") as f:
                reader = list(csv.reader(f))
                header = reader[0]
                for r in reader[1:]:
                    if len(r) >= 2 and r[0].strip() == old_msv and r[1].strip() == old_ten: continue
                    all_data.append(r)
            with open(path, "w", newline="", encoding="utf-8-sig") as f:
                writer = csv.writer(f)
                writer.writerow(header)
                writer.writerows(all_data)
            self.load_schedule_list(self.entry_tim_lich.get().strip().lower())
            self.clear_sched_inputs()
            messagebox.showinfo("Thành công", "Đã tiễn môn này khỏi lịch!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi DB: {e}")