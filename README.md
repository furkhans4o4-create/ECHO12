# ECHO/12 — Kendi Geçmişinle Kaç

Tarayıcıda oynanan, tek kişilik Türkçe bilim kurgu / **12 saniyelik zaman döngüsü bulmacası**. Geçmiş hareketlerin sonraki döngülerde yankılar tarafından tekrarlanır. Onların yardımıyla kilitli bölümleri aşar, eski kayıtları keşfeder ve çekirdeğin kaderini belirlersin.

## Build 008 — Kanıtın Gölgesi

**11 oynanabilir oda, 15 arşiv kaydı ve yeni adli inceleme bulmacası.** Bu sürüm yeni oda sayısı yerine oyuncunun çıkarım yapmasını ön plana çıkarır.

- **Oda 11 / Üç Tanık:** İlk kapıyı daha önce kaydettiğin bir yankıyla açarsın. Diğer tarafta üç ayrı istasyon vardır: kamera, basınç ve kayıt defteri. `F` ile doğrulayıcıyı açtıktan sonra her istasyondan `E` ile ayrı ölçüm toplarsın. Kanıtlar arşive otomatik olarak değil, bu odanın denetim ekranına aktarılır.
- **Gerçek kayıt izi:** Kayıt defteri, mevcut yankı hareketlerinden örneklenmiş bir tanımlayıcı hesaplar. Bu oyun içi karşılaştırma parmak izidir; kriptografik imza değildir. Sahte siluetin bu kayıtlarda bir karşılığı yoktur.
- **Kanıt panosu:** AUDIT konsolu zamanı durdurur ve üç bağımsız gözlemi yan yana gösterir. Üç ölçüm olmadan hüküm verilemez. Yanlış yorumlarda hangi çıkarımın delille çeliştiği açıklanır; doğru yorum ikinci kapının kilidini kaldırır. Önceki yankılar sıfırlanmaz.
- **Hikâye sonucu:** 00'ın bir kişi olduğu varsayımı sorgulanır. Kanıtın desteklediği dar sonuç, kayıt bulunmadan görüntü enjekte edilebildiğidir; bunun arkasında kimin olduğu hâlâ bilinmez. Yeni `A12` arşiv tutanağı son odadan sonra açılır.
- **Arayüz:** Kanıt ekranı mobil/dar ekranlara uyum sağlar, klavyeyle kullanılabilir ve `Esc` ile kapatılabilir. Eski 10 oda, hikâye seçimleri ve kayıtlar korunur.

## Build 007 — Bölüm III: Güvenilmez Kayıt

**Toplam 10 oynanabilir oda, 14 keşfedilebilir arşiv girdisi ve birbiriyle tutarlı iki hikâye hattı.**

- **9. oda / Hayalet İmza:** T ve U plakalarının üzerinde geçmişe benzeyen iki **sahte yankı** belirir. Görünür olmaları gerçek kayıt oldukları anlamına gelmez: sahte görüntüler fiziksel plakaları hiç etkinleştiremez. `F` veya ekrandaki doğrulama düğmesiyle tarayıcı açıldığında sahte imzalar kırmızı işaretlenir. Kapılar yalnızca **doğrulanmış gerçek yankı** ve tarayıcı birlikteyken açılır.
- **10. oda / Ters İz:** `F` ile sonraki kayıt `NORMAL` veya `TERS` oynatılacak şekilde değiştirilir. Ters kayıt son karede başlayıp başlangıca doğru ilerler; V kilidi yalnızca ters kayıt, Y kilidi yalnızca normal kayıt kabul eder. Çizelgede ters kayıtlar `R` etiketiyle belirtilir.
- **Bölüm II ara finali:** 8. oda, Bölüm III'e bağlanan ayrı hikâye ekranına dönüşür; önceki çekirdek kararına göre içeriden veya dışarıdan devam edilir.
- **Bölüm III keşifleri:** A09, A10 terminal kayıtları ve başlangıç kararına bağlı A11 son kaydı. `OPERATÖR 00` adı ilk kez görünür, ancak failin kim olduğu henüz kesinleşmez.
- **Uyumluluk:** 1–8. odalar, önceki kararların kaydı, yankı geri alma, ses, dokunmatik kontrol ve eski oyuncu ilerlemeleri korunur. Mevcut `index.html` tek dosyadır.

## Build 006 — Bölüm II: Karşı Sinyal

**Toplam 8 oynanabilir oda, iki dallanan hikâye hattı ve 10 arşiv kaydı.**

- **7. oda / Eşik:** Mor **R plakası aynı anda iki kaydedilmiş yankı** ister. Canlı oyuncu ikinci yankı yerine sayılmaz. Birinci Q kilidi ise yalnızca yankıyla açılır. Mor plakanın üzerinde `0/2`, `1/2`, `2/2` geri bildirimleri görünür.
- **8. oda / Karşı Sinyal:** İki yankı mor S kilidini aynı anda açar. Turuncu P plakası yalnızca **canlı oyuncuya** tepki verir; 2,8 saniyelik geçiş penceresinden koşarak çıkılır. Normal yankı bu süreyi tetikleyemez.
- **Bölüm I kararının devamı:** 6. odadaki *tanıkları koru* ya da *çekirdeği sustur* tercihinin sonucu `echo12-chapter-path` ile saklanır. Her iki yol Bölüm II'ye geçer ancak başlangıç metni, sonuç ve son arşiv kaydı farklıdır. İki tercih eşitlenmez: biri tesiste kalır, öteki dış hatta devam eder.
- **Yeni keşifler:** Eşik ve Karşı Sinyal odalarında iki yeni terminal; Bölüm II sonunda karara bağlı iki farklı rapor. Çözülmüş kayıtlar kalıcıdır.
- **Geriye uyumluluk:** İlk altı oda, önceki iki bölüm sonu, kayıt/geri alma, ses ve görsel efektler korunur. Eski kayıtlı ilerleme dosyaları sıfırlanmaz.

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

Testler tüm **on bir odayı** oynanış kurallarıyla çözerek denetler. Build 005 için kapı efektleri, sinyal göstergesi, kritik geri sayım ve ses tercihi ayrıca sınanır. Çift yankılı kilitler, arşiv sırasında zamanın durması, kararın iptali, her iki final, final tekrar oynama ve sonuçların depolamadan yeniden okunması ayrıca test edilir. Hız için yalnızca test sayfasına kontrollü zaman ilerletici eklenir. Test ortamındaki `about:blank` sayfasının güvenli depolama kökeni olmadığından, saklama kontrollerinde bir `localStorage` taklidi kullanılır; gerçek tarayıcı alanında tekrar yükleme davranışı ayrıca elle kontrol edilebilir. **GitHub Actions** her ana dal güncellemesinde aynı testleri çalıştırır.

## Teknik

Tamamen bağımsız HTML / CSS / JavaScript ve Canvas 2D. Oyun kaynak kodu `index.html` içindedir; `tests/smoke.py` testleri ve `.github/workflows/smoke.yml` otomatik doğrulamayı sağlar.

**Yön:** Build 009: doğrulama bulmacasının oyuncu tarafından anlaşılabilirliğini ve sürtünmesini yeniden değerlendirme; ses, erişilebilirlik ve zaman çizelgesi iyileştirmeleri.