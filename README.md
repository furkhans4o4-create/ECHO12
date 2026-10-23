# ECHO/12 — Kendi Geçmişinle Kaç

Tarayıcıda oynanan, tek kişilik Türkçe bilim kurgu / **12 saniyelik zaman döngüsü bulmacası**. Geçmiş hareketlerin sonraki döngülerde yankılar tarafından tekrarlanır. Onların yardımıyla kilitli bölümleri aşar, eski kayıtları keşfeder ve çekirdeğin kaderini belirlersin.

## Build 040 — Plaka Tanıkları / Kapıyı Kimin Açtığını Gör

Her plakanın yanında, gerçekten hangi yankının veya canlı karakterin bulunduğunu gösteren küçük iki satırlık tanık rozeti açılır. Etiketler E01–E06 numaralarını kullanır ve Yankı Odağı renkleriyle eşleşir.

- **Fiziksel temas:** Canlı oyuncu için SEN, gerçek kayıtlar için E01 / E02 etiketleri görünür. Birden fazla yankı üst üste gelirse fazlası +N olarak kısaltılır. Sahte fantomlar gerçek tanık olarak sayılmaz.
- **Doğru kural:** Çifte baskıda 1/2 veya 2/2; yalnız-yankı ve yalnız-canlı koşullarında YANKI GEREKLİ veya CANLI GEREKLİ; yanlış oynatma yönünde TERS / İLERİ GEREKLİ, kapalı F doğrulayıcısında F GEREKLİ uyarısı gösterilir.
- **Röle ayrımı:** Süreli geçit plaka boşalsa bile açık kaldığında tanık etiketi RÖLE olur. Bu geçici açıklık yeni bir yankı temasıyla karıştırılmaz.
- **Sade ve erişilebilir:** Yalnızca temas edilen veya açık rölesi bulunan plakalarda etiket çıkar. Görme engelli oyuncular için aynı olayların erişilebilir kısa açıklaması yalnızca durum değiştiğinde güncellenir. Oyun fizik ve kayıt kuralları hiç değişmez.
- **Testler:** Gerçek yankı teması, iki bağımsız yankının eşzamanlı baskısı, odak değişimi, fantomun hariç tutulması, F tarayıcısı, röle kuyruğu ve ekran okuyucu güncellemesi Chromium otomasyonuyla doğrulanır.

## Build 039 — Yankı Odağı / Altı Geçmişi Birbirinden Ayır

**Birden fazla yankı artık tek bir mor kütle gibi görünmüyor.** E01–E06 kayıtları sahne, mini harita, zaman çizelgesi, Yankı Laboratuvarı ve kayıt editöründe aynı renge ve numaraya sahiptir.

- **Numaralı sahne varlıkları:** Her kayıtlı yankının üstünde E01, E02… E06 etiketi bulunur. Ters oynatma ↶ sembolü ve kesikli rota çizgisiyle ayrılır. Renk göremeyen oyuncular da numarayla kayıtları izleyebilir.
- **Gerçek oynatmayı izleyen rota:** Çizgiler yalnızca eski hareket örneklerini değil, güncel oynatma zamanını gösterir. Faz Kaydırma, Zaman Çivisi ve ters oynatma gibi değişiklikler rotanın görünürlüğüne ve uzunluğuna yansır; plaka fiziği değişmez.
- **Yankı Odağı:** Hareket çizelgesinin altında, sade arayüzde de görünen küçük E01–E06 renkli düğmeler vardır. Bir yankıyı seçince onun izi ve çizelgesi belirginleşir, diğerleri soluklaşır ama sahnedeki fiziksel etkileri sürer. HEPSİ düğmesi veya aynı düğmeye tekrar basmak bütün yankıları gösterir.
- **Klavye ve laboratuvar:** 1–6 tuşları ilgili yankıyı vurgular; 0 bütün yankıları gösterir. Laboratuvar açılırken odaklanmış yankı önceden seçilir. Hiç kayıt yoksa odak düğmeleri gizlidir.
- **Güvenli düzenleme:** Hedef nesne referansıyla tutulur: Önceki yankı silinirse seçim yanlış bir kayda atlamaz. Seçili yankı silinince veya oda değişince odak temizlenir; geri yükleme sonrasında mevcut seçili kayıt nesnesi korunur. Bu yalnızca görselleştirmedir; kayıt parmak izleri, kapı kuralları, ipucu sayısı ve JSON kaydı etkilenmez.
- **Tarayıcı testleri:** İki farklı yankının rengi ve numarası, odak seçme ve kaldırma, klavye kısayolları, laboratuvar ile eşleşme, silme/geri yükleme sırasında kararlılık, ters ve gecikmeli kaydın görsel varlığı Playwright ile sınanır.

## Build 038 — Sade Görünüm / Oyuncuyu Önce Oyunla Tanıştır

Oyunun ilk dakikalarında karmaşık analiz araçları oyuncunun dikkatini dağıtmasın diye **Sade / Ayrıntılı** arayüz ayrımı eklendi.

- **İlk altı oda sade başlar:** Yeni oyuncuya önce gerçek oyun sahnesi, 12 saniyelik zaman çizelgesi, görev hedefi, kapı durumu, yankı kaydetme, denemeyi yenileme ve diğer temel kontroller sunulur. İleriye yönelik plaka tahmini, zaman çivisi editörü, imza doğrulaması, teşhis ve ustalık panelleri başlangıçta gizlenir. Birinci odada A plakasına gidip ilk yankıyı kaydetme akışını hatırlatan kısa bir temel kontrol satırı bulunur.
- **Yedinci odada ayrıntılı görünüme geçilir:** Bölüm II ile yeni mekanikler başlarken analiz ekranları varsayılan olarak açık görünür. Oyuncunun elle seçtiği mod bu otomatik geçişle değiştirilmez.
- **Tek tuşla geri alma:** Kontrollerin yanındaki **Görünüm: sade / ayrıntılı** düğmesine veya **C** tuşuna basarak görünümü değiştir. El ile seçilen görünüm tarayıcıda echo12-hud-mode altında tutulur; sonraki oturumlarda aynı tercih kullanılır.
- **Sadece sunum:** Oda, yankılar, plaka fiziği, ipucu kullanımı ve JSON yedek biçimi değişmez. Gizli teknik paneller gerekli durumları hesaplamaya devam eder; yeniden açıldığında bilgiler kaybolmaz. Sade moda geçiş ipucu sayılmaz veya İpucusuz ustalık rozeti hakkını bozmaz.
- **Testler:** Yeni oyuncuda sade başlangıç, C kısayoluyla tam görünüm, butonla geri dönüş, kalıcı tercih, gerçek yankı kaydı, ipucu sayısının korunması, ilk altı odanın otomatik sade oluşu ve ileri odada isteğe bağlı sade moda geçiş Playwright regresyonlarına eklendi.

