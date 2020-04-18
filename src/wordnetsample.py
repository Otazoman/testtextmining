import sqlite3
conn = sqlite3.connect("../models/wnjpn.db")

cur = conn.execute("select count(*) from word")
for row in cur:
    print("Wordnetに登録されているWordDBの単語数：%s" % row[0])
