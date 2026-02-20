import cv2
import numpy as np
import os

def nothing(x):
    pass

# Ayarlar penceresini ve trackbarları oluşturur.
def trackbars():
    cv2.namedWindow('Ayarlar')
    cv2.createTrackbar('Alt Esik', 'Ayarlar', 100, 255, nothing)
    cv2.createTrackbar('Ust Esik', 'Ayarlar', 200, 255, nothing)
    cv2.createTrackbar('Min Alan', 'Ayarlar', 500, 5000, nothing)

# Görüntüyü gri tonlamaya çevirir ve blurlar.
def preprocess_image(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    return blur

# Canny kenar tespiti ve kalınlaştırma uygular.
def get_edges(img, low, high):
    edges = cv2.Canny(img, low, high)
    kernel = np.ones((3, 3), np.uint8)
    dilated = cv2.dilate(edges, kernel, iterations=1)
    return edges, dilated

# Konturları sadece soldan sağa (x koordinatına) göre sıralar.
def kontur_sirala(contours):
    if not contours:
        return []

    contour_list = []
    for cnt in contours:
        M = cv2.moments(cnt)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            contour_list.append((cnt, cX))

    return [item[0] for item in contour_list]

# Sonuç görselini ve raporu kaydeder.
def sonuc(output_img, count, params):
    if not os.path.exists("output"):
        os.makedirs("output")

    cv2.imwrite("output/sayim_sonucu.jpg", output_img)

    with open("output/analiz_raporu.txt", "w", encoding="utf-8") as f:
        low, high, min_alan = params
        f.write("--- MEYVE SAYIM RAPORU ---\n")
        f.write(f"Toplam Nesne Sayısı: {count}\n")
        f.write(f"Kullanılan Alt Eşik: {low}\n")
        f.write(f"Kullanılan Üst Eşik: {high}\n")
        f.write(f"Kullanılan Min Alan Filtresi: {min_alan}\n")
        f.write("--------------------------\n")

    print("\nSonuçlar 'output' klasörüne kaydedildi.")


def main():

    img = cv2.imread("meyveler.jpeg")
    if img is None:
        print("Görsel bulunamadı!")
        return

    trackbars()
    processed_base = preprocess_image(img)

    while True:
        output = img.copy()

        # Parametreleri Oku
        low = cv2.getTrackbarPos('Alt Esik', 'Ayarlar')
        high = cv2.getTrackbarPos('Ust Esik', 'Ayarlar')
        min_alan = cv2.getTrackbarPos('Min Alan', 'Ayarlar')

        # İşleme
        edges, dilated = get_edges(processed_base, low, high)
        contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Sıralama ve Analiz
        sorted_contours = kontur_sirala(contours)

        count = 0
        for cnt in sorted_contours:
            if cv2.contourArea(cnt) > min_alan:
                count += 1
                M = cv2.moments(cnt)
                if M["m00"] != 0:
                    cX, cY = int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])

                    cv2.drawContours(output, [cnt], -1, (0, 255, 0), 2)
                    cv2.putText(output, str(count), (cX - 10, cY),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

        # 5. Görselleştirme
        cv2.putText(output, f"Toplam: {count}", (20, 40), 1, 2, (255, 0, 0), 2)
        cv2.imshow('Kenar Goruntusu', edges)
        cv2.imshow('Sayim Sonucu', output)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            # Kayıt işlemi için son parametreleri gönder
            sonuc(output, count, (low, high, min_alan))
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