## Build 037 — Oyun Kolu / Analog Kontrol Desteği

Artık ECHO/12 bir standart oyun koluyla da oynanabilir. Yeni kontrol sistemi mevcut fizik, 12 saniyelik döngü ve kayıt kurallarını değiştirmez; oyundaki normal komutları kullanır.

- **Hareket:** Sol analog çubuk analog hızla yürütür. %22 ölü bölgede karakter yerinde kalır; tam eğim standart klavye hareketiyle aynı en yüksek hıza ulaşır. D-pad ile dört/çapraz yön yürünebilir. Klavye, dokunmatik ve oyun kolu birlikte çalışır; ortak hız sınırı aşılamaz.
- **Oyun eylemleri:** **A** etkileşim / ana menüde başla, **B** canlı denemeyi yenile / açık pencereden çık, **X** yankıyı kaydet, **Y** son yankıyı sil. **LB** F doğrulayıcı veya ters kayıt, **RB** Yankı Laboratuvarı, **Back** arşiv, **Start** duraklat/devam et. Analog çubuk tıklamaları kamera/görev pusulasını açıp kapatır.
- **Pencerelerde gezinme:** Denetim, arşiv ve laboratuvar gibi pencerelerde D-pad ile odak ilerletilir, A odaktaki düğmeyi seçer, B kapatır. Klavye ve dokunmatik kontroller olduğu gibi korunur.
- **Bağlantı işareti:** Uyumlu, tarayıcı tarafından algılanmış standart kol varsa küçük bağlantı etiketi görünür; çıkarıldığında kaybolur. Tarayıcının oyun kolu API'si yoksa oyun normal klavye modunda çalışır.
- **Düğme güvenliği:** Her oyun kolu düğmesine sadece ilk basışta eylem uygulanır. Uzun süre X basmak onlarca yankı kaydetmez, Start basmak hızlıca tekrar duraklatmaz. Menü veya duraklatma açıkken analog çubuk karakteri hareket ettirmez.
- **Testler:** Gerçek tarayıcıda sahte Gamepad API ile analog deadzone, hareket hızı, D-pad, tek basış kaydı, geri alma, pause/unpause, bağlantı kopması, F ters kayıt modu ve laboratuvar/arşiv açma-kapatma doğrulanır.

## Build 036 — Hata İzi / Başarısız Denemeyi Gör

**Son hatanın nerede olduğunu artık hatırlamak zorunda değilsin.** Canlı deneme başarısız olduğunda o denemedeki hareket, yeni döngünün zemininde kısa süreli bir iz olarak kalır. Bu iz kayıtlı yankı değildir: plaka veya geçitleri açmaz.

- **Devriye teması:** Devriyeye yakalanınca önceki hareketin **kırmızı kesikli rota**, çarpışma noktası ise **kırmızı çarpı** olarak görünür. Bildirim, hangi saniyede yakalandığını ve kayıtlı yankıların korunduğunu açıklar. Devriyenin gerçek hızı ve çarpışma mesafesi değişmez.
- **Denemeyi yenile (X):** İptal edilen canlı yol **mavi kesikli rota** olarak gösterilir. Önceki yankılar, deliller ve ilerleme korunur; boş döngüyü yenileyince sahneye gereksiz iz çizilmez.
- **Kendiliğinden temizlenir:** Son tek bir iz tutulur; **6 saniye aktif oyun süresi** sonunda kaybolur. Laboratuvar, arşiv veya duraklatma modunda süre ilerlemez. Yeni yankı kaydı, oda değişimi veya tam yeniden başlatma izi hemen temizler.
- **Hafif ve erişilebilir:** İz, Canvas üzerinde az örnekli bir çizimdir; bir kerelik okunabilir yazılı açıklaması da vardır. Sadece renge dayanmaz. Kaydedilen asıl hareketleri, bulmaca fiziğini veya kayıt dosyası biçimini değiştirmez.
- **Testler:** X yenilemesinde rotanın görünmesi, yeni yankı üretilmemesi, incelemede zamanın durması, 6 saniyelik silinme, yeni kayıtta temizlenme ve gerçek devriye çarpışması Playwright regresyonlarıyla kontrol edilir.

## Build 035 — Devriye Öngörüsü / Tehlikeyi Önceden Gör

Kör Nokta odasının kırmızı güvenlik devriyesine gerçek hareket güzergâhı ve güvenli karar vermeyi kolaylaştıran kısa vadeli uyarılar eklendi.

- **Gerçek devriye hattı:** Devriyenin dikey hareket koridoru, döndüğü uç noktalar ve öldürücü 0,46 karelik temas sınırı sahnede çizilir. Görselleştirme gerçek hareket formülünden hesaplanır, yapay bir rota üretmez.
- **Yakın gelecek:** **0,8** ve **1,6 saniye** sonraki fiziksel devriye konumları hafif noktalarla gösterilir. Tahmin 12 saniyelik döngü sonunu geçerse yeni döngünün başından hesaplanır.
- **Tehlike uyarısı:** Oyuncu devriyeye 1,25 kare yakınsa yalnızca o sırada görünen uyarı alanı açılır. Girişte tek uyarı sesi çıkar; sesler arası en az 1,5 saniye vardır. Ekran okuyucusuna sürekli değişen rakamlar okutulmaz.
- **Küçük harita:** Yakın takip modunun mini haritası devriyenin hareket hattını ve mevcut konumunu gösterir.
- **Kurallar değişmedi:** Devriyenin hızı ve 0,46 karelik ölüm eşiği aynı kalır. Yakalanınca sadece o andaki canlı deneme sıfırlanır; kayıtlı yankılar korunur. Devriyesi olmayan odalarda sahte uyarı gösterilmez. Hareketi azaltma tercihi korunur.
- **Testler:** Güncel ve gelecek devriye konumları, dönme noktası, güvenli yakın mesafe, tekrarsız uyarı, fiziksel çarpışma sonrası sıfırlama ve beş devriyesiz oda Playwright testlerine eklendi.

