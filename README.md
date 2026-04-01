# YT-DLP Browser Bridge

Download videos and audio directly from your browser using yt-dlp installed on your system.

This project connects a Brave Chrome extension to a local Python-based native host, allowing you to send download requests from the browser to yt-dlp running on your machine.

---

## ✨ Features

* Download video or audio from supported websites
* Choose quality such as 720p, 1080p, or best
* Extract audio in MP3 format with bitrate options
* Save files to predefined folders
* Works fully offline using your local yt-dlp installation
* No tracking, no server, no data collection

---

## 🧠 How It Works

Browser Extension → Native Messaging → Python Host → yt-dlp → File Download

The extension sends a request to a local Python script using Chrome Native Messaging.
The Python script builds and executes the yt-dlp command.
The downloaded file is saved to your configured output folder.

---

## 🧰 Requirements

Install the following before setup:

1. Python
   https://www.python.org/downloads/
   Make sure "Add Python to PATH" is enabled

2. yt-dlp
   https://github.com/yt-dlp/yt-dlp/releases

3. ffmpeg
   https://ffmpeg.org/download.html

---

## 📁 Project Structure

```
YTBridge/
│
├── extension/
│   ├── manifest.json
│   ├── popup.html
│   ├── popup.css
│   ├── popup.js
│   └── background.js
│
├── native_host.py
├── native_host.bat
├── host_config.json
├── com.rnb.ytdlpbridge.json
├── register_host.reg
└── README.md
```

---

## ⚙️ Setup Instructions

### Step 1. Place the Project Folder

Place the `YTBridge` folder anywhere on your system.

Example:

```
C:\YTBridge\
```

Avoid spaces in folder names if possible.

---

### Step 2. Configure Paths

Edit the following files.

---

#### 2.1 host_config.json

Update paths:

```
{
  "yt_dlp_path": "C:\\yt-dlp\\yt-dlp.exe",
  "ffmpeg_path": "C:\\ffmpeg\\bin\\ffmpeg.exe",
  "output_dirs": {
    "YT": "C:\\Users\\YOUR_USERNAME\\Downloads\\YT",
    "Music": "C:\\Users\\YOUR_USERNAME\\Downloads\\Music"
  }
}
```

Replace:

* yt_dlp_path with your yt-dlp location
* ffmpeg_path with your ffmpeg location
* YOUR_USERNAME with your Windows username

---

#### 2.2 com.rnb.ytdlpbridge.json

Update:

```
"path": "C:\\YTBridge\\native_host.bat"
```

Replace with your actual folder path.

---

### Step 3. Load Extension

1. Open Brave
2. Go to
   brave://extensions
3. Enable Developer Mode
4. Click Load unpacked
5. Select the `extension` folder

---

### Step 4. Add Extension ID

After loading, copy the extension ID.

Edit:

```
"allowed_origins": [
  "chrome-extension://YOUR_EXTENSION_ID/"
]
```

Replace with your actual ID. Keep the trailing slash.

---

### Step 5. Register Native Host

Double click:

```
register_host.reg
```

Confirm the prompt.

---

### Step 6. Reload Extension

Reload the extension from:

```
brave://extensions
```

---

## 🚀 Usage

1. Open a supported video page
2. Click the extension icon
3. Click Use Current Tab
4. Choose format and quality
5. Click Download

---

## 📂 Output

Files are saved to:

```
C:\Users\YOUR_USERNAME\Downloads\YT
```

or

```
C:\Users\YOUR_USERNAME\Downloads\Music
```

---

## ❗ Troubleshooting

### Native host communication failed

Check:

* Python is installed and accessible
* Paths in config files are correct
* Extension ID matches exactly
* Registry file was imported

---

### Python not found

Edit `native_host.bat` and use full Python path:

```
"C:\Users\YOUR_USERNAME\AppData\Local\Programs\Python\Python310\python.exe" "%~dp0native_host.py"
```

---

### yt-dlp fails

Check:

* yt-dlp path is correct
* ffmpeg path is correct
* Site is supported by yt-dlp
* Some sites require cookies or login

---

## 🔐 Privacy

* No data is sent anywhere
* All processing happens locally
* Logs are stored only on your machine

---

## 🧹 Uninstall

1. Open registry editor
2. Delete:

```
HKEY_CURRENT_USER
→ Software
→ BraveSoftware
→ Brave-Browser
→ NativeMessagingHosts
→ com.rnb.ytdlpbridge
```

3. Remove extension from Brave

---

## 📌 Notes

* Some streaming platforms use DRM and cannot be downloaded
* Some sites require login or cookies
* yt-dlp support varies by site

---

## ⭐ Credits

* yt-dlp for the downloading engine
* Chromium Native Messaging for local communication

---
