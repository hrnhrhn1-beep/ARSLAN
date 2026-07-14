#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
from app.database.db_init import get_connection

class Parca:
    """Parça modeli"""
    
    @staticmethod
    def ekle(ad, kod, kategori, birim='Adet', min_stok=10, aciklama=''):
        """Yeni parça ekle"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO Parcalar (ad, kod, kategori, birim, min_stok, aciklama)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (ad, kod, kategori, birim, min_stok, aciklama))
            conn.commit()
            parca_id = cursor.lastrowid
            return {'success': True, 'id': parca_id, 'message': 'Parça başarıyla eklendi'}
        except Exception as e:
            return {'success': False, 'message': str(e)}
        finally:
            conn.close()
    
    @staticmethod
    def guncelle(parca_id, ad=None, kod=None, kategori=None, min_stok=None, aciklama=None):
        """Parça güncelle"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            updates = []
            params = []
            
            if ad is not None:
                updates.append('ad = ?')
                params.append(ad)
            if kod is not None:
                updates.append('kod = ?')
                params.append(kod)
            if kategori is not None:
                updates.append('kategori = ?')
                params.append(kategori)
            if min_stok is not None:
                updates.append('min_stok = ?')
                params.append(min_stok)
            if aciklama is not None:
                updates.append('aciklama = ?')
                params.append(aciklama)
            
            if not updates:
                return {'success': False, 'message': 'Güncellenecek alan bulunamadı'}
            
            updates.append('guncelleme_tarihi = CURRENT_TIMESTAMP')
            params.append(parca_id)
            
            query = f"UPDATE Parcalar SET {', '.join(updates)} WHERE id = ?"
            cursor.execute(query, params)
            conn.commit()
            return {'success': True, 'message': 'Parça başarıyla güncellendi'}
        except Exception as e:
            return {'success': False, 'message': str(e)}
        finally:
            conn.close()
    
    @staticmethod
    def tum_parcalari_al():
        """Tüm parçaları al"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT id, ad, kod, kategori, guncel_stok, min_stok FROM Parcalar ORDER BY ad')
            return cursor.fetchall()
        finally:
            conn.close()
    
    @staticmethod
    def ara(arama_terimi):
        """Parça ara (Ad, Kod veya OEM Kodu ile)"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            # Parça adı veya kodu ile ara
            cursor.execute('''
                SELECT DISTINCT p.id, p.ad, p.kod, p.kategori, p.guncel_stok, p.min_stok
                FROM Parcalar p
                LEFT JOIN OemKodlari o ON p.id = o.parca_id
                WHERE p.ad LIKE ? OR p.kod LIKE ? OR o.oem_kod LIKE ?
                ORDER BY p.ad
            ''', (f'%{arama_terimi}%', f'%{arama_terimi}%', f'%{arama_terimi}%'))
            return cursor.fetchall()
        finally:
            conn.close()
    
    @staticmethod
    def sil(parca_id):
        """Parça sil"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('DELETE FROM Parcalar WHERE id = ?', (parca_id,))
            conn.commit()
            return {'success': True, 'message': 'Parça başarıyla silindi'}
        except Exception as e:
            return {'success': False, 'message': str(e)}
        finally:
            conn.close()

class OemKodu:
    """OEM Kodu modeli"""
    
    @staticmethod
    def ekle(parca_id, oem_kod, uretici='', aciklama=''):
        """OEM kodu ekle"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO OemKodlari (parca_id, oem_kod, uretici, aciklama)
                VALUES (?, ?, ?, ?)
            ''', (parca_id, oem_kod, uretici, aciklama))
            conn.commit()
            return {'success': True, 'message': 'OEM kodu başarıyla eklendi'}
        except Exception as e:
            return {'success': False, 'message': str(e)}
        finally:
            conn.close()
    
    @staticmethod
    def parca_id_ile_al(parca_id):
        """Parçaya ait tüm OEM kodlarını al"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                SELECT id, oem_kod, uretici, aciklama FROM OemKodlari WHERE parca_id = ?
            ''', (parca_id,))
            return cursor.fetchall()
        finally:
            conn.close()

class Tedarikci:
    """Tedarikçi modeli"""
    
    @staticmethod
    def ekle(ad, telefon='', email='', adres='', sehir='', aciklama=''):
        """Tedarikçi ekle"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO Tedarikciler (ad, telefon, email, adres, sehir, aciklama)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (ad, telefon, email, adres, sehir, aciklama))
            conn.commit()
            return {'success': True, 'id': cursor.lastrowid, 'message': 'Tedarikçi başarıyla eklendi'}
        except Exception as e:
            return {'success': False, 'message': str(e)}
        finally:
            conn.close()
    
    @staticmethod
    def tum_tedarikcileri_al():
        """Tüm tedarikçileri al"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT id, ad, telefon, email, sehir FROM Tedarikciler ORDER BY ad')
            return cursor.fetchall()
        finally:
            conn.close()

