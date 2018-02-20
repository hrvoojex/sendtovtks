@echo off

REM How it works
REM https://stackoverflow.com/questions/9232308/how-do-i-minimize-the-command-prompt-from-my-bat-file
REM When the script is being executed IS_MINIMIZED is not defined (if not DEFINED IS_MINIMIZED) so:
REM
REM IS_MINIMIZED is set to 1: set IS_MINIMIZED=1.
REM Script starts a copy of itself using start command  && start "" /min "%~dpnx0" %* where:
REM
REM "" - empty title for the window.
REM /min - switch to run minimized.
REM "%~dpnx0" - full path to your script.
REM %* - passing through all your script's parameters.
REM Then initial script finishes its work: && exit.

if not DEFINED IS_MINIMIZED set IS_MINIMIZED=1 && start "http.server" /min "%~dpnx0" %* && exit
cd C:\web_pdo
C:\Python34\python -m http.server
exit
