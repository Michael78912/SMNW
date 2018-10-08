@ECHO off
:: keeps %CD% the directory of this file, when run as admin %CD% beomes C:\Windows\System32
@SETLOCAL ENABLEEXTENSIONS
@CD /D "%~dp0"
:: check for admin rights
NET SESSION >NUL 2>&1
IF %ERRORLEVEL% == 0 GOTO A
GOTO END

:END
ECHO Administrative permissions required...
PAUSE
EXIT


:A
ECHO installation for stickmanranger
set /p "install=install? [Y\N]: "
IF %install% == y GOTO INSTALL
IF %install% == Y GOTO INSTALL
IF %install% == n EXIT
IF %install% == N EXIT
ECHO invalid choice.
PAUSE
GOTO A

:INSTALL
ECHO installing...
IF not exist "C:\Program Files\stickmanranger" md "C:\Program Files\stickmanranger"
XCOPY . "C:\Program Files\stickmanranger" /S
IF %ERRORLEVEL% == 0 (
	ECHO installation complete
	PAUSE
	EXIT
	) ELSE (
	ECHO something went wrong in the installation. please contact me and send the error message as well.
	ECHO for now, you can probably run the game from the current directory, or download the GUI installer.
	PAUSE
	EXIT
)
