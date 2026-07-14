#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTableWidget, QTableWidgetItem, QHeaderView
)
from app.database.models import Parca, OemKodu, RafKonumu

class AramaTab(QWidget):
    """Arama Tabı (Parça, Kod, OEM ile)"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """UI Başlat"""
        layout = QVBoxLayout()
        
        # Arama Bölümü
        form_layout = QHBoxLayout()
        
        form_layout.addWidget(QLabel("🔍 Ara (Parça Adı / Kod / OEM Kodu):"))
        self.arama_input = QLineEdit()
        self.arama_input.setPlaceholderText("Parça adı, kod veya OEM kodu yazın...")
        form_layout.addWidget(self.arama_input)
        
        ara_btn = QPushButton("🔎 Ara")
        ara_btn.clicked.connect(self.ara)
        form_layout.addWidget(ara_btn)
        
        layout.addLayout(form_layout)
        
        # Arama Sonuçları
        self.tablo = QTableWidget()
        self.tablo.setColumnCount(7)
        self.tablo.setHorizontalHeaderLabels(["ID", "Parça Adı", "Kod", "Kategori", "Stok", "OEM Kodları", "Raf Konumu"])
        self.tablo.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.tablo)
        
        self.setLayout(layout)
    
    def ara(self):
        """Arama yap"""
        arama_terimi = self.arama_input.text().strip()
        
        if not arama_terimi:
            return
        
        sonuclar = Parca.ara(arama_terimi)
        self.tablo.setRowCount(len(sonuclar))
        
        for row, parca in enumerate(sonuclar):
            parca_id = parca[0]
            
            self.tablo.setItem(row, 0, QTableWidgetItem(str(parca_id)))
            self.tablo.setItem(row, 1, QTableWidgetItem(parca[1]))
            self.tablo.setItem(row, 2, QTableWidgetItem(parca[2]))
            self.tablo.setItem(row, 3, QTableWidgetItem(parca[3] or "-"))
            self.tablo.setItem(row, 4, QTableWidgetItem(str(parca[4])))
            
            # OEM Kodlarını al
            oem_kodlari = OemKodu.parca_id_ile_al(parca_id)
            oem_str = ", ".join([kod[1] for kod in oem_kodlari]) if oem_kodlari else "-"
            self.tablo.setItem(row, 5, QTableWidgetItem(oem_str))
            
            # Raf Konumunu al
            raf = RafKonumu.al(parca_id)
            raf_str = f"{raf[0]}/{raf[1]}/{raf[2]}" if raf else "-"
            self.tablo.setItem(row, 6, QTableWidgetItem(raf_str))
