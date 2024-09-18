
/* module for importing other js files */
function include(file) {
  const script = document.createElement('script');
  script.src = file;
  script.type = 'text/javascript';
  script.defer = true;

  document.getElementsByTagName('head').item(0).appendChild(script);
}
/* import components */
include('./static/js/components/index.js');


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
  const formData = {
      male_count: document.getElementById('male_count').value,
      female_count: document.getElementById('female_count').value,
      children_count: document.getElementById('children_count').value,
  };

  // Send form data to Rasa bot
  sendMessageToRasa('form_submission', formData);

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
// Bot pop-up intro
document.addEventListener("DOMContentLoaded", () => {
  const elemsTap = document.querySelector(".tap-target");
  // eslint-disable-next-line no-undef
  const instancesTap = M.TapTarget.init(elemsTap, {});
  instancesTap.open();
  setTimeout(() => {
    instancesTap.close();
  }, 4000);
});



window.addEventListener('load', () => {
  // initialization
  $(document).ready(() => {
    // Bot pop-up intro
    $("div").removeClass("tap-target-origin");




    // drop down menu for close, restart conversation & clear the chats.
    $(".dropdown-trigger").dropdown();

    // initiate the modal for displaying the charts,
    // if you dont have charts, then you comment the below line
    $(".modal").modal();
//     enable this if u have configured the bot to start the conversation.
     showBotTyping();
     $("#userInput").prop('disabled', true);



    // if you want the bot to start the conversation
     triggerAction()
  });
  // Toggle the chatbot screen
  $("#profile_div").click(() => {
    $(".profile_div").toggle();
    $(".widget").toggle();
  });

  // clear function to clear the chat contents of the widget.
  $("#clear").click(() => {
    $(".chats").fadeOut("normal", () => {
      $(".chats").html("");
      $(".chats").fadeIn();
    });
  });

  // close function to close the widget.
  $("#close").click(() => {
    $(".profile_div").toggle();
    $(".widget").toggle();
    scrollToBottomOfResults();
  });
});
