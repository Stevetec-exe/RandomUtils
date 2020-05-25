# Example Image "https://cdn.pixabay.com/photo/2020/04/24/15/40/the-common-seal-5087396_960_720.jpg"
$ImagePath = "[YOUR URL HERE]"


Invoke-WebRequest $ImagePath -OutFile wallpaper.png
$image = (Get-Item -Path ".\").FullName + "\wallpaper.png"
Add-Type -TypeDefinition @'
using System;
using System.Runtime.InteropServices;
public class Params
{
   [DllImport("User32.dll",CharSet=CharSet.Unicode)]
   public static extern int SystemParametersInfo (Int32 uAction,
                                                  Int32 uParam,
                                                  String lpvParam,
                                                  Int32 fuWinIni);
}
'@
$SPI_SETDESKWALLPAPER = 0x0014
$UpdateIniFile = 0x01
$SendChangeEvent = 0x02
$fWinIni = $UpdateIniFile -bor $SendChangeEvent
$ret = [Params]::SystemParametersInfo($SPI_SETDESKWALLPAPER, 0, $Image, $fWinIni)


function Get-ScriptDirectory { Split-Path $MyInvocation.ScriptName }
Remove-Item -LiteralPath (Join-Path (Get-ScriptDirectory) '\wallpaper.png')
Remove-Item -LiteralPath $MyInvocation.InvocationName
