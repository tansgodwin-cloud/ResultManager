import customtkinter as ctk
from Login import LoginFrame
from register import RegisterFrame
from Home import HomeFrame
from admin import AdminFrame


class MainApplication(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Phần mềm Quản lý Tài khoản")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.container = ctk.CTkFrame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        #kích cỡ của Giao diện admin
        self.kich_thuoc_cua_so = {
            "LoginFrame": "400x380",
            "RegisterFrame": "450x650",
            "HomeFrame": "1100x650",
            "AdminFrame": "800x600"
        }

        # import bài khác
        for F in (LoginFrame, RegisterFrame, HomeFrame, AdminFrame):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginFrame")

    def show_frame(self, page_name):
        frame = self.frames.get(page_name)
        if frame:
            size_moi = self.kich_thuoc_cua_so.get(page_name, "800x600")
            self.geometry(size_moi)
            frame.tkraise()
        else:
            print(f"Lỗi: Không tìm thấy giao diện {page_name}")


if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
