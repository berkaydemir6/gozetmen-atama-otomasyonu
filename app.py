from bottle import Bottle, route, run, static_file, redirect, request, response
import os
import olustur
import gozetmenTablosuOlustur
import excel
import izinliTablosuOlustur
import sinavTablosuOlustur
import sistemiCalistir
import donemTablosuOlustur
import genelSinavTablosuOlustur
import WebTabloVeriCek


app = Bottle()

# Bu sayfa web tarafı için. Algoritmaları anlatmak oldukça zor.

# Anasayfa
@app.route('/')
def giris_yonlendir():
    return """<title>Ankara Üniversitesi</title><link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
<h3 class="display-3" style="margin-top: 30px;text-align: center;">Sınav Gözetmeni Atama Otomasyonu</h3><button onclick="location.href='/program';" style="margin-left: 40%; margin-top: 10%; width: 300px; height: 100px;" type="button" class="btn btn-primary">{}</button>
<br><button onclick="location.href='/excel';" style="margin-left: 5%; margin-top: 12%; "type="button" class="btn btn-warning">Excel Yükle</button>
<button onclick="location.href='/izinli';" style="margin-left: 1%; margin-top: 12%; "type="button" class="btn btn-success">İzinlileri Güncelle</button>
<button onclick="location.href='/izinliler';" style="margin-left: 1%; margin-top: 12%; "type="button" class="btn btn-info">İzinlileri Görüntüle</button>
<button onclick="location.href='/donem';" style="margin-left: 1%; margin-top: 12%; "type="button" class="btn btn-success">Dönemi Güncelle</button>
<button onclick="location.href='/genel';" style="margin-left: 1%; margin-top: 12%; "type="button" class="btn btn-info">Genel Programı Görüntüle</button>
<button onclick="location.href='/gorev-sayaci';" style="margin-left: 1%; margin-top: 12%; "type="button" class="btn btn-warning">Görev Sayacı</button>
<button onclick="location.href='/atama-yap';" style="margin-left: 1%; margin-top: 12%; "type="button" class="btn btn-danger">Atama Yap</button>""".format(donemTablosuOlustur.donem_veri_cek())


# Atama yapmak için fonksiyonlar çağırılıyor.
@app.route('/atama-yap')
def atama_yap():
    yield """Atama yapılıyor, lütfen bekleyin.
Bu işlem birkaç dakika sürebilir."""
    sinavTablosuOlustur.sinav_tablosu_sifirla() # tablolar sıfırlanıyor
    genelSinavTablosuOlustur.genel_tablosu_sifirla() # tablolar sıfırlanıyor
    gozetmenTablosuOlustur.veritabani_olustur() # tablolar oluşturuluyor
    sistemiCalistir.excel_gozetmenler() # atama yapılıyor
    yield """<meta http-equiv="refresh"
   content="0; url=/program">"""
    
