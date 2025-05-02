@echo off
SET TESS_PATH="C:\Program Files\Tesseract-OCR"
REM If you installed Tesseract elsewhere, change the path above

REM Add to system PATH
setx /M PATH "%PATH%;%TESS_PATH%"
echo Tesseract path added to system PATH. You may need to restart your terminal or computer.
pause 