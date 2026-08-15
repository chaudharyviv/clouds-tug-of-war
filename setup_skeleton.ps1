# Setup Script for Cloud Bloodbath folder structure

# 1. Define folder paths to create
$directories = @(
    "src",
    "src/agents",
    "src/models",
    "src/services",
    "src/static",
    "src/ui"
)

# 2. Define empty files to initialize
$files = @(
    ".env.example",
    "requirements.txt",
    "app.py",
    "src/__init__.py",
    "src/config.py",
    "src/agents/__init__.py",
    "src/agents/base.py",
    "src/agents/scout.py",
    "src/agents/weaver.py",
    "src/agents/engine.py",
    "src/agents/chronicler.py",
    "src/models/__init__.py",
    "src/models/combatant.py",
    "src/models/battlefield.py",
    "src/models/battle.py",
    "src/services/__init__.py",
    "src/services/search.py",
    "src/services/llm.py",
    "src/services/orchestrator.py",
    "src/services/codex.py",
    "src/static/style.css",
    "src/ui/__init__.py",
    "src/ui/components.py",
    "src/ui/views.py"
)

Write-Host "Starting Cloud Bloodbath workspace scaffolding..." -ForegroundColor Cyan

# 3. Create Directories
foreach ($dir in $directories) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "  [+] Created Directory: $dir" -ForegroundColor Green
    } else {
        Write-Host "  [-] Directory already exists: $dir" -ForegroundColor Yellow
    }
}

# 4. Create Files
foreach ($file in $files) {
    if (-not (Test-Path $file)) {
        New-Item -ItemType File -Path $file -Force | Out-Null
        Write-Host "  [+] Created File: $file" -ForegroundColor Green
    } else {
        Write-Host "  [-] File already exists: $file" -ForegroundColor Yellow
    }
}

Write-Host "Scaffolding Complete! Ready to begin implementation." -ForegroundColor Cyan
