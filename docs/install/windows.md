# Install on Windows

**Needs:** Windows 10 or 11, 64-bit · about 30 MB of disk · your [access key](../faq.md#how-do-i-get-an-access-key) · the free **Npcap** driver (step 2).

## 1. Download
Download **`{{ windows_installer }}`** from the [Download page](../download.md#windows).

## 2. Install Npcap (once)
NetPulse needs **Npcap** to see network traffic. Npcap's licence does not allow other programs to bundle it, so **you install it yourself, once**. NetPulse never installs it for you and never works around it.

1. Open the official page: **<https://npcap.com/#download>**.
2. Download the latest *Npcap installer* and run it. Windows asks for administrator permission.
3. Keep the default options. Leave **"Restrict Npcap driver's access to Administrators only"** **unticked**; otherwise NetPulse can only capture when run as administrator.

If you skip this, NetPulse tells you on its setup screen, shows the same link with a *Copy link* button, and offers *Check again* once Npcap is installed. Saved captures (`netpulse scan --pcap`) can be analysed without Npcap.

## 3. Install NetPulse
1. Double-click `{{ windows_installer }}`.
2. Because the installer is not code-signed yet, Microsoft Defender SmartScreen may show **"Windows protected your PC"**:
    - Click **More info**.
    - Check that the file name is `{{ windows_installer }}` and the publisher reads *Unknown publisher*.
    - Click **Run anyway**.
3. The installer installs **for your user only**. It needs no administrator rights, and puts NetPulse in:
   ```
   %LOCALAPPDATA%\NetPulse\
   ├── netpulse-desktop.exe   the desktop app (Start menu: NetPulse)
   ├── netpulse.exe           the command line and background service
   └── uninstall.exe
   ```
4. Finish. NetPulse appears in the Start menu as **NetPulse**.

!!! tip "Silent install (IT admins)"
    `{{ windows_installer }} /S` installs without questions; `"%LOCALAPPDATA%\NetPulse\uninstall.exe" /S` removes it.

## 4. Launch and connect
1. Open **NetPulse** from the Start menu.
2. **Your access key:** paste the key you were given (`np_…`). It is stored in its own file, `%APPDATA%\NetPulse\secrets\agent.token`, and never shown again.
3. **This computer's name** is filled in from your computer name. Change it if you like (letters, numbers, dashes).
4. **Advanced → Service address** is already set to the NetPulse AI service. Leave it.
5. Click **Connect**. Settings are saved to `%APPDATA%\NetPulse\netpulse.toml`.

## 5. Start monitoring
- The setup screen checks Npcap (*NetPulse can see your network → Ready*).
- Press **Start protection**. Within a minute, Home lists your apps and *"Your computer looks safe"*, and the footer shows **Connected to NetPulse AI · model 2**.
- If the footer says **Access key not accepted**, the key is wrong or was revoked. See [Troubleshooting](../troubleshooting.md#access-key-not-accepted).

## Using the command line
`netpulse.exe` is in the install folder. It is not added to `PATH` (the installer does not change your system settings). Either use the full path:
```powershell
& "$env:LOCALAPPDATA\NetPulse\netpulse.exe" status
```
or add the folder to your own `PATH` once:
```powershell
[Environment]::SetEnvironmentVariable("Path", $env:Path + ";$env:LOCALAPPDATA\NetPulse", "User")
```
The CLI finds the settings the app wrote automatically. A CLI-only zip is also on the [Download page](../download.md#windows). See the [CLI reference](../cli.md).

## Run in the background (optional)
To keep protection on without the window, install the [background service](../service.md#windows) (administrator).

## Update
Run the newer installer. It replaces the program files and keeps your settings, key and history.

## Uninstall
*Settings → Apps → Installed apps → NetPulse → Uninstall*, or run `%LOCALAPPDATA%\NetPulse\uninstall.exe`.
- If you installed the service, remove it first: `netpulse service uninstall` (administrator).
- Your settings and history in `%APPDATA%\NetPulse` are kept. Delete that folder to remove them too.
- Npcap is a separate program; uninstall it from *Installed apps* if nothing else needs it.
