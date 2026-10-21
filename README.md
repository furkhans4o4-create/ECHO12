# ECHO/12

**Kendi geçmişinle kaç.** Türkçe arayüzlü, tarayıcıda oynanabilen tek oyunculu zaman-döngüsü bulmaca oyunu. Her 12 saniyelik hareket kaydı bir yankıya dönüşür; yankılar daha önce geçtiğin yolu tekrarlar. Kapıları açmak için geçmişinle işbirliği yap.

## Build 002 — Dört oynanabilir oda

- **İlk İz:** Bir yankıyla baskı plakasını tut ve çıkışı aç.
- **İki Ses:** İki yankıyı aynı anda kullanarak iki bariyeri aş.
- **Kör Nokta:** Hareketli bir güvenlik küresinden kaç.
- **Kısa Devre (yeni):** Altın renkli süreli röle plakaları, üzerlerinden ayrıldıktan sonra kapıyı kısa süre daha açık tutar.
- **Yeni:** 12 saniyelik yankı zaman çizelgesi. Hareketli kısımlar renkli; plakalara temaslar altın renkte.
- **Yeni:** Son yankıyı silme; doğru çözümü denemeyi kolaylaştırır.
- **Düzeltme:** Tarayıcı yerel depolamayı kısıtlasa bile oyun başlayabilir.
- **Düzeltme:** Altı yankı sınırında otomatik döngü zamanının kilitlenmesi giderildi.

## Oynama

`index.html` dosyasını modern bir tarayıcıda aç. Kurulum, bağımlılık ve hesap gerekmez. GitHub Pages kullanılıyorsa depodaki kök `index.html` doğrudan yayımlanabilir.

| Tuş | Eylem |
| --- | --- |
| WASD / ok tuşları | Hareket |
| Space | 12 saniyeyi beklemeden hareket kaydını bitir ve yankı oluştur |
| Z | Son yankıyı sil ve geçerli döngüyü sıfırla |
| R | Odayı tamamen sıfırla |
| P | Duraklat / devam et |

Mobilde yön tuşları, masaüstünde butonlar da vardır. Yerel kayıt mümkün olduğunda tamamlanan odalar saklanır.

## Test

Python ve [Playwright](https://playwright.dev/python/) ile dört odayı ve yankı silme özelliğini test edebilirsin:

```bash
pip install playwright
playwright install chromium
python tests/smoke.py
```

## Teknoloji ve geliştirme

Tek dosyalık HTML / CSS / JavaScript, Canvas 2D. Dış varlık, sunucu ya da oyun motoru gerektirmeyen prototip. Dört oyun odasının tamamı tarayıcı testleriyle doğrulanmıştır. Her sonraki **devam** isteğinde yeni bir oynanabilir dilim geliştirilecek.

Sonraki odak: oyun içi anlatı, farklı etkileşimli nesneler ve daha güçlü seviye tasarımı.