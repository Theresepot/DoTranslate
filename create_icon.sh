#!/bin/bash

# Check if ImageMagick is installed
if ! command -v convert &> /dev/null; then
    echo "Installing ImageMagick..."
    sudo apt-get update
    sudo apt-get install -y imagemagick
fi

# Create a temporary directory
TEMP_DIR=$(mktemp -d)

# Convert the icon to a round shape with transparent background
convert icon.png \
    -resize 512x512 \
    -background none \
    -gravity center \
    -extent 512x512 \
    \( +clone -alpha extract \
        -draw 'fill black polygon 0,0 0,512 512,512 512,0 fill white circle 256,256 256,0' \
        \( +clone -flip \) -compose Multiply -composite \
        \( +clone -flop \) -compose Multiply -composite \
    \) -alpha off -compose CopyOpacity -composite \
    -trim \
    icon_round.png

# Create different sizes for various uses
for size in 16 32 48 64 128 256 512; do
    convert icon_round.png -resize ${size}x${size} icon_${size}.png
done

# Create an ICO file with multiple sizes
convert icon_16.png icon_32.png icon_48.png icon_64.png icon_128.png icon_256.png icon_512.png icon.ico

echo "Icons created successfully!"
echo "You can find the new icons in the current directory:"
echo "- icon_round.png (main round icon)"
echo "- icon.ico (Windows icon with multiple sizes)"
echo "- Various size-specific PNG files (icon_16.png, icon_32.png, etc.)" 