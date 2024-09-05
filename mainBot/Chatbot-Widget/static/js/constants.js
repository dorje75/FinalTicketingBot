const action_name = "/action_session_start";  // Optional, based on your use case
const rasa_server_url = "http://localhost:5005/webhooks/rest/webhook";  // Points to your local Rasa server
const sender_id = uuidv4();  // Generates a unique session ID for each user

// Example usage of these constants in your  UI script

// Function to send user message to Rasa server
function sendMessageToRasa(message) {
    fetch(rasa_server_url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            sender: sender_id,
            message: message,
        }),
    })
    .then(response => response.json())
    .then(data => {
        // Handle the bot's response, e.g., display in UI
        setBotResponse(data);  // Update this to reflect your UI update code
        $("#userInput").prop('disabled', false);  // Re-enable user input
    })
    .catch(error => {
        console.error("Error:", error);
        setBotResponse('Error');  // Handle error in the UI
        $("#userInput").prop('disabled', false);  // Re-enable user input in case of error
    });
}

// If you need to trigger an action programmatically
function triggerAction() {
    sendMessageToRasa(action_name);
}

//sendMessageToRasa("hello");

//const action_name = "action_hello_world";
//const rasa_server_url = "http://localhost:5005/webhooks/rest/webhook";
//const sender_id = uuidv4();
