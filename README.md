# Chatbot SU - RAG FAQ System

## Overview

Chatbot SU is a Retrieval-Augmented Generation (RAG) chatbot system designed to answer questions related to information and services at Silpakorn University.

The system consists of:

* Frontend (React)
* Backend API (FastAPI)
* MySQL (User Management)
* MongoDB (Chat History Storage)
* ChromaDB (Vector Database)
* LLM API
* Docker Compose Deployment

---

## Features

### User Features

* User Registration and Authentication
* Chat with the AI Chatbot
* Available on both Web and LINE platforms

### Admin Features

* Authentication and Access Control
* Dashboard and Statistical Analytics
* RAG Knowledge Base Management (Add / Delete Documents)
* Conversation History Monitoring
* System Prompt Configuration

---

## Screenshots

### Login

![Login](images/login.png)

### Web Chat Interface

![Web Chat Interface](images/web-chat.png)

### LINE Chat Interface
![LINE Chat Interface](images/line-chat.png)

### Admin Dashboard

![Admin Dashboard](images/dashboard.png)

### Form Add Data

![Form Add Data](images/add-data-form.png)

### Data Management

![Data Management](images/manage-data.png)

### Chat History

![Chat History](images/chat-history.png)

### Edit Prompt

![Edit Prompt](images/edit-prompt.png)

---

## System Architecture

```text
Frontend (React)
        │
        ▼
FastAPI Backend
        ├── Authentication
        ├── Chat Service
        ├── RAG Service
        ├── Admin Services (Dashboard, Form Add Data, Data Management, Chat History, Edit Prompt)
        │
        ├── MySQL
        ├── MongoDB
        └── ChromaDB
```

---

## Technologies

### Frontend

* React
* Tailwind CSS

### Backend

* FastAPI

### Databases

* MySQL
* MongoDB
* ChromaDB

### AI

* BAAI/bge-m3 (Embedding Model)
* Typhoon v2.5 30B A3B Instruct
* LangChain
* LangGraph
* Retrieval-Augmented Generation (RAG)

### Deployment

* Docker
* Docker Compose
* Nginx
* Ngrok

---

## Core Technologies

| Category   | Technology                                     |
| ---------- | ---------------------------------------------- |
| Frontend   | React, Tailwind CSS                            |
| Backend    | FastAPI                                        |
| Databases  | MySQL, MongoDB, ChromaDB                       |
| AI         | BAAI/bge-m3, LangChain, LangGraph, Typhoon API |
| Deployment | Docker, Docker Compose, Nginx, Ngrok           |

---

## Project Structure

```text
Chatbot-RAG-FAQ-System
│
├── docker-compose.yml
├── .env.example
├── Backend
│   ├── Dockerfile
│   │
│   └── fastapi
│       ├── requirements.txt
│       │
│       └── app
│           ├── main.py
│           │
│           ├── api
│           │   ├── auth.py
│           │   ├── edit_prompt.py
│           │   ├── insert_and_delete_docs.py
│           │   ├── line_webhook.py
│           │   ├── web_chatbot.py
│           │   ├── web_conversation.py
│           │   └── web_dashboard.py
│           │
│           ├── config
│           │   └── prompt.py
│           │
│           ├── crud
│           │   ├── conversation.py
│           │   ├── dashboard.py
│           │   ├── database.py
│           │   ├── db_manager.py
│           │   ├── edit_prompt.py
│           │   ├── user.py
│           │   └── web_history.py
│           │
│           ├── images
│           │   └── line-chatbot-rich-menu.jpg
│           │
│           ├── models
│           │   ├── mongo_models.py
│           │   └── mysql_models.py
│           │
│           ├── schemas
│           │   ├── chat.py
│           │   ├── dashboard.py
│           │   ├── node_prompt.py
│           │   ├── upload.py
│           │   └── user.py
│           │
│           └── services
│               └── llm
│                   ├── test_chat_rag_memory.py
│                   └── docs-FAQ
│
└── Frontend
    ├── Dockerfile
    │
    ├── api
    │   └── Userapi.js
    │
    ├── component
    │   ├── AdminSidebar.jsx
    │   ├── ConfirmPromptModal.jsx
    │   ├── HistoryChatModal.jsx
    │   ├── HistoryTable.jsx
    │   ├── Loginfrom.jsx
    │   ├── Navbar.jsx
    │   ├── OverviewStatCard.jsx
    │   ├── PromptSection.jsx
    │   ├── QuestionCategoryBarChart.jsx
    │   ├── UserSourcePieChart.jsx
    │   └── UserTrendLineChart.jsx
    │
    ├── Page
    │   ├── ChatHistoryPage.jsx
    │   ├── Chatpage.jsx
    │   ├── DashboardPage.jsx
    │   ├── EditPromptPage.jsx
    │   ├── Homepage.jsx
    │   ├── ManageDataPage.jsx
    │   ├── Registerpage.jsx
    │   └── ViewDocsPage.jsx
    │
    ├── service
    │   └── Auth.jsx
    │
    └── src
        ├── App.jsx
        └── main.jsx
```

---

## Environment Variables

Create a `.env` file and configure the following variables:

```env
# MySQL Configuration

MYSQL_ROOT_PASSWORD=your_password
MYSQL_DATABASE=your_database_name
MYSQL_USER=your_username
MYSQL_PASSWORD=replace_with_your_mysql_password

# Ngrok Configuration

NGROK_AUTHTOKEN=replace_with_your_ngrok_auth_token
NGROK_DOMAIN=replace_with_your_ngrok_domain

# Backend Configuration

# Make sure the password in DATABASE_URL matches MYSQL_PASSWORD above
DATABASE_URL=mysql+pymysql://your_username:replace_with_your_mysql_password@mysql:3306/your_database_name

# MongoDB Configuration

MONGO_URL=mongodb://mongodb:27017/

# LINE Messaging API Configuration

ACCESS_TOKEN=replace_with_your_line_access_token
CHANNEL_SECRET=replace_with_your_line_channel_secret

# LLM API Configuration

TYPHOON_API_KEY=replace_with_your_typhoon_api_key

# Default Admin Account

ADMIN_USERNAME=replace_with_admin_username
ADMIN_EMAIL=replace_with_admin_email
ADMIN_PASSWORD=replace_with_admin_password
```

---

## Installation

### Clone Repository

```bash
git clone https://github.com/ArnutDev/chatbot-rag-faq-system.git
cd chatbot-rag-faq-system
```

### Build and Run Containers

```bash
docker compose up -d --build
```

### Stop Containers

```bash
docker compose down
```

---

## Default Ports

| Service    | Port  |
| ---------- | ----- |
| Frontend   | 5173  |
| FastAPI    | 8000  |
| MySQL      | 3306  |
| phpMyAdmin | 8080  |
| MongoDB    | 27017 |
| ChromaDB   | 4000  |

---

## First Startup

When the system starts for the first time, the backend will:

1. Wait for MySQL to become available.
2. Automatically create database tables.
3. Create the default administrator account using environment variables.
4. Check the ChromaDB vector database.
5. Insert initial RAG data if the database is empty.

---

## API Documentation

Swagger UI:

```text
http://localhost:8000/docs
```

---

## Contributors

### Arnut Buadonpai

Responsible for:

* LINE Messaging API Integration
* Admin Dashboard
* Chat History Management
* Prompt Configuration Management
* RAG System Development

### Team Member

Responsible for:

* Chat Interface
* Authentication and Login System
* RAG Knowledge Base Management
* Data Submission Forms
* RAG System Development

---

## License

This project was developed for educational and research purposes.
