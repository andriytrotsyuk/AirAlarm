Write-Host "Building Flutter app and generating Inno Setup script..." -ForegroundColor Cyan

# 1. Run inno_bundle but ONLY let it generate the script, no installer build yet 
dart run inno_bundle --no-installer

$issFile = "build\windows\x64\installer\Release\inno-script.iss"

if (-Not (Test-Path $issFile)) {
    Write-Host "Error: Could not find generated .iss file at $issFile" -ForegroundColor Red
    exit 1
}

Write-Host "Injecting Firewall Rules into Installer Script..." -ForegroundColor Yellow

# 2. Append Custom Firewall Rules
$firewallRules = @"

[Run]
Filename: "{sys}\netsh.exe"; Parameters: "advfirewall firewall add rule name=""AirAlarm"" dir=out action=allow program=""{app}\airalarm.exe"" enable=yes"; Flags: runhidden
Filename: "{sys}\netsh.exe"; Parameters: "advfirewall firewall add rule name=""AirAlarm"" dir=in action=allow program=""{app}\airalarm.exe"" enable=yes"; Flags: runhidden

[UninstallRun]
Filename: "{sys}\netsh.exe"; Parameters: "advfirewall firewall delete rule name=""AirAlarm"""; Flags: runhidden
"@

Add-Content -Path $issFile -Value $firewallRules

Write-Host "Compiling updated Installer Script via ISCC..." -ForegroundColor Cyan

# 3. Compile using ISCC.exe (Inno Setup Compiler)
$isccPath = "$env:LOCALAPPDATA\Programs\Inno Setup 6\ISCC.exe"
if (-Not (Test-Path $isccPath)) {
    $isccPath = "C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
}
if (-Not (Test-Path $isccPath)) {
    Write-Host "Warning: ISCC.exe not found at default location. Assuming it is in PATH." -ForegroundColor Yellow
    $isccPath = "iscc"
}

& $isccPath $issFile

Write-Host "Build complete! The new installer is in build\windows\x64\installer\Release\" -ForegroundColor Green
