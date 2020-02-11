import sqlite3 

con = sqlite3.connect("ankaraUni.db") # veritabanına bağlanıyor
cursor = con.cursor()

# tabloya izinli gözetmen ekleniyor.
def izinli_tablosu_veri_ekle(izinliler, tarih):
    cursor.execute("CREATE TABLE IF NOT EXISTS izinliler (izinliler TEXT, tarih TEXT)")
    con.commit()
    cursor.execute("INSERT INTO izinliler VALUES(?,?)",(izinliler, tarih,))
    con.commit()

# izinli seçilirken eski izinli tablosu sıfırlanıyor.
def izinli_tablosu_sifirla():
    cursor.execute("DELETE FROM izinliler")
    con.commit()


# O tarihte izinli gözetmenler varsa dönderiliyor yoksa X, Y değeri dönderiliyor. X, Y nin karşıda bir anlamı yok.
# O gün kimsenin izlinli olmadığı anlaşılıyor
def izinli_tablosu_veri_cek(tarih):
    cursor.execute("Select izinliler From izinliler WHERE tarih = ?", (tarih,))
    try:
        return cursor.fetchall()[0][0]
    except:
        return 'X,Y'


def tum_izinlileri_goruntule():
    cursor.execute("Select * From izinliler")
    return cursor.fetchall()