@echo off
:: compare sha-256 hash of the scripts in the app directory (using certutil as I work on windows)
:: Created: 3 Mar 2021

set startdir=%CD%
set input="SHA256SUMS.txt"
set local="SHA256SUMS-local.txt"

IF EXIST %local% (
  echo Deleting the existing local hash
  del %local%
)

echo Creating local hash.....
echo.
certutil -hashfile .\app\file_hash.py SHA256 > %local%
type %local%
echo.
echo done.

echo Checking the local hash matches the one provided

fc %local% %input% > nul
if errorlevel 1 goto error

:next
echo Hash matched
pause
goto end

:error
echo ======================================
echo Error: Hash check failed
echo ======================================
pause

:end