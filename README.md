# Smart Electricity Distribution & Management System

A modular Python + SQLite backend system designed to manage electricity consumption, billing, assets, and fault data across a regional distribution network — built as a structured data foundation for ML use cases including consumption forecasting, anomaly detection, and predictive maintenance.

---

## 🤖 ML Potential

This system's rich structured data across 7 interconnected modules creates a natural foundation for machine learning:

| Use Case | Data Available | Approach |
|---|---|---|
| Consumption Forecasting | Monthly meter readings per consumer | ARIMA / LSTM time-series model |
| Anomaly Detection | Consumption patterns across meters | Isolation Forest / Z-score |
| Predictive Maintenance | Asset health history + fault frequency | Random Forest classifier |
| Overdue Payment Risk | Billing history + area type | Logistic Regression |
| Fault Auto-Classification | Fault description text | TF-IDF + Naive Bayes |

---

## 📌 Project Overview

This system provides a centralized platform for electricity distribution companies to manage operations efficiently. It integrates consumer data, infrastructure assets, consumption tracking, automated billing, and fault management into a single cohesive system across 7 normalized modules.

---

## ⚙️ Features

### Module 1 — Area & Consumer Management
- Create and manage distribution areas with priority levels
- Register and track consumers
- Area-wise consumer listing and analysis
- Search functionality for quick consumer lookup

### Module 2 — Asset Management
- Track electrical infrastructure (transformers, poles, cables)
- Monitor asset health status
- Maintenance scheduling and automated alerts
- Asset statistics and reporting

### Module 3 — Meter & Consumption Management
- One-to-one meter-consumer relationship
- Record electricity consumption readings
- Peak and off-peak consumption tracking
- Monthly consumption summaries
- Faulty meter identification

### Module 4 — Billing Management
- Automated bill generation from consumption data
- Area-type-based rate calculation:
  - Residential: ₹5.50/unit
  - Commercial: ₹7.00/unit
  - Industrial: ₹6.50/unit
- Payment tracking, overdue management, revenue analytics

### Module 5 — Fault Management
- Report and track infrastructure faults
- Priority-based fault resolution queue
- Critical fault identification
- Average resolution time tracking

---

## 🛠️ Technologies Used

- **Python 3.x** — Core programming language
- **SQLite** — Database management (built-in, no setup needed)
- **Object-Oriented Programming** — Modular, clean architecture
- **SQL** — Normalized relational schema (3NF)

---

## 📁 Project Structure

```
smart-electricity-system/
├── database/
│   ├── schema.sql              # Database table definitions
│   └── sample_data.sql         # Sample data for testing
├── src/
│   ├── config.py               # Configuration settings
│   ├── database.py             # Database connection handler
│   └── modules/
│       ├── area_consumer.py    # Module 1
│       ├── asset.py            # Module 2
│       ├── meter_consumption.py # Module 3
│       ├── billing.py          # Module 4
│       └── fault.py            # Module 5
├── main.py                     # CLI interface
├── database.py                 # Database setup script
├── requirements.txt
└── README.md
```

---

## 🚀 Installation & Setup

**Prerequisites:** Python 3.7 or higher. No external packages required.

```bash
# 1. Clone the repository
git clone https://github.com/teekshansalgotra-a11y/smart-electricity-system
cd smart-electricity-system

# 2. Initialize the database
python database.py
# Type 'yes' when prompted to load sample data

# 3. Run the application
python main.py
```

---

## 🗄️ Database Schema

7 normalized tables with foreign key constraints and proper indexing:

```
AREA ──────── CONSUMER ──── METER ──── CONSUMPTION
  │               │
  └── ASSET ──── FAULT      CONSUMER ── BILL
```

- **AREA** — Distribution areas with priority levels
- **CONSUMER** — Customer information linked to areas
- **ASSET** — Electrical infrastructure per area
- **METER** — One meter per consumer (1:1 relationship)
- **CONSUMPTION** — Meter readings over time
- **BILL** — Auto-generated bills per consumer
- **FAULT** — Reported infrastructure faults

---

## 📊 Sample Data Included

| Entity | Count |
|---|---|
| Distribution Areas | 5 |
| Consumers | 10 |
| Assets (transformers, poles, cables) | 15 |
| Meters with consumption records | 10 |
| Bills (various payment states) | 10 |
| Fault records | 5 |

---

## 🔑 Key Highlights

**Database Design**
- Normalized schema (3NF) ensuring data integrity
- Foreign key constraints maintaining referential integrity
- Check constraints for data validation

**Code Quality**
- Modular architecture — each module independent and testable
- Graceful error handling and input validation
- Well-commented and documented throughout

**Business Logic**
- Automated billing with area-type-based pricing
- Priority management for areas and fault resolution
- Health monitoring for infrastructure assets
- Overdue tracking with automatic status updates

---

## 📬 Contact

**Teekshan Salgotra**
- 📧 Email: [your email here]
- 💼 LinkedIn: [your LinkedIn here]
- 🐙 GitHub: [teekshansalgotra-a11y](https://github.com/teekshansalgotra-a11y)

---

*B.Tech CSE | VIT Chennai | Open to remote DS/ML internships*
