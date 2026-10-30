Set WshShell = CreateObject("WScript.Shell")
Set FSO = CreateObject("Scripting.FileSystemObject")
ScriptDir = FSO.GetParentFolderName(WScript.ScriptFullName)
WshShell.CurrentDirectory = ScriptDir

PortablePyW = ScriptDir & "\python_embed\pythonw.exe"
If FSO.FileExists(PortablePyW) Then
    WshShell.Run """" & PortablePyW & """ """ & ScriptDir & "\main.py""", 0, False
Else
    WshShell.Run "cmd /c baslat.bat", 0, False
End If
