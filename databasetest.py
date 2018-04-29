import sqlite3

con = sqlite3.connect("user_credentials.db")

#con.execute("CREATE TABLE credentials (fname TEXT ,lname TEXT,email TEXT,mobile TEXT PRIMARY KEY ,password TEXT,address TEXT,area TEXT,city TEXT,pin TEXT,purpose TEXT,dataplan TEXT,visit TEXT,validity INTEGER DEFAULT 30)")
#con.execute("CREATE TABLE card_details (card_no TEXT PRIMARY KEY ,card_name TEXT NOT NULL ,expire TEXT NOT NULL ,cvc TEXT NOT NULL ,balance INTEGER DEFAULT 10000)")

#con.execute("DROP TABLE card_details")
#con.execute("DROP TABLE credentials")


cur = con.cursor()

cur.execute("SELECT * from credentials")
#cur.execute("SELECT * from card_details")

rows=cur.fetchall();
print(list(rows))

#cur.execute("DELETE from credentials")
#cur.execute("DELETE from card_details")

#con.commit()
con.close()