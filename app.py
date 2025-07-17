import subprocess, sys, gradio as gr

def search_username(username: str) -> str:
    """
    Gọi Sherlock CLI rồi trả về kết quả (tối đa 60 dòng đầu để tránh tràn màn hình).
    """
    username = username.strip()
    if not username:
        return "❗️ Bạn chưa nhập username."

    try:
        # Gọi bằng Python hiện tại để tránh xung đột phiên bản
        output = subprocess.check_output(
            [sys.executable, "-m", "sherlock_project.sherlock", username, "--print-found"],
            stderr=subprocess.STDOUT,
            timeout=120,          # 2 phút – tránh job bị treo lâu trên HF
        ).decode("utf-8", errors="replace")

        lines = [l for l in output.splitlines() if l.strip()]
        if not lines:
            return "⚠️ Không tìm thấy tài khoản trùng khớp."
        return "\n".join(lines[:60])

    except subprocess.CalledProcessError as e:
        return f"❌ Sherlock báo lỗi:\n{e.output.decode('utf-8', errors='replace')}"
    except Exception as e:
        return f"❌ Lỗi không xác định: {e}"

demo = gr.Interface(
    fn          = search_username,
    inputs      = gr.Textbox(label="Username", placeholder="Ví dụ: johndoe"),
    outputs     = gr.Textbox(label="Kết quả"),
    title       = "Sherlock – Tìm username trên 400+ mạng xã hội",
    description = "Nhập một username để kiểm tra xem đã được dùng ở những mạng xã hội nào."
)

if __name__ == "__main__":
    demo.launch()

