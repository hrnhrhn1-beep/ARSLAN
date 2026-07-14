#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import os
from datetime import datetime

DB_PATH = 'arslan.db'

def init_database():
    """Veritabanını ve tabloları oluştur"""
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Parcalar Tablosu
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Parcalar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ad TEXT NOT NULL UNIQUE,
            kod TEXT NOT NULL UNIQUE,
            kategori TEXT,
            birim TEXT DEFAULT 'Adet',
            guncel_stok INTEGER DEFAULT 0,
            min_stok INTEGER DEFAULT 10,
            aciklama TEXT,
            olusturma_tarihi TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            guncelleme_tarihi TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # OEM Kodları Tablosu (Eşdeğer Kodlar)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS OemKodlari (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            parca_id INTEGER NOT NULL,
            oem_kod TEXT NOT NULL UNIQUE,
            uretici TEXT,
            aciklama TEXT,
            FOREIGN KEY (parca_id) REFERENCES Parcalar(id)
        )
    ''')
    
    # Tedarikciler Tablosu
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Tedarikciler (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ad TEXT NOT NULL UNIQUE,
            telefon TEXT,
            email TEXT,
            adres TEXT,
            sehir TEXT,
            aciklama TEXT,
            olusturma_tarihi TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Raf Konumu Tablosu
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS RafKonumu (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            parca_id INTEGER NOT NULL UNIQUE,
            depo TEXT NOT NULL,
            raf TEXT NOT NULL,
            sira TEXT,
            pozisyon TEXT,
            FOREIGN KEY (parca_id) REFERENCES Parcalar(id)
        )
    ''')
    
    # Stok Hareketleri Tablosu (Plaka ile)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS StokHareketleri (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            parca_id INTEGER NOT NULL,
            hareket_tipi TEXT NOT NULL,
            miktar INTEGER NOT NULL,
            plaka TEXT,
            tedarikci_id INTEGER,
            aciklama TEXT,
            olusturma_tarihi TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            olusturan_kullanici TEXT DEFAULT 'Sistem',
            FOREIGN KEY (parca_id) REFERENCES Parcalar(id),
            FOREIGN KEY (tedarikci_id) REFERENCES Tedarikciler(id)
        )
    ''')
    
    # İndeks oluştur (Hızlı sorgu için)
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_parca_kod ON Parcalar(kod)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_oem_kod ON OemKodlari(oem_kod)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_stok_plaka ON StokHareketleri(plaka)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_stok_tarih ON StokHareketleri(olusturma_tarihi)')
    
    conn.commit()
    conn.close()
    
    print(f"✅ Veritabanı başlatıldı: {DB_PATH}")

def get_connection():
    """Veritabanı bağlantısı al"""
    return sqlite3.connect(DB_PATH)
