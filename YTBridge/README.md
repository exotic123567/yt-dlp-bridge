# YT-DLP Browser Extension Bridge (Windows Setup Guide)

This tool allows you to download YouTube videos directly from your browser using your locally installed `yt-dlp`.

---

## 🔧 Requirements

Before starting, make sure you have:

1. **Python installed**

   * Download: https://www.python.org/downloads/
   * During install, enable: `Add Python to PATH`

2. **yt-dlp**

   * Download from: https://github.com/yt-dlp/yt-dlp/releases
   * Save it somewhere (example: `C:\yt-dlp\yt-dlp.exe`)
   * or run the following command in your windows terminal: winget install yt-dlp
   * Note the yt-dlp path by pasting the command in your terminal: `where yt-dlp`

3. **ffmpeg**

   * Download from: https://ffmpeg.org/download.html
   * Extract it (example: `C:\ffmpeg\bin\ffmpeg.exe`)
   * Or just run the following command in your windows terminal: winget install -e --id Gyan.FFmpeg --exact
   * Note the ffmpeg path by pasting the command in your terminal: `where ffmpeg`

---

## 📁 Step 1 — Place the Project Folder

Extract or place the `YTBridge` folder anywhere on your PC.

Example:

```text
C:\YTBridge\
```

⚠️ Avoid spaces in folder names if possible.

---

## ⚙️ Step 2 — Configure Paths (IMPORTANT)

You need to edit **3 files only**.

---

### 2.1 Edit `host_config.json`

Open this file and update:

```json
{
  "yt_dlp_path": "C:\\yt-dlp\\yt-dlp.exe",
  "ffmpeg_path": "C:\\ffmpeg\\bin\\ffmpeg.exe",
  "output_dirs": {
    "YT": "C:\\Users\\YOUR_USERNAME\\Downloads\\YT",
    "Music": "C:\\Users\\YOUR_USERNAME\\Downloads\\Music"
  }
}
```

#### What to change:

* Replace `yt_dlp_path` → where your `yt-dlp.exe` is located
* Replace `ffmpeg_path` → where your `ffmpeg.exe` is located
* Replace `YOUR_USERNAME` with your Windows username

---

### 2.2 Edit `com.rnb.ytdlpbridge.json`

Open and update:

```json
"path": "C:\\YTBridge\\native_host.bat",
```

Replace with your actual folder path.

Example:

```json
"path": "D:\\Projects\\YTBridge\\native_host.bat",
```

---

### 2.3 Add Extension ID (IMPORTANT)

Later, after loading the extension, you must update:

```json
"allowed_origins": [
  "chrome-extension://PASTE_EXTENSION_ID_HERE/"
]
```

You will do this in Step 4.

---

### 2.4 Edit `register_host.reg`

Open this file and update:

```reg
@="C:\\YTBridge\\com.rnb.ytdlpbridge.json"
```

Replace with your actual path.

---

## 🌐 Step 3 — Load Extension in Brave

1. Open:

   ```
   brave://extensions
   ```

2. Enable **Developer Mode**

3. Click **Load unpacked**

4. Select the folder:

   ```
   YTBridge\extension\
   ```

---

## 🆔 Step 4 — Copy Extension ID

After loading:

* Copy the Extension ID shown in Brave

Example:

```
eihcgchbkfocgkjjbomlgbkolecplamj
```

Now go back to:

### `com.rnb.ytdlpbridge.json`

Replace:

```json
"chrome-extension://PASTE_EXTENSION_ID_HERE/"
```

with:

```json
"chrome-extension://YOUR_REAL_ID/"
```

⚠️ Keep the trailing slash `/`

---

## 🧾 Step 5 — Register Native Host

Double-click:

```text
register_host.reg
```

Click **Yes** when prompted.

---

## 🔄 Step 6 — Reload Extension

Go back to:

```
brave://extensions
```

Click **Reload** on your extension.

---

## 🚀 Step 7 — Test

1. Open any YouTube video
2. Click the extension icon
3. Click **Use Current Tab**
4. Click **Download**

---

## 📂 Output Location

Files will be saved in:

```text
C:\Users\YOUR_USERNAME\Downloads\YT
```

or

```text
C:\Users\YOUR_USERNAME\Downloads\Music
```

---

## ❗ Troubleshooting

### Error: "Native host communication failed"

Check:

* Python is installed:

  ```
  python --version
  ```

* Paths are correct in:

  * `host_config.json`
  * `com.rnb.ytdlpbridge.json`

* Extension ID is correct

---

### Error: "python not found"

Fix `native_host.bat`:

Replace:

```bat
python ...
```

with full path:

```bat
"C:\Users\YOUR_USERNAME\AppData\Local\Programs\Python\Python313\python.exe" "%~dp0native_host.py"
```

---

### Error: Download fails

Check:

* `yt-dlp.exe` path is correct
* `ffmpeg.exe` path is correct

---

## 🧹 Uninstall

1. Delete registry entry:

Open `regedit` and delete:

```
HKEY_CURRENT_USER
→ Software
→ BraveSoftware
→ Brave-Browser
→ NativeMessagingHosts
→ com.rnb.ytdlpbridge
```

2. Remove extension from Brave

---

## ✅ Done

You now have a local YouTube downloader integrated into your browser.
