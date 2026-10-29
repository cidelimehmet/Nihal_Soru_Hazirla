Set WshShell = CreateObject("WScript.Shell")
' Bu dosyanın bulunduğu klasör yolunu al
ScriptDir = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName)
' baslat.bat dosyasını tamamen arka planda (siyah konsol penceresi olmadan) çalıştır
WshShell.CurrentDirectory = ScriptDir
WshShell.Run "cmd /c baslat.bat", 0, False