# veriler veritabanından çekip ekrana yazdırılıyor
@app.route('/program')
def program_anasayfa():
    sinava_girecek_hoca_listesi = sinavTablosuOlustur.sinava_girecek_hocalar()
    b = 0
    gunler = excel.izinliler_icin_gunler_listesi()
    gun_sayisi = sistemiCalistir.tarih_listesi_olustur()
    i = 0
    saat_listesi = [9, 10, 11, 12, 13, 14, 15, 16, 17]
    yield """
        <!doctype html>
    <html lang="tr">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.2.1/css/bootstrap.min.css" integrity="sha384-GJzZqFGwb1QTTN6wy59ffF1BuGJpLSa9DkKMp0DgiMDm4iYMj70gZWKYbI706tWS" crossorigin="anonymous">

    <title>Sınav Programı</title>
  </head>
  <body>
  <div class="container-xl">
  <fieldset style="margin: 30px;" class="form-group">
    <div id="accordion">"""
    ilk_hoca = True
    for i in sinava_girecek_hoca_listesi:
        veri = sinavTablosuOlustur.sinav_tablosu_veri_cek(i)
        yield """<div class="card">
        <div class="card-header" id="heading{}">
          <h5 class="mb-0">
            <button class="btn btn-link" data-toggle="collapse" data-target="#collapse{}" aria-expanded="false" aria-controls="collapse{}">
              {hoca_adi}
            </button>
          </h5>
        </div>
        <div id="collapse{}" class="collapse" aria-labelledby="heading{}" data-parent="#accordion">
          <div class="card-body">
            <div class="container-xl">
            <fieldset style="margin: 30px;" class="form-group">
              <table class="table table-sm table-bordered">
            <thead class="thead-dark">
              <tr>
                <th scope="col">Saat</th>""".format(b, b, b, b, b, hoca_adi = i)
        for tarih_gun in gun_sayisi:
            yield """
                    <th scope="col">{}/{}/{}<br>{}</th>""".format(tarih_gun.strftime("%d"), tarih_gun.strftime("%b"), tarih_gun.strftime("%Y"), tarih_gun.strftime("%A"))
            
        yield """
              </tr>
            </thead>
            <tbody>"""
        yaz = False
        saatXgun = []
        for saat in saat_listesi:
            if WebTabloVeriCek.genel_veri_cek(saat, i):
                saatXgun.append(WebTabloVeriCek.genel_veri_cek(saat, i))
            yield '<tr>'
            yield '<td>{}:00</td>'.format(saat)
            mylist = {}
            zx = 0
            if len(saatXgun) != 0:
                for d in saatXgun:
                    for x in d:
                        for gunum in gunler:
                            if gunum in x[4] and saat == int(x[1]):
                                deger = x[0] + '<br>' + x[3]
                                mylist[zx] = deger
                            zx += 1
                        zx = 0
                try:
                    if mylist[0]:
                        yield '<td>'
                        yield mylist[0]
                        yield '</td>'
                except:
                    yield '<td>-</td>'
                try:
                    if mylist[1]:
                        yield '<td>'
                        yield mylist[1]
                        yield '</td>'
                except:
                    yield '<td>-</td>'
                try:
                    if mylist[2]:
                        yield '<td>'
                        yield mylist[2]
                        yield '</td>'
                except:
                    yield '<td>-</td>'
                try:
                    if mylist[3]:
                        yield '<td>'
                        yield mylist[3]
                        yield '</td>'
                except:
                    yield '<td>-</td>'
                try:
                    if mylist[4]:
                        yield '<td>'
                        yield mylist[4]
                        yield '</td>'
                except:
                    yield '<td>-</td>'
                try:
                    if mylist[5]:
                        yield '<td>'
                        yield mylist[5]
                        yield '</td>'
                except:
                    yield '<td>-</td>'
                try:
                    if mylist[6]:
                        yield '<td>'
                        yield mylist[6]
                        yield '</td>'
                except:
                    yield '<td>-</td>'
                try:
                    if mylist[7]:
                        yield '<td>'
                        yield mylist[7]
                        yield '</td>'
                except:
                    yield '<td>-</td>'
                try:
                    if mylist[8]:
                        yield '<td>'
                        yield mylist[8]
                        yield '</td>'
                except:
                    yield '<td>-</td>'
                try:
                    if mylist[9]:
                        yield '<td>'
                        yield mylist[9]
                        yield '</td>'
                except:
                    yield '<td>-</td>'
            else:
                yield '<td>-</td><td>-</td><td>-</td><td>-</td><td>-</td><td>-</td><td>-</td><td>-</td><td>-</td><td>-</td>'
            yield '</tr>'
        yield """
            </tbody>
          </table>
            </fieldset>
          </div> 
          </div>
        </div>
      </div>"""
        b += 1
    yield """</div>
  </fieldset>
</div>
    <!-- Optional JavaScript -->
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.6/umd/popper.min.js" integrity="sha384-wHAiFfRlMFy6i5SRaxvfOCifBUQy1xHdJ/yoi7FRNXMRBu5WHdZYu1hA6ZOblgut" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.2.1/js/bootstrap.min.js" integrity="sha384-B0UglyR+jN6CkvvICOB2joaf5I4l3gm9GU6Hc1og6Ls7i6U/mkkaduKaBhlAXv9k" crossorigin="anonymous"></script>
  </body>
</html>
    """


