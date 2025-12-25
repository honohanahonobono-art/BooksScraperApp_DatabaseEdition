import sqlite3
import pandas as pd

DB_PATH="books.db"



def load_stock_alert(threshold:int):
    conn=sqlite3.connect(DB_PATH)
    query="""
    SELECT title,price,link,stock,rating
    FROM books
    WHERE stock<=?
    ORDER BY stock ASC,rating DESC
    """
    df=pd.read_sql_query(query,conn,params=(threshold,))
    conn.close()
    return df