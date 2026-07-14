#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox,
    QPushButton, QTableWidget, QTableWidgetItem, QSpinBox, QMessageBox, QHeaderView
)
from PyQt6.QtCore import Qt
from app.database.models import Parca, RafKonumu

class ParcaTab(QWidget):
    """Parça Yönetimi Tabı"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.parcalari_yükle()
    
    def init_ui(self):
        """UI Başlat"""
        layout = QVBoxLayout()
        
        # Parça Ekleme Bölümü
        form_layout = QHBoxLayout()
        
        form_layout.addWidget(QLabel("Parça Adı:"))
        self.ad_input = QLineEdit()
        form_layout.addWidget(self.ad_input)
        
        form_layout.addWidget(QLabel("Parça Kodu:"))
        self.kod_input = QLineEdit()
        form_layout.addWidget(self.kod_input)
        
        form_layout.addWidget(QLabel("Kategori:"))
        self.kategori_input = QLineEdit()
        form_layout.addWidget(self.kategori_input)
        
        form_layout.addWidget(QLabel("Min. Stok:"))
        self.min_stok_input = QSpinBox()
        self.min_stok_input.setValue(10)
        form_layout.addWidget(self.min_stok_input)
        
        ekle_btn = QPushButton("➕ Parça Ekle")
        ekle_btn.clicked.connect(self.parca_ekle)
        form_layout.addWidget(ekle_btn)
        
        layout.addLayout(form_layout)
        
        # Parça Listesi
        self.tablo = QTableWidget()
        self.tablo.setColumnCount(6)
        self.tablo.setHorizontalHeaderLabels(["ID", "Parça Adı", "Kod", "Kategori", "Stok", "İşlem"])
        self.tablo.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.tablo)
        
        self.setLayout(layout)
    
    def parca_ekle(self):
        """Parça ekle"""
        ad = self.ad_input.text().strip()
        kod = self.kod_input.text().strip()
        kategori = self.kategori_input.text().strip()
        min_stok = self.min_stok_input.value()
        
        if not ad or not kod:
            QMessageBox.warning(self, "Uyarı", "Parça adı ve kodu zorunludur!")
            return
        
        sonuc = Parca.ekle(ad, kod, kategori, min_stok=min_stok)
        
        if sonuc['success']:
            QMessageBox.information(self, "Başarı", sonuc['message'])
            self.ad_input.clear()
            self.kod_input.clear()
            self.kategori_input.clear()
            self.parcalari_yükle()
        else:
            QMessageBox.critical(self, "Hata", sonuc['message'])
    
    def parcalari_yükle(self):
        """Parçaları tablodan yükle"""
        parcalar = Parca.tum_parcalari_al()
        self.tablo.setRowCount(len(parcalar))
        
        for row, parca in enumerate(parcalar):
            self.tablo.setItem(row, 0, QTableWidgetItem(str(parca[0])))
            self.tablo.setItem(row, 1, QTableWidgetItem(parca[1]))
            self.tablo.setItem(row, 2, QTableWidgetItem(parca[2]))
            self.tablo.setItem(row, 3, QTableWidgetItem(parca[3] or "-"))
            self.tablo.setItem(row, 4, QTableWidgetItem(str(parca[4])))
            
            sil_btn = QPushButton("🗑️ Sil")
            sil_btn.clicked.connect(lambda checked, p_id=parca[0]: self.parca_sil(p_id))
            self.tablo.setCellWidget(row, 5, sil_btn)
    
    def parca_sil(self, parca_id):
        """Parça sil"""
        reply = QMessageBox.question(self, "Onay", "Bu parçayı silmek istediğinizden emin misiniz?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            sonuc = Parca.sil(parca_id)
            if sonuc['success']:
                QMessageBox.information(self, "Başarı", sonuc['message'])
                self.parcalari_yükle()
            else:
                QMessageBox.critical(self, "Hata", sonuc['message'])
