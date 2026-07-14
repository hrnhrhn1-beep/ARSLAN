#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTableWidget, QTableWidgetItem, QComboBox, QMessageBox, QHeaderView
)
from app.database.models import Parca, OemKodu

class OemTab(QWidget):
    """OEM Kodları Tabı (Eşdeğer Kodlar)"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.parcalari_yukle()
    
    def init_ui(self):
        """UI Başlat"""
        layout = QVBoxLayout()
        
        # OEM Kodu Ekleme Bölümü
        form_layout = QHBoxLayout()
        
        form_layout.addWidget(QLabel("Parça Seç:"))
        self.parca_combo = QComboBox()
        form_layout.addWidget(self.parca_combo)
        
        form_layout.addWidget(QLabel("OEM Kodu:"))
        self.oem_kod_input = QLineEdit()
        form_layout.addWidget(self.oem_kod_input)
        
        form_layout.addWidget(QLabel("Üretici:"))
        self.uretici_input = QLineEdit()
        form_layout.addWidget(self.uretici_input)
        
        ekle_btn = QPushButton("➕ OEM Kodu Ekle")
        ekle_btn.clicked.connect(self.oem_ekle)
        form_layout.addWidget(ekle_btn)
        
        layout.addLayout(form_layout)
        
        # OEM Kodları Listesi
        self.tablo = QTableWidget()
        self.tablo.setColumnCount(5)
        self.tablo.setHorizontalHeaderLabels(["Parça ID", "Parça Adı", "OEM Kodu", "Üretici", "Açıklama"])
        self.tablo.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.tablo)
        
        self.setLayout(layout)
    
    def parcalari_yukle(self):
        """Parçaları combo box'a yükle"""
        parcalar = Parca.tum_parcalari_al()
        self.parca_combo.clear()
        
        for parca in parcalar:
            self.parca_combo.addItem(f"{parca[1]} ({parca[2]})", parca[0])
    
    def oem_ekle(self):
        """OEM kodu ekle"""
        parca_id = self.parca_combo.currentData()
        oem_kod = self.oem_kod_input.text().strip()
        uretici = self.uretici_input.text().strip()
        
        if not oem_kod:
            QMessageBox.warning(self, "Uyarı", "OEM kodu zorunludur!")
            return
        
        sonuc = OemKodu.ekle(parca_id, oem_kod, uretici)
        
        if sonuc['success']:
            QMessageBox.information(self, "Başarı", sonuc['message'])
            self.oem_kod_input.clear()
            self.uretici_input.clear()
            self.oem_kodlarini_yukle()
        else:
            QMessageBox.critical(self, "Hata", sonuc['message'])
    
    def oem_kodlarini_yukle(self):
        """OEM kodlarını tablodan yükle"""
        from app.database.db_init import get_connection
        
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT p.id, p.ad, o.oem_kod, o.uretici, o.aciklama
            FROM OemKodlari o
            JOIN Parcalar p ON o.parca_id = p.id
            ORDER BY p.ad, o.oem_kod
        ''')
        kodlar = cursor.fetchall()
        conn.close()
        
        self.tablo.setRowCount(len(kodlar))
        for row, kod in enumerate(kodlar):
            self.tablo.setItem(row, 0, QTableWidgetItem(str(kod[0])))
            self.tablo.setItem(row, 1, QTableWidgetItem(kod[1]))
            self.tablo.setItem(row, 2, QTableWidgetItem(kod[2]))
            self.tablo.setItem(row, 3, QTableWidgetItem(kod[3] or "-"))
            self.tablo.setItem(row, 4, QTableWidgetItem(kod[4] or "-"))
