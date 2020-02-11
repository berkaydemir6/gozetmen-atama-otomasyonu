import sqlite3 

con = sqlite3.connect("ankaraUni.db") # veritabanına bağlanıyor
cursor = con.cursor()

# Genel gözetmen tablosuna veri ekleniyor.
def genel_tablosu_veri_ekle(ders_adi, sinav_saati, ders_hocasi, sinif, gun, gozetmenler):
    cursor.execute("CREATE TABLE IF NOT EXISTS genel (ders_adi TEXT, sinav_saati TEXT, ders_hocasi TEXT, sinif TEXT, gun TEXT, gozetmenler TEXT)")
    con.commit()
    cursor.execute("INSERT INTO genel VALUES(?,?,?,?,?,?)",(ders_adi, sinav_saati, ders_hocasi, sinif, gun, gozetmenler,))
    con.commit()


# Genel gözetmen tablosu sıfırlanıyor.
def genel_tablosu_sifirla():
    cursor.execute("DROP TABLE genel")
    con.commit()
    cursor.execute("CREATE TABLE genel (ders_adi TEXT, sinav_saati TEXT, ders_hocasi TEXT, sinif TEXT, gun TEXT, gozetmenler TEXT)")
    con.commit()

# Genel gözetmen tablosundan verilen tarihe göre veri çekiliyor. Genel program sayfası için.
def genel_tablosu_veri_cek(gun):
    cursor.execute("Select * From genel WHERE gun = ?", (gun,))
    return cursor.fetchall()

# Distinct ile sınav olan günler teke düşürülüyor.
def gun_sayisi():
    cursor.execute("Select Distinct gun From genel")
    gun_listesi = []
    for i in cursor.fetchall():
        gun_listesi.append(i[0])
    return gun_listesi