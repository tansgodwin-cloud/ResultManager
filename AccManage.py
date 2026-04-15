import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
import csv
import os

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

TEN_FILE = '../database/tai_khoan_cua_toi.csv'


def doc_du_lieu():
    for item in tree.get_children():
        tree.delete(item)

    if not os.path.isfile(TEN_FILE):
        return

    with open(TEN_FILE, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader, None)
        for row in reader:
            if len(row) >= 3:
                tree.insert('', tk.END, values=(row[0], row[1], row[2]))


def tim_kiem_tai_khoan():
    tu_khoa = entry_tim_kiem.get().lower()

    for item in tree.get_children():
        tree.delete(item)

    if not os.path.isfile(TEN_FILE):
        return

    with open(TEN_FILE, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader, None)
        for row in reader:
            if len(row) >= 3:
                if tu_khoa in row[0].lower():
                    tree.insert('', tk.END, values=(row[0], row[1], row[2]))


def huy_tim_kiem():
    entry_tim_kiem.delete(0, tk.END)
    doc_du_lieu()


def ghi_lai_toan_bo(danh_sach_du_lieu):
    with open(TEN_FILE, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Tên đăng nhập', 'Mật khẩu', 'Vai trò'])
        writer.writerows(danh_sach_du_lieu)


def chon_dong(event):
    selected_item = tree.selection()
    if selected_item:
        row = tree.item(selected_item)['values']
        lam_moi_o_nhap()
        entry_tk.insert(0, row[0])
        entry_mk.insert(0, str(row[1]))
        role_var.set(row[2])


def xoa_tai_khoan():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Cảnh báo", "Vui lòng chọn một dòng để xóa!")
        return

    xac_nhan = messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa tài khoản này?")
    if xac_nhan:
        tk_can_xoa = tree.item(selected_item)['values'][0]
        du_lieu_moi = []
        with open(TEN_FILE, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader, None)
            for row in reader:
                if row[0] != str(tk_can_xoa):
                    du_lieu_moi.append(row)

        ghi_lai_toan_bo(du_lieu_moi)

        if entry_tim_kiem.get() != "":
            tim_kiem_tai_khoan()
        else:
            doc_du_lieu()

        lam_moi_o_nhap()
        messagebox.showinfo("Thành công", "Đã xóa tài khoản!")


def cap_nhat_tai_khoan():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Cảnh báo", "Vui lòng chọn một dòng để cập nhật!")
        return

    tk_moi = entry_tk.get()
    mk_moi = entry_mk.get()
    vt_moi = role_var.get()

    if tk_moi == "" or mk_moi == "":
        messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin!")
        return

    tk_cu = tree.item(selected_item)['values'][0]
    du_lieu_moi = []
    with open(TEN_FILE, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader, None)
        for row in reader:
            if row[0] == str(tk_cu):
                du_lieu_moi.append([tk_moi, mk_moi, vt_moi])
            else:
                du_lieu_moi.append(row)

    ghi_lai_toan_bo(du_lieu_moi)

    if entry_tim_kiem.get() != "":
        tim_kiem_tai_khoan()
    else:
        doc_du_lieu()

    messagebox.showinfo("Thành công", "Đã cập nhật thông tin!")


def lam_moi_o_nhap():
    entry_tk.delete(0, tk.END)
    entry_mk.delete(0, tk.END)
    role_var.set("User")


root = ctk.CTk()
root.title("Hệ thống - Quản lý Tài khoản")
root.geometry("620x560")

style = ttk.Style(root)
style.theme_use("default")

bg_color = "#242424"
text_color = "white"
selected_color = "#1f538d"
header_bg = "#343638"

style.configure("Treeview",
                background=bg_color,
                foreground=text_color,
                fieldbackground=bg_color,
                font=("Arial", 20),
                rowheight=35,
                bordercolor="#343638",
                borderwidth=0)
style.map('Treeview', background=[('selected', selected_color)])

style.configure("Treeview.Heading",
                background=header_bg,
                foreground=text_color,
                relief="flat",
                font=("Arial", 11, "bold"))
style.map("Treeview.Heading", background=[('active', '#444444')])

frame_top = ctk.CTkFrame(root, fg_color="transparent")
frame_top.pack(fill="x", padx=20, pady=(20, 0))

ctk.CTkLabel(frame_top, text="Tìm kiếm:").pack(side="left", padx=(0, 10))
entry_tim_kiem = ctk.CTkEntry(frame_top, width=220, placeholder_text="Nhập tên đăng nhập...", corner_radius=10)
entry_tim_kiem.pack(side="left", padx=5)

ctk.CTkButton(frame_top, text="Tìm", width=80, corner_radius=10, command=tim_kiem_tai_khoan).pack(side="left", padx=5)
ctk.CTkButton(frame_top, text="Hủy", width=80, corner_radius=10, fg_color="#6c757d", hover_color="#5a6268",
              command=huy_tim_kiem).pack(side="left", padx=5)

columns = ('tai_khoan', 'mat_khau', 'vai_tro')
tree = ttk.Treeview(root, columns=columns, show='headings', height=7)

tree.heading('tai_khoan', text='Tên đăng nhập')
tree.heading('mat_khau', text='Mật khẩu')
tree.heading('vai_tro', text='Vai trò')

tree.column('tai_khoan', width=220)
tree.column('mat_khau', width=220)
tree.column('vai_tro', width=140)

tree.pack(pady=(15, 10), padx=20, fill="both", expand=True)
tree.bind('<ButtonRelease-1>', chon_dong)

frame_bottom = ctk.CTkFrame(root, fg_color="transparent")
frame_bottom.pack(fill="x", padx=30, pady=10)

frame_nhap = ctk.CTkFrame(frame_bottom, fg_color="transparent")
frame_nhap.pack(side="left", anchor="n")

ctk.CTkLabel(frame_nhap, text="Tài khoản:", font=("Arial", 13)).grid(row=0, column=0, padx=10, pady=10, sticky="e")
entry_tk = ctk.CTkEntry(frame_nhap, width=200, corner_radius=10)
entry_tk.grid(row=0, column=1, padx=5, pady=10, sticky="w")

ctk.CTkLabel(frame_nhap, text="Mật khẩu:", font=("Arial", 13)).grid(row=1, column=0, padx=10, pady=10, sticky="e")
entry_mk = ctk.CTkEntry(frame_nhap, width=200, corner_radius=10)
entry_mk.grid(row=1, column=1, padx=5, pady=10, sticky="w")

ctk.CTkLabel(frame_nhap, text="Vai trò:", font=("Arial", 13)).grid(row=2, column=0, padx=10, pady=10, sticky="e")
role_var = ctk.StringVar(value="User")

frame_role = ctk.CTkFrame(frame_nhap, fg_color="transparent")
frame_role.grid(row=2, column=1, sticky="w", padx=5)

ctk.CTkRadioButton(frame_role, text="User", variable=role_var, value="User").pack(side="left", pady=10)
ctk.CTkRadioButton(frame_role, text="Admin", variable=role_var, value="Admin").pack(side="left", padx=15, pady=10)

frame_nut = ctk.CTkFrame(frame_bottom, fg_color="transparent")
frame_nut.pack(side="right", anchor="n")

ctk.CTkButton(frame_nut, text="Làm mới form", width=140, corner_radius=10, command=lam_moi_o_nhap).grid(row=0, column=0,
                                                                                                        pady=8)
ctk.CTkButton(frame_nut, text="Cập nhật (Sửa)", width=140, corner_radius=10, fg_color="#E5A900", hover_color="#C69300",
              text_color="black", command=cap_nhat_tai_khoan).grid(row=1, column=0, pady=8)
ctk.CTkButton(frame_nut, text="Xóa tài khoản", width=140, corner_radius=10, fg_color="#DC3545", hover_color="#B02A37",
              command=xoa_tai_khoan).grid(row=2, column=0, pady=8)

doc_du_lieu()
root.mainloop()