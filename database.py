import sqlite3
from flask import current_app, g


def get_db_connection():
    if "db" not in g:
        database = current_app.config["DATABASE"]
        g.db = sqlite3.connect(database)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def close_db(_error=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = get_db_connection()
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT NOT NULL,
            email TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT NOT NULL,
            priority TEXT NOT NULL DEFAULT 'Medium'
                CHECK(priority IN ('Low', 'Medium', 'High')),
            status TEXT NOT NULL DEFAULT 'Pending'
                CHECK(status IN ('Pending', 'In Progress', 'Resolved')),
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    db.commit()


def register_database(app):
    app.teardown_appcontext(close_db)
