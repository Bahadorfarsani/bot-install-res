#!/bin/bash
set -e  # Script bricht bei Fehler ab

echo "🔧 Starte Installation..."

# Update Paketliste
sudo apt update
sudo apt install pkg-config -y
sudo apt install python3-dev default-libmysqlclient-dev build-essential -y
sudo apt install python3-pip -y
pip install pandas==1.5.3
pip install numpy
pip install pip==21.3.1
pip install openpyxl
pip install bcrypt==4.0.1
pip install greenlet==2.0.2
pip install protobuf==3.20.3
pip install pyaes==1.6.1
pip install Pyrogram==2.0.99
pip install pyromod==1.5
pip install PySocks==1.7.1
pip install SQLAlchemy==2.0.4
pip install TgCrypto==1.2.5
pip install typing_extensions==4.5.0
pip install mysql-connector-python
pip install mysqlclient


# Python-Abhängigkeiten installieren
if [ -f requirements.txt ]; then
    echo "📦 Installiere Python-Abhängigkeiten..."
    pip3 install -r requirements.txt
fi

# Node-Abhängigkeiten installieren (optional)
if [ -f package.json ]; then
    echo "📦 Installiere Node.js-Abhängigkeiten..."
    npm install
fi

# Build-Prozess (optional)
if [ -f Makefile ]; then
    echo "⚙️  Führe make aus..."
    make
fi

# Projekt starten (optional)
echo "✅ Installation abgeschlossen."