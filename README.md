# ECHO/12 — Kendi Geçmişinle Kaç

Tarayıcıda oynanan, tek kişilik Türkçe bilim kurgu / **12 saniyelik zaman döngüsü bulmacası**. Geçmiş hareketlerin sonraki döngülerde yankılar tarafından tekrarlanır. Onların yardımıyla kilitli bölümleri aşar, eski kayıtları keşfeder ve çekirdeğin kaderini belirlersin.

## Build 016 — Bölüm VI: Ayrı Tanıklar

**17 oynanabilir oda, 6 hikâye bölümü ve 27 arşiv girdisi.** Bu sürüm yalnızca daha fazla baskı plakası eklemez: iki ayrı kaydedilmiş kişinin hareketinin **aynı saniyede iki farklı sensörde doğrulanmasını** ve bunun bilinçli bir tanıklığa dönüşmesini sağlar.

- **Oda 16 / Ayrı Tanıklar:** İlk kapıyı M plakasındaki bir yankıyla aç. Ardından ayrı döngülerde bir gerçek yankıyı I, diğer gerçek yankıyı II sensöründe tut. XSYNC kapısı yalnızca **farklı kayıt kimlikleri aynı anda iki noktadaysa** ve F doğrulayıcısı açıksa açılır. Aynı sensörde iki hayalet, tek hayalet veya sahte siluet bunu sağlayamaz.
- **Oda 17 / Kora Protokolü:** Aynı eşzamanlılık bulmacasını çöz, ardından Kora konsolunda E ile son tanıklığı onayla. Önceden **yayınlama** seçilmişse tarayıcı açık olmalıdır; **karantina** seçilmişse iki yankıyı doğrulayıp kapıdan geçtikten sonra tarayıcı kapatılmalıdır. Her iki rotada da finale ulaşmak mümkündür ama farklı işlem protokolleri gerekir.
- **Yeni kanıt paneli:** I ve II sensörlerinde hangi gerçek yankının bulunduğu ve çift tanıklığın onaylanıp onaylanmadığı görülebilir. Sensörler oyun alanında ve mobil küçük haritada işaretlenir.
- **Anlatı ve arşiv:** Bölüm V tamamlanınca Bölüm VI açılır. A19, A20 ve iki farklı son kayıt (A21_PUBLIC/A21_SEALED) eklendi. Kora'nın yetkiye erişebildiğine dair izler var; fakat yönetici anahtarının ilk sahibini kesinleştiren bir iddiada bulunulmuyor.
- **Testler:** Eski 15 oda korunurken iki yeni odanın tarayıcı testleri eklendi. Aynı sensörde iki hayaletin yetersizliği, ayrı iki yankının kabul edilmesi, tarayıcı kilidi, karantinada tarayıcıyı kapatmadan E komutunun reddi ve iki final denetlenir.

## Build 015 — Bölüm V: Kayıp Saniye

**15 oda, 5 bölüm, 23 arşiv girdisi.** Yeni bölüm, OPERATÖR 00'ın tek bir kimlik olmadığı bulgusunu bu kez **doğrulanabilir zaman aralığı** ve eski seçimlerin yeni fiziksel kapılara etkisi üzerinden ilerletir.

- **Oda 14 / Kayıp Saniye:** Önce yankıyla M kapısını aç, sonra gerçek bir A→B izi üret. Sıra doğru olsa bile iki sensörün arasındaki **1,6–3,6 saniyelik** pencereye uymayan kayıt STAMP geçidini açamaz. Oyuncu B'ye koşmak yerine ölçülmüş bekleme/movement temposu oluşturmalıdır. Gerçek kayıtların A→B zaman farkı, geçerli/geçersiz etiketiyle kanıt ekranına yansır.
- **Oda 15 / Yetki Kapısı:** Aynı zaman damgasını doğrula; son rölenin mekanik koşulu Bölüm IV'ün kalıcı kararına göre değişir. **Yayınlama** yolunda iki ayrı yankı son plakaya *aynı anda* dokunmalıdır. **Karantina** yolunda ise yalnızca **canlı oyuncu** dokunabilir; kısa röle yaklaşık 3 saniye açık kalır. İki yol da aynı mekânda oynanabilir, fakat farklı strateji gerektirir.
- **Hikâye:** Kopya yönetici anahtarı ile gerçek bir kişinin kimliği arasındaki ayrım sürer. Yeni arşiv A16, A17 ve karar temelli A18_PUBLIC/A18_SEALED kayıtları eklendi. İlk ve dördüncü bölüm kararları saklanır; ayrı son raporları üretilir.
- **Kanıt paneli:** Doğru sıra fakat yanlış süre, geçersiz zaman damgası olarak gösterilir. Yakın kameranın haritası, ses efektleri, mevcut oda seçimi ve ipuçları önceki sürümlerle uyumludur.
- **Testler:** 15 odanın tarayıcı regresyonuna ek olarak hızlı/yanlış aralık reddi, kabul edilen zaman damgası, iki yankıyla yayın geçidi, canlı röleyle karantina geçidi ve iki ayrı final yer alır.

