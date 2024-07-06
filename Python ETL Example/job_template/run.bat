rem this script initally doesn some calculations on order to generate the month key
rem The month key is used in the log filename (momnthy log files for easier cleanup)
rem Also, it passes vars about the python path, current dir, and run mode
rem When python is called we use -u in order to send the unbuffered stdout directly to the log file
rem >> means direct stdout to file and 2>&1 is for writing both stdout and errors in the file.

@echo off
for /f "skip=1" %%x in ('wmic os get localdatetime') do if not defined MyDate set MyDate=%%x
for /f %%x in ('wmic path win32_localtime get /format:list ^| findstr "="') do set %%x
set fmonth=00%Month%
set fday=00%Day%
set monthvar=%Year%%fmonth:~-2%
set pypath=%BI_PYTHON1%
set curdir=%~dp0
set run_mode=auto
%pypath%\python.exe -u %curdir%main.py "%run_mode%" >> data\%monthvar%.log 2>&1
