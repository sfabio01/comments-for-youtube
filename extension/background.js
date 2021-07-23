chrome.runtime.onInstalled.addListener((reason) => {
    if (reason === chrome.runtime.OnInstalledReason.INSTALL) {
        chrome.tabs.create({
            url: 'welcome.html'
        });
    }
});

chrome.tabs.onUpdated.addListener(function (tabId, info, tab) {
    if (tab.url.startsWith("https://www.youtube.com/watch?v=")) {
        chrome.action.enable(tabId);
        chrome.action.setBadgeText({ tabId: tabId, text: "ON" });
    } else {
        chrome.action.disable(tabId);
        chrome.action.setBadgeText({ tabId: tabId, text: "OFF" });
    }
});