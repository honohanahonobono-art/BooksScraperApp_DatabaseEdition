import sqlite3
from pathlib import Path

#DBファイルのパス設定
DB_PATH = Path(__file__).resolve().parent / "books.db"

def init_db():
    """データベースの初期化を行う関数"""
    # ① books.db というデータベースファイルに接続
    conn = sqlite3.connect(DB_PATH)

    # ② SQLを実行するためのカーソルを取得
    cur = conn.cursor()

    # ③ books というテーブルを作成
    cur.execute("""
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        price REAL,
        link TEXT,
        stock INTEGER,
        rating INTEGER
    );
    """)

    # ④ 変更を保存
    conn.commit()

    # ⑤ 接続を閉じる
    conn.close()




# テスト用の1件
#cur.execute("""
#INSERT INTO books (title, price, link, stock, rating)
#VALUES (?, ?, ?, ?, ?)
#""", (
#    "Test Book",
#    9.99,
#    "https://example.com/test-book",
#    5,
#    4
#))

#conn.commit()






