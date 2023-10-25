from flask import *

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

#หน้า login
@app.route("/login")
def login():
    return render_template("login.html")

#หน้าสมัครแบบ ทดลอง
@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/home")
def home():
    return render_template("home.html")
#หน้า Error ในกรณีที่ Url ผิด
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404
if __name__ == "__main__":
    app.run(debug=True, port=3000)