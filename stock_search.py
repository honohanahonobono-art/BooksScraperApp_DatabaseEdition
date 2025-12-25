import sqlite3
import pandas as pd

DB_PATH="books.db"

def search_books(keyword:str,min_stock:int,stock_only:bool):
    conn=sqlite3.connect(DB_PATH)
    
    where=[]
    params=[]
    
    if keyword :
        where.append("title LIKE ?")
        params.append(f"%{keyword}%")
        
    if stock_only :
        where.append("stock>0")
    
    if min_stock is not None :
        where.append("stock>=?")
        params.append(int(min_stock))

    where_sql = "WHERE "+" AND ".join(where) if where else ""

    query=f"""
        SELECT title, price, link, stock, rating
        FROM books
        {where_sql}
        ORDER BY rating DESC, stock DESC, price ASC
        """
    df=pd.read_sql_query(query,conn,params=params)
    conn.close()
    return df
    


