document.getElementById('submitBtn').addEventListener('click', async () => {
    const userInput = document.getElementById('userInput').value;
    const responseContainer = document.getElementById('response');
    const baseUrl = window.location.origin === 'null' ? 'http://127.0.0.1:8000' : window.location.origin;

    if (!userInput) {
        responseContainer.textContent = 'Please enter a command.';
        return;
    }

    try {
        const response = await fetch(`${baseUrl}/agent`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ input: userInput }),
        });

        const data = await response.json();
        if (!response.ok) {
            responseContainer.textContent = JSON.stringify(data, null, 2);
            return;
        }
        responseContainer.textContent = JSON.stringify(data, null, 2);
    } catch (error) {
        responseContainer.textContent = 'Error: Could not connect to the agent.';
        console.error('Error:', error);
    }
});
