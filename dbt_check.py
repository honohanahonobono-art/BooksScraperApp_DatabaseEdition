import sqlite3

conn = sqlite3.connect("books.db")
cur = conn.cursor()

# テーブル一覧
cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cur.fetchall())

# categoriesの中身を先頭5件
cur.execute("SELECT category_name, average_rating, score FROM categories ORDER BY average_rating DESC LIMIT 5;")
print(cur.fetchall())

conn.close()