## Build 034 — Sinyal Hatları / Görsel Kapı Geri Bildirimi

Kapıları ilgili plakalara bağlayan, sahnenin döşemesine işlenmiş ince elektrik hatları eklendi. Böylece oyuncu haritadaki kapının hangi fiziksel plaka tarafından beslendiğini ek bir kontrol paneline bakmadan görebilir.

- **Sahnedeki gerçek durum:** Sönük hat kapalı geçidi, turkuaz hat etkin plakayı, altın hat temas sona erse bile rölenin sürdürdüğü açıklığı gösterir. Bir plaka üzerinde fiziksel temas olsa bile kapı henüz açılmamışsa açık yeşil ışık gösterilmez.
- **Kapının yanında geri sayım:** Süreli röleli geçitlerde kalan süre ondalık saniyeyle gösterilir. Gösterge mevcut röle zaman damgasından okunur, tahmin etmez.
- **Geniş oda uyumu:** Birden fazla kapısı olan odalarda ayrı elektrik hatları bulunur. Kanıt, denetim, tanık ve final yetki kapıları için sahte bir plaka bağlantısı çizilmez. Yankı fazı veya zaman çivisi değiştirilince ışık, fiziksel kapı durumuyla birlikte değişir.
- **Erişilebilirlik ve performans:** Hareket azaltma tercihinde hareketli akım animasyonu kapatılır. Çizgiler ince bir sahne katmanıdır; oyun kuralları, kayıt dosyaları, hikâye ve ustalık rozetleri etkilenmez.
- **Tarayıcı testleri:** Plaka açılma/kapanma, yankıyı geri alma, süreli röle bitişi ve altı farklı odanın fiziksel bağlantıları kapsanır.

## Build 033 — Sahne Pusulası / Hedefi Haritanın İçinde Bul

**Yeni bir panel yerine doğrudan oynanış sahnesine küçük bir hedef pusulası eklendi.** Build 032'deki dinamik görev rehberinin henüz tamamlanmamış adımı, varsa tek bir oyun içi konuma bağlanır. Oyuncunun çevresinde o konumu işaret eden küçük bir ok görünür; hedefte hafif bir halka ve yakın takip haritasında işaret bulunur.

- **Somut, değişken hedefler:** Plaka, açık kapı zamanı, canlı röle, çıkış, A/B okuma noktası, iki tanığın eksik sensörü, ölçümü yapılmamış en yakın kanıt istasyonu, denetim/kora konsolu gibi gerçek dünya nesnelerine yön verir. Bir A/B kaydında önce A'ya, A'ya dokunduktan sonra B'ye yönelir.
- **Oyuncunun yerine karar vermez:** F ile tarama, seçilecek hikâye kararı ve diğer oyuncu eylemleri için sahte harita konumu gösterilmez. Pusula engellerin içinden hayalî bir rota çizmez, yalnızca yönü gösterir.
- **Tercih ve erişilebilirlik:** **G** tuşu veya yakın takip yanındaki **Görev pusulası** düğmesiyle aç/kapat. Tercih tarayıcıda saklanır. Azaltılmış hareket açıkken halka sabit kalır; mini haritadaki hedef işareti aynı tercihe bağlıdır.
- **Ödün vermeyen yönlendirme:** Pusula mevcut görevi ve oyuncu konumunu okur; yankıları, kapıları, kanıtları, zamanlayıcıları ve kayıt dosyalarını değiştirmez. H ile verilen ipucundan bağımsızdır; İpucusuz ustalık ödülünü etkilemez.
- **Testler:** İlk oda hedefi, geçide ve çıkışa geçiş, geri alma, aç/kapat ve saklanan tercih, A/B olay sırasıyla yön değiştirme, tarayıcı bekleme durumu ve eksik kanıt istasyonu tarayıcı testlerinde doğrulanır.

## Build 032 — Dinamik Görev Rehberi

Oyunun ilk anlarını ve ileri bulmacalarını daha okunur hâle getirdim. Her odada üstte **Operatör / Aktif Hedef** satırı, güncel hedef ve küçük bir ilerleme şeridi vardır. Oyuncu isterse **Tüm görev adımlarını göster** bölümünü açabilir.

- **19 odaya özel plan:** Baskı plakası için gerçekten kaydedilmiş yankı, A/B imza sırası, zaman aralığı, F doğrulaması, kanıt karşılaştırması, I/II ortak tanık zamanı ve konsol kararları gibi oda kurallarından türeyen hedefler. Toplam kayıt sayısı tek başına plaka başarısı sayılmaz.
- **Çözümü ele vermeden yönlendirir:** Hedefler sıradaki somut işi gösterir; ayrıntılı bulmaca ipuçları ayrı kalır. Görev panelini kullanmak ipucu sayacını artırmaz ve İpucusuz ustalık rozetini bozmaz.
- **Gerçek anlık durum:** Oda içindeki plaka geçidi veya kısa süreli P rölesi kapanırsa görev durumu da değişir. Kayıt, tarayıcı, denetim ve hikâye kararları gerçek oyun durumuyla senkron kalır. Yankı silme, faz ve zaman çivisi düzenleme sonrası tekrar hesaplanır.
- **Daha temiz ekran:** Yalnızca bir satırlık mevcut hedef her zaman görünür; uzun kontrol listesi kapalıdır. Mobil cihazlar ve klavye erişimi desteklenir. Oyun fiziği, kaydetme biçimi, hikâye rotaları, üç final, 57 ustalık rozeti değiştirilmedi.

## Build 031 — Zaman Çivisi / Yankının İçinde Bir Anı Dondur

