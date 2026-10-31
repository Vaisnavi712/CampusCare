import os
from flask import Flask, flash, redirect, render_template, request, session, url_for
from database import init_db, get_db_connection, register_database

CATEGORIES = [
    "Wi-Fi Problem",
    "Computer/Lab Problem",
    "Software Installation",
    "Projector Problem",
    "Printer Problem",
    "Other",
]
STATUSES = ["Pending", "In Progress", "Resolved"]
PRIORITIES = ["Low", "Medium", "High"]


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.update(
        SECRET_KEY=os.environ.get("CAMPUSCARE_SECRET_KEY", "dev-only-change-this-secret"),
        DATABASE=os.environ.get("CAMPUSCARE_DATABASE", "campuscare.db"),
        ADMIN_PASSWORD=os.environ.get("CAMPUSCARE_ADMIN_PASSWORD", "admin123"),
    )
    if test_config:
        app.config.update(test_config)

    register_database(app)
    with app.app_context():
        init_db()

    @app.route("/")
    def home():
        conn = get_db_connection()
        counts = {
            "total": conn.execute("SELECT COUNT(*) FROM tickets").fetchone()[0],
            "pending": conn.execute(
                "SELECT COUNT(*) FROM tickets WHERE status = 'Pending'"
            ).fetchone()[0],
            "progress": conn.execute(
                "SELECT COUNT(*) FROM tickets WHERE status = 'In Progress'"
            ).fetchone()[0],
            "resolved": conn.execute(
                "SELECT COUNT(*) FROM tickets WHERE status = 'Resolved'"
            ).fetchone()[0],
        }
        conn.close()
        return render_template("index.html", counts=counts)

    @app.route("/submit", methods=["GET", "POST"])
    def submit():
        if request.method == "POST":
            name = request.form.get("student_name", "").strip()
            email = request.form.get("email", "").strip().lower()
            category = request.form.get("category", "").strip()
            description = request.form.get("description", "").strip()

            if not name or len(name) > 100:
                flash("Enter a name (maximum 100 characters).", "error")
            elif "@" not in email or len(email) > 254:
                flash("Enter a valid email address.", "error")
            elif category not in CATEGORIES:
                flash("Choose a valid issue category.", "error")
            elif not description or len(description) > 2000:
                flash("Enter a description (maximum 2,000 characters).", "error")
            else:
                conn = get_db_connection()
                cursor = conn.execute(
                    """INSERT INTO tickets
                       (student_name, email, category, description)
                       VALUES (?, ?, ?, ?)""",
                    (name, email, category, description),
                )
                ticket_id = cursor.lastrowid
                conn.commit()
                conn.close()
                return render_template("success.html", ticket_id=ticket_id)

        return render_template("submit.html", categories=CATEGORIES)

    @app.route("/track", methods=["GET", "POST"])
    def track():
        ticket = None
        if request.method == "POST":
            ticket_id = request.form.get("ticket_id", "").strip()
            email = request.form.get("email", "").strip().lower()
            if not ticket_id.isdigit():
                flash("Enter a valid numeric ticket ID.", "error")
            else:
                conn = get_db_connection()
                ticket = conn.execute(
                    "SELECT * FROM tickets WHERE id = ? AND email = ?",
                    (int(ticket_id), email),
                ).fetchone()
                conn.close()
                if ticket is None:
                    flash("No complaint matched that ticket ID and email.", "error")
        return render_template("track.html", ticket=ticket)

    @app.route("/admin/login", methods=["GET", "POST"])
    def admin_login():
        if request.method == "POST":
            password = request.form.get("password", "")
            if password and password == app.config["ADMIN_PASSWORD"]:
                session.clear()
                session["is_admin"] = True
                flash("You are now signed in.", "success")
                return redirect(url_for("admin"))
            flash("Incorrect admin password.", "error")
        return render_template("admin_login.html")

    @app.route("/admin/logout", methods=["POST"])
    def admin_logout():
        session.clear()
        flash("You have been signed out.", "success")
        return redirect(url_for("home"))

    @app.route("/admin", methods=["GET", "POST"])
    def admin():
        if not session.get("is_admin"):
            return redirect(url_for("admin_login"))

        conn = get_db_connection()
        if request.method == "POST":
            ticket_id = request.form.get("ticket_id", "").strip()
            status = request.form.get("status", "")
            priority = request.form.get("priority", "")
            if not ticket_id.isdigit() or status not in STATUSES or priority not in PRIORITIES:
                flash("Invalid ticket update. Please try again.", "error")
            else:
                conn.execute(
                    "UPDATE tickets SET status = ?, priority = ? WHERE id = ?",
                    (status, priority, int(ticket_id)),
                )
                conn.commit()
                flash("Ticket updated successfully.", "success")

        tickets = conn.execute(
            "SELECT * FROM tickets ORDER BY created_at DESC, id DESC"
        ).fetchall()
        conn.close()
        return render_template(
            "admin.html", tickets=tickets, statuses=STATUSES, priorities=PRIORITIES
        )

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(os.environ.get("PORT", 5000)), debug=False)
