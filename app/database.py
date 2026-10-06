import sqlite3

DATABASE = "events.db"


def get_db():
    db = sqlite3.connect(DATABASE, detect_types=sqlite3.PARSE_DECLTYPES, check_same_thread=False)
    db.row_factory = sqlite3.Row
    try:
        yield db
    finally:
        db.close()


def init_db():
    db = sqlite3.connect(DATABASE)
    db.executescript("""
        CREATE TABLE IF NOT EXISTS events (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT    NOT NULL,
            description TEXT    NOT NULL,
            location    TEXT    NOT NULL,
            date        TEXT    NOT NULL,
            capacity    INTEGER NOT NULL
        );
    """)
    db.commit()

    if db.execute("SELECT COUNT(*) FROM events").fetchone()[0] == 0:
        db.executescript("""
            INSERT INTO events (name, description, location, date, capacity) VALUES
                ('AI in the Enterprise',
                 'A full-day conference exploring how organizations are adopting AI responsibly at scale.',
                 'New York, NY',
                 '2026-09-18',
                 300),
                ('DevOps & Platform Engineering Summit',
                 'Best practices in CI/CD pipelines, platform teams, and internal developer portals.',
                 'Armonk, NY',
                 '2026-10-02',
                 150),
                ('Cloud Architecture Workshop',
                 'Hands-on workshop covering multi-cloud design patterns and cost optimization.',
                 'Austin, TX',
                 '2026-11-13',
                 60),
                ('Security & Compliance Forum',
                 'Panel discussions on threat modeling, zero-trust architecture, and regulatory compliance.',
                 'Research Triangle Park, NC',
                 '2026-12-04',
                 200);
        """)
        db.commit()

    db.close()