## Build 014 — Kanıt Zaman Çizelgesi ve Yetki Zinciri

Dört hikâye bölümü ve 13 oda korunur. Bu sürüm 12 ve 13. odaların doğrulama mekaniklerini **oyuncunun okuyabileceği, karşılaştırabileceği ve denetleyebileceği** hâle getirir.

- **Canlı kanıt paneli:** A ve B okuma noktalarından yapılan geçişler gerçek zaman damgalarıyla gösterilir. Yanlış yönde kayıt, geçersiz kayıt veya doğru A→B/B→A imzaları kayıt başına ayrı görünür. Konsol sırasıyla gereken yönleri ve F tarayıcısının durumunu belirtir.
- **Zaman çizelgesi işaretçileri:** Her kayıt satırında A ve B noktalarına girişler renkli/harfli işaretlerle, kaydedildiği gerçek saniyede gösterilir. Geçiş sırasını bir bakışta anlamak ve yankı rotalarını karşılaştırmak kolaylaşır. İmza sırası için sadece görüntüye değil gerçek pozisyon örneklerine bakılır.
- **Dört aşamalı yetki zinciri:** Bölüm IV tamamlanınca kamera görüntüsü, fiziksel hareket kayıtları, kimliği bilinmeyen 00 yetki sahibi ve yayın/karantina seçiminin sonucu yan yana görünür. Gerçekten doğrulanan kanıtlarla **henüz bilinmeyen yetki sahibi** birbirinden ayrı işaretlenir.
- **İki ayrı finale özgü görsellik:** Dış hatta yayınlama tanıkların yerinin açığa çıkması ihtimaliyle vurgulanır; karantina seçimi kanıtın dış incelemeden saklandığını gösterir. Önceki hikâye seçimleri ve yerel kayıtlar korunur.
- **Teknik ayrım:** Geçiş sırasını ispat eden işaretler oyun içi konum/zaman örnekleridir; bunlar gerçek bir kriptografik kimlik doğrulaması değildir. Sahte 00 görüntüsü kayıt geçmişine eklenmez.
- **Testler:** 13 odanın regresyonuna ek olarak, geçersiz ters kayıt, canlı A/B zaman sırası, iki doğrulanmış farklı yankı, tarayıcı kilidi ve iki finale özgü yetki zinciri kontrolleri.

## Build 013 — Bölüm IV: Köken / İmza Denetimi

**13 oynanabilir oda, 4 hikâye bölümü ve 19 arşiv girdisi.** İki yeni odanın temelinde görüntünün gerçek olup olmamasından ziyade **kaydedilmiş hareketin hangi sırada yapıldığını doğrulamak** var.

- **12. oda — İzin Sırası:** İlk M plakası için bir yankı oluştur. İlk bariyerden geçtikten sonra parlak A ve B okuma noktalarından sırasıyla yürü. Yeni bir yankı olarak kaydet ve F ile doğrulayıcıyı aç. Doğru kaydedilmiş A→B hareketi PROOF kilidini açar. Sadece B→A yapan bir yankı veya sahte görüntü açamaz.
- **13. oda — İki İmza:** Aynı mekanik büyür: **iki ayrı yankı**, biri A→B, diğeri B→A sırasını kaydetmeli. Bir kayıt her iki koşulu birden karşılayamaz; bu da daha önce hazırladığın iki ayrı imzanın gerçekten farklı rotalardan geldiğini gösterir. M plakası yankıyla tutulur, PROOF iki yönlü kanıt ister ve son çıkış ancak konsoldaki bilinçli seçimle açılır.
- **Hikâye kararı:** Doğrulanmış kayıtları dış gözlemcilere **yayınlamak** ya da tanıkların izlerini **karantinaya almak** seçilir. Yayınlama sahteciliğin sorgulanmasını sağlar fakat yankıların yerlerini ifşa edebilir; karantina izleri korur fakat dış incelemeyi geciktirir. İlk bölümdeki *çekirdeği koru/sustur* seçimi de kapanış metinlerini etkilemeye devam eder.
- **Kalıcı sonuçlar:** Son kaynak kararı `echo12-source-verdict` anahtarında kaydedilir; geçmiş karar, arşiv ve ilerleme verileri korunur. Son odanın kararı tekrar oynanabilir. Yeni arşiv: A13, A14 ve yalnızca ilgili kararda açılan A15_PUBLISH / A15_SEAL.
- **Oynanış güvenilirliği:** Kimlik doğrulaması fiziksel kayıt örneklerinin sıra denetimidir, gerçek dünyadaki kriptografik kimlik imzası değildir. Kapı metinleri hangi yönün eksik olduğunu gösterir, küçük harita okuma istasyonlarını çizer, her yeni oda için isteğe bağlı üç ipucu bulunur.
- **Testler:** Önceki 11 odanın otomatik senaryoları, yeni iki oda, ters sıralama reddi, sahte görüntü, tarayıcı koşulu, karar iptali, iki alternatif final ve ilerleme kayıtları birlikte sınanır.

