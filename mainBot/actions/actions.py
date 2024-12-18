import re
from datetime import datetime
from typing import Any, Text, Dict, List

import qrcode
from rasa_sdk import Action, Tracker
from rasa_sdk import FormValidationAction
from rasa_sdk.events import SlotSet, SessionStarted, EventType
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict

from .custom_functions import extract_and_convert_ticket, convert_to_date, cidgen, add_data, sendQRViaEmail

# from sqlalchemy.testing.util#Divyansh what is this do we need this

#Global variable>>
MAX_TICKET_ALLOWED= 15
MIN_TICKET_ALLOWED=1

INDIAN_NATIONAL_PRICE = 20 #price in rupees
NON_INDIAN_NATIONAL_PRICE = 500 #price in rupees

NATIONAL_SUICIDE_PREVENTION_NUMBER=9152987821
NATIONAL_EMERGENCY_NUMBER=102
POLICE_STATION=100
FIRE_STATION=101
AMBULANCE=102

UPI_LINK = f"https://upload.wikimedia.org/wikipedia/commons/d/d0/QR_code_for_mobile_English_Wikipedia.svg"
MUSEUM_LOCATION = f"https://maps.app.goo.gl/csKfa2B4vFSL6kHU6"

#<<<Global Variables

class TicketPrice(Action): #return default ticket price

    def name(self) -> Text:
        return "action_return_price"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(
            text=(
                f"Pricing Details:<br>"
                f"Indian Nationals: ₹{INDIAN_NATIONAL_PRICE}<br>"
                f"Foreigners: ₹{NON_INDIAN_NATIONAL_PRICE}"

            ),
            buttons = [
                {"title": "Buy Ticket", "payload": "/book_ticket"},
            ],
        )

        return []

class MaxTicketLimit(Action): # tells the user maximum number of ticket that it can purchase

    def name(self) -> Text:
        return "action_max_ticket_allowed"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        message = (
            f"Sorry, you can book a maximum of {MAX_TICKET_ALLOWED} tickets. "
            f"If you're attending with a large group or academic institution, "
            f"please email us to arrange your booking."
        )
        dispatcher.utter_message(message)
        return []

