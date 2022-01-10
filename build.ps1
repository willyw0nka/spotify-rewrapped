$Major = 1
$Minor = 0
$Compillation = "$(Get-Date -Format 'yy')$((Get-Date).DayOfYear)"
$Version = "$Major.$Minor.$Compillation"

pyinstaller.exe -y ./spotify_rewrapped_gui.py
Copy-Item -Path .\resources\ -Destination .\dist\spotify_rewrapped_gui\ -Recurse

Compress-Archive -Path ./dist/spotify_rewrapped_gui -DestinationPath ./dist/spotify-rewrapped-gui-$Version.zip

Write-Output "Build complete!"
Write-Output "Generated version: $Version"