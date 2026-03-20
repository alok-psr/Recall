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
            file_path  TEXT NOT NULL UNIQUE,
            ocr_text   TEXT,
            indexed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def save_file(file_path: str, ocr_text: str):
    conn = get_db()
    conn.execute("""
        INSERT INTO files (file_path, ocr_text)
        VALUES (?, ?)
    """, (file_path, ocr_text))
    conn.commit()
    conn.close()

def update_file(file_path: str, ocr_text: str):
    conn = get_db()
    conn.execute("""
        UPDATE files set ocr_text = ? 
        where file_path = ?
    """, ( ocr_text,file_path))
    conn.commit()
    conn.close()

def delete_file(file_path: str):
    conn = get_db()
    conn.execute("""
        DELETE from file 
        where file_path = ?
    """, ( file_path))
    conn.commit()
    conn.close()

def search_files_ocr(query: str):
    conn = get_db()
    results = conn.execute("""
        SELECT file_path, ocr_text
        FROM files WHERE ocr_text LIKE ?
    """, (f"%{query}%",)).fetchall()
    conn.close()
    return [dict(row) for row in results]


def get_all_files():
    conn = get_db()
    results = conn.execute("SELECT * FROM files").fetchall()
    conn.close()
    return [dict(row) for row in results]


def get_all_files_path():
    conn = get_db()
    results = conn.execute("SELECT file_path FROM files").fetchall()
    conn.close()
    return [dict(row) for row in results]