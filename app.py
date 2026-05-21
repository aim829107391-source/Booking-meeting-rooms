from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "super_secret_key_for_session" 

def init_db():
    try:
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS rooms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                capacity INTEGER NOT NULL,
                status TEXT NOT NULL
            )
        """)
        c.execute("""
            CREATE TABLE IF NOT EXISTS bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                room TEXT NOT NULL,
                date TEXT NOT NULL,
                start_time TEXT NOT NULL,
                end_time TEXT NOT NULL,
                payment_status TEXT NOT NULL DEFAULT 'Pending'
            )
        """)
        c.execute("SELECT COUNT(*) FROM rooms")
        if c.fetchone()[0] == 0:
            default_rooms = [
                ("Room 1", 6, "Available"),
                ("Room 2", 8, "Available"),
                ("Room 3", 10, "Available"),
                ("Room 4", 12, "Available"),
                ("Room 5", 14, "Available")
            ]
            c.executemany("INSERT INTO rooms (name, capacity, status) VALUES (?, ?, ?)", default_rooms)
        conn.commit()
        conn.close()
    except sqlite3.Error:
        pass

init_db()

def get_rooms():
    try:
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("SELECT name, capacity, status FROM rooms")
        rows = c.fetchall()
        conn.close()
        return [{"name": row[0], "capacity": row[1], "status": row[2]} for row in rows]
    except:
        return [
            {"name": "Room 1", "capacity": 6, "status": "Available"},
            {"name": "Room 2", "capacity": 8, "status": "Available"},
            {"name": "Room 3", "capacity": 10, "status": "Available"},
            {"name": "Room 4", "capacity": 12, "status": "Available"},
            {"name": "Room 5", "capacity": 14, "status": "Available"}
        ]

@app.route("/")
def home():
    rooms = get_rooms()
    return render_template("index.html", rooms=rooms, message=request.args.get('message'))

@app.route("/booking", methods=["GET", "POST"])
def booking():
    rooms = get_rooms()
    message = ""
    if request.method == "POST":
        username = request.form["username"].strip()
        room = request.form["room"]
        date = request.form["date"].strip()
        start_time = request.form["start_time"].strip()
        end_time = request.form["end_time"].strip()
        
        if not username or not date or not start_time or not end_time or not room:
            return render_template("booking.html", rooms=rooms, message="Error: Empty input detected!")
            
        try:
            conn = sqlite3.connect("database.db")
            c = conn.cursor()
            c.execute("""
                SELECT COUNT(*) FROM bookings 
                WHERE room = ? AND date = ? 
                AND ((start_time < ? AND end_time > ?) OR (start_time >= ? AND start_time < ?))
            """, (room, date, end_time, start_time, start_time, end_time))
            
            if c.fetchone()[0] > 0:
                message = f"Error: {room} is already booked during this time slot!"
            else:
                c.execute("""
                    INSERT INTO bookings (username, room, date, start_time, end_time, payment_status) 
                    VALUES (?, ?, ?, ?, ?, 'Paid')
                """, (username, room, date, start_time, end_time))
                conn.commit()
                message = f"Booking and payment successful for {username} in {room}."
            conn.close()
        except sqlite3.Error:
            message = "Error: Database connection failed."
            
    return render_template("booking.html", rooms=rooms, message=message)

@app.route("/cancel_booking", methods=["POST"])
def cancel_booking():
    username = request.form["username"].strip()
    date = request.form["date"].strip()
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM bookings WHERE LOWER(username) = LOWER(?) AND date = ?", (username, date))
    if c.fetchone()[0] > 0:
        c.execute("DELETE FROM bookings WHERE LOWER(username) = LOWER(?) AND date = ?", (username, date))
        conn.commit()
        message = f"All reservations for {username} on {date} have been successfully canceled."
    else:
        message = f"Error: No reservations found for {username} on {date}."
    conn.close()
    rooms = get_rooms()
    return render_template("index.html", rooms=rooms, message=message)

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    error = ""
    if request.method == "POST":
        if request.form["username"] == "admin" and request.form["password"] == "12345":
            session["admin_logged_in"] = True
            return redirect("/admin")
        else:
            error = "Invalid secret credentials!"
    return render_template("admin_login.html", error=error)

@app.route("/admin")
def admin():
    if not session.get("admin_logged_in"):
        return redirect("/admin/login") 
        
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT id, username, room, date, start_time, end_time, payment_status FROM bookings")
    rows = c.fetchall()
    conn.close()
    bookings_list = [{"id": r[0], "username": r[1], "room": r[2], "date": r[3], "start_time": r[4], "end_time": r[5], "status": r[6]} for r in rows]
    return render_template("admin.html", bookings=bookings_list)

@app.route("/admin/delete", methods=["POST"])
def admin_delete():
    if not session.get("admin_logged_in"):
        return redirect("/admin/login")
    booking_id = request.form["booking_id"]
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("DELETE FROM bookings WHERE id = ?", (booking_id,))
    conn.commit()
    conn.close()
    return redirect("/admin")

@app.route("/admin/logout")
def admin_logout():
    session.pop("admin_logged_in", None)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
