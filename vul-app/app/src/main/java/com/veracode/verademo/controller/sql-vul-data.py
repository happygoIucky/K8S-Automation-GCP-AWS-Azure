19 cur = con.cursor()
20 cur.execute("select * from test where username = '%s'" % name)
21 data = str(cur.fetchall())

cur = con.cursor()
cur.execute("SELECT * FROM test WHERE username = %s", (name,))
data = str(cur.fetchall())