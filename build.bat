pyinstaller --onefile --noconsole -i win32\megaphone.ico --hidden-import "PIL._tkinter_finder" src\airalarm.py || exit /b %ERRORLEVEL%
xcopy src\_internal dist\_internal\ /E || exit /b %ERRORLEVEL%
copy win32\root dist || exit /b %ERRORLEVEL%
copy LICENSE dist || exit /b %ERRORLEVEL%
set name=airalarm_windows_v%1
rename dist "%name%" || exit /b %ERRORLEVEL%
7z a -tzip "%name%.zip" "%name%" || exit /b %ERRORLEVEL%
rmdir /S /Q build || exit /b %ERRORLEVEL%
rmdir /S /Q "%name%" || exit /b %ERRORLEVEL%
