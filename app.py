from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('badminton.db')
    conn.row_factory = sqlite3.Row  # Để truy cập các cột theo tên như dict
    return conn

@app.route('/')
def index():
    # Trang chủ: Nơi người chơi nhập "Hồ sơ lông thủ"
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    # Thu thập "chỉ số" từ form
    trinh_do = request.form.get('trinh_do')
    loi_choi = request.form.get('loi_choi')
    ngan_sach_max = request.form.get('ngan_sach')
    
    conn = get_db_connection()
    
    # Câu lệnh SQL cơ bản để lọc theo Trình độ và Lối chơi (Sử dụng LIKE để bắt các chuỗi gần đúng)
    query = "SELECT * FROM rackets WHERE TrinhDo LIKE ? AND LoiChoi LIKE ?"
    params = [f"%{trinh_do}%", f"%{loi_choi}%"]
    
    # Nếu người dùng có nhập ngân sách tối đa
    if ngan_sach_max:
        query += " AND Gia <= ?"
        params.append(int(ngan_sach_max))
        
    # Sắp xếp theo giá tăng dần
    query += " ORDER BY Gia ASC"
    
    rackets = conn.execute(query, params).fetchall()
    conn.close()
    
    # Truyền kết quả và dữ liệu filter ngược lại giao diện để hiển thị
    return render_template('result.html', rackets=rackets, trinh_do=trinh_do, loi_choi=loi_choi)

if __name__ == '__main__':
    # Bật debug=True để khi sửa code web tự động reload
    app.run(debug=True)

import os
import webbrowser
from threading import Timer


def open_in_chrome():
    url = "http://127.0.0.1:5000"
    # Đường dẫn chuẩn của Google Chrome trên Windows
    chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"
    
    try:
        # Ép buộc hệ thống mở đường link bằng đúng Google Chrome
        webbrowser.get(chrome_path).open(url)
    except Exception:
        # Nếu không tìm thấy Chrome theo đường dẫn trên thì mở bằng trình duyệt mặc định
        webbrowser.open(url)

if __name__ == '__main__':
    # Chờ 1 giây cho server khởi động xong rồi tự bật Chrome
    Timer(1.0, open_in_chrome).start()
    app.run(debug=False)