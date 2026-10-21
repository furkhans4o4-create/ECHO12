# ECHO/12

**Kendi geçmişinle kaç.** Zaman döngüsü üzerine kurulu, tek oyunculu 2D bulmaca oyunu.

## Build 001 — Oynanabilir prototip
- Üç elle tasarlanmış oda
- Her 12 saniyede önceki hareketlerden yankı üretimi
- Baskı plakaları ve bunlara bağlı geçiş kapıları
- Üçüncü odada hareketli güvenlik küresi
- Döngüyü erken bitirme, yeniden başlatma, duraklatma, ses
- Tamamen özgün Canvas çizimleri; dış bağımlılık yok
- Tarayıcının yerel depolamasında ilerleme kaydı

## Çalıştırma
`index.html` dosyasını modern bir tarayıcıda aç. Kurulum gerekmez. GitHub Pages açık olduğunda kök dizindeki `index.html` webden oynanabilir.

## Kontroller
- `WASD` / oklar: hareket
- `Space`: mevcut hareketleri yankı olarak kaydet ve yeni döngüye geç
- `R`: odayı sıfırla
- `P`: duraklat / devam et

## Teknik
İlk sürüm bağımsız HTML/CSS/JS olarak geliştirildi. Derleme ve üçüncü taraf araç gerektirmez. Geliştikçe modüler mimariye geçilecek.

## Sonraki görev
Build 002: yankı zaman çizelgesi, yeni seviye mekaniği ve oyun akışı iyileştirmeleri.

Geliştirme yönetimi: Her sonraki adımı oyun yönetmeni belirler; oynanabilirlik ve test önceliklidir.
