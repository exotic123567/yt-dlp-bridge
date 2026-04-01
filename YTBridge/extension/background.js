const HOST_NAME = "com.rnb.ytdlpbridge";

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type !== "START_DOWNLOAD") {
    return;
  }

  chrome.runtime.sendNativeMessage(
    HOST_NAME,
    message.payload,
    (response) => {
      if (chrome.runtime.lastError) {
        sendResponse({
          ok: false,
          message: "Native host communication failed.",
          details: chrome.runtime.lastError.message
        });
        return;
      }

      sendResponse(response || {
        ok: false,
        message: "Native host returned no data."
      });
    }
  );

  return true;
});