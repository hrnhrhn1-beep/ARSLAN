#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTableWidget, QTableWidgetItem, QSpinBox, QMessageBox, QHeaderView
)
from PyQt6.QtCore import Qt
from app.database.models import StokHareketleri
from datetime import datetime, timedelta
import csv
import os

class RaporTab(QWidget):
    """Raporlama Tabı (Günlük, Aylık)"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """UI Başlat"""
        layout = QVBoxLayout()
        
        # Rapor Seçimi
        form_layout = QHBoxLayout()
        
        # Günlük Rapor
        form_layout.addWidget(QLabel("Günlük Rapor (Tarih):"))
        self.gunluk_tarih_input = QLineEdit()
        self.gunluk_tarih_input.setText(datetime.today().strftime('%Y-%m-%d'))
        self.gunluk_tarih_input.setPlaceholderText("YYYY-MM-DD")
        form_layout.addWidget(self.gunluk_tarih_input)
        
        gunluk_btn = QPushButton("📅 Günlük Rapor")
        gunluk_btn.clicked.connect(self.gunluk_rapor_goster)
        form_layout.addWidget(gunluk_btn)
        
        # Aylık Rapor
        form_layout.addWidget(QLabel("Yıl:"))
        self.yil_input = QSpinBox()
        self.yil_input.setValue(datetime.today().year)
        self.yil_input.setMinimum(2000)
        form_layout.addWidget(self.yil_input)
        
        form_layout.addWidget(QLabel("Ay:"))
        self.ay_input = QSpinBox()
        self.ay_input.setValue(datetime.today().month)
        self.ay_input.setMinimum(1)
        self.ay_input.setMaximum(12)
        form_layout.addWidget(self.ay_input)
        
        aylik_btn = QPushButton("📊 Aylık Rapor")
        aylik_btn.clicked.connect(self.aylik_rapor_goster)
        form_layout.addWidget(aylik_btn)
        
        layout.addLayout(form_layout)
        
        # Rapor Tablosu
        self.tablo = QTableWidget()
        self.tablo.setColumnCount(6)
        self.tablo.setHorizontalHeaderLabels(["Parça", "Kod", "Hareket", "Toplam Miktar", "Plaka/Sayı", "Not"])
        self.tablo.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.tablo)
        
        # Export Butonu
        export_btn = QPushButton("💾 Excel'e Aktar")
        export_btn.clicked.connect(self.excel_export)
        layout.addWidget(export_btn)
        
        self.setLayout(layout)
        self.rapor_tipi = None
        self.rapor_verisi = []
    
    def gunluk_rapor_goster(self):
        """Günlük raporu göster"""
        tarih_str = self.gunluk_tarih_input.text().strip()
        
        try:
            datetime.strptime(tarih_str, '%Y-%m-%d')
        except ValueError:
            QMessageBox.warning(self, "Hata", "Lütfen geçerli bir tarih girin (YYYY-MM-DD)")
            return
        
        rapor = StokHareketleri.gunluk_rapor(tarih_str)
        self.rapor_tipi = "Günlük"
        self.rapor_verisi = rapor
        self.rapor_goster(rapor, f"Günlük Rapor - {tarih_str}")
    
    def aylik_rapor_goster(self):
        """Aylık raporu göster"""
        yil = self.yil_input.value()
        ay = self.ay_input.value()
        
        rapor = StokHareketleri.aylik_rapor(yil, ay)
        self.rapor_tipi = "Aylık"
        self.rapor_verisi = rapor
        self.rapor_goster(rapor, f"Aylık Rapor - {yil}/{ay:02d}")
    
    def rapor_goster(self, rapor, baslik):
        """Raporu tablodan göster"""
        self.tablo.setWindowTitle(baslik)
        self.tablo.setRowCount(len(rapor))
        
        for row, kayit in enumerate(rapor):
            for col, veri in enumerate(kayit):
                self.tablo.setItem(row, col, QTableWidgetItem(str(veri)))
        
        if not rapor:
            QMessageBox.information(self, "Bilgi", f"{baslik} için kayıt bulunamadı.")
    
    def excel_export(self):
        """Raporu Excel'e aktar"""
        if not self.rapor_verisi:
            QMessageBox.warning(self, "Uyarı", "Lütfen önce bir rapor oluşturun!")
            return
        
        dosya_adi = f"rapor_{self.rapor_tipi}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        try:
            with open(dosya_adi, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                # Başlık
                if self.rapor_tipi == "Günlük":
                    writer.writerow(["Plaka", "Parça Adı", "Kod", "Hareket Tipi", "Toplam Miktar", "Hareket Sayısı"])
                else:
                    writer.writerow(["Parça Adı", "Kod", "Hareket Tipi", "Toplam Miktar", "Farklı Plaka Sayısı"])
                
                # Veriler
                for kayit in self.rapor_verisi:
                    writer.writerow(kayit)
            
            QMessageBox.information(self, "Başarı", f"Rapor başarıyla kaydedildi: {dosya_adi}")
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Excel export hatası: {str(e)}")
