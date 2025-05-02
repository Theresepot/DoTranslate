#!/bin/bash

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "Please run as root (use sudo)"
    exit 1
fi

# Create installation directory
INSTALL_DIR="/opt/translator"
mkdir -p $INSTALL_DIR

# Install required system libraries
apt-get update
apt-get install -y \
    libsdl2-2.0-0 \
    libsdl2-image-2.0-0 \
    libsdl2-mixer-2.0-0 \
    libsdl2-ttf-2.0-0 \
    python3-pip \
    python3-venv

# Create and activate virtual environment
python3 -m venv $INSTALL_DIR/venv
source $INSTALL_DIR/venv/bin/activate

# Install Kivy and other dependencies
pip install kivy==2.2.1
pip install requests

# Copy the entire dist directory
cp -r dist/* $INSTALL_DIR/

# Create desktop shortcut
cat > /usr/share/applications/translator.desktop << EOF
[Desktop Entry]
Name=Translation App
Comment=Multi-engine translation application
Exec=$INSTALL_DIR/translator
Icon=$INSTALL_DIR/icon.png
Terminal=false
Type=Application
Categories=Utility;
EOF

# Set permissions
if [ -f "$INSTALL_DIR/translator" ]; then
    chmod +x $INSTALL_DIR/translator
else
    echo "Error: $INSTALL_DIR/translator not found! Installation may have failed."
fi
chown -R root:root $INSTALL_DIR

echo "Installation complete! You can find the application in your applications menu."
echo "You can also run it directly from: $INSTALL_DIR/translator" 