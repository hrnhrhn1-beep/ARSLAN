#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QTabWidget, QPushButton, QLabel, QMessageBox
)
from PyQt6.QtCore import Qt
from app.gui.tabs.parca_tab import ParcaTab
from app.gui.tabs.oem_tab import OemTab
from app.gui.tabs.tedarikci_tab import TedarikciTab
from app.gui.tabs.stok_tab import StokTab
from app.gui.tabs.rapor_tab import RaporTab
from app.gui.tabs.arama_tab import AramaTab

class MainWindow(QMainWindow):
    """Ana pencere"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ARSLAN - Oto Yedek Parça Yönetim Sistemi v1.0")
        self.setGeometry(100, 100, 1200, 700)
        self.setStyleSheet(self.get_stylesheet())
        
        # Ana widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout
        layout = QVBoxLayout(central_widget)
        
        # Tab Widget
        tabs = QTabWidget()
        
        # Tabları ekle
        tabs.addTab(AramaTab(), "🔍 Arama")
        tabs.addTab(ParcaTab(), "📦 Parçalar")
        tabs.addTab(OemTab(), "🔗 OEM Kodları")
        tabs.addTab(TedarikciTab(), "🏢 Tedarikçiler")
        tabs.addTab(StokTab(), "📊 Stok Yönetimi")
        tabs.addTab(RaporTab(), "📈 Raporlar")
        
        layout.addWidget(tabs)
        
        # Bilgi barı
        info_label = QLabel("✅ Sistem hazır | Veritabanı: arslan.db")
        layout.addWidget(info_label)
    
    def get_stylesheet(self):
        """Uygulama stilini döndür"""
        return """
            QMainWindow {
                background-color: #f0f0f0;
            }
            QTabWidget::pane {
                border: 1px solid #cccccc;
            }
            QTabBar::tab {
                background-color: #e0e0e0;
                padding: 8px 20px;
                border: 1px solid #999;
            }
            QTabBar::tab:selected {
                background-color: #4CAF50;
                color: white;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 8px 16px;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
            QLineEdit, QTextEdit {
                padding: 6px;
                border: 1px solid #999;
                border-radius: 4px;
                background-color: white;
            }
            QTableWidget {
                border: 1px solid #ddd;
                background-color: white;
            }
            QTableWidget::item:selected {
                background-color: #4CAF50;
                color: white;
            }
            QLabel {
                color: #333;
            }
        """
