import sqlite3

def get_db():
    conn = sqlite3.connect("recall.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS files (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            file_path  TEXT NOT NULL,
            ocr_text   TEXT,
            clip_tags  TEXT,
            indexed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def save_file(file_path: str, ocr_text: str, clip_tags: str):
    conn = get_db()
    conn.execute("""
        INSERT INTO files (file_path, ocr_text, clip_tags)
        VALUES (?, ?, ?)
    """, (file_path, ocr_text, clip_tags))
    conn.commit()
    conn.close()

def search_files(query: str):
    conn = get_db()
    results = conn.execute("""
        SELECT file_path, ocr_text, clip_tags
        FROM files WHERE ocr_text LIKE ?
    """, (f"%{query}%",)).fetchall()
    conn.close()
    return [dict(row) for row in results]


def get_all_files():
    conn = get_db()
    results = conn.execute("SELECT * FROM files").fetchall()
    conn.close()
    return [dict(row) for row in results]