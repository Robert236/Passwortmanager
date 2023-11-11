###########
# Das Script muss noch einmalig ausgeführt werden!
###########

import sqlite3
connection = sqlite3.connect("passwort_manager.db")
cursor = connection.cursor()
cursor.execute("CREATE TABLE password_entry (id integer PRIMARY KEY AUTOINCREMENT, title TEXT, user_name TEXT, "
               "password TEXT, url TEXT, note TEXT);")

###########
# Ende!
###########
