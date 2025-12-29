import sqlite3
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt


#日本語フォント設定
from pathlib import Path
from matplotlib import font_manager, rcParams

FONT_PATH = Path(__file__).parent / "fonts" / "NotoSansJP-Regular.ttf"

# デフォルト
rcParams["font.family"] = "DejaVu Sans"

# フォントがあれば、それを“直接使う”設定にする（登録しない）
if FONT_PATH.exists():
    jp_font = font_manager.FontProperties(fname=str(FONT_PATH))
else:
    jp_font = None
    
import streamlit as st

with st.sidebar:
    st.header("⚙️ 表示設定")
    stock_only = st.checkbox("📦 在庫ありのみ表示", value=True)



# Streamlitアプリの設定
st.set_page_config(page_title="Book App",layout="wide")

st.title("📚　在庫確認ページ　📚")

# 在庫検索　

from stock_search import search_books
st.subheader("🔍　在庫検索　🔍")

with st.form("search_form"):
    col1,col2,col3=st.columns([2,2,1])
    with col1:
        keyword=st.text_input("キーワード検索（タイトルに含む）",value="")
    with col2:
        min_stock_raw=st.text_input("最低在庫数絞込（未入力OK）",value="")
    with col3:
        submitted=st.form_submit_button("検索")
    min_stock=None
    input_error=False
    if min_stock_raw.strip():
        try:
            min_stock_val=int(min_stock_raw)
            if min_stock_val<0:
                st.warning("最低在庫数は0以上で入力してください")
                input_error=True
            else:
                min_stock=min_stock_val
        except ValueError:
            st.error("最低在庫数は数字で入力してください")
            input_error=True

if submitted and not input_error:
    df_search=search_books(keyword,min_stock,stock_only)
    st.caption(f"検索結果：{len(df_search)}件")
    st.data_editor(
        df_search,
        column_config={"link":st.column_config.LinkColumn("詳細ページ",display_text="詳細ページ")},
        hide_index=True,
        use_container_width=True
    )
elif not submitted:
    st.info("検索条件を入力して「検索」を押してください")
