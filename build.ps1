$Major = 1
$Minor = 0
$Compillation = "$(Get-Date -Format 'yy')$((Get-Date).DayOfYear)"
$Version = "$Major.$Minor.$Compillation"

pyinstaller.exe --noconsole -y ./SpotifyRewrappedGUI.py
Copy-Item -Path ./resources ./dist/SpotifyRewrappedGUI/

Compress-Archive -Path ./dist/SpotifyRewrappedGUI -DestinationPath ./dist/spotify-rewrapped-$Version.zip

Write-Output "Build complete!"
Write-Output "Generated version: $Version"