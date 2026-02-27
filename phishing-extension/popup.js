document.getElementById('checkBtn').addEventListener('click', () => {
    const url = document.getElementById('urlInput').value;

    if (!url) {
        alert("Please enter a URL!");
        return;
    }

    fetch('http://127.0.0.1:5000/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: url })
    })
    .then(response => response.json())
    .then(data => {
        if (data.prediction === "Legitimate") {
            // Open the URL in a new tab
            chrome.tabs.create({ url: url });
        } else {
            // Save blocked URL to show on warning page
            localStorage.setItem("lastCheckedUrl", url);
            // Open local warning page
            chrome.tabs.create({ url: chrome.runtime.getURL("warning.html") });
        }
    })
    .catch(err => {
        console.error(err);
        alert("Error connecting to backend!");
    });
});