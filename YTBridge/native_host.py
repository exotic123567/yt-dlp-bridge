import sys
import os
import json
import struct
import subprocess
from pathlib import Path
from urllib.parse import urlparse

SCRIPT_DIR = Path(__file__).resolve().parent
CONFIG_FILE = SCRIPT_DIR / "host_config.json"
LOG_FILE = SCRIPT_DIR / "host_log.txt"


def log(message: str):
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(message + "\n")
    except Exception:
        pass


def load_config():
    if not CONFIG_FILE.exists():
        raise FileNotFoundError(f"Config file not found: {CONFIG_FILE}")

    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def read_message():
    raw_length = sys.stdin.buffer.read(4)
    if len(raw_length) == 0:
        sys.exit(0)

    message_length = struct.unpack("<I", raw_length)[0]
    message_bytes = sys.stdin.buffer.read(message_length)
    return json.loads(message_bytes.decode("utf-8"))


def send_message(data):
    encoded = json.dumps(data).encode("utf-8")
    sys.stdout.buffer.write(struct.pack("<I", len(encoded)))
    sys.stdout.buffer.write(encoded)
    sys.stdout.buffer.flush()


def is_valid_url(url: str) -> bool:
    try:
        parsed = urlparse(url)
        return parsed.scheme in ("http", "https") and bool(parsed.netloc)
    except Exception:
        return False


def get_output_template(output_dirs: dict, folder_key: str, filename_template: str) -> str:
    base_dir = output_dirs.get(folder_key)
    if not base_dir:
        raise ValueError(f"Missing output directory for folder key: {folder_key}")

    Path(base_dir).mkdir(parents=True, exist_ok=True)

    if filename_template == "title_id":
        template = "%(title)s [%(id)s].%(ext)s"
    elif filename_template == "uploader_title":
        template = "%(uploader)s - %(title)s.%(ext)s"
    else:
        template = "%(title)s.%(ext)s"

    return str(Path(base_dir) / template)


def build_command(payload: dict, config: dict):
    yt_dlp_path = config["yt_dlp_path"]
    ffmpeg_path = config["ffmpeg_path"]
    output_dirs = config["output_dirs"]

    url = payload["url"]
    mode = payload.get("mode", "video")
    quality = payload.get("quality", "best")
    folder = payload.get("folder", "YT")
    filename_template = payload.get("filenameTemplate", "title")
    embed_metadata = bool(payload.get("embedMetadata", True))
    write_thumbnail = bool(payload.get("writeThumbnail", False))
    write_subtitles = bool(payload.get("writeSubtitles", False))


    output_template = get_output_template(output_dirs, folder, filename_template)

    cmd = [
        yt_dlp_path,
        url,
        "-o", output_template,
        "--ffmpeg-location", ffmpeg_path,
        "--no-playlist"
    ]

    if embed_metadata:
        cmd += ["--embed-metadata"]

    if write_thumbnail:
        cmd += ["--write-thumbnail"]

    if write_subtitles:
        cmd += ["--write-auto-subs", "--sub-langs", "en.*", "--embed-subs"]

    if mode == "audio":
        cmd += ["-x", "--audio-format", "mp3"]
        if quality in ("128", "192", "320"):
            cmd += ["--audio-quality", f"{quality}K"]
    else:
        if quality == "720":
            cmd += ["-f", "bestvideo[height<=720]+bestaudio/best[height<=720]"]
        elif quality == "1080":
            cmd += ["-f", "bestvideo[height<=1080]+bestaudio/best[height<=1080]"]
        else:
            cmd += ["-f", "bestvideo+bestaudio/best"]

        cmd += ["--merge-output-format", "mp4"]

    return cmd


def validate_config(config: dict):
    yt_dlp_path = config.get("yt_dlp_path")
    ffmpeg_path = config.get("ffmpeg_path")
    output_dirs = config.get("output_dirs", {})

    if not yt_dlp_path or not os.path.isfile(yt_dlp_path):
        raise FileNotFoundError(f"yt-dlp not found: {yt_dlp_path}")

    if not ffmpeg_path or not os.path.isfile(ffmpeg_path):
        raise FileNotFoundError(f"ffmpeg not found: {ffmpeg_path}")

    if "YT" not in output_dirs or "Music" not in output_dirs:
        raise ValueError("output_dirs must contain both 'YT' and 'Music'")


def execute_download(payload: dict):
    if "url" not in payload or not payload["url"].strip():
        return {"ok": False, "message": "URL is missing."}

    if not is_valid_url(payload["url"]):
        return {"ok": False, "message": "Invalid URL."}

    try:
        config = load_config()
        validate_config(config)

        cmd = build_command(payload, config)
        log("Running command: " + " ".join(cmd))

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            shell=False,
            encoding="utf-8",
            errors="replace"
        )

        if result.returncode == 0:
            return {
                "ok": True,
                "message": "Download completed successfully.",
                "details": (result.stdout or "")[-1200:]
            }

        return {
            "ok": False,
            "message": "yt-dlp failed.",
            "details": (result.stderr or "Unknown error")[-1800:]
        }

    except Exception as e:
        log(f"Exception: {e}")
        return {
            "ok": False,
            "message": "Native host error.",
            "details": str(e)
        }


def main():
    try:
        payload = read_message()
        response = execute_download(payload)
        send_message(response)
    except Exception as e:
        send_message({
            "ok": False,
            "message": "Fatal host error.",
            "details": str(e)
        })


if __name__ == "__main__":
    main()