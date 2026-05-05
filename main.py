import customtkinter as ctk
import os
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
        self.frame_classes = {
            "LoginFrame": LoginFrame,
            "RegisterFrame": RegisterFrame,
            "HomeFrame": HomeFrame,
            "AdminFrame": AdminFrame
        }
        
        # Cấu hình kích cỡ cố định cho từng giao diện
        self.kich_thuoc_cua_so = {
            "LoginFrame": "400x380",
            "RegisterFrame": "450x650",
            "HomeFrame": "1500x800",
            "AdminFrame": "1200x900"
        }

        self.current_page_name = "LoginFrame"
        self.show_frame("LoginFrame")

        # -- Tính năng Load lại trang & Tự động cập nhật Realtime --
        self.bind("<F5>", self.reload_page) # Bấm F5 để tải lại thủ công
        self.db_path = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "Database"))
        self.last_csv_mtimes = self.get_all_csv_mtimes()
        self.check_csv_updates_realtime()

    def get_all_csv_mtimes(self):
        """Lấy thời gian sửa đổi (mtime) của tất cả các file CSV trong thư mục Database."""
        mtimes = {}
        if os.path.exists(self.db_path):
            with os.scandir(self.db_path) as entries:
                for entry in entries:
                    if entry.is_file() and entry.name.endswith(".csv"):
                        mtimes[entry.name] = entry.stat().st_mtime
        return mtimes

    def check_csv_updates_realtime(self):
        """Kiểm tra thay đổi file và tự động reload nếu có file bị sửa."""
        current_mtimes = self.get_all_csv_mtimes()
        if current_mtimes != self.last_csv_mtimes:
            self.last_csv_mtimes = current_mtimes
            self.reload_page()
        # Lặp lại sau mỗi 2 giây
        self.after(2000, self.check_csv_updates_realtime)

    def reload_page(self, event=None):
        """Tải lại giao diện hiện tại."""
        if hasattr(self, 'current_page_name') and self.current_page_name:
            frame = self.frames.get(self.current_page_name)
            if frame:
                # Nếu frame có hàm dựng lại giao diện, ta gọi nó để làm mới dữ liệu
                if hasattr(frame, "dung_giao_dien"):
                    frame.dung_giao_dien()
                print(f"Đã làm mới {self.current_page_name} (F5 hoặc Realtime)")

    def get_frame(self, page_name):
        """Khởi tạo giao diện nếu chưa có (Lazy Loading) và trả về frame."""
        if page_name not in self.frames:
            FrameClass = self.frame_classes.get(page_name)
            if FrameClass:
                frame = FrameClass(parent=self.container, controller=self)
                self.frames[page_name] = frame
                frame.grid(row=0, column=0, sticky="nsew")
        return self.frames.get(page_name)

    def show_frame(self, page_name):
        self.current_page_name = page_name
        
        frame = self.get_frame(page_name)
        if frame:
            size_moi = self.kich_thuoc_cua_so.get(page_name, "800x600")
            width, height = map(int, size_moi.split('x'))
            
            # --- TỐI ƯU UX: Đóng/Mở tính năng kéo dãn cửa sổ ---
            if page_name in ["LoginFrame", "RegisterFrame"]:
                self.resizable(False, False) # Không cho kéo dãn màn Đăng nhập, Đăng ký
            else:
                self.resizable(True, True)   # Cho phép kéo dãn (phóng to) đối với Home và Admin

            # Tự động căn chỉnh cho vừa với kích cỡ màn hình (Tối ưu không flicker)
            screen_w = self.winfo_screenwidth()
            screen_h = self.winfo_screenheight()
            x = (screen_w // 2) - (width // 2)
            y = (screen_h // 2) - (height // 2) - 30 # Trừ hao 30px thanh Taskbar
            
            self.geometry(f"{width}x{height}+{x}+{y}")
            frame.tkraise()
        else:
            print(f"Lỗi: Không tìm thấy giao diện {page_name}")


if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()