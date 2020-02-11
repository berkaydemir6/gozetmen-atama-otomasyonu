import sqlite3 

con = sqlite3.connect("ankaraUni.db") # veritabanına bağlanıyor
cursor = con.cursor()

# Eski dönem ismi silinip yenisi ekleniyor.
def donem_ekle(donem):
    cursor.execute("CREATE TABLE IF NOT EXISTS donem(donem TEXT)")
    con.commit()
    cursor.execute("DELETE FROM donem")
    con.commit()
    cursor.execute("INSERT INTO donem VALUES(?)",(donem,))
    con.commit()


def donem_veri_cek():
    cursor.execute("Select * From donem")
    return cursor.fetchall()[0][0]