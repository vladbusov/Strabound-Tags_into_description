@echo off
echo Unpacking .\packed.pak into .\
echo This may take a long time.
start /wait /min ..\win32\asset_unpacker.exe .\packed.pak .\assets
erase .\packed.pak
echo Done.
pause