document.getElementById('checkBtn').addEventListener('click', () => {
    const url = document.getElementById('urlInput').value;

    fetch('http://127.0.0.1:5000/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: url })
    })
    .then(response => response.json())
    .then(data => {
        if (data.prediction === "Phishing") {
            localStorage.setItem("lastCheckedUrl", url);
            window.location.href = chrome.runtime.getURL("warning.html");
        } else {
            // Legitimate URL → redirect directly to actual website
            window.location.href = url;
        }
    })
    .catch(err => {
        console.error(err);
        document.getElementById('result').innerText = "Error connecting to backend!";
    });
});