**Yeni gerçek oynanış mekaniği:** 10. oda (*Ters İz*) ve sonrasında her kayıtlı yankıya bir zaman çivisi eklenebilir. Oyuncu yankının oynatma akışı içinde **0,5–11,5 saniye** arası duraklayacağı anı, **0 / 0,5 / 1 / 1,5 saniye** bekleme süresini belirler.

- **Fiziksel duraklama:** Yankı seçilen anda gerçekten durur. Üzerinde bulunduğu plaka veya I/II sensörü baskıyı kaybetmez; süre bitince hareket kayıtlı kaldığı noktadan devam eder. 12. saniyeyi aşan son kısım gösterilmez. Faz Kaydırma ile birleşebilir; faz boyunca yankı henüz yoktur.
- **Değişmeyen geçmiş:** Hareket örnekleri, A/B kaynak imzaları ve yankı parmak izleri aynıdır. Zaman çivisi kurmak veya süresini değiştirmek güncel döngüyü sıfırlar; kanıt ve yetki kilitleri gerçek zamanlamaya göre yeniden doğrulanır. Silinen kayıt geri getirilirse faz ve çivi birlikte geri gelir.
- **Oyuna yansıması:** İki fiziksel yankının aynı anda baskı uyguladığı bulmacalarda hareketleri tekrar kaydetmek yerine kısa bir anı uzatabilirsin. Ana sahne, mini harita, yankı laboratuvarı, olay işaretleri, plaka zaman tahmini ve 12 saniyelik zaman çizelgesi aynı fiziksel oynatma zamanını kullanır.
- **Kapsam:** İlk dokuz oda aynı kalır; ileri odalar yeni bir alternatif çözüm yolu kazanır. Kampanya, ilerleme kaydı, 57 ustalık rozeti ve mevcut JSON yedek biçimi değişmez.
- **Kontroller:** Yankı Kayıtlarını Yönet → **Durak Noktası** ve **Bekleme**. Bekleme Kapalı seçilirse çivi kaldırılır. Tüm kontroller klavye ve dokunmatik girişe uygundur.

## Build 030 — Faz Kaydırma / Yankıları Yeniden Zamanla

**Yankıların ne zaman ortaya çıktığı artık gerçek bir bulmaca değişkeni.** Bölüm II'den itibaren Yankı Kayıtlarını Yönet panelinde E01–E06 kayıtlarını ayrı ayrı **0–3 saniye** geciktirebilirsin. Gecikme 0,5 saniyelik adımlarla ayarlanır; yeni bir yankı kaydetmeye gerek yoktur.

- **Gerçek fizik:** Faz süresi dolmadan yankı sahnede bulunmaz, plakalara basmaz, I/II tanık sensörlerinde görünmez ve kapı açamaz. Süre dolduğunda gerçek kaydından normal veya ters yönde oynar. 12. saniyede kayıt kesilir.
- **Kayıt kimliği korunur:** Kaydedilmiş hareketin örnekleri, kaynak imzası ve A/B olaylarının sırası değişmez. Bir yankının fazını düzenlemek, canlı döngüyü başa sarar ve daha önce onaylanmış kayıt-bağımlı delilleri yeniden doğrulatır. Geri getirilen yankı önceki fazını da korur.
- **Çapraz görünürlük:** Faz miktarı her yankı satırında görülür; ana sahne ve mini harita, laboratuvar oynatıcısı, plaka zaman haritası, tanık çakışma analizi ve zaman çizelgesi aynı fazlı hareketi gösterir.
- **Sınırlar:** İleri bölüm mekaniğidir; ilk bölümde düğmeler kilitlidir. Oynayan 19 oda, hikâye rotaları, ustalık madalyaları ve mevcut sürüm 1 JSON kayıt yapısı değiştirilmez.
- **Testler:** Fiziksel kapı açılma anı, faz aralığı sınırları, plaka zamanı, silip aynı fazda geri getirme, ilk bölümde kilit ve ters oynatılan yankının 12 saniye dışındaki teması tarayıcı testlerine eklendi.

## Build 029 — Operatör Sınamaları

Kampanyanın **19 odası, 7 bölümü ve 35 arşivi** korunur. Her oda için üç bağımsız, isteğe bağlı ustalık hedefi vardır. Rozetler **kalıcıdır**; farklı tekrar oynayışlarda kazanılabilir ve normal bulmaca kurallarını değiştirmez.

- **Az Yankı:** Odaya özel yankı bütçesini aşmadan tamamla. Bütçeler her odanın ihtiyaçlarına göre ayarlanmıştır.
- **İpucusuz:** Odayı hiçbir aşamalı ipucu açmadan bitir. İpucu kullanmak diğer rozetleri etkilemez.
- **Zaman:** Yankı bütçesi hesaba katılarak belirlenen aktif süre sınırını geçme. Menüde, laboratuvarda veya duraklatma ekranında geçen süre sayılmaz.
- **Rozetler:** Her odada katlanır hedef paneli, sonuç ekranında yeni kazanılan rozetler, oda seçiminde **SINAMA x/3** ve Kayıt Kasası'nda toplam **57 rozet** sayacı bulunur.
- **Kayıt uyumluluğu:** Rozetler tarayıcıda otomatik saklanır ve mevcut sürüm 1 JSON yedeğinde isteğe bağlı alan olarak taşınır. Build 028 ve önceki yedekler geçerlidir; bilinmeyen, çift veya tamamlanmamış oda madalyaları doğrulamada reddedilir.
- **Testler:** Gerçek oda çözümüyle üç rozet, sonuç ekranı, oda seçimi, yedek, eski sürüm uyumluluğu ve bozuk verilerin reddi Playwright testlerine eklendi.

## Build 028 — Yankı Laboratuvarı Oynatıcı

**19 oda, 7 bölüm ve 35 arşiv** korunur. Laboratuvardaki kayıtlar artık manuel zaman kaydırma olmadan oynatılıp önemli temas anları incelenebilir.

