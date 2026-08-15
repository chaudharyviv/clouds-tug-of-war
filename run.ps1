# Quick Launch PowerShell Script for Cloud Bloodbath Streamlit UI

Write-Host "Checking python dependencies..." -ForegroundColor Cyan

# Install dependencies if requirements.txt is newer or packages missing
pip install -r requirements.txt

Write-Host "Launching Cloud Bloodbath Arena..." -ForegroundColor Green
streamlit run app.py
