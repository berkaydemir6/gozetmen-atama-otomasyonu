import excel
import gozetmenTablosuOlustur
import olustur
import izinliTablosuOlustur
import sinavTablosuOlustur
import genelSinavTablosuOlustur


def atamayiBaslat(sutun, izin_tarih):
    gun = excel.gozetmen_sinav_sayisi(excel.ogretmen_listesi_olustur(sutun, 5)) # Bugün yalnızca kendi sınavı olan öğretim görevlileri alınıyor.
    gozetmenler = excel.ogretmen_listesi_olustur(sutun, 5) # Bugün kendi sınavı olan öğretim görevlileri alınıyor.
    saat = excel.tarih(sutun, 2) # Gelen sütuna göre o saat verisi Excel'den alınıyor.
    izinli_hocalar_tablosu = izinliTablosuOlustur.izinli_tablosu_veri_cek(izin_tarih) # O tarihte izinli olan hocalar alınıyor.
    izinliler_listesi = []
    for izinli_hoca in izinli_hocalar_tablosu.split(","): # Gelen veri türüne göre ayrıştırılıyor.
        izinliler_listesi.append(izinli_hoca) # Bugün izinli olan öğretim görevlileri, izinliler listesine ekleniyor.
    for gozetmen in gozetmenler: 
        izinliler_listesi.append(gozetmen) # Bugün sınavı olan gözetmenler izinli listesine ekleniyor.
    izinli_ogretmenler = izinliler_listesi
    ogretmen = gozetmenTablosuOlustur.ogretmen_sozlugu()
    gozetmen_olmayacaklar = gun[-1] # Gözetmen olmayacaklar değişkeni iki veri dönderiyor. Aynı saatte kendi dersi olanlar ve birden fazla dersi olanlar 1. indis birden fazla dersi olanlar. Bunu bir değişkene atıyoruz.
    gun.pop(-1) # Birden fazla dersi olanları atıyoruz ve elimizde kendi dersi olanlar kalıyor.


    for tek_ogretmen in gun: # Kendi sınavı olan öğretim görevlileri arasında atama yapılıyor.
        i = 0
        for gozetmen in gozetmenler:
            if tek_ogretmen == gozetmen: # Bugün sınavı olan öğretim görevlileri arasında kendi dersi olanlar tüm öğretim görevlilerinin listesiyle karşılaştırılarak kendi dersi olan için atama başlıyor.
                try: # Eğer sınava girecek öğrenci sayısı kutucuğunda veri varsa alınıyor
                    ogrenci_sayisi = excel.ogrenci_sayisi_listesi_olustur(sutun, 4)[i]
                except: # Yoksa 1 olarak varsayılıyor.
                    ogrenci_sayisi = 1
                ders_adi = excel.ders_listesi_olustur(sutun, 3)[i] # Ders adı Excel'den alınıyor.
                sinif_ve_kapasite = (excel.sinif_ve_kapasite_listesi_olustur(sutun)[i]).split('*') # Sınıf ve kapasite de Excel'den alınıyor.
                if ogrenci_sayisi < 40: # Sınava girecek öğrenci sayısı 40'tan küçükse atama fonksiyonu çağırılmıyor. Kendi dersi olan öğretim görevlisinin durumu 1 arttırılıyor ve atanmış olarak veritabanına ekleniyor.
                    durum = gozetmenTablosuOlustur.durum_goruntule(tek_ogretmen) + 1 # Durumu değişkene aldık ve 1 arttırdık
                    gozetmenTablosuOlustur.durum_guncelle(tek_ogretmen, durum) # Arttırdığımız durumu güncelledik
                    sinavTablosuOlustur.sinav_tablosu_veri_ekle(ders_adi, saat.hour, tek_ogretmen, sinif_ve_kapasite[1], excel.gunu_bul(sutun), tek_ogretmen, tek_ogretmen) # Gerekli verilerle birlikte sınav sayfası için sınav veritabanına ekledik.
                    genelSinavTablosuOlustur.genel_tablosu_veri_ekle(ders_adi, saat.hour, tek_ogretmen, sinif_ve_kapasite[1], excel.gunu_bul(sutun), tek_ogretmen) # Gerekli verilerle birlikte genel sayfası için genel veritabanına ekledik.
                    print("Gözetmen: {} Ders Adı: {} Sınıf: {} - Kapasite: {} Öğrenci Sayısı: {} Saat: {} Durum: {}".format(tek_ogretmen, ders_adi, sinif_ve_kapasite[1], sinif_ve_kapasite[2], ogrenci_sayisi, saat.hour, durum))    
                else: # # Sınava girecek öğrenci sayısı 40'tan büyükse
                    durum = gozetmenTablosuOlustur.durum_goruntule(tek_ogretmen) + 1 # Kendi dersi olan gözetmenin durumu arttırılıyor.
                    gozetmenTablosuOlustur.durum_guncelle(tek_ogretmen, durum) # Durum güncelleniyor.
                    atama_yap = olustur.sinav_sistemi(izinli_ogretmenler, [ders_adi], ogretmen) # Öğretim görevlisinin yanına bir gözetmen atanıyor.
                    diger_gozetmen = atama_yap[ders_adi] # Diğer gözetmenin adı alınıyor.
                    durum = gozetmenTablosuOlustur.durum_goruntule(diger_gozetmen) + 1 # Durumu alınıyor ve arttırılıyor.
                    gozetmenTablosuOlustur.durum_guncelle(diger_gozetmen, durum)  # Durumu güncelleniyor.
                    izinli_ogretmenler.append(diger_gozetmen) # Aynı saatte yapılan diğer atamalarda atanmaması için izinli listesine ekleniyor.
                    sinavTablosuOlustur.sinav_tablosu_veri_ekle(ders_adi, saat.hour, tek_ogretmen, sinif_ve_kapasite[1], excel.gunu_bul(sutun), tek_ogretmen, tek_ogretmen + ", " + diger_gozetmen) # Her iki gözetmeninde kendi sayfasında erişebilmesi için 5. indiste kendi isimlerini gönderiyoruz. Veritabanından da o bölümden çağırarak iki gözetmenin de sayfasında görünmesini sağlıyoruz. Veritabanına ekledik.
                    sinavTablosuOlustur.sinav_tablosu_veri_ekle(ders_adi, saat.hour, tek_ogretmen, sinif_ve_kapasite[1], excel.gunu_bul(sutun), diger_gozetmen, diger_gozetmen + ", " + tek_ogretmen) # Her iki gözetmeninde kendi sayfasında erişebilmesi için 5. indiste kendi isimlerini gönderiyoruz. Veritabanından da o bölümden çağırarak iki gözetmenin de sayfasında görünmesini sağlıyoruz. Veritabanına ekledik.
                    genelSinavTablosuOlustur.genel_tablosu_veri_ekle(ders_adi, saat.hour, tek_ogretmen, sinif_ve_kapasite[1], excel.gunu_bul(sutun), tek_ogretmen + ", " + diger_gozetmen) # Genel sınav tablosuna ekliyoruz.
                    print("Gözetmenler: {}, {} - Ders Adı: {} Sınıf: {} - Kapasite: {} Öğrenci Sayısı: {} Saat: {}  Durum: {}".format(tek_ogretmen, diger_gozetmen, ders_adi, sinif_ve_kapasite[1], sinif_ve_kapasite[2], ogrenci_sayisi, saat.hour, durum))
                print("-----")
            i += 1

    # Bugün dersi olan gözetmen listesini aldık. Ancak birden fazla ve tek dersi olan ayrımı olduğu için indisleri çakışıyor. For döngüsünde o listeyi kullanamayız.
    # Bu yüzden birden fazla dersi olanların indis sırasını bir listeye atıyoruz.
    ders_listesi = []
    for ogretmencim in gozetmen_olmayacaklar:
        a = 0
        for gozetmen in gozetmenler:
            if ogretmencim == gozetmen:
                ders_listesi.append(a)
            a += 1

    birden_fazla = []
    for indis in ders_listesi:
        try: # Eğer sınava girecek öğrenci sayısı kutucuğunda veri varsa alınıyor
            ogrenci_sayisi = excel.ogrenci_sayisi_listesi_olustur(sutun, 4)[indis]
        except: # Yoksa 1 olarak varsayılıyor.
            ogrenci_sayisi = 1
        ders_adi = excel.ders_listesi_olustur(sutun, 3)[indis] # Gelen indise göre ders listesi fonksiyonundan gelen bizim indisimizde olan veriyi alıyoruz.
        ders_hocasi = excel.ogretmen_listesi_olustur(sutun, 5)[indis] # İndisimizde hangi öğretim görevlisi varsa fonksiyon ile alıyoruz. Karşıdan gelen fonksiyon tüm öğretim görevlilerini veriyor. Biz indisi belirterek doğru öğretim görevlisini alıyoruz.
        sinif_ve_kapasite = (excel.sinif_ve_kapasite_listesi_olustur(sutun)[indis]).split('*')
        print('Sınıf: {} Kapasite: {} Öğrenci Sayısı: {}'.format(sinif_ve_kapasite[1], sinif_ve_kapasite[2], ogrenci_sayisi))
        print('Ders Adı: {} - Ders Hocası: {} - Saat: {}'.format(ders_adi, ders_hocasi, saat.hour))
        if ogrenci_sayisi < 40: # Sınava girecek öğrenci sayısı 40'tan küçükse 1 gözetmen atanacak.
            if not ders_hocasi in birden_fazla: # Birden fazla dersi olan öğretim görevlisinin durumunu her seferinde arttırmamak için kontrol ediyoruz.
                durum = gozetmenTablosuOlustur.durum_goruntule(ders_hocasi) + 1
                gozetmenTablosuOlustur.durum_guncelle(ders_hocasi, durum)
                birden_fazla.append(ders_hocasi)
                print('Dersin hocasının durumu: {}'.format(durum))
            # Aynı fonksiyonlar yukarıda belirtildiği için ek yorum satırı yazmıyorum.
            atama_yap = olustur.sinav_sistemi(izinli_ogretmenler, [ders_adi], ogretmen)
            gozetmen_tek = atama_yap[ders_adi]
            durum = gozetmenTablosuOlustur.durum_goruntule(gozetmen_tek) + 1
            gozetmenTablosuOlustur.durum_guncelle(gozetmen_tek, durum)
            print('Gözetmen: {}, Durum: {}'.format(gozetmen_tek, durum))
            izinli_ogretmenler.append(gozetmen_tek)
            sinavTablosuOlustur.sinav_tablosu_veri_ekle(ders_adi, saat.hour, ders_hocasi, sinif_ve_kapasite[1], excel.gunu_bul(sutun), gozetmen_tek, gozetmen_tek)
            sinavTablosuOlustur.sinav_tablosu_veri_ekle(ders_adi, saat.hour, ders_hocasi, sinif_ve_kapasite[1], excel.gunu_bul(sutun), ders_hocasi, gozetmen_tek) # Sınavın, dersin hocasının sayfasında da görünmesi için 6. indise ders hocasına da bu sınavı ekliyoruz.
            genelSinavTablosuOlustur.genel_tablosu_veri_ekle(ders_adi, saat.hour, ders_hocasi, sinif_ve_kapasite[1], excel.gunu_bul(sutun), gozetmen_tek)
        else: # Sınava girecek öğrenci sayısı 40'tan küçükse 1 gözetmen atanacak.
            if not ders_hocasi in birden_fazla:
                durum = gozetmenTablosuOlustur.durum_goruntule(ders_hocasi) + 1
                gozetmenTablosuOlustur.durum_guncelle(ders_hocasi, durum)
                birden_fazla.append(ders_hocasi)
                print('Dersin hocasının durumu: {}'.format(durum))
            atama_yap = olustur.sinav_sistemi(izinli_ogretmenler, [ders_adi], ogretmen)
            gozetmen_1 = atama_yap[ders_adi]
            durum1 = gozetmenTablosuOlustur.durum_goruntule(gozetmen_1) + 1
            gozetmenTablosuOlustur.durum_guncelle(gozetmen_1, durum1)
            izinli_ogretmenler.append(gozetmen_1)
            atama_yap = olustur.sinav_sistemi(izinli_ogretmenler, [ders_adi], ogretmen)
            gozetmen_2 = atama_yap[ders_adi]
            durum2 = gozetmenTablosuOlustur.durum_goruntule(gozetmen_2) + 1
            gozetmenTablosuOlustur.durum_guncelle(gozetmen_2, durum2)
            izinli_ogretmenler.append(gozetmen_2)
            # Hem 1. hem 2. hem de ders hocasına bu sınav ekleniyor.
            sinavTablosuOlustur.sinav_tablosu_veri_ekle(ders_adi, saat.hour, ders_hocasi, sinif_ve_kapasite[1], excel.gunu_bul(sutun), gozetmen_1, gozetmen_1 + ", " + gozetmen_2)
            sinavTablosuOlustur.sinav_tablosu_veri_ekle(ders_adi, saat.hour, ders_hocasi, sinif_ve_kapasite[1], excel.gunu_bul(sutun), gozetmen_2, gozetmen_2 + ", " + gozetmen_1)
            sinavTablosuOlustur.sinav_tablosu_veri_ekle(ders_adi, saat.hour, ders_hocasi, sinif_ve_kapasite[1], excel.gunu_bul(sutun), ders_hocasi, gozetmen_1 + ", " + gozetmen_2)
            genelSinavTablosuOlustur.genel_tablosu_veri_ekle(ders_adi, saat.hour, ders_hocasi, sinif_ve_kapasite[1], excel.gunu_bul(sutun), gozetmen_1 + ", " + gozetmen_2)
            print('Gözetmenler: {} Durum: {}, {} Durum:  {}'.format(gozetmen_1, durum1, gozetmen_2, durum2))        
        print("-----")
    for ogretmen in gun: # Burayı ne için yazdığımı hatırlamıyorum. Sanırım kullanılmıyor ama yine de silmedim.
        tek_ders = []
        a = 0