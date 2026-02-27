// Get last checked URL from localStorage
const blockedUrl = localStorage.getItem("lastCheckedUrl");
document.getElementById('blockedUrl').innerText = "Blocked URL: " + blockedUrl;

// Fetch full phishing report from backend
fetch('http://127.0.0.1:5000/predict', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ url: blockedUrl })
})
.then(res => res.json())
.then(data => {
    if (data.prediction === "Phishing") {
        document.getElementById('threatLevel').innerText = "Threat Level: " + data.threat_level;
        document.getElementById('riskScore').innerText = "Risk Score: " + data.risk_score + "%";

        const reasonsList = document.getElementById('reasonsList');
        data.reasons.forEach(reason => {
            const li = document.createElement("li");
            li.innerText = reason;
            reasonsList.appendChild(li);
        });
    }
})
.catch(err => console.error("Error fetching report:", err));

// Go Back button redirects to styled GoBack page
document.getElementById('goBackBtn').addEventListener('click', () => {
    window.location.href = chrome.runtime.getURL("goBack.html");
});