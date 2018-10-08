@echo off
if EXIST dist goto prompt

:main
	echo Hi! please do not close this console, until it says it is done.    :)
	set /p "fi=file to compile: "
	set/p "cho=console or windows: "
	if %cho%==c set %cho%=console
	if %cho%==w set %cho%=windows
	if %cho%==con set %cho%=console
	if %cho%==win set %cho%=windows
	echo from distutils.core import setup >> setup.tmp
	echo import py2exe >> setup.tmp
	echo setup(%cho%=['%fi%']) >> setup.tmp

python setup.tmp py2exe

del setup.tmp
echo process terminated.
pause
exit

:prompt
	echo the folder dist is not empty. remove? (Y/N)
	set /p "c=}  "
	if %c% == Y rmdir /s /q dist
	if %c% == y rmdir /s /q dist
	if %c% == N exit
	if %c% == n exit
	goto main