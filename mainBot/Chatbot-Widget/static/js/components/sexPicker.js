/**
 *  adds vertically stacked buttons as a bot response
 * @param {Array} suggestions buttons json array
 */
 //#########Temporary 1##############################>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
// Function to show the form and overlay, and disable chat input
function showForm() {
  document.getElementById('formTable').style.display = 'block';
  document.getElementById('overlay').style.display = 'block';
  document.querySelector('.chats').style.pointerEvents = 'none'; // Disable interaction with chat
  document.getElementById('userInput').disabled = true; // Disable chat input
}

// Function to hide the form and overlay, and enable chat input
function hideForm() {
  document.getElementById('formTable').style.display = 'none';
  document.getElementById('overlay').style.display = 'none';
  document.querySelector('.chats').style.pointerEvents = 'auto'; // Enable interaction with chat
  document.getElementById('userInput').disabled = false; // Enable chat input
}

// Example function to handle form submission
function submitForm() {
  const maleCount = document.getElementById('male_count').value;
  const femaleCount = document.getElementById('female_count').value;
  const childrenCount = document.getElementById('children_count').value;

  const formData = `male_count=${maleCount},female_count=${femaleCount},child_count=${childrenCount},`;

  // Send form data to Rasa bot
  sendMessageToRasa(formData);

  // Hide the form after submission
  hideForm();
}

// Function to handle bot actions
function handleBotAction(action) {
  if (action === 'trigger_date_form') {
      showForm();
  }
}

//#######################Temporary 1<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

function addSuggestion(suggestions) {
    setTimeout(() => {
        const suggLength = suggestions.length;
        $(
            ' <div class="singleCard"> <div class="suggestions"><div class="menu"></div></div></diV>',
        )
            .appendTo(".chats")
            .hide()
            .fadeIn(1000);
        // Loop through suggestions
        for (let i = 0; i < suggLength; i += 1) {
            $(
                `<div class="menuChips" data-payload='${suggestions[i].payload}'>${suggestions[i].title}</div>`,
            ).appendTo(".menu");
        }
        scrollToBottomOfResults();
    }, 1000);
}


// on click of suggestion's button, get the title value and send it to rasa
$(document).on("click", ".menu .menuChips", function () {
    const text = this.innerText;
    const payload = this.getAttribute("data-payload");
    console.log("payload: ", this.getAttribute("data-payload"));
    setUserResponse(text);
    send(payload);

    // delete the suggestions once user click on it.
    $(".suggestions").remove();
});
