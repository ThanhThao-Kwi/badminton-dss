import sqlite3
import pandas as pd
import os

def init_database():
    csv_path = 'data/votcaulong.csv'
    db_path = 'badminton.db'
    
    if not os.path.exists(csv_path):
        print(f"Không tìm thấy file {csv_path}. Bạn hãy kiểm tra lại thư mục data.")
        return

    print("Đang đọc dữ liệu vợt từ CSV...")
    # Đọc file CSV
    df = pd.read_csv(csv_path)
    
    # Kết nối đến SQLite (tự động tạo file nếu chưa có)
    conn = sqlite3.connect(db_path)
    
    # Ghi đè dữ liệu vào bảng 'rackets'
    df.to_sql('rackets', conn, if_exists='replace', index=False)
    
    print("Đã chuyển đổi dữ liệu thành Database SQLite thành công.")
    conn.close()

if __name__ == '__main__':
    init_database()
