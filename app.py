from flask import Flask, request, send_from_directory, jsonify
import os
import subprocess

app = Flask(__name__)
FILE_PATH = "gyj.txt"

# 主页
@app.route("/")
def home():
    return send_from_directory(".", "index.html")

# 读取内容
@app.route("/read")
def read_txt():
    if not os.path.exists(FILE_PATH):
        return "# 暂无内容，请编辑后保存", 200, {"Content-Type": "text/plain; charset=utf-8"}
    with open(FILE_PATH, encoding="utf-8") as f:
        return f.read(), 200, {"Content-Type": "text/plain; charset=utf-8"}

# 保存内容（覆盖）
@app.route("/save", methods=["POST"])
def save_txt():
    content = request.data.decode("utf-8")
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        f.write(content)

    # 可选：自动 push 回 GitHub
    subprocess.run(["git", "config", "user.name", "render-bot"], check=False)
    subprocess.run(["git", "config", "user.email", "render@example.com"], check=False)
    subprocess.run(["git", "add", FILE_PATH], check=False)
    subprocess.run(["git", "commit", "-m", "Update gyj.txt"], check=False)
    subprocess.run(["git", "push"], check=False)

    return jsonify({"url": f"https://yourname.github.io/yourrepo/gyj.txt"})

if __name__ == "__main__":
    import os
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
