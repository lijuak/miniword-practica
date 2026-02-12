; Script de instalación de MiniWord con Inno Setup

[Setup]
AppName=MiniWord
AppVersion=1.0
DefaultDirName={autopf}\MiniWord
DefaultGroupName=MiniWord
OutputDir=.\installer_output
OutputBaseFilename=MiniWord_Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern
ArchitecturesInstallIn64BitMode=x64
UninstallDisplayIcon={app}\MiniWord.exe

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"

[Tasks]
Name: "desktopicon"; Description: "Crear icono en el escritorio"; GroupDescription: "Iconos adicionales:"; Flags: unchecked

[Files]
Source: "dist\MiniWord.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\MiniWord"; Filename: "{app}\MiniWord.exe"
Name: "{group}\Desinstalar MiniWord"; Filename: "{uninstallexe}"
Name: "{autodesktop}\MiniWord"; Filename: "{app}\MiniWord.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\MiniWord.exe"; Description: "Ejecutar MiniWord"; Flags: nowait postinstall skipifsilent
