# 🚀 Metadata-Driven ETL Orchestration Framework

## 📌 Overview

This project implements a **metadata-driven ETL orchestration framework** inspired by modern tools like Azure Data Factory.
Instead of writing separate scripts for each pipeline, this system dynamically executes pipelines based on metadata stored in a database.

---

## 🎯 Objective

* Build a scalable and maintainable ETL system
* Dynamically orchestrate pipelines using metadata
* Handle multiple data sources (CSV, API, Database)
* Implement dependency management using DAG (Directed Acyclic Graph)
* Support full and incremental data loading
* Maintain audit logs and watermark tracking

---

## 🏗️ Architecture

The system consists of three main services:

### 1. Database (PostgreSQL)

* Stores pipeline metadata (`etl_control`)
* Tracks execution logs (`etl_audit_log`)
* Maintains incremental state (`etl_watermarks`)

### 2. Mock API (FastAPI)

* Simulates real-world API data source
* Supports incremental fetching using query parameter

### 3. Orchestrator (Python)

* Reads metadata from database
* Builds dependency graph (DAG)
* Executes pipelines dynamically
* Logs execution details

---

## ⚙️ Tech Stack

* Python
* PostgreSQL
* FastAPI
* Docker & Docker Compose
* Pandas
* NetworkX

---

## 📂 Project Structure

```
metadata-etl-framework/
│
├── docker-compose.yml
├── .env.example
│
├── orchestrator/
│   ├── main.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── mock_api/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── seeds/
│   └── init.sql
│
└── data/
    └── source_data.csv
```

---

## 🔄 Pipeline Flow

1. Fetch active pipelines from database
2. Build dependency graph using NetworkX
3. Validate DAG (detect cycles)
4. Perform topological sort
5. Execute pipelines in correct order
6. Log results in audit table

---

## 🔌 Supported Sources

| Source Type | Description                 |
| ----------- | --------------------------- |
| CSV         | Reads data from local file  |
| API         | Fetches data from REST API  |
| DB          | Reads from PostgreSQL table |

---

## 🔁 Load Strategies

### 🔹 Full Load

* Truncates destination table
* Reloads complete data

### 🔹 Incremental Load

* Uses watermark (`last_modified`)
* Loads only new records
* Updates watermark after execution

---

## 📊 Audit Logging

Each pipeline execution records:

* Start & End Time
* Status (SUCCESS / FAILED)
* Rows Read / Written
* Error Message

---

## 🔁 Watermark Tracking

* Maintains last processed value per pipeline
* Ensures efficient incremental loading
* Stored in `etl_watermarks` table

---

## ⚠️ Cycle Detection

* Detects circular dependencies automatically
* Prevents execution if cycle exists
* Ensures safe DAG execution

---

## ▶️ How to Run

### 1. Clone Repository

```
git clone <your-repo-url>
cd metadata-etl-framework
```

### 2. Setup Environment

```
copy .env.example .env
```

### 3. Run Application

```
docker-compose up --build
```

---

## ✅ Verification Steps

* Check containers are running
* Connect to PostgreSQL
* Run:

```
SELECT * FROM etl_audit_log;
```

* Verify pipelines executed successfully

---

## 🧪 Features Demonstrated

* Metadata-driven pipeline execution
* Dynamic DAG-based orchestration
* Multi-source data extraction
* Full & incremental loading
* Audit logging and monitoring
* Cycle detection
* Containerized architecture

---

## 📌 Future Enhancements

* Add transformation rules engine
* Implement UPSERT logic
* Add scheduling (cron / APScheduler)
* Build UI for pipeline management

---

## 👨‍💻 Author

Neeraja Palla

---
