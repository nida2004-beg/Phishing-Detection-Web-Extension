// background.js (Manifest V3 service worker)
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    if (changeInfo.status === 'loading' && tab.url.startsWith("http")) {
        fetch('http://127.0.0.1:5000/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url: tab.url })
        })
        .then(response => response.json())
        .then(data => {
            if (data.prediction === "Phishing") {
                // Store the blocked URL in localStorage
                chrome.scripting.executeScript({
                    target: { tabId: tabId },
                    func: (url) => localStorage.setItem("lastCheckedUrl", url),
                    args: [tab.url]
                });

                // Redirect phishing URL to local warning page
                chrome.tabs.update(tabId, { url: chrome.runtime.getURL("warning.html") });
            }
            // Legitimate URLs: do nothing → page loads normally
        })
        .catch(err => console.error("Error contacting backend:", err));
    }
});