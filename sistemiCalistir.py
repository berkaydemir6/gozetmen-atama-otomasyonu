import gozetmenTablosuOlustur
import excel
import string
import gunAtamaYap
import sinavTablosuOlustur
import datetime
import locale


def excel_gozetmenler():
    alfabe1 = list(string.ascii_uppercase) # Alfabenin tüm harfleri
    alfabe2 = list(string.ascii_uppercase) # Alfabenin tüm harfleri
    alfabe1.pop(0) # Alfabe1 den A'yı atıyoruz
    alfabe1.pop(0) # Alfabe1 den B'yi atıyoruz
    ogretmenler_listesi = []
    for harf in alfabe1:
        gunAtamaYap.atamayiBaslat(harf, excel.izin_icin_gunu_bul(harf)) # Alfadeki harflerin olduğu sütunlarda atama yapılması için fonksiyonu çağırıyoruz. Fonksiyonu harf gidiyor.
    for harf in alfabe2:
        gunAtamaYap.atamayiBaslat('A{}'.format(harf), excel.izin_icin_gunu_bul('A{}'.format(harf))) # Alfadeki A ile başlayan (örnek AA AB) harflerin olduğu sütunlarda atama yapılması için fonksiyonu çağırıyoruz. Fonksiyonu harf gidiyor.
    for harf in alfabe2:
        gunAtamaYap.atamayiBaslat('B{}'.format(harf), excel.izin_icin_gunu_bul('B{}'.format(harf)))
    for harf in alfabe2:
        if excel.deger_oku('C{}'.format(harf)): # C sütununun hepsinde veri olmadığı için hata almamak için değer olan kutucukta atama yapıyor.
            gunAtamaYap.atamayiBaslat('C{}'.format(harf), excel.izin_icin_gunu_bul('C{}'.format(harf)))


# Tarih listesi oluşturuyor.
def tarih_listesi_olustur():
    locale.setlocale(locale.LC_ALL, '') # Türkçe için
    alfabe1 = list(string.ascii_uppercase)
    alfabe2 = list(string.ascii_uppercase)
    alfabe1.pop(0)
    alfabe1.pop(0)
    tarih_listesi = []
    for harf in alfabe1:
        if excel.tarih(harf, 1):
            tarih_listesi.append(excel.tarih(harf, 1))
    for harf in alfabe2:
        if excel.tarih('A{}'.format(harf), 1):
            tarih_listesi.append(excel.tarih('A{}'.format(harf), 1))
    for harf in alfabe2:
        if excel.tarih('B{}'.format(harf), 1):
            tarih_listesi.append(excel.tarih('B{}'.format(harf), 1))
    for harf in alfabe2:
        if excel.deger_oku('C{}'.format(harf)):
            if excel.tarih('C{}'.format(harf), 1):
                tarih_listesi.append(excel.tarih('C{}'.format(harf), 1))
    return tarih_listesi