## Build 012 — Yakın Takip Kamerası ve Bölüm Finalleri

Yeni oda eklenmedi: **11 oda, 3 hikâye bölümü ve 15 arşiv kaydı** korunuyor. Amaç özellikle mobil cihazlarda küçük karo ve kapıların okunabilirliğini artırmak ve bölüm kapanışlarına anlamlı bir anlatı ritmi kazandırmak.

- **Yakın takip kamerası:** Kamera, oyun mekaniğini değiştirmeden sahneyi 1,65 kat büyütür ve karakterin konumunu takip eder. Masaüstünde varsayılan tam görünüm, küçük ekranda varsayılan yakın takip modu sunulur. Oyun altındaki düğmeyle iki görünüm arasında geçiş yapılabilir.
- **Harita görünümü:** Yakın takip açıkken oyun alanı dışında 18×11 odanın tamamını gösteren küçük harita açılır. Duvarlar, açık/kapalı geçitler, basınç plakaları, oyuncu, kaydedilmiş yankılar ve çıkış simgesi aynı anda görülebilir.
- **Kayıtlı tercih:** Kamera seçimi `echo12-camera-mode` anahtarıyla yerel saklanır. Diğer ilerleme kayıtlarından bağımsızdır; istenildiğinde değiştirilebilir.
- **Bölüm kapanış raporu:** Bölüm I (oda 6), Bölüm II (oda 8) ve Bölüm III (oda 11) bitiminde iki ayrı sonuç kartı eklenmiştir: **Kesinleşen bulgu** ve **Açık kalan soru**. İlk bölümdeki çekirdeği koruma veya susturma tercihleri raporların metnini de değiştirir. Bu kartlar önceki hikâye seçimlerini değiştirmez.
- **Görsel hareket izi:** Oyuncunun arkasında çok kısa süre kalan, yalnızca dekoratif bir ışık izi bulunur. Hareket fiziği, çarpışma, yankı kayıtları ve süreler aynı kalır. Sistemde az hareket tercihi açıkken iz çizilmez.
- **Tarayıcı testleri:** Yakın takip, zoom takibi, küçük harita, görünüm tercihi, iki farklı bölüm I raporu ve sonraki iki bölüm raporu otomatik kontrole eklendi.

## Build 011 — Mobil Kontroller ve Çizim Performansı

Bu sürüm, oyun kurallarına ve 11 oda / 15 arşiv yapısına dokunmadan mobil kullanım ile çizim maliyetini iyileştirir.

- **Yeniden düzenlenen mobil gamepad:** Dört yön tuşu artık 3×3 alanın kenarlarında, merkezde yankı kaydı var. Alt sırada Etkileşim, Geri Al ve Duraklat tuşları bulunuyor. Başparmak kullanımına uygun büyük dokunma alanları ve tuşun basılı olduğunu gösteren görsel durumlar eklendi. Mobil kumanda oyun alanının hemen altında, zaman çizelgesinden önce gösterilir.
- **Gerçek eşzamanlı dokunma:** İki farklı parmak/yön, çapraz yürümeyi destekler. Her dokunma ayrı kimlikle izlenir; parmağı bırakmak veya dokunmanın iptal edilmesi ilgili hareketi durdurur. Fiziksel klavye ile dokunmatik aynı anda kullanılsa da birinin serbest bırakılması diğerinin yönünü kesmez. Oda değiştirme, panel açma, duraklatma ve pencere odağını kaybetme tüm basılı yönleri temizler.
- **Mobilde daha okunaklı arayüz:** Dar ekranlarda kontrol butonları, görev durumu ve oyun alanı boşlukları yeniden düzenlendi. Mobil kumandadaki kontroller için erişilebilir etiket ve basılı durum bilgisi vardır.
- **Statik zemin önbelleği:** Odanın 18×11 sabit karo zemini ve sahne arka planı tekrar tekrar hesaplanmak yerine önbellekten çizilir; kapılar, yankılar ve güvenlik elemanları dinamik kalır.
- **Dengeli kare bütçesi:** Dokunmatik cihazlarda görsel yenileme yaklaşık 30 FPS hedefler; bulmaca simülasyonu 60 Hz adımlarla sürer. Oyun duraklatılmışken ve görsel efekt kalmadığında gereksiz çizimler atlanır. Sekme görünmezken simülasyon ilerlemez, girişler temizlenir.
- **Geriye uyumluluk:** Eski kayıtlar, bölüm kararları, mekanikler, ipuçları, yerel rekorlar ve tüm odalar korunur. Mobil dokunma/iptal davranışları için otomatik tarayıcı testleri eklendi.

