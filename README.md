```markdown
# 🚀 Setup and Usage Instructions

## 📦 Installation Guide

### 1. Prerequisites

- ✅ **Python 3.10.11** is required  
  (Rasa only works with Python <= 3.10)

- 💻 **Download or clone** the project directory:  
  `SihTicketingBot`

---

### 2. Install Python 3.10.11

If you don't already have Python 3.10.11:

- Download it from:  
  [https://www.python.org/downloads/release/python-31011/](https://www.python.org/downloads/release/python-31011/)

- ✅ On Windows: **Make sure to check "Add Python to PATH"** during installation.

---

### 3. Create a Virtual Environment with Python 3.10.11

#### ➤ Option A (If `python3.10` is available in your terminal):

```bash
python3.10 -m venv .venv
```

#### ➤ Option B (Use full path to Python 3.10.11):

- **Windows:**
  ```bash
  "C:\Users\YourName\AppData\Local\Programs\Python\Python310\python.exe" -m venv .venv
  ```

- **Mac/Linux:**
  ```bash
  /usr/local/bin/python3.10 -m venv .venv
  ```

#### ➤ Activate the environment:

- **Windows:**
  ```bash
  .venv\Scripts\activate
  ```

- **Mac/Linux:**
  ```bash
  source .venv/bin/activate
  ```

#### ✅ Confirm Python Version:

```bash
python --version
```

Output should be:

```plaintext
Python 3.10.11
```

---

### 4. Install Dependencies

Run the following command:

```bash
pip install -r requirements.txt
```

This installs all required libraries including:
- rasa
- datetime
- dateparser
- word2number
- rapidfuzz
- pytz
- fuzzywuzzy
- pyspellchecker  
...and more.

---

## 🤖 Running the Bot

### 5. Start the Action Server

In the same terminal:

```bash
cd mainBot
rasa run actions
```

You should see:

```plaintext
Action endpoint is up and running on http://0.0.0.0:5055
```

---

### 6. Start the Rasa Server

Open a **new terminal**, activate the environment again, then run:

```bash
cd SihTicketingBot/mainBot
rasa run -m models --enable-api --cors "*" --debug
```

This runs the Rasa backend with API and frontend support.

---

### 7. Run the Chatbot Frontend

1. Go to the `Chatbot-Widget` folder:
   ```bash
   cd ../../Chatbot-Widget
   ```

2. Open `index.html` in a browser by double-clicking it or right-click → **Open with browser**.

---

🎉 All set! Your chatbot is now live and ready to chat.
```
