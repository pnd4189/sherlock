import gradio as gr
import subprocess
import os

def search_username(username):
    # Chạy Sherlock qua dòng lệnh, chỉ trả về 20 dòng đầu kết quả cho nhanh
    try:
        result = subprocess.check_output(
            ["python3", "sherlock.py", username, "--print-found"],
            stderr=subprocess.STDOUT,
            timeout=60
        ).decode("utf-8")
        # Cắt bớt output nếu quá dài
        return "\n".join(result.splitlines()[:40])
    except subprocess.CalledProcessError as e:
        return e.output.decode("utf-8")
    except Exception as e:
        return str(e)

gr.Interface(
    fn=search_username,
    inputs=gr.Textbox(label="Username", placeholder="Nhập username bạn muốn kiểm tra..."),
    outputs=gr.Textbox(label="Kết quả"),
    title="Sherlock: Social Media Username Checker",
    description="Nhập username, Sherlock sẽ tìm các mạng xã hội trùng username đó."
).launch()
