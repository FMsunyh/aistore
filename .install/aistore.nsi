; Define the name of the installer and the version number
!define VERSION "1.0.0"
Name "AIStore"
OutFile "AIStoreInstaller_${VERSION}.exe"

; Default installation directory
InstallDir "$PROGRAMFILES\AIStore"

; Include necessary NSIS libraries
!include "MUI2.nsh"
!include "nsDialogs.nsh"

; Variable to store checkbox state
Var LaunchApp

; Installation sections
Section "Install"
    SetOutPath "$INSTDIR" ; Set output path to installation directory
    
    ; Copy application files
    File "..\.PyInstaller\aistore.exe" ; Adjust path to your application executable
    File "..\app\cache\cache.db" ; Adjust path to your application executable
    
    ; Create uninstaller
    WriteUninstaller "$INSTDIR\Uninstall.exe"
    
    ; Create desktop shortcut
    CreateShortcut "$DESKTOP\AIStore.lnk" "$INSTDIR\aistore.exe"
    
    ; Create start menu shortcuts
    CreateDirectory "$SMPROGRAMS\AIStore"
    CreateShortcut "$SMPROGRAMS\AIStore\AIStore.lnk" "$INSTDIR\aistore.exe"
    CreateShortcut "$SMPROGRAMS\AIStore\Uninstall AIStore.lnk" "$INSTDIR\Uninstall.exe"
    

SectionEnd

; Uninstallation section
Section "Uninstall"
    Delete "$INSTDIR\Uninstall.exe"
    Delete "$INSTDIR\aistore.exe"
    Delete "$DESKTOP\AIStore.lnk"
    Delete "$SMPROGRAMS\AIStore\AIStore.lnk"
    Delete "$SMPROGRAMS\AIStore\Uninstall AIStore.lnk"
    RMDir "$SMPROGRAMS\AIStore"
    RMDir /r "$INSTDIR"
SectionEnd

; Page for custom installation options
Page directory
Page instfiles
Page custom CustomPageCreate CustomPageLeave

; Custom page functions
Function CustomPageCreate
    nsDialogs::Create /NOUNLOAD 1018
    Pop $0
    
    ${If} $0 == error
        Abort
    ${EndIf}
    
    ${NSD_CreateCheckbox} 0 0 100% 10% "Launch AIStore"
    Pop $LaunchApp
    ${NSD_SetState} $LaunchApp ${BST_CHECKED}
    
    nsDialogs::Show
FunctionEnd

Function CustomPageLeave
    ${NSD_GetState} $LaunchApp $0

    StrCmp $0 ${BST_CHECKED} 0 +2
    ; Run the application if the checkbox is checked
    
    Exec '"$INSTDIR\aistore.exe"'

FunctionEnd

; Include additional language support if needed
!insertmacro MUI_LANGUAGE "English"