- **Oynat / duraklat:** 0–12 saniye boyunca kayıtlı yankıları izle; son saniyede dur veya Tekrar ile döngüsel oynat.
- **Üç hız:** 0,5×, 1× ve 2×. Kaydırıcıyı elle kullanmak ya da yarım saniye adım düğmesine basmak oynatmayı durdurur.
- **Olay işaretleri:** Her kayıtlı yankının plaka, A/B imza noktası ve I/II tanık sensörlerine değdiği anlar zaman damgalı düğmelere dönüşür. Önceki/sonraki önemli an denetimleriyle olaylara atlanabilir. Ters oynatılan kayıtlar kaynak hareket zamanında değil, **gerçek oynatma sırasındaki zamanlarında** listelenir.
- **Güvenli inceleme:** Laboratuvar oyunun saatini, röleleri, kapıları, kanıtı veya yankı kayıtlarını değiştirmez. Kapatınca oynatıcı durur. Klavye odağı ve zaman kaydırıcısının yön tuşları korunur.
- **Testler:** Oynatma hızı, zaman sınırı, tekrar, manuel duraklatma, temas işaretleri, gerçek oyun saatinin donması ve ters kayıt senaryoları mevcut Playwright testlerine eklendi.

## Build 027 — Plaka Zaman Haritası

19 oda, 7 bölüm ve 35 arşiv korunur. **Plakaların 12 saniyelik zaman haritası** adlı katlanır panel, kayıtlı yankıların herhangi bir odadaki her plakayı hangi zaman aralıklarında etkinleştirebileceğini hesaplar. Eski oynanışı ve kayıt dosyalarını değiştirmez.

- **Bütün plakalarda zaman tahmini:** Mavi şeritler yalnızca geçerli türde ve yeterli sayıda yankının bulunduğu anlarda görünür; mor iki-yankı plakalarında bir kayıt tek başına başarı sayılmaz. Ters/normal kayıt kısıtları hesaba katılır.
- **Kısa süreli röleler:** Altın şeritler, kayıtlı yankı teması sona erdikten sonra açık kalması öngörülen röle sürelerini gösterir. Hesap sıfırdan başlayan bir döngü içindir; canlı oyuncunun henüz atmadığı adımları tahmin etmez.
- **Canlı ve F koşulları:** Yalnızca canlı oyuncunun etkinleştirebildiği plakalar ayrı işaretlenir. F doğrulayıcısına bağımlı plakalar, yankı zamanlaması uygun olsa bile F kapalıyken hazır görünmez.
- **Anlık güncelleme:** Yankı ekleme/silme/geri getirme, oda değiştirme, F açma ve zaman ilerlemesinde görünüm yenilenir; beyaz çizgi döngü saatini takip eder.
- **Testler:** Sıfır ve bir kayıt, seçili yankıyı silip geri getirme, aynı plakada iki kayıt, altın röle uzantısı ve tarayıcı geçerliliği tarayıcı testlerine eklendi.

## Build 026 — Hızlı Deneme / Yankıları Koru

**19 oda, 7 bölüm ve 35 arşiv** korunur. Denemede yanlış yöne yürüdüğünde artık yankıları silmeden yeni bir 12 saniyelik başlangıç yapabilirsin.

- **X · Denemeyi yenile:** Mevcut canlı hareket izi iptal edilir; oyuncu ve saat başlangıca döner. Hiçbir yeni yankı oluşmaz ve mevcut E01–E06 kayıtları, sıraları, kayıt imzaları korunur.
- **R farklı çalışır:** R bütün odayı ve geçici yankıları sıfırlar. X yalnızca o anki canlı denemeyi bırakır. Z son yankıyı silmeye, Shift+Z onu geri getirmeye devam eder.
- **Kısa süreli sensör güvenliği:** Tekrar denemede anlık röle ve o anki canlı pozisyon temizlenir. Daha önce bilinçli olarak onaylanan kararlar veya toplanan denetim delilleri, gerçek kayıtları değiştirmediğin sürece korunur.
- **Erişim:** Klavyedeki X, kontrol alanındaki **Denemeyi yenile** ve mobil **Deneme** düğmesi aynı işlevi görür. Oyun duraklatılmışken veya arşiv gibi pencereler açıkken yeniden başlatma kapalıdır.
- **Uyumluluk:** Kampanya, kayıt kasası ve JSON yedek biçimi değişmedi. Otomatik tarayıcı testlerine yankı/geri alma korunumu, üç farklı kontrol şekli ve duraklatma denetimleri eklendi.

## Build 025 — Yankı Kayıtlarını Yönet

**19 oda, 7 bölüm, 35 arşiv** korunur. Kayıt alanının altında açılan **Yankı kayıtlarını yönet** panelinde E01–E06 arasından istenen yankı ayrı ayrı silinebilir; sonraki yankıları yeniden kaydetmek gerekmez.

- **Tek kayıt silme:** Her satırda NORMAL/TERS ve varsa A→B/B→A kanıtı, zaman farkı ile kaydın geçerliliği görülür. Silme sonrasında canlı döngü başa sarılır, kalan yankılar eski sıralarını korur.
- **Geri getirme:** Son silinen kayıt, yeni yankı oluşmadan aynı sıraya döndürülebilir. Ekrandaki düğme veya **Shift+Z** kullanılır; mevcut **Z** son yankıyı silmeye devam eder. Yeni bir kayıt oluşturulunca veya oda değişince geri getirme hakkı temizlenir.
- **Fiziksel tutarlılık:** Yankıya bağlı Kora tanıklığı, kanıt denetimi ve henüz tamamlanmamış kapı/karar onayı kaydı düzenlendiğinde yeniden hesaplanır; daha önce silinen kanıta dayanarak kapı açık kalmaz. Ayrı tanık zaman haritası da yeniden oluşturulur.
- **Testler:** Ortadan silme, özgün sıraya getirme, Shift+Z, zamanın sıfırlanması, yeni kayıtla geri getirme hakkının kaybolması, oda sıfırlama ve karşıt A/B imzaları silinince kapının yeniden kilitlenmesi doğrulanır.
- **Kayıt biçimi:** Kaydedilmiş kampanya ilerlemesi ve JSON yedek yapısı değişmez. Geçici yankılar/geri alma hafızası diske yazılmaz.

## Build 024 — İki Tanığın Zaman Haritası

**19 oda, 7 bölüm ve 35 arşiv** değişmedi. Ayrı tanıklık isteyen odalarda, kayıtlı yankıların I ve II sensörlerini **12 saniyenin hangi aralıklarında** tuttuğunu gösteren yeni bir eşzamanlılık haritası bulunur.

