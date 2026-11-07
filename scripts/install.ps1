# OmniForge Automated 1-Line Installer for Windows
# Official repository: https://github.com/howtosecu/OmniForge

$ErrorActionPreference = "Stop"

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "     OmniForge Autonomous Web Runtime Windows Installer   " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

$InstallDir = Join-Path $env:LOCALAPPDATA "OmniForge"

Write-Host "[+] Querying latest release metadata from howtosecu/OmniForge..." -ForegroundColor Yellow

try {
    $ReleaseInfo = Invoke-RestMethod -Uri "https://api.github.com/repos/howtosecu/OmniForge/releases/latest"
    $Asset = $ReleaseInfo.assets | Where-Object { $_.name -like "*windows*.zip" -or $_.name -like "*omniforge*.zip" } | Select-Object -First 1
    if (-not $Asset) {
        Write-Warning "[-] No compiled Windows release asset found yet on GitHub Releases."
        return
    }
    $DownloadUrl = $Asset.browser_download_url
} catch {
    Write-Warning "[-] Could not retrieve release metadata. Please ensure an official release has been published."
    return
}

$TempZip = Join-Path $env:TEMP "omniforge-windows.zip"
Write-Host "[+] Downloading OmniForge package from $DownloadUrl..." -ForegroundColor Yellow
Invoke-WebRequest -Uri $DownloadUrl -OutFile $TempZip

Write-Host "[+] Installing to $InstallDir..." -ForegroundColor Yellow
if (Test-Path $InstallDir) {
    Remove-Item -Path $InstallDir -Recurse -Force
}
New-Item -ItemType Directory -Path $InstallDir -Force | Out-Null
Expand-Archive -Path $TempZip -DestinationPath $InstallDir -Force
Remove-Item -Path $TempZip -Force

# Rename chrome.exe to omniforge.exe if present
$ChromeExe = Join-Path $InstallDir "chrome.exe"
$OmniForgeExe = Join-Path $InstallDir "omniforge.exe"
if ((Test-Path $ChromeExe) -and (-not (Test-Path $OmniForgeExe))) {
    Rename-Item -Path $ChromeExe -NewName "omniforge.exe"
}

Write-Host "[✔] OmniForge successfully installed at: $InstallDir" -ForegroundColor Green
Write-Host "[*] Executable path: $OmniForgeExe" -ForegroundColor Cyan