## Build 010 — Bölüm Akışı ve Bulmaca Geri Bildirimi

Bu sürümde oda sayısı yine **11** olarak korunur. Öncelik artık oyuncunun hedefleri fark etmesi, ilk mekaniği kendisi öğrenmesi ve uzun bir oyunda kendi gelişimini izlemesidir.

- **Bölüm şeridi:** 11 odanın ilerlemesi, üç bölüm halinde görünür. Bulunulan oda öne çıkar; tamamlanıp açılmış önceki odalar farklı renktedir.
- **Dinamik hedefler:** Sabit, doğrudan çözüm veren oda açıklaması yerine kısa bir görev tanımı gösterilir. İlk odada oyuncu yeşil plakaya ulaşınca yönlendirme değişir: önce hareket, sonra kayıt, sonra çıkış. Geri kalanı için isteğe bağlı üç kademeli H ipucu sistemi korunur.
- **Kapı durum panosu:** Her kapının harfi, açık/kapalı hâli ve neden açılmadığı anlık gösterilir. İki yankı isteyen plakaların sayacı, tarayıcı, canlı oyuncu, ters kayıt, süreli röle, kanıt sayısı ve onaylanmamış karar gibi mekanikler kendi açıklamalarıyla izlenebilir.
- **Bölüm açılışları:** İlk bölüm ve Bölüm II/III başlangıçlarında kısa bağlamsal hikâye girişleri gösterilir. Kısa oda başlıkları ve ilgili arşiv kayıtları korunur.
- **Oda sonuç özeti:** Tamamlanan odada kaydedilmiş yankı sayısı, aktif toplam süre ve kullanılan ipucu düzeyi gösterilir. Oyuncunun en iyi sonucu daha az yankı, eşitlik hâlinde daha kısa aktif süre ölçütüne göre yerel olarak saklanır; tekrar oynanan oda seçme ekranında görünür.
- **Kayıt politikası:** Yeni rekorlar `echo12-best-runs` anahtarında tutulur. Mevcut `echo12-unlocked`, hikâye seçimleri ve arşiv kayıtları değiştirilmez. Oda yeniden başlatılırsa yeni denemenin sayaçları sıfırlanır.

## Build 009 — Oyun deneyimi ve kontrol kalitesi

Bu sürümde yeni oda eklemek yerine **oynanış erişimini ve keşfedilebilirliği** iyileştirdik. Mevcut 11 oda ve 15 arşiv kaydı korunur.

- **Oda seçimi (O):** Açılmış herhangi bir odaya geri dönebilirsin. Kilitli odalar erişilemez ve ayrı gösterilir. Seçim ekranı zamanı durdurur; oda değiştirmek yalnızca o odanın aktif yankılarını sıfırlar. Arşiv, önceki seçimler ve açılmış oda ilerlemesi silinmez.
- **Üç kademeli ipucu (H):** Her oda için aşamalı, isteğe bağlı üç ayrı çözüm desteği vardır. Önce mekaniğe yönlendirir; sonraki seviyeler daha somut yol gösterir. İpuçları otomatik gösterilmez. Oda değiştirince aşama sıfırlanır.
- **Odak ve klavye kontrolü:** Space tuşu ekrandaki bir butona odaklıysa yanlışlıkla yankı kaydetmez; butonun doğal klavye etkileşimini korur. Açılış menüsü kapanınca gizli buton odağı temizlenir.
- **Ters kayıt zaman çizelgesi:** Ters oynatılan yankılar artık çizelgede gerçekten **ters örnek sırasıyla** görünür; hareket ve baskı plakası temasları ters yönde doğru zamanlarda işaretlenir.
- **Erişilebilirlik:** Oda düğmeleri ekran okuyucu etiketleri, belirgin klavye odağı ve dar ekranlarda sütun sayısı değişen düzen kullanır.
- **Testler:** Açılmamış odaların kilitli kalması, mevcut ilerlemenin korunması, seçim menüsünde saatin durması, ipuçları ve tuş odağı için ek tarayıcı testleri.

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
| `O` | Oda seçimi ekranını aç (açılmış odalar) |
| `H` | Kademeli ipucu göster |
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

**Yön:** Build 014: kanıt sıralaması için anlaşılır görsel geri bildirim, mobil oynanış ve bağımsız kanıt kaynakları arasında daha büyük anlatı sonuçları.