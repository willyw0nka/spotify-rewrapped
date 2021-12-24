$Major = 1
$Minor = 0
$Compillation = "$(Get-Date -Format 'yy')$((Get-Date).DayOfYear)"
$Version = "$Major.$Minor.$Compillation"

pyinstaller.exe ./gui.py
Copy-Item -Path ./resources ./dist/gui/

Compress-Archive -Path ./dist/gui -DestinationPath ./dist/spotify-rewrapped-$Version.zip

Write-Output "Build complete!"
Write-Output "Generated version: $Version"