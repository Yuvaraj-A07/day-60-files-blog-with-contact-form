from flask import Flask, render_template, request
import requests
import smtplib

my_mail = "dhonikohli0718at@gmail.com"
password = "abzprawjtywcxmsz"

# USE YOUR OWN npoint LINK! ADD AN IMAGE URL FOR YOUR POST. 👇
posts = requests.get("https://api.npoint.io/c790b4d5cab58020d391").json()

app = Flask(__name__)


@app.route('/')
def get_all_posts():
    return render_template("index.html", all_posts=posts)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        data = request.form
        name = data["name"]
        email = data["email"]
        phone = data["phone"]
        message = data["message"]
        with smtplib.SMTP("smtp.gmail.com") as send_info:
            send_info.starttls()
            send_info.login(user=my_mail, password=password)
            send_info.sendmail(from_addr=my_mail,
                               to_addrs=my_mail,
                               msg=f"Subject:Contact info \n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}"
                               )
        return render_template("contact.html", msg_sent=True)
    return render_template("contact.html", msg_sent=False)


#
# @app.route("/contact")
# def contact():
#     return render_template("contact.html")
#
#
# @app.route("/contact", methods=["POST", "GET"])
# def receive_data():
#     if request.method == "POST":
#         return "<h1>Successfully sent your message</h1>"
#     else:
#         return "hi"


@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
