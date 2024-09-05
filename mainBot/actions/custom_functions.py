import re
import dateparser
from word2number import w2n
from rapidfuzz import process
import pytz
from datetime import datetime, timedelta
import uuid
import mysql.connector
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

#rasa run -m models --enable-api --cors "*" --debug



#>>>>Start: code to convert number of tickets from string to integer
# Dictionary of written numbers and their numeric equivalents
written_number_map = {
    'zero': 0,
    'one': 1, 'on': 1, 'onee': 1, 'oen': 1,
    'two': 2, 'to': 2, 'tw': 2, 'tow': 2, 'too': 2, 'tuo': 2, 'twe': 2, 'twu': 2,
    'three': 3, 'tree': 3, 'thre': 3, 'turee': 3,
    'four': 4, 'for': 4, 'fou': 4, 'foor': 4, 'fuor': 4,
    'five': 5, 'fiv': 5, 'fife': 5, 'fiive': 5, 'fivve': 5,
    'six': 6, 'sik': 6, 'sics': 6, 'sx': 6, 'sxi': 6, 'siks': 6,
    'seven': 7, 'sevn': 7, 'sevan': 7, 'sevven': 7, 'sevin': 7,
    'eight': 8, 'eigt': 8, 'eigth': 8, 'eit': 8, 'eite': 8,
    'nine': 9, 'nien': 9, 'nin': 9, 'ninne': 9, 'niine': 9,
    'ten': 10, 'tne': 10, 'tn': 10, 'tenn': 10, 'tehn': 10,
    'eleven': 11, 'elven': 11, 'elevan': 11, 'eleve': 11, 'elefen': 11,
    'twelve': 12, 'twleve': 12, 'twelv': 12, 'twel': 12, 'twellve': 12, 'twelf':12,
    'thirteen': 13, 'thirtean': 13, 'thirtn': 13, 'thirten': 13, 'thrteen': 13,
    'fourteen': 14, 'fourten': 14, 'forteen': 14, 'fourtin': 14, 'foruten': 14,
    'fifteen': 15, 'fiften': 15, 'fiftenn': 15, 'fifeten': 15, 'fifteenss': 15,'fyfteen': 15,'fivteen': 15
}

def fuzzy_match_number(text):
    match = process.extractOne(text, written_number_map.keys())
    if match:
        matched_word, score, _ = match # Changed from 4 values to 3
        if score > 80:  # Adjust threshold for accuracy
            return written_number_map[matched_word]
    return None

def extract_and_convert_ticket(text: str) -> int:
    # Strip leading and trailing whitespace
    text = text.strip()

    # Check for numeric digits
    numeric_match = re.search(r'\b\d+\b', text)
    if numeric_match:
        return int(numeric_match.group(0))

    # Checking for written numbers
    number_text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    try:
        return w2n.word_to_num(number_text)
    except ValueError:
        # Handling potential spelling errors using fuzzy
        words = number_text.split()
        total = 0
        for word in words:
            if word in written_number_map: # Check if the word is actually a number
                matched_number = fuzzy_match_number(word)
                if matched_number is not None:
                    total += matched_number
        if total > 0:
            return total
    return 0
#<<<<End:Code to convert number of tickets from string to integer

#>>>>Start: Code to convert date of any format into DD/MM/YYYY string
def convert_to_date(date_str: str) -> str:
    # Define timezone
    ist = pytz.timezone('Asia/Kolkata')
    days_of_week = {
        'monday': 0, 'mon': 0,
        'tuesday': 1, 'tue': 1,
        'wednesday': 2, 'wed': 2,
        'thursday': 3, 'thurs': 3, 'thur': 3,
        'friday': 4, 'fri': 4,
        'saturday': 5, 'sat': 5, 'satur': 5,
        'sunday': 6, 'sun': 6
    }

    try:
        # Normalize and parse the date
        date_str = date_str.lower()
        parsed_date = dateparser.parse(date_str)

        # Handle cases where the year is not provided
        current_year = datetime.now(ist).year
        if parsed_date and parsed_date.year < current_year:
            parsed_date = parsed_date.replace(year=current_year)

        # Check if the date is valid
        if not parsed_date:
            raise ValueError("Invalid date format")

        # Get current date and make parsed_date timezone-aware
        current_date = datetime.now(ist).date()
        parsed_date = ist.localize(parsed_date).date()

        # Check if the date is older than today
        if parsed_date < current_date:
            return "old date"

        return parsed_date.strftime("%d/%m/%Y")  # Return the date in DD/MM/YYYY format

    except ValueError:
        # Handle specific relative date cases
        today = datetime.now(ist).date()

        # Check for "next day"
        if 'next day' or 'coming day' in date_str:
            parsed_date = today + timedelta(days=1)
            return parsed_date.strftime("%d/%m/%Y")

        # Check for "next {day_name}"
        for day_name, day_index in days_of_week.items():
            if f'next {day_name}' in date_str:
                today_weekday = today.weekday()
                days_until_target = (day_index - today_weekday + 7) % 7
                if days_until_target == 0:
                    days_until_target = 7  # To get the next occurrence of the same day
                parsed_date = today + timedelta(days=days_until_target)
                return parsed_date.strftime("%d/%m/%Y")

        # Check for 'x days from now'
        match = re.search(r'(\d+)\s+days?\s+from\s+now', date_str)
        if match:
            days_from_now = int(match.group(1))
            parsed_date = today + timedelta(days=days_from_now)
            return parsed_date.strftime("%d/%m/%Y")

        # If none of the above conditions are met
        return "Invalid date format"

    except Exception as e:
        # Handle unexpected errors
        return f"Error occurred: {str(e)}"

def cidgen():
    return str(uuid.uuid4())

def addData(new):
    mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "qwerty1234@#",
    database = "Users"
    )
    cursor = mydb.cursor()
    insert_query = "INSERT INTO users (booking_date, customer_id, customer_name, customer_email, total_tickets, indian_bookings, foreign_bookings) VALUES (%s, %s, %s, %s, %s, %s, %s)"

    cursor.execute(insert_query, new)

    mydb.commit()
    mydb.close()

def sendQRViaEmail(img_path, img_name, email):
    # Compose the email
    img_path = "mainBot/qr_codes/1234567890.png"
    img_name = os.path.basename(img_path)
    msg = MIMEMultipart()
    sender_email = "sihticketingbot@outlook.com"
    receiver_email = "dhondupnerchung@gmail.com"
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = 'Your QR Code for the Ticket Booking'
    body = 'Please find your QR code attached to this email.'
    msg.attach(MIMEText(body, 'plain'))

    # Attach the QR code image
    with open(img_path, 'rb') as attachment:
        part = MIMEApplication(attachment.read(), Name=os.path.basename(img_path))
        part['Content-Disposition'] = f'attachment; filename="{img_name}"'
        msg.attach(part)

    # Convert the message to string format
    text = msg.as_string()

    # Set up the email server (Outlook SMTP)
    server = smtplib.SMTP('smtp.office365.com', 587)
    server.starttls()

    # Log in to the server
    server.login(sender_email, 'paneerlababdar9999@#')

    # Send the email
    server.sendmail(sender_email, receiver_email, text)

    # Quit the server
    server.quit()

    # Optionally, remove the QR code file after sending the email
    os.remove(img_path)
