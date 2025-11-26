# 🔐 Secure Entity Scanner – Mini Intelligence Platform

A Python-based intelligence platform that analyzes digital identities (email, username, phone) by generating related entities, mapping their relationships, and producing a risk assessment. This project simulates how real-world OSINT (Open Source Intelligence) and security analysis systems work.

---

## 🚀 Project Overview

Secure Entity Scanner allows users to:

* Scan digital entities (email, username, phone)
* Automatically generate related data
* Visualize relationships using a graph database
* Perform semantic similarity search
* Generate AI-based risk summaries

This project is designed to showcase skills in:

* Python backend development
* Microservice-style architecture
* Graph-based intelligence systems
* AI integration
* Real-world security workflows

---

## 🧠 How It Works

1. User submits an entity (e.g., email)
2. System generates related entities such as:

   * Username
   * Domain
   * Simulated breach record
3. All entities are linked in a graph
4. Data is analyzed
5. A risk level (Low / Medium / High) is generated

Example relationship:

Email → Username → Domain → Breach

---

## 🛠️ Tech Stack

| Technology            | Purpose                          |
| --------------------- | -------------------------------- |
| Python                | Core backend language            |
| FastAPI               | REST API framework               |
| PostgreSQL            | Structured data storage          |
| Neo4j                 | Graph relationship storage       |
| Sentence Transformers | Vector embeddings                |
| Docker                | Service containerization         |
| OpenAI API            | AI-based risk summary (optional) |

---

## 📁 Project Structure

```
secure-entity-scanner/
│
├── app/
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── database.py
│   ├── graph.py
│   ├── vector_store.py
│   ├── ai_summary.py
│   └── services.py
│
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

---

## ⚙️ Features

* ✅ Entity scanning & storage
* ✅ Graph relationship creation
* ✅ Risk evaluation system
* ✅ Semantic search
* ✅ AI-based summary generation
* ✅ Swagger API documentation

---

## ▶️ How to Run the Project

### 1. Start Docker Services

```bash
docker compose up -d
```

### 2. Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Create .env File

```bash
copy .env.example .env
```

Edit `.env` if needed.

### 5. Run the Server

```bash
python -m uvicorn app.main:app --reload
```

Open browser:

```
http://127.0.0.1:8000/docs
```

---

## 🧪 API Endpoints

| Method | Endpoint               | Description                |
| ------ | ---------------------- | -------------------------- |
| POST   | /scan                  | Scan and analyze entity    |
| GET    | /entities              | List all entities          |
| GET    | /entities/{id}         | Get entity details         |
| GET    | /entities/{id}/graph   | View relationship graph    |
| GET    | /search                | Semantic similarity search |
| GET    | /entities/{id}/summary | Risk summary               |

---

## 📊 Sample Output

```json
{
  "risk_level": "Medium",
  "summary": "The entity is linked to suspicious domain and breach records.",
  "key_signals": [
    "Appears in breach data",
    "Connected to suspicious domain",
    "Username used multiple times"
  ]
}
```

---

## 🎯 Use Case

This project simulates how intelligence platforms analyze digital identities to detect suspicious behavior. It can be used for:

* Cybersecurity research
* OSINT analysis
* Security monitoring
* Academic projects

---

## 📌 Future Improvements

* Frontend UI for graph visualization
* Real OSINT API integration
* Authentication system
* Role-based access control
* Real-time threat monitoring

---

## 👨‍💻 Author

**Bikash Yadav**
Aspiring Python Developer & Security Systems Enthusiast

GitHub: [https://github.com/bikas-yadav](https://github.com/bikas-yadav)

---

## ⭐ If you like this project

Give it a star on GitHub and feel free to fork or contribute!

---

### ✅ Perfect for showcasing to recruiters and security tech companies
