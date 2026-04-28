document.getElementById('submitBtn').addEventListener('click', async () => {
    const userInput = document.getElementById('userInput').value;
    const responseContainer = document.getElementById('response');

    if (!userInput) {
        responseContainer.textContent = 'Please enter a command.';
        return;
    }

    try {
        const response = await fetch('http://127.0.0.1:8000/agent', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ input: userInput }),
        });

        const data = await response.json();
        const formattedResponse = JSON.stringify(JSON.parse(data.response), null, 2);
        responseContainer.textContent = formattedResponse;
    } catch (error) {
        responseContainer.textContent = 'Error: Could not connect to the agent.';
        console.error('Error:', error);
    }
});