# veriler veritabanından çekip ekrana yazdırılıyor
@app.route('/genel')
def program_genel():
    gun_sayisi = genelSinavTablosuOlustur.gun_sayisi() 
    b = 0
    yield """
        <!doctype html>
    <html lang="tr">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.2.1/css/bootstrap.min.css" integrity="sha384-GJzZqFGwb1QTTN6wy59ffF1BuGJpLSa9DkKMp0DgiMDm4iYMj70gZWKYbI706tWS" crossorigin="anonymous">

    <title>Sınav Programı</title>
  </head>
  <body>
  <div class="container">
  <fieldset style="margin: 30px;" class="form-group">
    <div id="accordion">"""
    for i in gun_sayisi:
        veri = genelSinavTablosuOlustur.genel_tablosu_veri_cek(i)
        yield """<div class="card">
        <div class="card-header" id="heading{}">
          <h5 class="mb-0">
            <button class="btn btn-link" data-toggle="collapse" data-target="#collapse{}" aria-expanded="false" aria-controls="collapse{}">
              {gun_adi}
            </button>
          </h5>
        </div>
        <div id="collapse{}" class="collapse" aria-labelledby="heading{}" data-parent="#accordion">
          <div class="card-body">
            <div class="container">
            <fieldset style="margin: 30px;" class="form-group">
              <table class="table">
            <thead class="thead-dark">
              <tr>
                <th scope="col">Tarih</th>
                <th scope="col">Sınav Salonu</th>
                <th scope="col">Ders</th>
                <th scope="col">Dersin Hocası</th>
                <th scope="col">Gözetmenler</th>
              </tr>
            </thead>
            <tbody>""".format(b, b, b, b, b, gun_adi = i)
        for x in veri:
            yield """<tr>
                    <td>{}</td>
                    <td>{}</td>
                    <td>{}</td>
                    <td>{}</td>
                    <td>{}</td>
              </tr>""".format(x[1] + ":00", x[3], x[0],x[2], x[5])
        yield """
            </tbody>
          </table>
            </fieldset>
          </div> 
          </div>
        </div>
      </div>"""
        b += 1
    yield """</div>
  </fieldset>
</div>
    <!-- Optional JavaScript -->
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.6/umd/popper.min.js" integrity="sha384-wHAiFfRlMFy6i5SRaxvfOCifBUQy1xHdJ/yoi7FRNXMRBu5WHdZYu1hA6ZOblgut" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.2.1/js/bootstrap.min.js" integrity="sha384-B0UglyR+jN6CkvvICOB2joaf5I4l3gm9GU6Hc1og6Ls7i6U/mkkaduKaBhlAXv9k" crossorigin="anonymous"></script>
  </body>
</html>
    """


# excel yükleme sayfası
@app.route('/excel')
def excel_anasayfa():
    return static_file('pages/excel.html', root='.')

# excel yükleniyor
@app.route('/excel-yukle', method='POST')
def excel_yukle():
    upload = request.files.get("excel")
    if upload is not None:
        name, ext = os.path.splitext(upload.filename)
        if ext not in ('.xlsx'):
            return "Lütfen Excel dosyası yükleyin."

        save_path = "Excel"
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        file_path = "Excel/AnkaraUni.xlsx"
        with open(file_path, 'wb') as open_file:
            open_file.write(upload.file.read())
        redirect('/izinli')
    else:
        return 'Bir hata oluştu.'


