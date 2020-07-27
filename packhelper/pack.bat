@echo off
echo Packing ./assets into .\packed.pak
echo This may take a long time.
start /wait /min ..\win32\asset_packer.exe .\assets .\packed.pak
erase .\assets
echo Done.
pause