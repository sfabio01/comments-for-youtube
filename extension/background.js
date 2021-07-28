chrome.tabs.onUpdated.addListener(function (tabId, info, tab) {
    if (tab.url.startsWith("https://www.youtube.com/watch?v=")) {
        chrome.action.enable(tabId);
    } else {
        chrome.action.disable(tabId);
    }
});