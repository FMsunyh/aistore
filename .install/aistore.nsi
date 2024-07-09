; Define the name of the installer and the version number
!define VERSION "1.1.7"
Name "AIStore"
OutFile "AIStoreInstaller_${VERSION}.exe"

; Default installation directory
InstallDir "$PROGRAMFILES\AIStore"

; Include necessary NSIS libraries
!include "MUI2.nsh"
!include "FileFunc.nsh"
!include "LogicLib.nsh"
!include "InstallOptions.nsh"

; Variables
Var LaunchApp

; MUI Settings
!define MUI_ABORTWARNING
!define MUI_ICON "${NSISDIR}\Contrib\Graphics\Icons\modern-install.ico"
!define MUI_UNICON "${NSISDIR}\Contrib\Graphics\Icons\modern-uninstall.ico"

; Welcome page
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "license.txt"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES

; Finish page with checkbox to launch application
!insertmacro MUI_PAGE_FINISH
!define MUI_FINISHPAGE_RUN

; Uninstaller pages
!insertmacro MUI_UNPAGE_WELCOME
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_UNPAGE_FINISH

; Language files
!insertmacro MUI_LANGUAGE "SimpChinese"

; Installation sections
Section "Install"
    ; Check if old version is running
    ; Call CheckForRunningProcess

    SetOutPath "$INSTDIR" ; Set output path to installation directory
    
    ; Copy application files
    File "..\.pyInstaller\aistore.exe" ; Adjust path to your application executable

    ; Copy other files
    File /r "source\*.*" 

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

; Function to check for running process
Function CheckForRunningProcess
    StrCpy $1 "aistore.exe"
    nsProcess::_FindProcess $1
    Pop $0

    ${If} $0 = 0
        MessageBox MB_OK "AIStore is currently running. Please close the application before proceeding with the installation."
        Push 1
    ${Else}
        Push 0
    ${EndIf}
FunctionEnd

; Function to terminate the old process
Function TerminateOldProcess
    ExecDos::exec 'taskkill /F /IM aistore.exe'
FunctionEnd

; Function to start the application
Function StartApplication
    Exec '"$INSTDIR\aistore.exe"'
FunctionEnd

; Page for custom installation options
Page custom CustomPageCreate CustomPageLeave

; Custom page functions
Var Label
Function CustomPageCreate
    !insertmacro MUI_HEADER_TEXT "Select additional tasks" ""
    !insertmacro MUI_HEADER_TEXT " " " "
    nsDialogs::Create /NOUNLOAD 1018
    Pop $0
    
    ${If} $0 == error
        Abort
    ${EndIf}
    
    ${NSD_CreateLabel} 0 0 100% 12u "Hello, Start the AiStore immediately!"
	Pop $Label

    ${NSD_CreateCheckbox} 0 20u 100% 10u "Launch AIStore"
    Pop $LaunchApp
    ${NSD_SetState} $LaunchApp ${BST_CHECKED}
    
    nsDialogs::Show
FunctionEnd

Function CustomPageLeave
    ${NSD_GetState} $LaunchApp $0
    StrCmp $0 ${BST_CHECKED} 0 +2
    Call StartApplication
FunctionEnd

; Function .onInit
;     StrCpy $1 "aistore.exe"
;     nsProcess::_FindProcess "$1" 
;     Pop $R0
;     ${If} $R0 = 0
;       MessageBox MB_OK|MB_ICONSTOP "AIStore is currently running. Please close the application before proceeding with the installation." IDOK
;       ;Abort
;     ${EndIf}
; FunctionEnd