- **Kayıt başına gerçek zaman aralıkları:** Her yankının I (mavi) ve II (lila) üzerindeki temasları, ters oynatılan kayıtlar da dahil olmak üzere oynatma saatine göre çizilir. Beyaz çizgi o anki saniyeyi gösterir.
- **Bağımsız eşzamanlılık:** Yeşil **ORTAK** satırı, yalnızca *farklı* yankıların I ve II üzerinde çakışan zaman aralıklarını gösterir. İki yankının aynı I noktasında bulunması yanlışlıkla kabul edilmez.
- **Gerçeklik kontrolü ayrı:** Ortak zamanı bulmak, F tarayıcısını otomatik açmaz. Harita gerçek kayıtlardan hesaplanır; sahte siluetler sayılmaz ve bulmacanın kapı mantığı değiştirilmez.
- **Okunabilir alternatif:** Şeritlerin yanında E01/E02 gibi kimlikler ve saniye aralığı metni vardır. Kayıt yoksa veya ortak pencere oluşmamışsa sebebi açıkça belirtilir. Diğer odalarda panel gizlidir.
- **Test:** Sıfır/bir/iki/üç yankı, aynı sensöre yığılma, ayrı sensörlerde çakışma ve F doğrulayıcısının açık-kapalı durumları mevcut tarayıcı testlerinde denetlenir.

## Build 023 — Klavye Odağı ve Pencere Güvenliği

**19 oda, 7 bölüm ve 35 arşiv kaydı** korunur. Geliştirme bu kez oyunun bütün büyük pencerelerinde tek ve tutarlı bir klavye sözleşmesi kurar.

- **Sekmeyle güvenli gezinme:** Yankı Laboratuvarı, Kayıt Kasası, Delil Panosu, Oda Seçimi, arşiv ve karar/denetim pencerelerinde `Tab` veya `Shift+Tab` ile odak pencerenin dışına kaçmaz. Son düğmeden ilk düğmeye, ilk düğmeden son düğmeye gidilebilir. Kilitli/engelli düğmeler odak sırasına alınmaz.
- **Kapatınca eski odağı geri getir:** Esc veya kapat düğmesiyle çıkışta pencereyi açan düğmeye dönülür. Arşivden, karar konsolundan ve delil denetiminden çıkan oyuncu da etkileşime kaldığı yerden devam edebilir.
- **Klavye kısayolları:** Oyun yalnızca oynanırken ok tuşlarıyla hareket eder; farklı pencerelerde ok tuşları normal kaydırma ve form navigasyonu için kullanılabilir. Yankı Laboratuvarı zaman kaydırıcısının klavye kullanımına müdahale edilmez.
- **Oynanış değişmedi:** Döngünün uzunluğu, yankı hareketleri, bölüm koşulları, kayıt kasası biçimi ve final şartları aynıdır.
- **Tarayıcı testleri:** Altı farklı pencerenin ileri/geri sekme döngüleri, oyun/araç durumuna dönüş, karar penceresinden çıkış ve delil denetiminden sonra odak iadesi denetlenir.

## Build 023 — Canlı Kapı Teşhisi

19 odanın tümünde, kontroller altındaki **Kapılar neden kapalı?** bölmesi açılıp kapanabilir. Her kapının mevcut durumu oyuncunun gerçek kaydı, yankı sayısı, F doğrulayıcısı ve eşzamanlı sensörlere göre yeniden hesaplanır. Genel bir ipucundan farklı olarak sıradaki eksik koşulu belirtir: A→B, B→A, tarayıcı, I/II ayrı yankılar, Kora konsolu, canlı plaka veya zaman penceresi. Kapı açılınca durum **Açık · geçiş hazır** olarak değişir.

Bu teşhis bulmacayı çözmez, zamanı durdurmaz, yankı kaydetmez; yalnızca gerçek koşulları okunabilir Türkçe olarak gösterir. Fare, klavye ve dokunmatik ekranla erişilir. Tarayıcı testleri plaka etkinleştirme, ters imza ve eşzamanlı tanık senaryolarını kapsar.

## Build 022 — Erişilebilirlik: Yüksek Kontrast ve Azaltılmış Hareket

**19 oda, 7 bölüm, 35 arşiv** aynı kalır. Oyun başlangıçtan finale kadar daha okunabilir ve hareket hassasiyeti olan kullanıcılar için daha konforlu hâle getirilmiştir.

- **Görünüm ve Hareket:** Oyun kontrollerinin altındaki açılır ayarlar panelinden iki tercih yönetilir. Panel oyun alanını kaplamaz; klavye, fare veya dokunmatik kontrollerle erişilebilir. Seçimler ayrı düğmelerde görünür.
- **Hareket:** Sistem (cihazın `prefers-reduced-motion` tercihini takip eder), Azaltılmış veya Normal. Azaltılmış seçeneği gereksiz parçacıkları, parlak yayılan halkaları, hareket izlerini ve ekrana yayılan geri-sarma yıkamasını kaldırır; CSS geçişlerini de kısaltır. **12 saniyelik fizik simülasyonu, oyuncu hızı, kapılar ve kayıtların zamanlaması değişmez.**
- **Kontrast:** Yüksek kontrast modu metinleri ve panel çerçevelerini belirginleştirir, sahne ile zaman çizelgesinin görünürlüğünü artırır, odak işaretlerini kuvvetlendirir. Normal moda geri dönülebilir.
- **Kalıcı ayarlar ve taşınabilir yedek:** `echo12-motion-setting` ve `echo12-contrast-setting` yerel olarak saklanır. İsteğe bağlı `motion` ve `contrast` alanları mevcut `ECHO12_SAVE_V1` kayıt kasası yedeklerine eklenir. Eski yedeklerde bu alanlar yoksa Sistem/Normal varsayılanlarıyla uyum korunur.
- **Testler:** Üç hareket modu arasında geçiş, tarayıcının azaltılmış hareket sınıfı, efekt bastırma, yüksek kontrastta gerçek CSS değişikliği, oyun saatinin aynı hızda işlemesi, ayarların yedekten geri yüklenmesi ve geçersiz tercih değerlerinin reddedilmesi denetlenir.

