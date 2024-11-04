////// Function to show the date input form and overlay
////function showForm() {
////    document.getElementById('formTable_date').style.display = 'block';
////    document.getElementById('overlay').style.display = 'block';
////    document.querySelector('.chats').style.pointerEvents = 'none'; // Disable interaction with chat
////    document.getElementById('userInput').disabled = true; // Disable chat input
////}
////
////// Function to hide the form and overlay, and enable chat input
////function hideForm() {
////    document.getElementById('formTable_date').style.display = 'none';
////    document.getElementById('overlay').style.display = 'none';
////    document.querySelector('.chats').style.pointerEvents = 'auto'; // Enable interaction with chat
////    document.getElementById('userInput').disabled = false; // Enable chat input
////}
////
////// Function to submit the form
////function submitForm() {
////    const dateValue = document.getElementById('date').value; // Get the selected date
////    if (dateValue) {
////        const formData = `date=${dateValue}`; // Format the data to send to Rasa
////        send(formData); // Use your send function to send data
////        hideForm(); // Hide the form after submission
////    } else {
////        alert('Please select a date.'); // Alert if no date is selected
////    }
////}
////
////
////// Trigger the form to show when the bot asks for the visit date
////function triggerDateForm() {
////    showForm(); // Show the date form
////}
////
////// Listen for messages from the Rasa bot
////$(document).on("click", ".menu .menuChips", function () {
////    const payload = this.getAttribute("data-payload");
////
////    // Check if the payload indicates the bot is asking for a date
////    if (payload === 'utter_ask_date') {
////        triggerDateForm(); // Show the date form
////    } else {
////        const text = this.innerText;
////        console.log("payload: ", payload);
////        setUserResponse(text);
////        send(payload);
////    }
////
////    // Delete the suggestions once the user clicks on it
////    $(".suggestions").remove();
////});
//// Function to show the date picker form
//function showForm() {
//    document.getElementById('formTable_date').style.display = 'block';
//    document.getElementById('overlay').style.display = 'block';
//    document.querySelector('.chats').style.pointerEvents = 'none'; // Disable interaction with chat
//    document.getElementById('userInput').disabled = true; // Disable chat input
//}
//
//// Function to hide the form and overlay
//function hideForm() {
//    document.getElementById('formTable_date').style.display = 'none';
//    document.getElementById('overlay').style.display = 'none';
//    document.querySelector('.chats').style.pointerEvents = 'auto'; // Enable interaction with chat
//    document.getElementById('userInput').disabled = false; // Enable chat input
//}
//
//// Function to submit the date form
//function submitForm() {
//    const dateValue = document.getElementById('date').value; // Get the selected date
//    if (dateValue) {
//        const formData = `date=${dateValue}`; // Format the data to send to Rasa
//        setUserResponse(text);
//        send(formData); // Use your send function to send data
//        hideForm(); // Hide the form after submission
//    } else {
//        alert('Please select a date.'); // Alert if no date is selected
//    }
//}
//
//// Function to handle the response from Rasa
////triggerDateForm();
//
////if (response.text && response.text.includes("Preferred date?")) {
////    triggerDateForm(); // Show the date form
////}
////setUserResponse(response.text); // Process other responses
//
//$(document).on("click", ".menu .menuChips", function () {
//    const dateValue = document.getElementById('date').value; // Get the selected date
//    if (dateValue) {
//        const formData = `date=${dateValue}`; // Format the data to send to Rasa
//        setUserResponse(text);
//        send(formData); // Use your send function to send data
//        hideForm(); // Hide the form after submission
//    } else {
//        alert('Please select a date.'); // Alert if no date is selected
//    }
//}
//});
// Assuming datePicker.js is imported in index.js and contains your date picker functions

// Function to show the date picker form
function showForm() {
    document.getElementById('formTable_date').style.display = 'block';
    document.getElementById('overlay').style.display = 'block';
    document.querySelector('.chats').style.pointerEvents = 'none'; // Disable interaction with chat
    document.getElementById('userInput').disabled = true; // Disable chat input
}

// Function to hide the form and overlay
function hideForm() {
    document.getElementById('formTable_date').style.display = 'none';
    document.getElementById('overlay').style.display = 'none';
    document.querySelector('.chats').style.pointerEvents = 'auto'; // Enable interaction with chat
    document.getElementById('userInput').disabled = false; // Enable chat input
}

// Function to submit the date form
function submitForm() {
    const dateValue = document.getElementById('date').value; // Get the selected date
    if (dateValue) {
        const formData = `date=${dateValue}`; // Format the data to send to Rasa
        send(formData); // Use your send function to send data
        hideForm(); // Hide the form after submission
    } else {
        alert('Please select a date.'); // Alert if no date is selected
    }
}

// Function to trigger the date form when the bot asks for a visit date
function triggerDateForm() {
    showForm(); // Show the date form
}

// Listen for messages from the Rasa bot
$(document).on("click", ".menu .menuChips", function () {
    const payload = this.getAttribute("data-payload");

    // Check if the payload indicates the bot is asking for a date
    if (payload === 'utter_ask_date' || this.innerText.includes("Visit date?")|| this.innerText.includes("Preferred date?")) {
        triggerDateForm(); // Show the date form
    } else {
        const text = this.innerText;
        console.log("payload: ", payload);
        setUserResponse(text);
        send(payload);
    }

    // Delete the suggestions once the user clicks on it
    $(".suggestions").remove();
});
