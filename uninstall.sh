#!/bin/bash

# Uninstall script for DoTranslate
INSTALL_DIR="/opt/translator"
DESKTOP_FILE="/usr/share/applications/translator.desktop"

# Check for root
if [ "$EUID" -ne 0 ]; then
    echo "Please run as root (use sudo)"
    exit 1
fi

echo "This will remove DoTranslate from your system, including $INSTALL_DIR and desktop shortcut."
read -p "Are you sure you want to continue? [y/N]: " confirm
if [[ ! $confirm =~ ^[Yy]$ ]]; then
    echo "Uninstall cancelled."
    exit 0
fi

# Remove installation directory
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "Removed $INSTALL_DIR."
else
    echo "$INSTALL_DIR not found."
fi

# Remove desktop shortcut
if [ -f "$DESKTOP_FILE" ]; then
    rm "$DESKTOP_FILE"
    echo "Removed desktop shortcut."
else
    echo "$DESKTOP_FILE not found."
fi

echo "DoTranslate has been uninstalled." 