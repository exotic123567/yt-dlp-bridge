const $ = (id) => document.getElementById(id);

async function getCurrentTabUrl() {
  const tabs = await chrome.tabs.query({ active: true, currentWindow: true });
  const tab = tabs[0];
  return tab?.url || "";
}

async function loadSavedSettings() {
  const data = await chrome.storage.local.get([
    "mode",
    "quality",
    "folder",
    "filenameTemplate",
    "embedMetadata",
    "writeThumbnail",
    "writeSubtitles"
  ]);

  if (data.mode) $("mode").value = data.mode;
  if (data.quality) $("quality").value = data.quality;
  if (data.folder) $("folder").value = data.folder;
  if (data.filenameTemplate) $("filenameTemplate").value = data.filenameTemplate;

  $("embedMetadata").checked = data.embedMetadata ?? true;
  $("writeThumbnail").checked = data.writeThumbnail ?? false;
  $("writeSubtitles").checked = data.writeSubtitles ?? false;
}

async function saveSettings() {
  await chrome.storage.local.set({
    mode: $("mode").value,
    quality: $("quality").value,
    folder: $("folder").value,
    filenameTemplate: $("filenameTemplate").value,
    embedMetadata: $("embedMetadata").checked,
    writeThumbnail: $("writeThumbnail").checked,
    writeSubtitles: $("writeSubtitles").checked
  });
}

function setStatus(message, isError = false) {
  const status = $("status");
  status.textContent = message;
  status.style.color = isError ? "#ff8a8a" : "#cfcfcf";
}

$("useCurrentTab").addEventListener("click", async () => {
  const url = await getCurrentTabUrl();
  $("url").value = url;
  setStatus("Current tab URL loaded.");
});

$("downloadBtn").addEventListener("click", async () => {
  const payload = {
    url: $("url").value.trim(),
    mode: $("mode").value,
    quality: $("quality").value,
    folder: $("folder").value,
    filenameTemplate: $("filenameTemplate").value,
    embedMetadata: $("embedMetadata").checked,
    writeThumbnail: $("writeThumbnail").checked,
    writeSubtitles: $("writeSubtitles").checked
  };

  if (!payload.url) {
    setStatus("Please enter or load a URL.", true);
    return;
  }

  await saveSettings();
  setStatus("Sending job to local host...");

  chrome.runtime.sendMessage(
    { type: "START_DOWNLOAD", payload },
    (response) => {
      if (chrome.runtime.lastError) {
        setStatus(`Extension error: ${chrome.runtime.lastError.message}`, true);
        return;
      }

      if (!response) {
        setStatus("No response received.", true);
        return;
      }

      if (response.ok) {
        setStatus(response.message || "Download started/completed.");
      } else {
        const extra = response.details ? `\n\n${response.details}` : "";
        setStatus((response.message || "Download failed.") + extra, true);
      }
    }
  );
});

document.addEventListener("DOMContentLoaded", loadSavedSettings);