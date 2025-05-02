# DoTranslate

A powerful, privacy-friendly desktop translation app with offline OCR and file support, powered by the LibreNode translation API.

## Features

- **Multiple Translation Engines**: Google, DuckDuckGo, Yandex, DeepL (via https://translate.librenode.com/)
- **Offline OCR**: Extract text from images (PNG, JPG, JPEG) and PDFs using Tesseract and PyPDF2, all locally
- **Privacy First**: Text extraction from files is done 100% offline; only the text you choose to translate is sent to the translation API
- **Modern Desktop UI**: Built with Kivy for a clean, responsive, and cross-platform experience
- **Language Support**: English, Spanish, French, German, Russian, Chinese, Italian
- **Easy Language Swapping**: One-click swap between source and target languages
- **Clipboard Integration**: Copy/paste support for both input and translated text
- **File Chooser**: Select images or PDFs for instant text extraction
- **Custom Icons**: Beautiful app icons included

## Installation

### 1. Clone the repository
```bash
git clone <your-github-repo-url>
cd DoTranslate
```

### 2. Install system dependencies
- **Tesseract OCR** (for image text extraction):
  ```bash
  sudo apt-get update
  sudo apt-get install -y tesseract-ocr tesseract-ocr-chi-sim tesseract-ocr-chi-tra tesseract-ocr-rus tesseract-ocr-deu tesseract-ocr-fra tesseract-ocr-spa tesseract-ocr-ita
  ```
- **Python 3.8+**

### 3. Create and activate a virtual environment (recommended)
```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 5. Run the app
```bash
python translator.py
```

### 6. (Optional) Build a standalone executable
```bash
./build_translator.sh
cd dist
./install.sh
./translator
```

## Why Use DoTranslate?
- **Works with images and PDFs**: Extract text from files locally, even when offline
- **No vendor lock-in**: Choose your preferred translation engine
- **Privacy-respecting**: Only the text you want to translate is sent to the API; file contents never leave your computer
- **Cross-platform**: Works on Linux, Windows, and macOS (with minor adjustments)
- **Open source**: Free to use, modify, and share

## Screenshots
*(Add screenshots here if you wish)*

## Contributing
Pull requests and suggestions are welcome!

## License
MIT License

---

### Credits
- [LibreNode Translate API](https://translate.librenode.com/)
- [Kivy](https://kivy.org/)
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- [PyPDF2](https://pypdf2.readthedocs.io/)

---

**DoTranslate**: The easiest way to translate anything, from anywhere, with privacy and power. 