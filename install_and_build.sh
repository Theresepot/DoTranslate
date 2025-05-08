#!/bin/bash

# This script builds and installs dotranslate as a standalone app with menu integration.
# Run as: sudo ./install_and_build.sh

set -e

# Check for root
if [ "$EUID" -ne 0 ]; then
    echo "Please run as root (use sudo)"
    exit 1
fi

# Build the app
./build_translator.sh

# Install location
INSTALL_DIR="/opt/translator"

# Remove previous install if exists
rm -rf "$INSTALL_DIR"
mkdir -p "$INSTALL_DIR"

# Copy built files
cp -r dist/* "$INSTALL_DIR/"

# Copy icon (if not already in dist)
if [ ! -f "$INSTALL_DIR/icon.png" ] && [ -f "icon_512.png" ]; then
    cp icon_512.png "$INSTALL_DIR/icon.png"
fi

# Create .desktop entry
cat > /usr/share/applications/translator.desktop << EOF
[Desktop Entry]
Name=DoTranslate
Comment=Multi-engine translation application
Exec=$INSTALL_DIR/translator
Icon=$INSTALL_DIR/icon.png
Terminal=false
Type=Application
Categories=Utility;
EOF

# Set permissions
chmod +x "$INSTALL_DIR/translator"
chown -R root:root "$INSTALL_DIR"

# Notify user
if [ -f "$INSTALL_DIR/translator" ]; then
    echo "Installation complete! You can find DoTranslate in your applications menu or run: $INSTALL_DIR/translator"
else
    echo "Error: $INSTALL_DIR/translator not found! Build or install may have failed."
fi 