class ValidateTicketBookingForm(FormValidationAction): # to validate the form
    def name(self) -> Text:
        return "validate_ticket_booking_form"

    def validate_number(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
    ) -> Dict[Text, Any]:
        # Convert the slot value to a numeric value
        numeric_slot_value = extract_and_convert_ticket(str(slot_value))
        if numeric_slot_value > MAX_TICKET_ALLOWED or numeric_slot_value < MIN_TICKET_ALLOWED:
            dispatcher.utter_message(text=f"Sorry, you can book {MAX_TICKET_ALLOWED} tickets at max.")
            return {"number": None}

        dispatcher.utter_message(text=f"Great! {numeric_slot_value} tickets.")
        return {"ticket_count": numeric_slot_value, "number": numeric_slot_value}

    def validate_date(self,
                      slot_value: Any,
                      dispatcher: CollectingDispatcher,
                      tracker: Tracker,
                      domain:  DomainDict,
                      )-> Dict[Text, Any]:
        # Convert and validate the extracted date
        formatted_date = convert_to_date(slot_value)

        if formatted_date == "Invalid date format" or formatted_date == "old date":
            dispatcher.utter_message(
                text="Looks like the date is invalid. Can you give it in DD/MM/YYYY format?"
            )
            return {"date": None}

        return {"date": formatted_date}

    def validate_client_name(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        # Define the regex pattern for a valid name
        pattern = r'^[A-Za-z]{2,}(?:\s[A-Za-z]{2,})?$'

        # Check if the name matches the regex pattern
        if re.match(pattern, slot_value):
            dispatcher.utter_message(text=f"Nice to meet you, {slot_value.strip().upper()}!")
            return {"client_name": slot_value}
        else:
            dispatcher.utter_message(
                text="Sorry, can you please repeat."
            )
            return {"client_name": None}

    def validate_email(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        # Define the regex pattern for a valid email address
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        # Check if the email matches the regex pattern
        if re.match(pattern, slot_value):
            slot_value=slot_value.strip().lower()
            dispatcher.utter_message(text=f"Ok, got your email")
            return {"email": slot_value}
        else:
            dispatcher.utter_message(
                text="Invalid email"
            )
        return {"email": None}

###>action to show booking details
class BookingDetails(Action):
    def name(self) -> str:
        return "action_booking_details"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> List[Dict[str, Any]]:
        # Extract and handle ticket count
        ticket_count_slot = tracker.get_slot("ticket_count")
        try:
            #ticket_count = extract_and_convert_ticket(str(ticket_count_slot))
            ticket_count = ticket_count_slot

        except (ValueError, TypeError) as e:
            dispatcher.utter_message(text="Sorry, having problem with ticket count")
            return []

        # Extract and handle date
        date_slot = tracker.get_slot("date")
        try:
            date = date_slot
#           #date = convert_to_date(date_slot)

        except (ValueError, TypeError) as e:
            dispatcher.utter_message(text="Sorry, having problem with date")
            return []

        # Extract and handle foreigner count
        foreigner_count_slot = tracker.get_slot("foreigner_count")
        if foreigner_count_slot is None:
            foreigner_count_slot=0
        try:
            foreigner_count = foreigner_count_slot
            #foreigner_count = extract_and_convert_ticket(str(foreigner_count_slot))

        except (ValueError, TypeError) as e:

            dispatcher.utter_message(text="Sorry, having problem with foreigner count")
            return []

        # Calculate local count
        try:
            local_count = int(ticket_count) - int(foreigner_count)
        except (ValueError, TypeError) as e:
            dispatcher.utter_message(text="Sorry, having problem with indian count")
            return []
        try:
            client_name_slot=tracker.get_slot("client_name")
            formated_client_name=client_name_slot.strip().upper()
        except (ValueError,TypeError) as e:
            dispatcher.utter_message(text="Sorry, having problem with name")
            return []
        try:
            email_slot=tracker.get_slot("email")
            formatted_email=email_slot.strip().lower()
        except(ValueError,TypeError) as e:
            dispatcher.utter_message(text="Sorry, having problem with email")
            return []
        try:
            indian_price = (local_count * INDIAN_NATIONAL_PRICE)
            foreigner_price = (foreigner_count * NON_INDIAN_NATIONAL_PRICE)
            total_price = indian_price + foreigner_price
        except(ValueError,TypeError) as e:
            dispatcher.utter_message(text="Sorry, having problem with price calculation")
            return []

        # Format and send the message

        dispatcher.utter_message(
            text = ( f"Booking Details:<br>\n"
                        f"Name: {formated_client_name}<br>\n"
                        f"Email: {formatted_email}<br>\n"
                        f"Date of Visit: {date}<br>\n"
                        f"Indians: {local_count}<br>\n"
                        f"Indian Price: {indian_price}<br>"
                        f"Foreigners: {foreigner_count}<br>"
                        f"Foreigner Price: {foreigner_price}<br>"
                        f"Total Ticket: {ticket_count}<br>\n "
                        f"Total Price: ₹{total_price}<br>\n"
            ),
            buttons=
            [
                {"title": "Pay", "payload": "/payment_confirmation"},
                {"title": "Cancel", "payload": "/utter_ask_for_change"},
            ]
        )

        return []

#>>>>Action redirected to payment gateway(function to go to payment gateway)
##>>>we have to use this function to store data to the backend
class RedirectPaymentGateWay(Action):
    def name(self) -> str:
        return "action_redirect_to_payment"
    def run(
        self,
        dispatcher: "CollectingDispatcher",
        tracker: Tracker,
        domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        ticket_count = extract_and_convert_ticket(str(tracker.get_slot("ticket_count")))
        foreigner_count = extract_and_convert_ticket(str(tracker.get_slot("foreigner_count")))
        indian_count = ticket_count - foreigner_count

        total_price = (foreigner_count * NON_INDIAN_NATIONAL_PRICE) + (indian_count * INDIAN_NATIONAL_PRICE)

        dispatcher.utter_message(f"Please scan the QR code to complete the payment. The total price is ₹{total_price}.",UPI_LINK)
        return []
class SelfHarmPrevention(Action):
    def name(self) -> str:
        return "action_contact_self_help"
    def run(
        self,
        dispatcher: "CollectingDispatcher",
        tracker: Tracker,
        domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:

        text=("I'm sorry you're feeling this way.<br>"
              "Please reach out to someone who can help, like a mental health professional or a trusted person.<br>"
              "If you're in danger, contact emergency services.<br>"
              f"National Emergency Number: {NATIONAL_EMERGENCY_NUMBER}<br>"
              f"Police Station: {POLICE_STATION}<br>"
              f"Ambulance: {AMBULANCE}<br>"
              f"Fire Station: {FIRE_STATION}<br>"
              )
        dispatcher.utter_message(text)
        return []
class EmergencyNumbers(Action):
    def name(self) -> str:
        return "action_show_emergency_contacts"
    def run(
        self,
        dispatcher: "CollectingDispatcher",
        tracker: Tracker,
        domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        text=("If there is an emergency, please contact the relevant services immediately:<br> \n"
              f"National Emergency Number: {NATIONAL_EMERGENCY_NUMBER}<br>\n"
              f"Police Station: {POLICE_STATION}<br>\n"
              f"Ambulance: {AMBULANCE}<br>\n"
              f"Fire Station: {FIRE_STATION}<br>"
              )
        dispatcher.utter_message(text)
        return []

class ActionCheckEmail(Action): #it will chekck if we got the email or not
    def name(self) -> str:
        return "action_check_email"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> list:
        email = tracker.get_slot('email')
        if email:
            dispatcher.utter_message(text="I've got your email address")
        else:
            dispatcher.utter_message(text="Could you please repeat your email again?")
        return []


class ClientDetailsInExcel(Action):
    def name(self) -> str:
        return "action_store_slot_value_in_excel"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        try:
            # Retrieve slot values
            client_name = tracker.get_slot("client_name")
            ticket_count = tracker.get_slot("ticket_count")
            date = tracker.get_slot("date")
            foreigner_count =tracker.get_slot("foreigner_count")
            email = tracker.get_slot("email")
            indian_count=int(ticket_count)-int(foreigner_count)

            # Generate a customer ID
            customer_id = cidgen()

            # Make the date SQL ready in yyyy-mm-dd format
            f_date = datetime.strptime(date, "%d/%m/%Y")
            f_date = f_date.strftime("%Y-%m-%d")

            # Prepare the data row
            new_row = (
                f_date,
                str(customer_id),
                client_name,
                int(ticket_count),
                int(indian_count),
                int(foreigner_count),
                email
            )

            # write the new row
            add_data(new_row)
            img = qrcode.make(customer_id)
            img_name = f"{customer_id}.png"
            img_path = "qr_codes/" + img_name
            img.save(img_path)

            # send email with the generated qr code
            sendQRViaEmail(img_path, img_name, email)

            dispatcher.utter_message(text=f"The tickets have been sent to your email:  {email}")

        except Exception as e:
            # Log the exception and notify the user
            dispatcher.utter_message(text="Sorry, I couldn't send the email.")
            # Log the error message (you may want to log this to a file or monitoring service)
            print(f"Error occurred: {e}")

        return []



class ValidateForeignerCountForm(FormValidationAction): # to validate the form
    def name(self) -> Text:
        return "validate_foreigner_count_form"

    def validate_number(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
    ) -> Dict[Text, Any]:
        # Convert the slot value to a numeric value
        ticket_count=tracker.get_slot("ticket_count")
        if ticket_count is None:
            dispatcher.utter_message(text="Please, first provide the ticket count")
            return{"numer":None,"ticket_count": None,}
        else:
            ticket_count=extract_and_convert_ticket(str(ticket_count))

        numeric_slot_value = extract_and_convert_ticket(str(slot_value))
        if numeric_slot_value> ticket_count or numeric_slot_value > MAX_TICKET_ALLOWED or numeric_slot_value < MIN_TICKET_ALLOWED:
            dispatcher.utter_message(text="Great! How many foreign nationals are there?")
            return {"number": None}

        dispatcher.utter_message(text=f"I'll take it from here..")
        return {"foreigner_count": numeric_slot_value, "number": numeric_slot_value}

class SetNumberToNone(Action):
    def name(self) -> Text:
        return "action_set_number_to_zero"
    def run(
        self,
        dispatcher: "CollectingDispatcher",
        tracker: Tracker,
        domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        return [SlotSet("number",None)]


class SetForeigner(Action):
    def name(self) -> Text:
        return "action_set_foreigner"

    def run(
        self,
        dispatcher: "CollectingDispatcher",
        tracker: Tracker,
        domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        # Set the foreigner_count slot to 0
        value=tracker.get_slot("foreigner_count")
        if value is not None:
            return [SlotSet("foreigner_count",value)]
        value = 0
        events = [SlotSet("foreigner_count", value)]

        # Trigger the utter_wonderful action

        return events


class ActionSessionStart(Action):
    def name(self) -> Text:
        return "action_session_start"

    @staticmethod
    def fetch_slots(tracker: Tracker) -> List[EventType]:
        """Collect slots that contain the user's client_name and email."""

        slots = []
        for key in ("client_name", "email","ticket_count","foreigner_count","date","number"):
            value = tracker.get_slot(key)
            if value is not None:
                slots.append(SlotSet(key=key, value=None))
        return slots

    async def run(
      self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:

        # The session should begin with a `session_started` event
        events = [SessionStarted()]

        # Carry over slots if they have values
        events.extend(self.fetch_slots(tracker))

        # Bot introduces itself and offers options
        dispatcher.utter_message(
            text="Hello! I'm Darshan. How can I help you today?",
            buttons=[
                {"title": "Buy Ticket", "payload": "/book_ticket"},
                {"title": "Ticket Price", "payload": "/ticket_price"},
            ],
        )

        # Add `action_listen` at the end as a user message follows
        # events.append(ActionExecuted("action_listen"))

        return events




