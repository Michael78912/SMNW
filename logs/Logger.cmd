@ECHO OFF
@SETLOCAL ENABLEEXTENSIONS
@CD /D "%~dp0"

SET FILE=stickmanranger.log


SET /P "INPUT=>> "
ECHO %DATE% %TIME% %INPUT% >> %FILE%
BASH -c "bash upload.sh"
ECHO remove directory?
RMDIR /S >nul
