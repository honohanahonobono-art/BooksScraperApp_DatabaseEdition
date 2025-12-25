import sqlite3

conn = sqlite3.connect("books.db")
cur = conn.cursor()

cur.execute("""SELECT title,rating FROM books ORDER BY rating DESC LIMIT 5""")
rows = cur.fetchall()

for row in rows:
    print(row)
#print("登録件数：",cur.fetchone()[0])
conn.close()

