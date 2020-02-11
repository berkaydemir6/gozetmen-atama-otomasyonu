def sinav_sistemi(izinli_ogretmenler, dersler, ogretmen):
    sinav_atama = []
    eski_deger = 100
    ders_sayisi = len(dersler)
    # Gelen öğretmen listesindeki durumu en düşük olan öğretmen bulunuyor.
    for durum in ogretmen:
        if ogretmen[durum] < eski_deger:
            eski_deger = ogretmen[durum] # En düşük duruma sahip gözetmen.
    ders_ogretim_gorevlisi = {}
    while ders_sayisi != 0: # Ders sayısı bitmediği sürece atama yapılıyor.
        for ders in dersler:
            for i in ogretmen:
                if i not in izinli_ogretmenler and ders not in sinav_atama: # Öğretmen izinli öğretmenler listesinde değilse ve ders atanmamışsa.
                    if eski_deger == ogretmen[i]: # Gözetmen en düşük duruma sahip gözetmene eşitse atama yapılıyor.
                        ogretmen[i] += 1 # Gözetmenin durumu  bu sayfa için arttırılıyor.
                        sinav_atama.append(ders) # Ders, atanmış dersler listesine arttırılıyor.
                        ders_ogretim_gorevlisi[ders] = i
                        ders_sayisi -= 1 # Ders sayısı azaltılıyor.
                    else:
                        continue
        eski_deger += 1
    return ders_ogretim_gorevlisi

