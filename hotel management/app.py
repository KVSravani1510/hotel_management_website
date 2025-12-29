from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime, timedelta
from data import all_rooms, guests, admin_data, busy, free, prices


app = Flask(__name__)
app.secret_key = "key123" # just for session


# this is to check login
@app.before_request
def check_login():
    allowed = ["/login", "/static/"]
    if request.path.startswith("/static/"):
        return
    if request.path not in allowed and not session.get("login"):
        return redirect("/login")


@app.route("/")
def home():
    return redirect("/dashboard")


@app.route("/login", methods=["GET", "POST"])
def login():
# simple login check
    if request.method == "POST":
        u = request.form.get("user")
        p = request.form.get("pwd")
        if u == admin_data["user"] and p == admin_data["pwd"]:
            session["login"] = True
            return redirect("/dashboard")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


@app.route("/dashboard")
def dash():
# calculating simple values
    total = sum(len(v) for v in all_rooms.values())
    used = len([g for g in guests if g["status"] == "IN"])
    free_rooms = total - used
    return render_template("dashboard.html", total=total, used=used, free=free_rooms)


@app.route("/rooms/<rtype>")
def show_rooms(rtype):
# marking rooms busy/free
    taken = {g["room"] for g in guests if g["status"] == "IN"}
    show = []
    for r in all_rooms[rtype]:
        show.append({"num": r, "free": r not in taken})
    return render_template("room_type.html", rtype=rtype, rooms=show)


@app.route("/add", methods=["GET", "POST"])
def add_guest():
    if request.method == "POST":
        name = request.form.get("name")
        phone = request.form.get("phone")
        rtype = request.form.get("rtype")
        room_no = int(request.form.get("room"))
        ac_type = request.form.get("ac")
        hrs = int(request.form.get("hrs"))
        days = hrs / 24
        total_amount = prices[rtype] * days

        # if room is already taken
        if not free(room_no):
            return redirect("/add")

        now = datetime.now()
        out_time = now + timedelta(hours=hrs)

        # storing simple guest record
        guests.append({
            "name": name,
            "phone": phone,
            "room": room_no,
            "type": rtype,
            "ac": ac_type,
            "in": now,
            "out": out_time,
            "status": "IN",
            "amount": total_amount
        })

        busy(room_no)
        return redirect("/records")
    return render_template("add_guest.html", rooms=all_rooms)



@app.route("/records")
def record_page():
    return render_template("records.html", guests=guests)


@app.route("/checkout/<int:num>")
def checkout(num):
    for g in guests:
        if g["room"] == num and g["status"] == "IN":
            g["status"] = "OUT"
            free(num, ok=True)
            break
    return redirect("/records")

@app.route("/room/<int:num>")
def room_page(num):
    try:
        return render_template(f"rooms/{num}.html")
    except Exception:
        return f"No page created for room {num}", 404


if __name__ == "__main__":
    app.run()