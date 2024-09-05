

---

# Setup and Usage Instructions

## Installation Guide

### Prerequisites
1. **Download PyCharm** and open it.

2. **In the PyCharm Projects Directory:**
   - Download or paste this directory: `SihTicketingBot`.

3. **Install Dependencies:**
   - **RASA:** `pip install rasa`  
     (Rasa only works on python version <= 3.10.xx)
     (You can directly download python version 3.10.xx from pycharm itself)
   - **Python 3.10.11**

4. **Python Libraries:**
   ```plaintext
   datetime: pip install datetime
   dateparser: pip install dateparser
   word2number: pip install word2number
   rapidfuzz: pip install rapidfuzz
   pytz: pip install pytz
   fuzzywuzzy: pip install fuzzywuzzy
   pyspellchecker: pip install pyspellchecker
   ```

## Training and Running the Model

1. **Change Your Terminal:**
   - Switch your terminal from PowerShell to CMD if you encounter difficulties. You should see something like this:
     ```plaintext
     (.venv) C:\Users\{user_name}\PycharmProjects\SihTicketingBot>
     ```

2. **Start the Action Server:**
   ```plaintext
   (.venv) C:\Users\{user_name}\PycharmProjects\SihTicketingBot> cd mainBot
   (.venv) C:\Users\{user_name}\PycharmProjects\SihTicketingBot\mainBot> rasa run actions
   ```
   - You should see: `2024-08-27 17:55:10 INFO     rasa_sdk.endpoint  - Action endpoint is up and running on http://0.0.0.0:5055`

3. **Train the Model:**
   - Open a new terminal without closing the previous one.
   ```plaintext
   (.venv) C:\Users\{user_name}\PycharmProjects\SihTicketingBot> cd mainBot
   (.venv) C:\Users\{user_name}\PycharmProjects\SihTicketingBot\mainBot> rasa train
   ```

4. **Run the Model:**
   ```plaintext
   rasa shell
   ```
   - This will allow you to interact with the model and see it in action.

5. **Interactive Mode (Optional):**
   ```plaintext
   rasa interactive
   ```
   - Use this to see each step of the bot, guide it if it makes mistakes, and it will remember your corrections(**!!!If you safe it!!!**).

---

Feel free to adjust any specifics or additional instructions as needed!
