document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('checkButton').addEventListener('click', function () {
        const emailText = document.getElementById('emailInput').value;

        fetch('http://localhost:5000/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: emailText }),
        })
        .then(response => response.json())
        .then(data => {
            const resultDiv = document.getElementById('result');
            resultDiv.innerText = "Result: " + data.prediction;
            resultDiv.className = ''; // clear previous class
            if (data.prediction === "Spam") {
                resultDiv.classList.add('spam');
            } else {
                resultDiv.classList.add('ham');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('result').innerText = "Error connecting to server.";
        });
    });
});
