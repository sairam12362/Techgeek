@echo off
echo 🚀 Uploading VidyāMitra AI Agent to GitHub...
echo.

echo 📍 Repository: https://github.com/sairam12362/Techgeek
echo.

cd /d "c:\Users\K Sai Ram Yadav\Downloads\Gen Ai Hackhton"

echo 🔧 Configuring Git...
"C:\Program Files\Git\bin\git.exe" config --global user.name "sairam12362"
"C:\Program Files\Git\bin\git.exe" config --global user.email "sairam12362@github.com"

echo 📁 Initializing repository...
"C:\Program Files\Git\bin\git.exe" init

echo 🔗 Adding remote repository...
"C:\Program Files\Git\bin\git.exe" remote add origin https://github.com/sairam12362/Techgeek.git

echo 📋 Adding all files...
"C:\Program Files\Git\bin\git.exe" add .

echo 💾 Committing changes...
"C:\Program Files\Git\bin\git.exe" commit -m "Initial commit: VidyāMitra AI Agent - Complete Resume Analysis Platform"

echo 🚀 Pushing to GitHub...
"C:\Program Files\Git\bin\git.exe" push -u origin main

echo.
echo ✅ Upload complete!
echo 🌟 Your project is now live at: https://github.com/sairam12362/Techgeek
echo.
pause
