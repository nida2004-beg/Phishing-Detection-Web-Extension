document.getElementById('checkBtn').addEventListener('click', () => {
    const url = document.getElementById('urlInput').value;

    fetch('http://127.0.0.1:5000/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ url: url })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('result').innerText = 
            `URL: ${data.url}\nPrediction: ${data.prediction}\nProbability: ${data.phishing_probability}`;
    })
    .catch(err => {
        console.error(err);
        document.getElementById('result').innerText = "Error connecting to backend!";
    });
});