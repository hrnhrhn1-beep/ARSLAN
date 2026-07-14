#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from PyQt6.QtWidgets import QApplication
from app.gui.main_window import MainWindow
from app.database.db_init import init_database

def main():
    # Veritabanını başlat
    init_database()
    
    # Uygulamayı başlat
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
