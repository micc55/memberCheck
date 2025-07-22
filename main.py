import os
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import streamlit as st
import pandas as pd
import datetime # 日付（本日）取得のため

# 定数：スプレッドシートIDとシート名
JOIN_SHEET_ID = "1hEJwSJ3PRuoA3xIk9mrfBKHr0t4tAkVoCkAR78-5RS4"
SHEET_NAME = "フォームの回答"

# JSONファイルの絶対パスを設定
# KEY_PATH = os.path.join(os.path.dirname(__file__),"credentials", "service_account.json")

# 必要なスコープ（ここではGoogle Sheets）
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# 認証情報の作成
# creds = Credentials.from_service_account_file(KEY_PATH, scopes=SCOPES)
creds = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=SCOPES
)

gc = gspread.authorize(creds)

def attendcheck(day=None):
    # スプレッドシートを開く
    sheet = gc.open_by_key(JOIN_SHEET_ID).worksheet(SHEET_NAME)

    # データ取得
    values = sheet.get_all_values()

    # 日付の指定がなければ今日にする（yyyy/M/d 形式）
    if day is None:
        target = datetime.now().strftime("%Y/%#m/%#d")
    else:
        target = day

    # 日付に一致する行を抽出（2列目：values[i][1] が対象）
    day_data = [row for row in values if len(row) > 1 and row[1] == target]

    return day_data

st.subheader("参加者確認")
d = st.date_input("確認日", datetime.date.today())
# checkDay = d.strftime("%Y/") + str(d.month) + "/" + str(d.day)
checkDay = d.strftime("%Y/%#m/%#d")

data = attendcheck(checkDay)
# print(data)

dispmembers = []
pay = ""
for row in data:
    if len(row) > 2:
        if row[4] == "いいえ":
            pay = "×"
        else:
            pay = "〇"
    dispmembers.append({"コートネーム": row[3],"氏名": row[2], "参加費":pay})


# 日付に該当するデータを取得
df = pd.DataFrame(dispmembers)

# インデックスを1から開始
df.index = range(1, len(df) + 1)  
st.table(df)

