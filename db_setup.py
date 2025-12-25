import sqlite3

# ① books.db というデータベースファイルに接続
conn = sqlite3.connect("books.db")

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

conn.commit()







# ⑤ 接続を閉じる
conn.close()
