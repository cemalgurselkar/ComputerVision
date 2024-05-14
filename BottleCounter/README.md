Burada kırmızı şişeleri ayırt etmek için hsv(Hue Saturation,Value) tekniği kullandık.
buradaki amaç şudur:
1. Kırmızı renk için alt ve üst sınır belirlenecek.
2. Ardından cv2.inRange fonksiyonunu kullanarak kırmızı şişeler için maskeleme uygulanacak. Alt ve üst sınır sayesinde
kırmızı renkler hariç bütün renkler siyaha dönüşecek. Bu sayede şişeleri kolayca tespit edebilceğiz.Buna binary mask denir.
3. Ardından, maskelenen görüntüdeki konturları (nesne kenarlarını) bulur ve bunları cnts adlı listede depolar.
(cv2.findContours fonksiyonu iki tane çıktı verir. contours ve hierarch adlı iki tane çıktı. Bu kodda sadece konturlara ihtiyac olduğu için sonuna [-2] ekledik.)
4. Ardından cnts listesi üzerinde gezinerek,şişelerin etrafındaki konturları bulunur. cv2.boundingRect ile şişeleri kaplayacak en küçük dikdörtgenin koordinatlarını hesaplar.
5. Son olarak, burada hsv yöntemi ile nesne tespiti konusunu öğrnemiş oldum. Nesne tespiti için iyi bir alıştırma oldu.
