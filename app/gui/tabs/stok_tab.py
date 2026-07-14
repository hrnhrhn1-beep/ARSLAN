#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTableWidget, QTableWidgetItem, QComboBox, QSpinBox,
    QMessageBox, QHeaderView
)
from app.database.models import Parca, StokHareketleri, Tedarikci
from datetime import datetime

class StokTab(QWidget):
    """Stok Yönetimi Tabı (Plaka ile)"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.parcalari_yukle()
    
    def init_ui(self):
        """UI Başlat"""
        layout = QVBoxLayout()
        
        # Stok Hareketi Ekleme Bölümü
        form_layout = QHBoxLayout()
        
        form_layout.addWidget(QLabel("Parça Seç:"))
        self.parca_combo = QComboBox()
        form_layout.addWidget(self.parca_combo)
        
        form_layout.addWidget(QLabel("Hareket Tipi:"))
        self.hareket_combo = QComboBox()
        self.hareket_combo.addItems(["Çıkışı", "Girişi"])
        form_layout.addWidget(self.hareket_combo)
        
        form_layout.addWidget(QLabel("Miktar:"))
        self.miktar_input = QSpinBox()
        self.miktar_input.setMinimum(1)
        self.miktar_input.setValue(1)
        form_layout.addWidget(self.miktar_input)
        
        form_layout.addWidget(QLabel("Plaka (Çıkışı için):"))
        self.plaka_input = QLineEdit()
        self.plaka_input.setPlaceholderText("34 ABC 123")
        form_layout.addWidget(self.plaka_input)
        
        kaydet_btn = QPushButton("💾 Kaydet")
        kaydet_btn.clicked.connect(self.stok_hareketi_ekle)
        form_layout.addWidget(kaydet_btn)
        
        layout.addLayout(form_layout)
        
        # Stok Hareketleri Listesi
        self.tablo = QTableWidget()
        self.tablo.setColumnCount(6)
        self.tablo.setHorizontalHeaderLabels(["Parça", "Kod", "Hareket", "Miktar", "Plaka", "Tarih"])
        self.tablo.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.tablo)
        
        self.setLayout(layout)
    
    def parcalari_yukle(self):
        """Parçaları combo box'a yükle"""
        parcalar = Parca.tum_parcalari_al()
        self.parca_combo.clear()
        
        for parca in parcalar:
            self.parca_combo.addItem(f"{parca[1]} ({parca[2]})", parca[0])
    
    def stok_hareketi_ekle(self):
        """Stok hareketi ekle"""
        parca_id = self.parca_combo.currentData()
        hareket_tipi = self.hareket_combo.currentText()
        miktar = self.miktar_input.value()
        plaka = self.plaka_input.text().strip() if hareket_tipi == "Çıkışı" else None
        
        if hareket_tipi == "Çıkışı" and not plaka:
            QMessageBox.warning(self, "Uyarı", "Çıkışı için plaka zorunludur!")
            return
        
        sonuc = StokHareketleri.ekle(parca_id, hareket_tipi, miktar, plaka)
        
        if sonuc['success']:
            QMessageBox.information(self, "Başarı", sonuc['message'])
            self.plaka_input.clear()
            self.miktar_input.setValue(1)
            self.stok_hareketlerini_yukle()
        else:
            QMessageBox.critical(self, "Hata", sonuc['message'])
    
    def stok_hareketlerini_yukle(self):
        """Son 100 stok hareketini yükle"""
        from app.database.db_init import get_connection
        
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT p.ad, p.kod, sh.hareket_tipi, sh.miktar, sh.plaka, sh.olusturma_tarihi
            FROM StokHareketleri sh
            JOIN Parcalar p ON sh.parca_id = p.id
            ORDER BY sh.olusturma_tarihi DESC
            LIMIT 100
        ''')
        hareketler = cursor.fetchall()
        conn.close()
        
        self.tablo.setRowCount(len(hareketler))
        for row, hareket in enumerate(hareketler):
            self.tablo.setItem(row, 0, QTableWidgetItem(hareket[0]))
            self.tablo.setItem(row, 1, QTableWidgetItem(hareket[1]))
            self.tablo.setItem(row, 2, QTableWidgetItem(hareket[2]))
            self.tablo.setItem(row, 3, QTableWidgetItem(str(hareket[3])))
            self.tablo.setItem(row, 4, QTableWidgetItem(hareket[4] or "-"))
            self.tablo.setItem(row, 5, QTableWidgetItem(str(hareket[5])))