## Build 021 — Yankı Laboratuvarı / Zamanın İçini Gör

**19 oda, 7 bölüm, 35 arşiv kaydı** aynı kalır. Son karmaşık odaların zamanlama bulmacalarında, oyuncunun geçmişte ne kaydettiğini görebilmesi için tüm kayıtlar üzerinde çalışan **oyun dışı bir inceleme ekranı** eklenmiştir.

- **Yankı Laboratuvarı (I):** Oyun sırasında veya duraklatılmışken açılır, tüm simülasyonu dondurur. 18×11 odanın şematik planı üzerinde duvarlar, çıkış, kapılar, plakalar, A/B ile I/II sensörleri ve kaydedilmiş izler çizilir. **Kapılar şematik gösterilir:** Bu önizleme gelecekteki geçitlerin gerçek zamanlı durumu gibi sunulmaz.
- **12 saniye tarama:** 0–12 saniyelik kaydırıcı veya ±0,5 sn düğmeleri, sahneyi oyunu ilerletmeden istediğin zamana taşır. Fare, dokunmatik giriş ve kaydırıcı odaklanmışken klavye ok tuşları desteklenir.
- **Yankı seçimi:** Tüm gerçek yankılar, seçilen tek yankı veya o anki canlı hareket izi ayrı görülebilir. Ters kayıtlar **TERS** etiketiyle gösterilir. Kanıtlanan A→B/B→A sırası ve zaman penceresi varsa ölçülen geçiş süresi de yazılır.
- **Yan etkisiz analiz:** Kaydırıcı ve görünüm seçimi gerçek oyunun `elapsed`, hareket dizileri, oyuncu konumu, yankı sayısı ve kayıtlarını değiştirmez. Laboratuvardan Esc/I ile çıktığında o anki oyun veya duraklatma durumuna geri dönülür.
- **Uyumluluk:** Kaydedilen ilerleme biçimi değişmez ve harici hizmet gerekmez. Tüm tarama işlemleri oyun HTML dosyası içinde gerçekleşir.
- **Otomatik test:** Gerçek bir yankı oluşturma, incelemede saat ve oyuncu durumunun değişmemesi, 12 saniye içinde zaman seçimi, klavyeyle kaydırma, duraklatma durumuna geri dönme ve ters bir yankının incelenmesi denetlenir.

## Build 020 — Gerçek Oda Tamamlama ve Güvenli Geri Yükleme

**19 oda / 7 bölüm / 35 arşiv** değişmedi. Oyuncu açısından ana iyileştirme, açılmış odalarla gerçekten tamamlanan odaları ayıran güvenilir bir kampanya kaydı; kayıt güvenliği açısından ise yarıda kesilen geri yüklemelerde eski verilerin korunmasıdır.

- **Tamamlama bilgisi:** Her başarılı oda geçişi `echo12-room-clears` listesine kaydedilir. Kampanya ilerleme çubuğunda tamamlanan sektörler ayrı görünür, oda seçimi ekranında **✓ TAMAMLANDI** rozeti taşır. Sadece açılmış ama bitirilmemiş odalar tamamlanmış gibi gösterilmez.
- **Kasa ilerleme sayacı:** Kayıt kasası artık kaç odanın gerçekten tamamlandığını (örn. 13/19), diğer oda rekorları ve arşiv kayıtlarından ayrı gösterir. Bitirilmiş son oda da hesaplanır.
- **Taşınabilir kayıt:** `ECHO12_SAVE_V1` biçimi korunur; `clearedRooms` adlı isteğe bağlı yeni alanla hangi odaların tamamlandığı taşınır. Eski v1 yedekleri bozulmaz: bu alan yoksa açılmış ilerlemeden tamamlanan önceki odalar çıkarılır; henüz açılmamış hiçbir odaya rozet verilmez.
- **Güvenilirlik:** JSON kayıtları geçersiz oda numaralarını reddeder. Geri yükleme başlamadan önce mevcut bütün oyun anahtarları yedeklenir; depolama kota hatası veya yazma sorunu çıkarsa önceki değerler geri yazılmaya çalışılır ve yeni oyun içi durum uygulanmaz. Tam geri alma tarayıcının depolamaya hâlâ yazabilmesine bağlıdır.
- **Testler:** Gerçek oda tamamlaması, renkli kampanya bölmeleri ve oda seçimi rozetleri, geçerli/invalid yedekler, eski v1 uyumluluğu, ilerleme paneli ve geri yükleme sırasında simüle edilmiş depolama arızası denetlenir.

## Build 019 — Kayıt Kasası ve Final Arşivi

**19 oynanabilir oda, 7 hikâye bölümü, 35 arşiv girdisi** değişmeden kalır. Bu aşama oyunun bitiş sonrası kullanılabilirliğine, ilerlemenin taşınabilirliğine ve veri güvenilirliğine odaklanır.

- **Kayıt Kasası (B):** Oyun sırasında, duraklatıldığında veya ana menüden açılabilen ayrı ekran. Kasa açıkken döngü ilerlemez. Mobil arayüzde menü düğmesi, masaüstünde B kısayolu bulunur.
- **Dışarı aktarma:** `ECHO12_Kayit_Yedegi.json` adlı tamamen yerel JSON dosyasını üretir. Oda ilerlemesi, ilk bölüm ve kaynak yayın/karantina kararları, son final tercihi, keşfedilen arşivler, üç bağımsız çıkarım, oda rekorları, ses ve kamera tercihleri saklanır. **O an oynanan 12 saniyelik döngü ve geçici yankılar dosyaya dahil edilmez.**
- **Geri yükleme:** Dosya içeriği hiçbir sunucuya gönderilmez. `ECHO12_SAVE_V1` sürüm etiketi, oda sınırları, bilinen arşiv kimlikleri, son kararlar, kayıt dizileri, performans sayıları ve delil dosyasının kaynakları denetlenir. Hatalı veri kayıtları değiştirmeden reddedilir. Geçerli kayıt, üzerine yazma onayından sonra yüklenir ve ilgili odanın başından devam edilir.
- **Final galerisi:** Oyunun üç sonu keşfedildikçe kasadaki kilitli kartlar açılır. Önceden ulaşılan farklı bitişler arşivden tekrar tespit edilir; yalnızca son tercih görüntülenmez.
- **Uyumluluk:** Eski Build 018 kayıtları otomatik olarak çalışır, yedek alma için mevcut oyunu sıfırlamak gerekmez. Tarayıcıların özel/gizli modlarında yerel saklama kalıcı olmayabilir; bu nedenle JSON yedeği önerilir.
- **Tarayıcı testleri:** Kasanın zamanı durdurması, sürüm biçimi, geçersiz JSON'un reddi, bozulmuş rekorların kabul edilmemesi, bütün kayıt ve tercih alanlarının yeniden yüklenmesi, farklı final arşivinin algılanması ve masaüstü kısayolları sınanır.

