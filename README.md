# Smart Electricity Distribution & Management System
A comprehensive database-driven electricity distribution management system built with Python and SQLite, designed to manage areas, consumers, assets, meters, billing, and fault tracking — with a data foundation built to support future ML-driven intelligence.

## Project Overview
This system provides a centralized platform for electricity distribution companies to manage their operations efficiently. It integrates consumer data, infrastructure assets, consumption tracking, automated billing, and fault management into a single cohesive system.
The structured, normalized data it generates across consumption, billing, and fault records makes it a strong candidate for layering in machine learning capabilities — such as consumption forecasting, anomaly detection, and predictive maintenance.

## Features

### Module 1: Area & Consumer Management
- Create and manage distribution areas with priority levels
- Register and track consumers
- Area-wise consumer listing and analysis
- Search functionality for quick consumer lookup

### Module 2: Asset Management
- Track electrical infrastructure (transformers, poles, cables)
- Monitor asset health status
- Maintenance scheduling and alerts
- Asset statistics and reporting

### Module 3: Meter & Consumption Management
- One-to-one meter-consumer relationship
- Record electricity consumption readings
- Peak and off-peak consumption tracking
- Monthly consumption summaries
- Faulty meter identification

### Module 4: Billing Management
- Automated bill generation from consumption data
- Area-type-based rate calculation (residential, commercial, industrial)
- Payment tracking and history
- Overdue bill management
- Revenue analytics

### Module 5: Fault Management
- Report and track infrastructure faults
- Priority-based fault resolution
- Critical fault identification
- Fault statistics and analysis

## Technologies Used

- **Python 3.x** - Core programming language
- **SQLite** - Database management
- **Object-Oriented Programming** - Clean, modular code structure

## Project Structure

```
smart-electricity-system/
├── database/
│   ├── schema.sql              # Database table definitions
│   └── sample_data.sql         # Sample data for testing
├── src/
│   ├── __init__.py
│   ├── config.py               # Configuration settings
│   ├── database.py             # Database connection handler
│   └── modules/
│       ├── __init__.py
│       ├── area_consumer.py    # Module 1
│       ├── asset.py            # Module 2
│       ├── meter_consumption.py # Module 3
│       ├── billing.py          # Module 4
│       └── fault.py            # Module 5
├── main.py                     # CLI interface
├── test_database.py            # Database setup script
├── requirements.txt
└── README.md
```

## Installation & Setup

### Prerequisites
- Python 3.7 or higher
- No external packages required (SQLite is built into Python)

### Setup Instructions

1. **Clone or download the project**
   ```bash
   cd smart-electricity-system
   ```

2. **Initialize the database**
   ```bash
   python test_database.py
   ```
   When prompted, type `yes` to load sample data.

3. **Run the application**
   ```bash
   python main.py
   ```

## Database Schema

The system uses a normalized relational database with 7 tables:

1. **AREA** - Distribution areas with priority levels
2. **CONSUMER** - Customer information
3. **ASSET** - Electrical infrastructure assets
4. **METER** - Electricity meters (1:1 with consumers)
5. **CONSUMPTION** - Consumption readings
6. **BILL** - Generated bills
7. **FAULT** - Reported faults

### Entity Relationships
- Each consumer belongs to one area
- Each asset is located in one area
- Each consumer has exactly one meter
- Meters can have multiple consumption records
- Consumers can have multiple bills
- Assets can have multiple faults

## Key Functionalities

### Automated Bill Generation
The system can automatically generate bills based on consumption data with area-type-based pricing:
- **Residential**: ₹5.50 per unit
- **Commercial**: ₹7.00 per unit
- **Industrial**: ₹6.50 per unit

### Maintenance Alerts
Automatically identifies assets needing maintenance based on health status, sorted by area priority.

### Consumption Analytics
- Monthly consumption summaries
- Peak vs off-peak analysis
- Historical consumption trends
- System-wide statistics

### Fault Tracking
- Priority-based fault queue
- Critical fault identification (power outages, high-priority areas)
- Average resolution time tracking

## Future Enhancements

### ML Integration (Planned)
The system's rich structured data across consumption, billing, assets, and faults creates a natural foundation for machine learning enhancements:

- **Consumption Forecasting** — Historical meter readings can train a time-series model (ARIMA / LSTM) to predict next-month consumption per consumer, enabling better load planning
- **Anomaly Detection on Meters** — Isolation Forest or Z-score methods on consumption records to automatically flag faulty or tampered meters, replacing manual faulty meter identification
- **Predictive Maintenance** — A classifier trained on asset health history, fault frequency, and area priority could predict asset failures before they occur, moving from reactive to proactive maintenance
- **Overdue Payment Risk Scoring** — Consumer billing history and area-type features could power a logistic regression model to flag high-risk accounts before they become overdue
- **Fault Classification via NLP** — TF-IDF + Naive Bayes on fault description text to auto-categorize and route faults faster, reducing manual triage

### Other Planned Enhancements
- Web interface using Flask/Django
- Real-time consumption monitoring
- SMS/Email notifications for bills and faults
- Payment gateway integration
- Advanced analytics dashboard
- Mobile app support
- Report export (PDF/Excel)

## Sample Data

The system includes sample data with:
- 5 distribution areas
- 10 consumers across different areas
- 15 assets (transformers, poles, cables)
- 10 meters with consumption records
- 10 bills in various payment states
- 5 fault records

## Project Highlights

### Database Design
- **Normalized schema** (3NF) ensuring data integrity
- **Foreign key constraints** maintaining referential integrity
- **Proper indexing** for query performance
- **Check constraints** for data validation

### Code Quality
- **Modular architecture** - Each module is independent and testable
- **Error handling** - Graceful error messages and validation
- **Input validation** - Prevents invalid data entry
- **Clean code** - Well-commented and documented

### Business Logic
- **Rate calculation** based on consumer area type
- **Priority management** for areas and faults
- **Overdue tracking** with automatic status updates
- **Health monitoring** for assets

## Configuration

Edit `src/config.py` to customize:
- Database file location
- Billing rates per area type
- Bill due date period (days)

## License

This project is created for educational purposes.

## Contributing

This is a portfolio/academic project. Feel free to fork and customize for your needs.

## Contact

For questions or suggestions, please reach out through GitHub.

---

**Built with Python and SQLite**