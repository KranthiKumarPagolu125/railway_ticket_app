from flask import Flask, render_template, request, jsonify
import sqlite3
import random

app = Flask(__name__)

# Train data (still in memory)
trains = {
    101: {
        "name": "Tirupati Express",
        "from": "Hyderabad",
        "to": "Tirupati",
        "fare": 450,
        "seats": 10
    },
    102: {
        "name": "Godavari Express",
        "from": "Visakhapatnam",
        "to": "Hyderabad",
        "fare": 750,
        "seats": 10
    },
    103: {
        "name": "Krishna Express",
        "from": "Vijayawada",
        "to": "Hyderabad",
        "fare": 500,
        "seats": 12
    },
    104: {
        "name": "Charminar Express",
        "from": "Chennai",
        "to": "Hyderabad",
        "fare": 650,
        "seats": 15
    },
    105: {
        "name": "Kakatiya Express",
        "from": "Warangal",
        "to": "Hyderabad",
        "fare": 300,
        "seats": 20
    },
    106: {
        "name": "Vande Bharat Express",
        "from": "Secunderabad",
        "to": "Visakhapatnam",
        "fare": 1200,
        "seats": 25
    }
}


# ---------- DATABASE ----------
def get_db():
    return sqlite3.connect("railway.db")

def create_table():
    con = get_db()
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            pnr TEXT PRIMARY KEY,
            name TEXT,
            age INTEGER,
            passengers INTEGER,
            berth TEXT,
            train TEXT,
            fare INTEGER
        )
    """)
    con.commit()
    con.close()

create_table()

def generate_pnr():
    return "PNR" + str(random.randint(10000, 99999))

# ---------- ROUTES ----------
@app.route("/")
def home():
    return render_template("index.html", trains=trains)

@app.route("/book", methods=["POST"])
def book_ticket():
    data = request.get_json()

    train_no = int(data["train_no"])
    name = data["name"]
    age = data["age"]
    passengers = int(data["passengers"])
    berth = data["berth"]

    if trains[train_no]["seats"] < passengers:
        return jsonify({"error": "Not enough seats"})

    pnr = generate_pnr()
    fare = trains[train_no]["fare"] * passengers
    train_name = trains[train_no]["name"]

    con = get_db()
    cur = con.cursor()
    cur.execute(
        "INSERT INTO tickets VALUES (?, ?, ?, ?, ?, ?, ?)",
        (pnr, name, age, passengers, berth, train_name, fare)
    )
    con.commit()
    con.close()

    trains[train_no]["seats"] -= passengers

    return jsonify({"pnr": pnr})

@app.route("/view/<pnr>")
def view_ticket(pnr):
    con = get_db()
    cur = con.cursor()
    cur.execute("SELECT * FROM tickets WHERE pnr=?", (pnr,))
    row = cur.fetchone()
    con.close()

    if not row:
        return jsonify({"error": "PNR not found"})

    return jsonify({
        "pnr": row[0],
        "name": row[1],
        "age": row[2],
        "passengers": row[3],
        "berth": row[4],
        "train": row[5],
        "fare": row[6]
    })

@app.route("/cancel/<pnr>")
def cancel_ticket(pnr):
    con = get_db()
    cur = con.cursor()
    cur.execute("SELECT passengers FROM tickets WHERE pnr=?", (pnr,))
    row = cur.fetchone()

    if not row:
        con.close()
        return jsonify({"error": "PNR not found"})

    cur.execute("DELETE FROM tickets WHERE pnr=?", (pnr,))
    con.commit()
    con.close()

    return jsonify({"message": "Ticket cancelled successfully"})

if __name__ == "__main__":
    print("Starting Flask app...")
    if __name__ == "__main__":
     app.run(host="0.0.0.0", port=5000)