class RafKonumu:
    """Raf Konumu modeli"""
    
    @staticmethod
    def ekle_yada_guncelle(parca_id, depo, raf, sira='', pozisyon=''):
        """Raf konumu ekle veya güncelle"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO RafKonumu (parca_id, depo, raf, sira, pozisyon)
                VALUES (?, ?, ?, ?, ?)
            ''', (parca_id, depo, raf, sira, pozisyon))
            conn.commit()
            return {'success': True, 'message': 'Raf konumu başarıyla kaydedildi'}
        except Exception as e:
            return {'success': False, 'message': str(e)}
        finally:
            conn.close()
    
    @staticmethod
    def al(parca_id):
        """Raf konumunu al"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                SELECT depo, raf, sira, pozisyon FROM RafKonumu WHERE parca_id = ?
            ''', (parca_id,))
            return cursor.fetchone()
        finally:
            conn.close()

class StokHareketleri:
    """Stok Hareketleri modeli (Plaka ile)"""
    
    @staticmethod
    def ekle(parca_id, hareket_tipi, miktar, plaka=None, tedarikci_id=None, aciklama=''):
        """Stok hareketi kaydet (Stok Girişi/Çıkışı)"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO StokHareketleri (parca_id, hareket_tipi, miktar, plaka, tedarikci_id, aciklama)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (parca_id, hareket_tipi, miktar, plaka, tedarikci_id, aciklama))
            
            # Stok güncelle
            if hareket_tipi == 'Girişi':
                cursor.execute('UPDATE Parcalar SET guncel_stok = guncel_stok + ? WHERE id = ?', (miktar, parca_id))
            elif hareket_tipi == 'Çıkışı':
                cursor.execute('UPDATE Parcalar SET guncel_stok = guncel_stok - ? WHERE id = ?', (miktar, parca_id))
            
            conn.commit()
            return {'success': True, 'message': 'Stok hareketi başarıyla kaydedildi'}
        except Exception as e:
            return {'success': False, 'message': str(e)}
        finally:
            conn.close()
    
    @staticmethod
    def plaka_ile_al(plaka):
        """Plakaya ait stok çıkışlarını al"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                SELECT sh.id, p.ad, p.kod, sh.miktar, sh.olusturma_tarihi
                FROM StokHareketleri sh
                JOIN Parcalar p ON sh.parca_id = p.id
                WHERE sh.plaka = ? AND sh.hareket_tipi = 'Çıkışı'
                ORDER BY sh.olusturma_tarihi DESC
            ''', (plaka,))
            return cursor.fetchall()
        finally:
            conn.close()
    
    @staticmethod
    def gunluk_rapor(tarih_str):
        """Günlük rapor (Plaka ve parça ile)"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                SELECT 
                    sh.plaka,
                    p.ad,
                    p.kod,
                    sh.hareket_tipi,
                    SUM(sh.miktar) as toplam_miktar,
                    COUNT(*) as hareket_sayisi
                FROM StokHareketleri sh
                JOIN Parcalar p ON sh.parca_id = p.id
                WHERE DATE(sh.olusturma_tarihi) = ?
                GROUP BY sh.plaka, p.id, sh.hareket_tipi
                ORDER BY sh.plaka, p.ad
            ''', (tarih_str,))
            return cursor.fetchall()
        finally:
            conn.close()
    
    @staticmethod
    def aylik_rapor(yil, ay):
        """Aylık rapor"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                SELECT 
                    p.ad,
                    p.kod,
                    sh.hareket_tipi,
                    SUM(sh.miktar) as toplam_miktar,
                    COUNT(DISTINCT sh.plaka) as farkli_plaka_sayisi
                FROM StokHareketleri sh
                JOIN Parcalar p ON sh.parca_id = p.id
                WHERE CAST(strftime('%Y', sh.olusturma_tarihi) AS INTEGER) = ?
                  AND CAST(strftime('%m', sh.olusturma_tarihi) AS INTEGER) = ?
                GROUP BY p.id, sh.hareket_tipi
                ORDER BY p.ad
            ''', (yil, ay))
            return cursor.fetchall()
        finally:
            conn.close()
