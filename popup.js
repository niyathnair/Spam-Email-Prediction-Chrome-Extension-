// popup.js
function detectSpam() {
    var message = document.getElementById("message").value;
    fetch('http://localhost:5000/detect', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: message }),
    })
    .then(response => response.json())
    .then(data => {
        var result = data.prediction ? "Spam detected!" : "Not spam.";
        document.getElementById("result").innerText = result;
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Fetch accuracy and precision
fetch('http://localhost:5000/accuracy_precision')
    .then(response => response.json())
    .then(data => {
        document.getElementById("accuracy").innerText = "Accuracy: " + data.accuracy;
        document.getElementById("precision").innerText = "Precision: " + data.precision;
    })
    .catch(error => {
        console.error('Error:', error);
    });
