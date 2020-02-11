import sqlite3 

con = sqlite3.connect("ankaraUni.db")  # veritabanına bağlanıyor
cursor = con.cursor()

# Ataması yapılan sınavı veritabanına ekliyoruz.
# Veri çekerken daha ayrıntılı olması için ders hocasına göre listeleme, gözetmene göre listeleme ve sınava hangi öğretim görevlilerinin gözetmen olacağını veritabanına aktarıyoruz.
def sinav_tablosu_veri_ekle(ders_adi, sinav_saati, ders_hocasi, sinif, gun, gozetmen, gozetmenler):
    cursor.execute("CREATE TABLE IF NOT EXISTS sinavlar (ders_adi TEXT, sinav_saati TEXT, ders_hocasi TEXT, sinif TEXT, gun TEXT, gozetmen TEXT, gozetmenler TEXT)")
    con.commit()
    cursor.execute("INSERT INTO sinavlar VALUES(?,?,?,?,?,?,?)",(ders_adi, sinav_saati, ders_hocasi, sinif, gun, gozetmen, gozetmenler,))
    con.commit()

# Yeni atama yapılacağı zaman veritabanı sıfırlanıyor.
def sinav_tablosu_sifirla():
    cursor.execute("DROP TABLE sinavlar")
    con.commit()
    cursor.execute("CREATE TABLE sinavlar (ders_adi TEXT, sinav_saati TEXT, ders_hocasi TEXT, sinif TEXT, gun TEXT, gozetmen TEXT, gozetmenler TEXT)")
    con.commit()


def sinav_tablosu_veri_cek(gozetmen):
    cursor.execute("Select * From sinavlar WHERE gozetmen = ?", (gozetmen,))
    return cursor.fetchall()


# Tekil halde gözetmen olan öğretim görevlilerinin listesi alınıyor.
def sinava_girecek_hocalar():
    cursor.execute("Select Distinct gozetmen From sinavlar")
    ogretmen_listesi = []
    for i in cursor.fetchall():
        ogretmen_listesi.append(i[0])
    return ogretmen_listesi