# izinli seçme sayfası
@app.get('/izinli')
def izinli():
    yield """<!doctype html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.2.1/css/bootstrap.min.css" integrity="sha384-GJzZqFGwb1QTTN6wy59ffF1BuGJpLSa9DkKMp0DgiMDm4iYMj70gZWKYbI706tWS" crossorigin="anonymous">

    <title>İzinli Gözetmenler</title>
  </head>
  <body>
  <div class="container">
    <form name="izin" action="/izinliler-belirlendi" method="post">
    <h1 style="text-align: center; margin: 15px;">Gözetmen Atama Otomasyonu</h1>
  <fieldset style="margin: 30px;" class="form-group">
    <legend>İzinli gözetmenleri seçiniz</legend>"""
    gunler = excel.izinliler_icin_gunler_listesi() # günler çekiliyor
    ogretmenler = gozetmenTablosuOlustur.excel_gozetmenler() # gözetmenler çekiliyor
    gun_sayisi = len(gunler)
    a = 0
    for gun in gunler:
        yield """<div class="btn-group dropright">
        <button type="button" class="btn btn-secondary dropdown-toggle" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
          İzinli gözetmenleri seçiniz {}
        </button>
        <div class="dropdown-menu">
          <div class="form-check">
        <label class="form-check-label">
        <input style="display: none;" id="gizli{}" name="gizli{}" style="visibility: hidden;">""".format(gun, a, a)
        first = True
        for ogretmen in ogretmenler:
            yield """<input type="checkbox" class="form-check-input" name="gun{}" value="{}" style="width: 20px; height: 20px">
                    <h6>&nbsp {}</h6>
                  </label>""".format(a, ogretmen, ogretmen)
            if first:
              yield "<br>"
              first = False
        yield """ </div>
          </div>
        </div><br><br>"""
        a += 1
    
    yield """
    <button type="submit" id="gonder">Gönder</button></form>
    
    <script>
          function veriAl(form, sayi) {
      var selchbox = [];
      var inpfields = document.getElementsByTagName('input');
      var nr_inpfields = inpfields.length;

      for(var i=0; i<nr_inpfields; i++) {
        if(inpfields[i].name == 'gun' + sayi && inpfields[i].type == 'checkbox' && inpfields[i].checked == true) selchbox.push(inpfields[i].value);
      }

      return selchbox;
    }"""

    yield """document.getElementById('gonder').onclick = function(){"""
    b = 0
    for gun in gunler:
        yield """ var veri_degisken{} = veriAl(this.form, {});

          var degisken{} = document.getElementById("gizli{}");

          degisken{}.value = veri_degisken{};
          """.format(b, b, b, b, b, b)
        b = b + 1

    yield """document.izin.submit();
} 
          </script>
        
    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.6/umd/popper.min.js" integrity="sha384-wHAiFfRlMFy6i5SRaxvfOCifBUQy1xHdJ/yoi7FRNXMRBu5WHdZYu1hA6ZOblgut" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.2.1/js/bootstrap.min.js" integrity="sha384-B0UglyR+jN6CkvvICOB2joaf5I4l3gm9GU6Hc1og6Ls7i6U/mkkaduKaBhlAXv9k" crossorigin="anonymous"></script>
  """

# izinliler belirleniyor
@app.post('/izinliler-belirlendi')
def izinliler_belirlendi():
    gunler = excel.izinliler_icin_gunler_listesi()
    izinliTablosuOlustur.izinli_tablosu_sifirla()
    if request.forms.gizli0 != "":
        izinliTablosuOlustur.izinli_tablosu_veri_ekle(request.forms.gizli0, gunler[0])
    if request.forms.gizli1 != "":
        izinliTablosuOlustur.izinli_tablosu_veri_ekle(request.forms.gizli1, gunler[1])
    if request.forms.gizli2 != "":
        izinliTablosuOlustur.izinli_tablosu_veri_ekle(request.forms.gizli2, gunler[2])
    if request.forms.gizli3 != "":
        izinliTablosuOlustur.izinli_tablosu_veri_ekle(request.forms.gizli3, gunler[3])
    if request.forms.gizli4 != "":
        izinliTablosuOlustur.izinli_tablosu_veri_ekle(request.forms.gizli4, gunler[4])
    if request.forms.gizli5 != "":
        izinliTablosuOlustur.izinli_tablosu_veri_ekle(request.forms.gizli5, gunler[5])
    if request.forms.gizli6 != "":
        izinliTablosuOlustur.izinli_tablosu_veri_ekle(request.forms.gizli6, gunler[6])
    if request.forms.gizli7 != "":
        izinliTablosuOlustur.izinli_tablosu_veri_ekle(request.forms.gizli7, gunler[7])
    if request.forms.gizli8 != "":
        izinliTablosuOlustur.izinli_tablosu_veri_ekle(request.forms.gizli8, gunler[8])
    if request.forms.gizli9 != "":
        izinliTablosuOlustur.izinli_tablosu_veri_ekle(request.forms.gizli9, gunler[9])
    if request.forms.gizli10 != "":
        izinliTablosuOlustur.izinli_tablosu_veri_ekle(request.forms.gizli10, gunler[10])
    if request.forms.gizli11 != "":
        izinliTablosuOlustur.izinli_tablosu_veri_ekle(request.forms.gizli11, gunler[11])
    if request.forms.gizli12 != "":
        izinliTablosuOlustur.izinli_tablosu_veri_ekle(request.forms.gizli12, gunler[12])
    if request.forms.gizli13 != "":
        izinliTablosuOlustur.izinli_tablosu_veri_ekle(request.forms.gizli13, gunler[13])
    if request.forms.gizli14 != "":
        izinliTablosuOlustur.izinli_tablosu_veri_ekle(request.forms.gizli14, gunler[14])
    if request.forms.gizli15 != "":
        izinliTablosuOlustur.izinli_tablosu_veri_ekle(request.forms.gizli15, gunler[15])
    redirect('/izinliler')

