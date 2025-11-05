from flask import Flask, render_template, request, redirect, url_for, session
import json, os

app = Flask(__name__)
app.secret_key = "bloodcampsecret"

# File to store donor data
DATA_FILE = "donors.json"

# Staff login credentials
staff_accounts = {
    "HOSP123": {"admin": "admin123"},
    "HOSP999": {"citystaff": "staffpass"}
}

# --- Helper Functions ---
def load_donors():
    """Load donors from file"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_donors(donors):
    """Save donors to file"""
    with open(DATA_FILE, "w") as f:
        json.dump(donors, f, indent=4)

# --- Routes ---
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        donor = {
            "name": request.form["name"],
            "email": request.form["email"],
            "phone": request.form["phone"],
            "blood_group": request.form["blood_group"],
            "location": request.form["location"]
        }
        donors = load_donors()
        donors.append(donor)
        save_donors(donors)
        return render_template("home.html", message="✅ Thank you for registering as a donor!")
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        hospital_id = request.form["hospital_id"]
        username = request.form["username"]
        password = request.form["password"]

        if hospital_id in staff_accounts and username in staff_accounts[hospital_id]:
            if staff_accounts[hospital_id][username] == password:
                session["staff"] = username
                session["hospital_id"] = hospital_id
                return redirect(url_for("staff_dashboard"))
        return render_template("login.html", error="❌ Invalid credentials!")
    return render_template("login.html")

@app.route("/staff")
def staff_dashboard():
    if "staff" not in session:
        return redirect(url_for("login"))

    donors = load_donors()
    hospital_id = session["hospital_id"]
    return render_template("staff.html", donors=donors, hospital_id=hospital_id, staff=session["staff"])

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)