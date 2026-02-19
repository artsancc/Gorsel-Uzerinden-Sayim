# Görsel Üzerinden Sayım

Bu proje, görüntü işleme tekniklerini kullanarak fotoğraf üzerindeki nesneleri (meyveleri) tespit eden ve sayan Python tabanlı bir uygulamadır.
Canny Kenar Algılama ve Alan Filtreleme gibi kritik parametreleri kullanıcı TrackBar üzerinden canlı olarak optimize edilebilir.

# Projenin Amacı
Projenin temel amacı, görüntü işleme süreçlerinde manuel olarak girilen eşik değerleri (thresholds) ve filtreleme parametrelerini dinamik hale getirmektir.

# Kullanılan Kütüphaneler
OpenCV
NumPy
OS

Kütüphanelerin İndirilmesi

pip install opencv-python numpy

# Teknik İşleyiş ve Kod Mantığı

Ön İşleme: cv2.cvtColor ile görsel gri tonlamaya çekilir. cv2.GaussianBlur ile pikseller arasındaki sert gürültüler yumuşatılır.

Dinamik Kenar Tespiti: TrackBar'dan alınan low ve high değerleri cv2.Canny fonksiyonuna aktarılır. Bu, nesne sınırlarının netliğini anlık olarak kontrol etmemizi sağlar.

Morfolojik Genişletme: cv2.dilate kullanılarak Canny sonucunda oluşan küçük kenar boşlukları kapatılır. Bu, kontur algoritmasının nesneyi bütün bir kapalı alan olarak görmesini sağlar.

Kontur ve Alan Analizi: cv2.findContours ile tüm kapalı alanlar haritalanır. cv2.contourArea sayesinde, kullanıcının belirlediği min_alan değerinden küçük olan parazitler elenir.

Momentler ve Merkezleme: cv2.moments istatistiği ile her meyvenin kütle merkezi hesaplanır ve numara etiketi tam bu koordinata basılır.

#Input

![meyveler](https://github.com/user-attachments/assets/38f2ae87-abbb-4d4b-9bf6-ff4c0dc73ace)

#Output

![sayim_sonucu](https://github.com/user-attachments/assets/7e63bbc1-e339-4c58-baed-ac8a5c976899)

# Sonuç

Program başarıyla sonlandırıldığında:

Görsel Çıktı: Yapılan tüm çizimlerin ve sayımların işlendiği final görüntüsü sayim_sonucu.jpg adıyla kaydedilir.

Veri Raporu: Toplam nesne sayısı ve kullanılan hassas ayarlar (eşik değerleri) analiz_raporu.txt dosyasına teknik bir rapor olarak yazdırılır.

Bu sayede sadece bir görüntü elde etmekle kalınmaz, aynı zamanda işlemin tekrarlanabilirliği için gerekli teknik veriler de arşivlenmiş olur.