# izinli görüntüleme sayfası
@app.route('/izinliler')
def izinlileri_goruntule():
    yield """<!doctype html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.2.1/css/bootstrap.min.css" integrity="sha384-GJzZqFGwb1QTTN6wy59ffF1BuGJpLSa9DkKMp0DgiMDm4iYMj70gZWKYbI706tWS" crossorigin="anonymous">

    <title>İzinli Listesi</title>
  </head>
  <body>
  <div class="container">
    
    <h1 style="text-align: center; margin: 15px;">İzinli Listesi</h1>
  <fieldset style="margin: 30px;" class="form-group">
"""
    izinliler = izinliTablosuOlustur.tum_izinlileri_goruntule()
    for izinli in izinliler:
        izinliler_listesi = []
        for izinli_hoca in izinli[0].split(","):
            izinliler_listesi.append(izinli_hoca)
        yield """<div class="form-group">
<legend>{}</legend>
<ul class="list-group">""".format(izinli[1])
        for izinli_gozetmen in izinliler_listesi:
            yield """<li class="list-group-item">{}</li>""".format(izinli_gozetmen)
        yield """</ul></div>"""
    yield """<button onclick="location.href='/izinli';" style="margin-left: 1%;" "type="button" class="btn btn-info">İzinlileri Güncelle</button>
    <button onclick="location.href='/atama-yap';" style="margin-left: 1%;" "type="button" class="btn btn-success">Atama Başlat</button>"""


@app.post('/donem-guncelle')
def donem_guncelle():
    donemTablosuOlustur.donem_ekle(request.forms.donem)
    redirect('/')


@app.route('/gorev-sayaci')
def gorev_sayaci():
    durumlar = gozetmenTablosuOlustur.tum_durumlari_goruntule()
    yield """<!doctype html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.2.1/css/bootstrap.min.css" integrity="sha384-GJzZqFGwb1QTTN6wy59ffF1BuGJpLSa9DkKMp0DgiMDm4iYMj70gZWKYbI706tWS" crossorigin="anonymous">

    <title>Gözetmen Görev Sayacı</title>
  </head>
  <body>
  <div class="container">
    
    <h1 style="text-align: center; margin: 15px;">Hangi Gözetmen Kaç Kez Görev Aldı?</h1>
  <fieldset style="margin: 30px;" class="form-group">
    <table class="table">
  <thead class="thead-dark">
    <tr>
      <th scope="col">Gözetmen</th>
      <th scope="col">Görev Sayısı</th>
    </tr>
  </thead>
  <tbody>
"""
    for durum in durumlar:
        yield """<tr>
      <td>{}</td>
      <td>{}</td>
    </tr>""".format(durum[0], durum[1])

    yield """</tbody>
</table>


  </fieldset>
      
</div>
</body></html>"""




@app.route('/<filename>')
def server_static(filename):  
    return static_file('{}.html'.format(filename), root='pages')


@app.route('/<filename:re:.*\.css>')
def css(filename):
    return static_file(filename, root='pages')


@app.get('/<filename:re:.*\.js>')
def javascript(filename):
    return static_file(filename, root='pages')


@app.get('/<filename:re:.*\.png>')
def png(filename):
    return static_file(filename, root='pages')


@app.get('/<filename:re:.*\.woff>')
def woff(filename):
    return static_file(filename, root='pages')


@app.get('/<filename:re:.*\.woff2>')
def woff2(filename):
    return static_file(filename, root='pages')


@app.get('/<filename:re:.*\.tff>')
def tff(filename):
    return static_file(filename, root='pages')


@app.get('/proje/<filename:re:.*\.zip>')
def zip(filename):
    return static_file(filename, root='proje')


@app.get('/proje/<filename:re:.*\.pdf>')
def pdf(filename):
    return static_file(filename, root='proje')

run(app, host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))