## Build 018 — Bölüm VII: Son On İki Saniye / Hikâyenin Finali

**19 oynanabilir oda · 7 hikâye bölümü · 35 arşiv girdisi.** Bu sürüm, ana kampanyaya yeni bir bölüm daha eklemek yerine hikâyenin ana soruşturmasını **üç farklı sonla tamamlar**. Bundan sonraki geliştirme önceliği oynanışın dengesi, görsel kalite, ses ve üretim kararlılığıdır.

- **Oda 18 / Zaman Köprüsü:** Önceden ayrı ayrı öğrenilen iki sistemi birlikte kullanır. En az bir A→B gerçek yankısı, 1,6–3,6 saniyelik imzalı süreye uymalı ve başka bir gerçek yankı aynı anda I sensöründe bulunurken ilki II noktasında olmalıdır. Üç kapının güvenilirliği sahte görüntü veya tek bir yankıyla sağlanamaz.
- **Oda 19 / Son Yetki:** Başlangıç M yankısıyla açılır. PROOF geçidi **farklı iki gerçek kayıtta** A→B ve B→A imzalarını, F doğrulayıcısını açık tutmayı şart koşar. Son kapı için bilinçli bir yetki kararı gerekir.
- **Üç alternatif final:** *Anahtarı İptal Et* kötüye kullanımın önünü keser, fakat kayıtların erişimi de kesilebilir. *İzleri Kilitli Tut* kayıtları korur, ama yönetici yetkisinin gelecekte yeniden kullanılma riski sürer. *Bağımsız Denetim* yalnızca K delil panosundaki üç bağımsız, kaynaklı çıkarım tamamlanırsa seçilebilir; denetçilerin güvenilirliği yine kesin değildir.
- **Önceki kararların sonucu:** Çekirdeği koruma/susturma ile kanıtı yayınlama/karantinaya alma tercihleri, final anlatısında geri alınmış sayılmaz. Kimliği bilinmeyen yönetici ile yankıların bilinci üzerine kanıtsız bir kesinlik sunulmaz.
- **Kapanış arşivi:** A22 ve A23 adlı iki son soruşturma kaydı, F01_PURGE/F01_PRESERVE/F01_REVIEW adlı üç final arşiv kaydı eklenmiştir. Son karar yerel `echo12-final-verdict` anahtarında saklanır; yeniden oynayarak farklı sonlar görülebilir.
- **Testler:** Önceki 17 odanın testleri korunur; karma zaman + iki tanık kapısı, karşıt doğrulanmış iki iz, final kararı olmadan son kapının kilitli olması, üçüncü seçeneğin kaynak koşulu, üç alternatif final ve ilerleme kayıtları eklenen testlerle kontrol edilir.

## Build 017 — Delil Panosu / Bağımsız Çıkarımlar

**17 oda, 6 bölüm ve 30 arşiv kaydı.** Bu sürümde amaç daha fazla aynı tip kapı açmak değil: oyuncunun keşfettiği kayıtları kendi mantığıyla karşılaştırıp, kesin delil ile varsayımı ayırabildiği tekrar kullanılabilir bir **soruşturma arayüzü** kurmak.

- **K tuşu / Delil Panosu:** Oyun sırasında ya da menüde erişilebilen ayrı bir ekran. Açıkken zaman döngüsü durur ve yanlış hareket kaydedilmez. Telefon ekranında tek sütun olur, klavye odağı ve Esc ile kapatma desteği vardır.
- **Üç soruşturma:** Görüntünün fiziksel izden farkı (A09 + A12), OPERATÖR 00'ın kişi değil yetki etiketi olması (A14 + A17), eşzamanlı yankıların bilinç kanıtı olup olmadığı (A19 + A20).
- **Kaynağa bağlı erişim:** Gerekli arşiv belgelerinin ikisi de oyuncu tarafından bulunmadıkça açıklama seçenekleri kilitli kalır. Yanlış yorum ilerlemeyi silmez veya yeni belgeyi açmaz. Doğru yorum **D01–D03** yeni bağımsız çıkarım tutanaklarını arşive ekler.
- **Kalıcı kayıt:** Başarılı çıkarımlar `echo12-case-deductions` anahtarında tutulur; açılan belgeler önceki `echo12-archive` arşiv listesine eklenir. Oda ilerlemesi, seçimler, altı yankı sınırı ve rekorlar değişmez.
- **Bilgi doğruluğu:** Kayıtlar haklı çıkarılabilir fiziksel bulgularla belirsiz kimlik/öznel bilinç iddialarını birbirinden ayırır. 00 etiketinin kesin sahibini veya yankıların bilinç taşıdığını uydurmaz.
- **Tarayıcı testleri:** 17 odanın önceki oynanışı korunurken kaynak sayısı, kilitli seçenekler, yanlış cevabın reddi, 3 doğru değerlendirme, dosyaların kalıcılığı, durdurulan zaman ve arşiv görünürlüğü test edilir.

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
| `X` | Geçerli denemeyi iptal edip döngüyü başlat; mevcut yankıları koru |
| `Z` | Son yankıyı sil |
| `Shift+Z` | Son silinen yankıyı geri getir (bir sonraki kayda kadar) |
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

**Yön:** Sonraki aşamalarda tekrar oynanabilirlik, öğretici akış ve son bölüm zorluk dengesini iyileştirmek; 19 odalık kampanyayı ve kayıt biçimini korumak.