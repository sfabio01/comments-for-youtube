// EXTENSION ACTIVATION 
chrome.tabs.onUpdated.addListener(function (tabId, info, tab) {
    if (tab.url.startsWith("https://www.youtube.com/watch?v=")) {
        chrome.browserAction.enable(tabId);
    } else {
        chrome.browserAction.disable(tabId);
    }
});