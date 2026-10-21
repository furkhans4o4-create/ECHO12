# ECHO/12 — Kendi Geçmişinle Kaç

Tarayıcıda oynanan, tek kişilik Türkçe bilim kurgu / **12 saniyelik zaman döngüsü bulmacası**. Geçmiş hareketlerin sonraki döngülerde yankılar tarafından tekrarlanır. Onların yardımıyla kilitli bölümleri aşar, eski kayıtları keşfeder ve çekirdeğin kaderini belirlersin.

## Build 004 — Çekirdek Çatışması

**Altı oynanabilir oda:**

1. **İlk İz** — Bir yankıyı baskı plakasında bırak.
2. **İki Ses** — İki eşzamanlı kayıtla kapıları aç.
3. **Kör Nokta** — Güvenlik küresinden kaç.
4. **Kısa Devre** — Süreli röleleri yönet.
5. **Sahte Yankı** — Yalnızca geçmiş yankının etkinleştirebildiği kapıyı geç.
6. **Karar Odası (yeni)** — Önce yankılarla iki kilidi aş, ardından iki farklı çekirdek konsolu arasında fiziksel olarak seçim yap. Odayı terk edeceğin güzergâh bu tercihe göre çekirdeğe veya dış dünyaya yönlenir.

**Yeni hikâye sistemi:** Altıncı odada M. Kora'nın yeni terminal kaydını bulabilirsin. Son bölümde iki bilinçli tercih sunulur: yankıların belleğini koruyup tesiste kalmak veya çekirdeği kapatıp dışarı çıkmak. Her tercih önceden açıkça anlatılır ve onay istenir. Vazgeçilebilir; yalnızca onaylanan karar çıkış kapısını açar.

**Kalıcı sonuçlar:** İki farklı bölüm sonu ve bunlara özel ayrı arşiv kayıtları vardır. Tamamlanan finaller tarayıcı izin verirse `localStorage` ile korunur; son bölüm tekrar oynanıp diğer final de keşfedilebilir. Seviye ilerlemesi artık önceki odalara dönerken geriye sarılmaz. Toplam **6 keşfedilebilir arşiv kaydı** vardır (iki kayıt farklı finallere bağlıdır).

## Oyna

`index.html` dosyasını tarayıcıda aç. Tek dosyadır, dış kütüphane, sunucu, hesap veya kurulum gerektirmez. GitHub Pages gibi bir statik barındırma sağlayıcısıyla yayımlanabilir; kaynak dosyanın GitHub'a yüklenmesi tek başına canlı site oluşturmaz.

| Kontrol | İşlev |
| --- | --- |
| `WASD` veya oklar | Hareket |
| `Space` | Döngüyü bitirip yankıyı kaydet |
| `Z` | Son yankıyı sil |
| `R` | Odayı sıfırla |
| `P` | Duraklat |
| `E` | Yakındaki arşiv terminalini veya karar konsolunu kullan |
| `L` | Bulunan kayıtları oku |
| `Esc` | Arşivi veya henüz onaylanmamış kararı kapat |
| `Enter` | Açılış, onay ve oda geçişi |

Dokunmatik yön tuşları ve ekrandaki butonlar da kullanılabilir. Zaman çizelgesi geçmiş hareketleri, plaka temaslarını ve anlık döngü ilerlemesini gösterir.

## Otomatik test

```sh
python -m pip install playwright
python -m playwright install chromium
python tests/smoke.py
```

Testler tüm **altı odayı** oynanış kurallarıyla çözerek denetler. Çift yankılı kilitler, arşiv sırasında zamanın durması, kararın iptali, her iki final, final tekrar oynama ve sonuçların depolamadan yeniden okunması ayrıca test edilir. Hız için yalnızca test sayfasına kontrollü zaman ilerletici eklenir. Test ortamındaki `about:blank` sayfasının güvenli depolama kökeni olmadığından, saklama kontrollerinde bir `localStorage` taklidi kullanılır; gerçek tarayıcı alanında tekrar yükleme davranışı ayrıca elle kontrol edilebilir. **GitHub Actions** her ana dal güncellemesinde aynı testleri çalıştırır.

## Teknik

Tamamen bağımsız HTML / CSS / JavaScript ve Canvas 2D. Oyun kaynak kodu `index.html` içindedir; `tests/smoke.py` testleri ve `.github/workflows/smoke.yml` otomatik doğrulamayı sağlar.

**Yön:** Build 005'te ilk bölüm boyunca mekâna duyarlı anlatı, daha derin yankı kullanımı ve güçlü ses/görsel geri bildirimler.