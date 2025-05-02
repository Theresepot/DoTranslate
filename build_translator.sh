#!/bin/bash

# Use the correct virtual environment
source /home/user/apkbuild/apk/kivy_venv/bin/activate

# Clean up previous builds
rm -rf build/ dist/ __pycache__/ *.spec

# Install required packages
pip install kivy requests pytesseract Pillow PyPDF2 pyinstaller

# Create the spec file
cat > translator.spec << 'EOL'
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# Add Tesseract data files
tesseract_data = [
    ('/usr/share/tesseract-ocr/5/tessdata/eng.traineddata', 'tessdata'),
    ('/usr/share/tesseract-ocr/5/tessdata/chi_sim.traineddata', 'tessdata'),
    ('/usr/share/tesseract-ocr/5/tessdata/chi_tra.traineddata', 'tessdata'),
    ('/usr/share/tesseract-ocr/5/tessdata/rus.traineddata', 'tessdata'),
    ('/usr/share/tesseract-ocr/5/tessdata/deu.traineddata', 'tessdata'),
    ('/usr/share/tesseract-ocr/5/tessdata/fra.traineddata', 'tessdata'),
    ('/usr/share/tesseract-ocr/5/tessdata/spa.traineddata', 'tessdata'),
    ('/usr/share/tesseract-ocr/5/tessdata/ita.traineddata', 'tessdata'),
]

a = Analysis(
    ['translator.py'],
    pathex=[],
    binaries=[],
    datas=tesseract_data,
    hiddenimports=['PIL._tkinter_finder'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='translator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
EOL

# Build the executable
pyinstaller --clean --distpath dist/ translator.spec

# Create README file
cat > dist/README.txt << 'EOL'
Translator Application

This application requires Tesseract OCR to be installed on your system.
On Linux, you can install it using:
sudo apt-get install tesseract-ocr

Required Tesseract language packs:
sudo apt-get install tesseract-ocr-chi-sim tesseract-ocr-chi-tra tesseract-ocr-rus tesseract-ocr-deu tesseract-ocr-fra tesseract-ocr-spa tesseract-ocr-ita

Usage:
1. Make sure Tesseract OCR is installed (run install.sh)
2. Run the translator executable: ./translator
3. Use the "Select Image/PDF" button to choose a file
4. The extracted text will appear in the input area
5. Select source and target languages
6. Choose a translation engine
7. Click "Translate" to get the translation

Supported file formats:
- Images: PNG, JPG, JPEG
- PDF files

Translation engines:
- Google
- DuckDuckGo
- Yandex
- DeepL
EOL

# Create installation script
cat > dist/install.sh << 'EOL'
#!/bin/bash

# Check if Tesseract OCR is installed
if ! command -v tesseract &> /dev/null; then
    echo "Installing Tesseract OCR and language packs..."
    sudo apt-get update
    sudo apt-get install -y tesseract-ocr tesseract-ocr-chi-sim tesseract-ocr-chi-tra \
        tesseract-ocr-rus tesseract-ocr-deu tesseract-ocr-fra tesseract-ocr-spa tesseract-ocr-ita
fi

# Make the translator executable
chmod +x translator

echo "Installation complete! You can run the translator by executing ./translator"
EOL

# Make the installation script executable
chmod +x dist/install.sh

# Clean up build files
rm -rf build/ *.spec

echo "Build complete! All files are in the dist/ directory"
echo "To install and run:"
echo "1. cd dist"
echo "2. ./install.sh"
echo "3. ./translator" 