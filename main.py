import subprocess
import sys

def main():
    # Khởi chạy file đăng nhập
    subprocess.Popen([sys.executable, "login.py"])

if __name__ == "__main__":
    main()