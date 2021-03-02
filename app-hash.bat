@echo off
:: write a sha-256 hash of the scripts in the app directory (using certutil as I work on windows)
:: Created: 3 Mar 2021

set startdir=%CD%
set output="SHA256SUMS.txt"

echo Writing hash.....
echo.
certutil -hashfile .\app\file_hash.py SHA256 > %output%
type %output%
echo.
echo done.