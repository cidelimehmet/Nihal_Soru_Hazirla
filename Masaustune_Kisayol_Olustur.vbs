Set WshShell = CreateObject("WScript.Shell")
strDesktop = WshShell.SpecialFolders("Desktop")
strCurrentDir = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName)

Set oShortcut = WshShell.CreateShortcut(strDesktop & "\Tevfik İleri İHO Soru Hazırla.lnk")
oShortcut.TargetPath = strCurrentDir & "\baslat.bat"
oShortcut.WorkingDirectory = strCurrentDir
oShortcut.WindowStyle = 1
oShortcut.Description = "Tevfik İleri İmam Hatip Ortaokulu Soru Hazırlama Sistemi"
oShortcut.IconLocation = "shell32.dll,13"
oShortcut.Save

MsgBox "Masaüstünüze 'Tevfik İleri İHO Soru Hazırla' simgesi başarıyla eklendi!" & vbCrLf & vbCrLf & "Artık programı masaüstündeki bu simgeye çift tıklayarak açabilirsiniz.", 64, "Kısayol Oluşturuldu"
