# 🚀 Swiggy Smart Agent  
### AI-Powered Autonomous Commerce Assistant

---

## 🧠 Overview

Swiggy Smart Agent is an AI-powered assistant designed to automate everyday food ordering, grocery purchases, and dining bookings. Instead of manually browsing apps, users can simply express their intent, and the agent intelligently executes actions using Swiggy services.

Built with an agentic approach, this system moves beyond chat-based interaction to real-world execution.

---

## 🎯 Problem Statement

Users repeatedly perform similar actions on food delivery and grocery platforms:
- Ordering the same meals
- Restocking common items
- Searching for dining options  

This leads to friction, time consumption, and decision fatigue.

---

## 💡 Solution

Swiggy Smart Agent learns user preferences and automates workflows such as:
- Scheduled food ordering  
- Smart grocery restocking  
- Context-aware dining recommendations  

The system transforms user intent into actionable workflows using AI.

---

## ⚙️ Key Features

- 🤖 **AI Intent Recognition**  
  Understands natural language commands like:  
  *“Order my usual dinner at 8 PM”*

- 🔁 **Automated Workflows (Agentic Execution)**  
  Converts intent into actions such as:
  - Food ordering
  - Grocery purchasing
  - Dining bookings  

- 🧩 **Reusable Skills**
  - Reorder previous meals  
  - Weekly grocery restock  
  - Budget-based restaurant selection  

- ⏰ **Scheduling & Habit Learning**
  - Learns recurring patterns  
  - Automates daily/weekly tasks  

- 🌐 **Web Interface (MVP)**
  - Simple UI for interaction  
  - Real-time response simulation  

---

## 🏗️ Architecture Overview
User Input (Text / Command)
↓
AI Agent Layer (LLM Processing)
↓
Intent Detection & Decision Engine
↓
Skill Mapping Layer
↓
MCP API Integration (Swiggy Services)
↓
Execution (Order / Booking / Purchase)

---

## 🔧 Tech Stack

- **Backend:** FastAPI  
- **Frontend:** HTML / CSS / JavaScript (MVP)  
- **AI Layer:** Rule-based intent + agentic execution (LLM integration planned)  
- **Storage:** JSON store for user profile + order memory  
- **Deployment:** Local / container-ready  

---

## 🔌 MCP Integration (Planned)

This project is designed to integrate with:

- 🍔 Swiggy Food → Order meals  
- 🛒 Swiggy Instamart → Grocery purchases  
- 🍽️ Swiggy Dineout → Dining reservations  

The agent will use MCP tools to execute real-world actions.

---

## 🧪 Current Status

🚧 MVP in development  

- Basic UI implemented  
- Intent recognition logic in progress  
- API simulation for actions  

---

## 📸 Demo (To be added)

- Live Demo: *(Add link)*  
- Video Walkthrough: *(Add link)*  

---

## 📂 Project Structure

SWIGGY-AGENT/
│── backend/
│   ├── main.py
│   ├── requirements.txt
│   └── agent/
│       ├── __init__.py
│       ├── config.py
│       ├── intent.py
│       ├── integrations.py
│       ├── memory.py
│       ├── models.py
│       ├── orchestrator.py
│       └── skills.py
│
│── frontend/
│   ├── app.js
│   ├── index.html
│   └── styles.css
│
│── README.md


---

## 🚀 Future Enhancements

- Real MCP API integration with Swiggy Builders Club  
- Voice-based interaction  
- Personalized recommendation engine  
- Multi-user collaborative ordering  
- Mobile application  

---

## 🤝 Why This Project Matters

This project represents a shift from:

> “AI that suggests” → “AI that executes”

It demonstrates how agentic systems can bridge the gap between user intent and real-world services.

---

## 📬 Contact

**ANISH KARTHIC**  
📧 anishkarthicvs@gmail.com  

---
**Trying to complete this is to get an offer from Swiggy u can also contribute**
## ⭐ Acknowledgement

Inspired by the vision of agentic commerce and Swiggy's developer ecosystem.

---

## ⚖️ License

MIT License

---

## How to Run

### 1. Backend

First, you need to have Python and `pip` installed.

1.  Navigate to the `backend` directory:
  ```bash
  cd backend
  ```

2.  Install the required packages:
  ```bash
  pip install -r requirements.txt
  ```

3.  Run the FastAPI server:
  ```bash
  uvicorn main:app --reload
  ```
  The backend will be running at `http://127.0.0.1:8000`.

### 2. Frontend

Option A: use the backend-served UI at `http://127.0.0.1:8000`.

Option B: open `frontend/index.html` directly in your browser.

### 3. Optional Environment Variables

- `SWIGGY_MODE` (default: `mock`)
- `SWIGGY_API_BASE_URL` (default: `https://www.swiggy.com`)
- `DEFAULT_CITY`, `DEFAULT_ADDRESS`, `DEFAULT_RESTAURANT`
- `DEFAULT_DINE_RESTAURANT`, `DEFAULT_DINE_TIME`, `DEFAULT_PARTY_SIZE`
- `DEFAULT_BUDGET`, `DEFAULT_CUISINE`

## Example Inputs

-   "Order pizza at 8 PM"
-   "Buy milk and bread"
-   "Book dinner for 2 tomorrow"
-   "Reorder last meal"
-   "Track my order"
-   "Cancel order #1234"
-   "Apply coupon SAVE20"
