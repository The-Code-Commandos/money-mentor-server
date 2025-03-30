# 📌 MoneyMentor API
An Intuitive and simple fintech service to help users save and investments.It help beginners overcome fear and take their first steps in saving and investing. This service seamlessly integrates with **Achieve’s financial features** (DigiSave, Eurobond, Goal-Oriented Investments) by offering:  
✅ **Micro-Challenges** – Small, personalized tasks to build habits.  
✅ **Jargon-Free Education** – Simple explanations of investment concepts.  
✅ **Investment Simulations** – “What If?” trials with fake money.  

---

## 🚀 Features
- **User Quiz & Data Storage:** Collects user income, fears, and goals.  
- **AI-Generated Challenges:** Small tasks based on user financial profile.  
- **Progress Tracking:** Monitors challenge completion.  

---

## 🛠️ Tech Stack
- **Backend:** FastAPI (Python)  
- **Database:** SQLite  
- **AI Logic:** Open Source LLM , Llama3.2 for challenge recommendations

---

## 🔧 Setup & Installation
### 1️⃣ Clone the Repository
```bash
git clone https://github.com/The-Code-Commandos/money-mentor-server.git
cd money-mentor-server
```

### 2️⃣ Create & Activate a Virtual Environment
#### Windows:
```bash
python -m venv venv
venv\Scripts\activate
```
#### macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Set Up the Database
```bash
python
>>> from database import Base, engine
>>> Base.metadata.create_all(engine)
>>> exit()
```

### 5️⃣ Run the API
```bash
uvicorn app.main:app --reload
```

### 6️⃣ Test in Swagger UI
Once running, access API docs at 👉 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 📡 API Endpoints
### 1️⃣ Simulations
| Method | Endpoint      | Description |
|--------|--------------|-------------|
| `GET` | `/sims/{fund}`    | Runs a financial simulation for a specific fund(portfolio) |

### 2️⃣ Challenges
| Method | Endpoint          | Description |
|--------|------------------|-------------|
| `POST` | `/challenges/`   | Generate a micro-challenge using llama3.2 |
| `GET`  | `/challenges/{user_id}` | Get a challenge for a user |
| `GET`  | `/challenges/` | Get all challenges for a user |
| `POST`  | `/challenges/update-progress/{challenge-id}` | Get all challenges for a user |
| `GET`  | `/challenges/nudges/check` | Checks inactive users and nudges them |
| `GET`  | `/challenges/nudge/trigger` | Manually triggers a nudge check in the background |




---

## 📌 Next Steps
- ✅ **JWT Authentication** 🔐  
- ✅ **Behavioural Nudge and Rewards Implementation**
- ✅ **AI Challenge Recommendation Enhancement** 🤖  
- ✅ **Deployment (Render, Railway, or Fly.io)** 🚀  

---
