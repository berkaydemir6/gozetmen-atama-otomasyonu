import sqlite3 

con = sqlite3.connect("ankaraUni.db") #veritabanına bağlandık
cursor = con.cursor()

# /program sayfası için gelen tarih ve gözetmen bilgisine göre sınav bilgisi alma
def genel_veri_cek(saat, gozetmen):
    cursor.execute("Select * From sinavlar where sinav_saati = ? and gozetmen = ?",(saat,gozetmen)) 
    return cursor.fetchall()