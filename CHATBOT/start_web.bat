@echo off
echo ================================================
echo   APS NATURALS CHATBOT - WEB UI LAUNCHER
echo ================================================
echo.
echo Checking if model is trained...
if not exist qa_model.h5 (
    echo Model not found! Training now...
    python train.py
    if errorlevel 1 (
        echo.
        echo Training failed! Please check the errors above.
        pause
        exit /b 1
    )
    echo.
)

echo Starting web server...
echo.
echo ================================================
echo   Opening browser at http://localhost:5000
echo ================================================
echo.
echo Press Ctrl+C to stop the server
echo.

start http://localhost:5000
python app.py

pause
