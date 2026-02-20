-- Smart Electricity Distribution & Management System
-- Database Schema

-- Drop tables if they exist (for fresh start)
DROP TABLE IF EXISTS FAULT;
DROP TABLE IF EXISTS BILL;
DROP TABLE IF EXISTS CONSUMPTION;
DROP TABLE IF EXISTS METER;
DROP TABLE IF EXISTS ASSET;
DROP TABLE IF EXISTS CONSUMER;
DROP TABLE IF EXISTS AREA;

-- =====================================================
-- MODULE 1: AREA MANAGEMENT
-- =====================================================

CREATE TABLE AREA (
    area_id INTEGER PRIMARY KEY AUTOINCREMENT,
    area_name VARCHAR(100) NOT NULL,
    area_type VARCHAR(20) NOT NULL CHECK(area_type IN ('residential', 'commercial', 'industrial')),
    priority_level VARCHAR(10) DEFAULT 'medium' CHECK(priority_level IN ('high', 'medium', 'low'))
);

-- =====================================================
-- MODULE 1: CONSUMER MANAGEMENT
-- =====================================================

CREATE TABLE CONSUMER (
    consumer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    address VARCHAR(255) NOT NULL,
    phone VARCHAR(15) NOT NULL,
    area_id INTEGER NOT NULL,
    FOREIGN KEY (area_id) REFERENCES AREA(area_id)
);

-- =====================================================
-- MODULE 2: ASSET MANAGEMENT
-- =====================================================

CREATE TABLE ASSET (
    asset_id INTEGER PRIMARY KEY AUTOINCREMENT,
    asset_type VARCHAR(20) NOT NULL CHECK(asset_type IN ('transformer', 'pole', 'cable')),
    capacity VARCHAR(50),
    installation_date DATE NOT NULL,
    health_status VARCHAR(10) DEFAULT 'good' CHECK(health_status IN ('good', 'fair', 'poor')),
    area_id INTEGER NOT NULL,
    FOREIGN KEY (area_id) REFERENCES AREA(area_id)
);

-- =====================================================
-- MODULE 3: METER MANAGEMENT
-- =====================================================

CREATE TABLE METER (
    meter_id INTEGER PRIMARY KEY AUTOINCREMENT,
    meter_number VARCHAR(50) UNIQUE NOT NULL,
    installation_date DATE NOT NULL,
    meter_status VARCHAR(10) DEFAULT 'active' CHECK(meter_status IN ('active', 'inactive', 'faulty')),
    consumer_id INTEGER UNIQUE NOT NULL,
    FOREIGN KEY (consumer_id) REFERENCES CONSUMER(consumer_id)
);

-- =====================================================
-- MODULE 3: CONSUMPTION MANAGEMENT
-- =====================================================

CREATE TABLE CONSUMPTION (
    consumption_id INTEGER PRIMARY KEY AUTOINCREMENT,
    reading_time DATETIME NOT NULL,
    units_consumed DECIMAL(10,2) NOT NULL,
    peak_period BOOLEAN DEFAULT 0,
    meter_id INTEGER NOT NULL,
    FOREIGN KEY (meter_id) REFERENCES METER(meter_id)
);

-- =====================================================
-- MODULE 4: BILLING MANAGEMENT
-- =====================================================

CREATE TABLE BILL (
    bill_id INTEGER PRIMARY KEY AUTOINCREMENT,
    billing_month VARCHAR(20) NOT NULL,
    total_units DECIMAL(10,2) NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    payment_status VARCHAR(10) DEFAULT 'pending' CHECK(payment_status IN ('pending', 'paid', 'overdue')),
    due_date DATE NOT NULL,
    consumer_id INTEGER NOT NULL,
    FOREIGN KEY (consumer_id) REFERENCES CONSUMER(consumer_id)
);

-- =====================================================
-- MODULE 5: FAULT MANAGEMENT
-- =====================================================

CREATE TABLE FAULT (
    fault_id INTEGER PRIMARY KEY AUTOINCREMENT,
    fault_type VARCHAR(30) NOT NULL CHECK(fault_type IN ('power_outage', 'voltage_fluctuation', 'equipment_failure', 'other')),
    fault_date DATETIME NOT NULL,
    description TEXT,
    resolution_status VARCHAR(15) DEFAULT 'pending' CHECK(resolution_status IN ('pending', 'in_progress', 'resolved')),
    resolution_date DATETIME,
    asset_id INTEGER NOT NULL,
    FOREIGN KEY (asset_id) REFERENCES ASSET(asset_id)
);

-- =====================================================
-- Indexes for Better Performance
-- =====================================================

CREATE INDEX idx_consumer_area ON CONSUMER(area_id);
CREATE INDEX idx_asset_area ON ASSET(area_id);
CREATE INDEX idx_meter_consumer ON METER(consumer_id);
CREATE INDEX idx_consumption_meter ON CONSUMPTION(meter_id);
CREATE INDEX idx_bill_consumer ON BILL(consumer_id);
CREATE INDEX idx_fault_asset ON FAULT(asset_id);