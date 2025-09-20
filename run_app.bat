@echo off
echo ========================================
echo    UNG DUNG NHAN DIEN KHUON MAT
echo ========================================
echo.

:menu
echo Chon ung dung ban muon chay:
echo.
echo 1. Demo nhanh (Kiem tra he thong)
echo 2. Ung dung Streamlit (Giao dien web)
echo 3. Ung dung Console (OpenCV)
echo 4. Cai dat thu vien
echo 5. Thoat
echo.
set /p choice="Nhap lua chon (1-5): "

if "%choice%"=="1" goto demo
if "%choice%"=="2" goto streamlit
if "%choice%"=="3" goto console
if "%choice%"=="4" goto install
if "%choice%"=="5" goto exit
goto menu

:demo
echo.
echo Chay demo nhanh...
python demo.py
pause
goto menu

:streamlit
echo.
echo Khoi dong ung dung Streamlit...
echo Trinh duyet se tu dong mo tai http://localhost:8501
streamlit run simple_face_age_app.py
pause
goto menu

:console
echo.
echo Khoi dong ung dung Console...
python opencv_face_age.py
pause
goto menu

:install
echo.
echo Cai dat cac thu vien can thiet...
pip install -r requirements.txt
echo.
echo Hoan thanh cai dat!
pause
goto menu

:exit
echo.
echo Tam biet!
pause
exit
