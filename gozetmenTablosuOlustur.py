import sqlite3
import excel
import string

con = sqlite3.connect("ankaraUni.db") # veritabanına bağlanıyor
cursor = con.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS gozetmen_listesi (isim TEXT, durum INT)") # tablo oluşturuluyor
con.commit()

def excel_gozetmenler():
    alfabe = list(string.ascii_uppercase)

    ogretmenler_listesi = []
    # A. B. C. AA dan başlayarak tüm alfabe dönüyor. Her seferinde farklı bir sütun etkileniyor.
    # Bu şekilde her sütundaki gözetmen alınıyor.
    for harf in alfabe:
        gecici_liste = []
        gecici_liste = excel.ogretmen_listesi_olustur("A{}".format(harf), 5)
        for ogretmen in gecici_liste:
            if ogretmen not in ogretmenler_listesi:
                ogretmenler_listesi.append(ogretmen)

    for harf in alfabe:
        gecici_liste = []
        gecici_liste = excel.ogretmen_listesi_olustur("B{}".format(harf), 5)
        for ogretmen in gecici_liste:
            if ogretmen not in ogretmenler_listesi:
                ogretmenler_listesi.append(ogretmen)

    for harf in alfabe:
        gecici_liste = []
        gecici_liste = excel.ogretmen_listesi_olustur("C{}".format(harf), 5)
        for ogretmen in gecici_liste:
            if ogretmen not in ogretmenler_listesi:
                ogretmenler_listesi.append(ogretmen)

    #A ve B harflerinde gözetmen olmadığı için bunlar çıkarılarak C den başlayıp alfabenin son harfine kadar dönüyor.
    alfabe.pop(0)
    alfabe.pop(0)

    for harf in alfabe:
        gecici_liste = []
        gecici_liste = excel.ogretmen_listesi_olustur(harf, 5)
        for ogretmen in gecici_liste:
            if ogretmen not in ogretmenler_listesi:
                ogretmenler_listesi.append(ogretmen)

    ogretmenler = { i : 0 for i in ogretmenler_listesi }
    return ogretmenler

# Yeni excel eklendiğinde eski gözetmen tablosu sıfırlanıyor.
def veritabani_olustur():
    cursor.execute("DELETE FROM gozetmen_listesi") 
    gozetmenler = excel_gozetmenler()
    for gozetmen in gozetmenler:
        cursor.execute("INSERT INTO gozetmen_listesi (isim, durum) VALUES(?,?)",(gozetmen, gozetmenler.get(gozetmen))) 
        con.commit()

# Her atama yapıldığında gözetmenin durumu arttırılıyor. gunAtamaYap dosyasından gelen veri ile.
def durum_guncelle(isim, durum): 
    cursor.execute("Update gozetmen_listesi Set durum =  ? where isim = ?",(durum, isim)) 
    con.commit()

# Gözetmenin durumu görüntüleniyor.
def durum_goruntule(isim):
    cursor.execute("Select durum From gozetmen_listesi Where isim = ?",(isim,)) 
    return cursor.fetchall()[0][0]

# Sayaç sayfası için tüm gözetmenlerin durumları.
def tum_durumlari_goruntule():
    cursor.execute("Select * From gozetmen_listesi") 
    return cursor.fetchall()

# Atama yap sayfasına gönderilmesi için sözlük şeklinde gözetmen:durum verisi ediniliyor.
def ogretmen_sozlugu():
    ogretmen_sozlugu = {}
    cursor.execute("Select * From gozetmen_listesi")
    for i in cursor.fetchall():
        ogretmen_sozlugu[i[0]] = i[1]
    return ogretmen_sozlugu