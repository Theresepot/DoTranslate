# Translation App

A simple translation application that supports multiple translation engines (Google, DuckDuckGo, Yandex, DeepL).

## Building the Application

1. Make sure you have Python 3 installed on your system
2. Run the build script:
   ```bash
   chmod +x build.sh
   ./build.sh
   ```
3. The executable will be created in the `dist/` directory

## Creating Distribution Package

1. Build the application as described above
2. Create the icon:
   ```bash
   chmod +x create_icon.sh
   ./create_icon.sh
   ```
3. Copy these files to your distribution package:
   - `dist/translator` (the executable)
   - `install.sh` (installation script)
   - `icon.png` (application icon)

## Installing on Another System

1. Copy the distribution package to the target system
2. Make the installation script executable:
   ```bash
   chmod +x install.sh
   ```
3. Run the installation script as root:
   ```bash
   sudo ./install.sh
   ```

The application will be installed in `/opt/translator` and will be available in your applications menu.

## System Requirements

- Debian-based Linux distribution
- Required system libraries (will be installed by the installation script)

## Features

- Multiple translation engines (Google, DuckDuckGo, Yandex, DeepL)
- Language selection with swap functionality (English, Spanish, French, German, Russian, Chinese, Italian)
- Copy translation to clipboard
- Keyboard shortcuts (Ctrl+C to copy, Ctrl+V to paste)
- Support for multiple languages including Chinese characters 