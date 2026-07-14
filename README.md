# ARSLAN - Oto Yedek Parça Yönetim Sistemi

## Özellikler

- ✅ Parça Yönetimi (Ekleme, Güncelleme, Silme)
- ✅ OEM Kodu Eşleştirmesi (Eşdeğer Kodlar)
- ✅ Tedarikçi/Firma Yönetimi
- ✅ Raf Konumu Takibi
- ✅ Plaka ile Stok Çıkışı Kaydı
- ✅ Raporlama (Günlük, Aylık)
- ✅ Arama ve Filtreleme
- ✅ SQLite Veritabanı
- ✅ PyQt6 GUI (Masaüstü)

## Kurulum

```bash
pip install -r requirements.txt
python main.py
```

## Veritabanı Yapısı

- **Parcalar**: Parça bilgileri (Ad, Kod, Kategori)
- **OemKodlari**: OEM eşdeğer kodları
- **Tedarikciler**: Firma/Tedarikçi bilgileri
- **RafKonumu**: Raf ve depo konumu
- **StokHareketleri**: Stok giriş/çıkışı (Plaka ile)
- **Raporlar**: Günlük/Aylık raporlar

## Gereksinimler

- Python 3.8+
- PyQt6
- SQLite3
- pandas (Raporlama için)
