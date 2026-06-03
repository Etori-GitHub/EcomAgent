@echo off
echo 启动 Chrome (远程调试端口 9222)...
echo 请在此 Chrome 中登录 TikTok Shop，然后运行 tiktok_browser.py
echo.
start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="%USERPROFILE%\.openclaw\chrome-tiktok"
echo Chrome 已启动！
echo.
echo 现在请在这个 Chrome 中打开 TikTok Shop 并登录。
echo 登录完成后，按任意键继续运行自动化脚本...
pause > nul
python "%~dp0tiktok_browser.py"
