# ECHO/12 — Kendi Geçmişinle Kaç

Tarayıcıda oynanan, tek kişilik Türkçe bilim kurgu / **12 saniyelik zaman döngüsü bulmacası**. Geçmiş hareketlerin sonraki döngülerde yankılar tarafından tekrarlanır. Onların yardımıyla kilitli bölümleri aşar, eski kayıtları keşfeder ve çekirdeğin kaderini belirlersin.

## Build 005 — Sinyal ve Yankı

Bu sürümün oda ve final sayısı değişmedi; altı odanın tamamında **oynanış geri bildirimleri** yenilendi:

- **Reaktif kapılar:** Baskı plakaları kapıyı açtığında kısa bir ses, parçacık yayılımı ve genişleyen enerji halkası görülür. Kapı kapanırken ayrı bir uyarı sesi duyulur.
- **Zaman baskısı:** Döngünün son üç saniyesinde kırmızı kenar aydınlatması, kısa uyarı tonları ve HUD üzerinde geri sayım görünür.
- **Yankı kaydı:** Yeni döngü oluştuğunda mor enerji halkası, ekran titreşimi yerine kısa renk parlaması ve iki katmanlı sentezlenmiş efekt kullanılır.
- **Çevresel ses:** Web Audio API ile bağımsız müzik dosyası olmadan hafif, yankı sayısı ve döngü süresiyle değişen atmosferik bir drone üretilir. Modal ekranlar açıldığında ses düzeyi düşer.
- **Karar ve bölüm geçişleri:** Seçim ve zafer için farklı ses dizileri, kısa sektör başlıkları ve karar anında renk geri bildirimi.
- **Sinyal göstergesi:** Canlı kayıt, açık geçiş, kritik sayaç, arşiv ve karar durumunu metin olarak yansıtır.
- **Ses tercihi:** `M` veya ses düğmesi ile sesi aç/kapat. Tercih tarayıcı depolamasına kaydedilir. Ses kapalıyken oyunun tamamı oynanabilir.

Her şey tek `index.html` içindedir; harici ses/görsel paketi, ağ bağlantısı veya derleme gerekmez.

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
| `M` | Sesi aç / kapat |
| `Esc` | Arşivi veya henüz onaylanmamış kararı kapat |
| `Enter` | Açılış, onay ve oda geçişi |

Dokunmatik yön tuşları ve ekrandaki butonlar da kullanılabilir. Zaman çizelgesi geçmiş hareketleri, plaka temaslarını ve anlık döngü ilerlemesini gösterir.

## Otomatik test

```sh
python -m pip install playwright
python -m playwright install chromium
python tests/smoke.py
```

Testler tüm **altı odayı** oynanış kurallarıyla çözerek denetler. Build 005 için kapı efektleri, sinyal göstergesi, kritik geri sayım ve ses tercihi ayrıca sınanır. Çift yankılı kilitler, arşiv sırasında zamanın durması, kararın iptali, her iki final, final tekrar oynama ve sonuçların depolamadan yeniden okunması ayrıca test edilir. Hız için yalnızca test sayfasına kontrollü zaman ilerletici eklenir. Test ortamındaki `about:blank` sayfasının güvenli depolama kökeni olmadığından, saklama kontrollerinde bir `localStorage` taklidi kullanılır; gerçek tarayıcı alanında tekrar yükleme davranışı ayrıca elle kontrol edilebilir. **GitHub Actions** her ana dal güncellemesinde aynı testleri çalıştırır.

## Teknik

Tamamen bağımsız HTML / CSS / JavaScript ve Canvas 2D. Oyun kaynak kodu `index.html` içindedir; `tests/smoke.py` testleri ve `.github/workflows/smoke.yml` otomatik doğrulamayı sağlar.

**Yön:** Build 006: yankılara daha gelişmiş çevresel tepkiler ve yeni bir ana bölümün çekirdeği.