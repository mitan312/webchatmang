from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, send
import os, json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app, cors_allowed_origins="*")

USER_FILE = "users.json"


# Hỗ trợ lưu users
def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

def save_users(users):
    with open(USER_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2, ensure_ascii=False)

# Trang đăng nhập / đăng ký

@app.route('/')
def home():
    if "username" in session:
        return redirect(url_for("chat"))
    return render_template("login.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        if not username or not password:
            return "Vui lòng nhập tên đăng nhập và mật khẩu", 400

        users = load_users()
        if username in users:
            return "Tên đăng nhập đã tồn tại!", 400
        users[username] = password
        save_users(users)
        return redirect(url_for("home"))
    return render_template("register.html")

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")

    users = load_users()
    if username in users and users[username] == password:
        session["username"] = username
        return redirect(url_for("chat"))
    return "Sai tên đăng nhập hoặc mật khẩu!", 401

@app.route('/logout')
def logout():
    session.pop("username", None)
    return redirect(url_for("home"))


# Trang chat

@app.route('/chat')
def chat():
    if "username" not in session:
        return redirect(url_for("home"))
    return render_template("index.html", username=session["username"])


# Xử lý SocketIO
@socketio.on('message')
def handle_message(msg):
    username = session.get("username", "Ẩn danh")
    print(f"📩 {username}: {msg}")
    send(f"{username}: {msg}", broadcast=True)

# Chạy server
if __name__ == "__main__":
    if not os.path.exists(USER_FILE):
        save_users({})
    socketio.run(app, host="127.0.0.1", port=5000, debug=True)
