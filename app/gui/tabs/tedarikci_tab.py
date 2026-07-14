#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QHeaderView
)
from app.database.models import Tedarikci

class TedarikciTab(QWidget):
    """Tedarikçi Yönetimi Tabı"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.tedarikciyi_yukle()
    
    def init_ui(self):
        """UI Başlat"""
        layout = QVBoxLayout()
        
        # Tedarikçi Ekleme Bölümü
        form_layout = QHBoxLayout()
        
        form_layout.addWidget(QLabel("Firma Adı:"))
        self.ad_input = QLineEdit()
        form_layout.addWidget(self.ad_input)
        
        form_layout.addWidget(QLabel("Telefon:"))
        self.telefon_input = QLineEdit()
        form_layout.addWidget(self.telefon_input)
        
        form_layout.addWidget(QLabel("Email:"))
        self.email_input = QLineEdit()
        form_layout.addWidget(self.email_input)
        
        form_layout.addWidget(QLabel("Şehir:"))
        self.sehir_input = QLineEdit()
        form_layout.addWidget(self.sehir_input)
        
        ekle_btn = QPushButton("➕ Tedarikçi Ekle")
        ekle_btn.clicked.connect(self.tedarikci_ekle)
        form_layout.addWidget(ekle_btn)
        
        layout.addLayout(form_layout)
        
        # Tedarikçi Listesi
        self.tablo = QTableWidget()
        self.tablo.setColumnCount(5)
        self.tablo.setHorizontalHeaderLabels(["ID", "Firma Adı", "Telefon", "Email", "Şehir"])
        self.tablo.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.tablo)
        
        self.setLayout(layout)
    
    def tedarikci_ekle(self):
        """Tedarikçi ekle"""
        ad = self.ad_input.text().strip()
        telefon = self.telefon_input.text().strip()
        email = self.email_input.text().strip()
        sehir = self.sehir_input.text().strip()
        
        if not ad:
            QMessageBox.warning(self, "Uyarı", "Firma adı zorunludur!")
            return
        
        sonuc = Tedarikci.ekle(ad, telefon, email, sehir=sehir)
        
        if sonuc['success']:
            QMessageBox.information(self, "Başarı", sonuc['message'])
            self.ad_input.clear()
            self.telefon_input.clear()
            self.email_input.clear()
            self.sehir_input.clear()
            self.tedarikciyi_yukle()
        else:
            QMessageBox.critical(self, "Hata", sonuc['message'])
    
    def tedarikciyi_yukle(self):
        """Tedarikçileri tablodan yükle"""
        tedarikciler = Tedarikci.tum_tedarikcileri_al()
        self.tablo.setRowCount(len(tedarikciler))
        
        for row, ted in enumerate(tedarikciler):
            self.tablo.setItem(row, 0, QTableWidgetItem(str(ted[0])))
            self.tablo.setItem(row, 1, QTableWidgetItem(ted[1]))
            self.tablo.setItem(row, 2, QTableWidgetItem(ted[2] or "-"))
            self.tablo.setItem(row, 3, QTableWidgetItem(ted[3] or "-"))
            self.tablo.setItem(row, 4, QTableWidgetItem(ted[4] or "-"))
