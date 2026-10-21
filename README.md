# ECHO/12 — Kendi Geçmişinle Kaç

Beş odalık, Türkçe, tarayıcıda oynanabilen bir **zaman döngüsü bulmaca / bilim kurgu** prototipi. Her 12 saniyelik hareket kaydın, önceki davranışlarını yeniden oynatan bağımsız bir yankıya dönüşür. Kendi kayıtlarınla iş birliği yaparak tesisin kapılarını aç ve kayıpların neden silindiğini öğren.

## Build 003 — Arşiv Protokolü

Oynanabilir odalar:

1. **İlk İz:** Baskı plakasında yankını bırakarak çıkışı aç.
2. **İki Ses:** İki yankıyı eşzamanlı kullan.
3. **Kör Nokta:** Yankıları yönetirken güvenlik küresinden kaç.
4. **Kısa Devre:** Sadece kısa süre açık kalan röle kapılarını zamanla.
5. **Sahte Yankı (yeni):** Mavi `C` plakasını canlı oyuncu **etkinleştiremez**. Kaydedilmiş bir yankı onu açmalı; ikinci yankıyla diğer kapıyı açıp çıkışa ulaş.

Bu sürümde ayrıca:

- **Keşfedilebilir üç terminal:** 1., 3. ve 5. odalarda bulunan tesis kayıtları hikâyeyi açar. `E` ile yaklaşarak oku veya **Terminali oku** düğmesini kullan.
- **Arşiv defteri:** `L` / **Arşiv** ile bulunan kayıtları tekrar oku. Henüz bulunmayan kayıtlar şifreli görünür. Arşiv açıkken oyun zamanı durur. Kayıtlar mümkün olduğunda tarayıcının yerel depolamasına yazılır.
- **Yankı zaman çizelgesi:** Hareketlerin, plakalara temasların ve saniye göstergesinin görsel karşılığı.
- **Son yankıyı geri alma:** `Z` ile son kaydı silerek yeniden dene.
- **Mobil arşiv arayüzü:** Dar ekranlarda kaydırılabilir, tam ekran kayıt okuyucusu.

## Oynamak

Kök dizindeki **`index.html`** dosyasını güncel bir tarayıcıda aç. Derleme, harici asset, hesap veya sunucu gerekmez. İstenirse GitHub Pages, Vercel vb. statik barındırmada aynı dosyayla yayımlanabilir; repoya kod yüklemek tek başına siteyi canlıya almaz.

| Tuş | Eylem |
| --- | --- |
| `WASD` veya oklar | Hareket et |
| `Space` | Döngüyü kaydet, yeni yankı oluştur |
| `Z` | Son yankıyı sil |
| `R` | Geçerli odayı sıfırla |
| `P` | Duraklat / devam et |
| `E` | Yakındaki terminali aç |
| `L` | Arşiv defterini aç veya kapat |
| `Escape` | Arşiv defterini kapat |
| `Enter` | Açılış ve oda geçişlerini onayla |

Ekrandaki düğmeler dokunmatik girişe de uygundur. Ses isteğe bağlıdır. Tamamlanan odalar ve bulunan terminal kayıtları yerel depolama izin veriyorsa hatırlanır.

## Test

Python Playwright ile beş odanın bitirilebildiği, yankı geri alma, canlı oyuncunun mavi plakayı tetikleyememesi, kayıtlı yankının tetiklemesi, terminalin keşfi ve arşivde zamanın durması sınanır.

```sh
python -m pip install playwright
python -m playwright install chromium
python tests/smoke.py
```

Testler hızlı ve deterministiktir: oyun kodu yalnızca test sayfasında enjekte edilen kontrollü zaman ilerletme arabirimiyle sınanır; ürün sürümünde test kancası yoktur. GitHub Actions iş akışı aynı testleri her push'ta çalıştırır.

## Teknoloji

Dış bağımlılığı olmayan HTML / CSS / JavaScript ve Canvas 2D. Aşamalı prototip geliştirme yaklaşımı: oynanabilirlik, okunabilirlik ve testlerden sonra yeni içerik.

**Sonraki geliştirme yönü:** Seçim sonuçları olan daha ileri arşiv kayıtları, yeni kapı mantığı, gerçek bir bölüm sonu ve seviyeler arasında güçlü dramatik geçiş.