import cv2
import numpy as np

def nothing(x):
    pass

img = cv2.imread("meyveler.jpeg")

if img is None:
    print("Görsel bulunamadı!")
    exit()

# Trackbar pencereleri ve isimlerini oluşturma
cv2.namedWindow('Ayarlar')
cv2.createTrackbar('Alt Esik', 'Ayarlar', 100, 255, nothing)
cv2.createTrackbar('Ust Esik', 'Ayarlar', 200, 255, nothing)
cv2.createTrackbar('Min Alan', 'Ayarlar', 500, 5000, nothing)

while True:
    # Görüntüyü kopyalama
    output = img.copy()

    # Görseli gri tonlamalı renk uzayına ekleme ve blurlama (Gürültüssüz daha düzgün kenarlar için)
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    blur_meyve = cv2.GaussianBlur(gray, ksize=(5, 5), sigmaX=0)

    # TrackBar değerlerini okuma
    low = cv2.getTrackbarPos('Alt Esik', 'Ayarlar')
    high = cv2.getTrackbarPos('Ust Esik', 'Ayarlar')
    min_alan = cv2.getTrackbarPos('Min Alan', 'Ayarlar')

    # Canny ile kenar belirleme
    edges = cv2.Canny(blur_meyve, low, high)

    # Kenarları kalınlaştırma
    kernel = np.ones((3, 3), np.uint8)
    dilated = cv2.dilate(edges, kernel, iterations=1)

    # Kontur bulma
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    count = 0
    for cnt in contours:
        area = cv2.contourArea(cnt)

        # Sadece belirli bir büyüklükteki nesneleri say
        if area > min_alan:
            count += 1

            # Nesne merkezini bulma
            M = cv2.moments(cnt)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])

                # Konturu çiz ve üzerine numara yaz
                cv2.drawContours(output, [cnt], -1, (0, 255, 0), 2)
                cv2.putText(output, str(count), (cX - 10, cY),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

    cv2.putText(output, f"Toplam Nesne: {count}", (20, 40),
                cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 0), 2)

    cv2.imshow('Kenar Goruntusu', edges)
    cv2.imshow('Sayim Sonucu', output)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Sonuc görselini kaydete
cv2.imwrite("output/sayim_sonucu.jpg", output)

# Analiz verilerini bir metin dosyasına yazdırma
with open("output/analiz_raporu.txt", "w", encoding="utf-8") as f:
    f.write("--- MEYVE SAYIM RAPORU ---\n")
    f.write(f"Toplam Nesne Sayısı: {count}\n")
    f.write(f"Kullanılan Alt Eşik: {low}\n")
    f.write(f"Kullanılan Üst Eşik: {high}\n")
    f.write(f"Kullanılan Min Alan Filtresi: {min_alan}\n")
    f.write("--------------------------\n")

print("Analiz raporu 'analiz_raporu.txt' dosyasına yazıldı.")

cv2.destroyAllWindows()