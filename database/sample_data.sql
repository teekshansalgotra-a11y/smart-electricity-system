-- Sample Data for Testing
-- Smart Electricity Distribution System

-- =====================================================
-- AREAS (3 sample areas)
-- =====================================================

INSERT INTO AREA (area_name, area_type, priority_level) VALUES
('Koramangala Block 5', 'residential', 'high'),
('MG Road Business District', 'commercial', 'high'),
('Whitefield Tech Park', 'industrial', 'medium'),
('Jayanagar 4th Block', 'residential', 'medium'),
('HSR Layout Sector 1', 'residential', 'low');

-- =====================================================
-- CONSUMERS (10 sample consumers)
-- =====================================================

INSERT INTO CONSUMER (name, address, phone, area_id) VALUES
('Rajesh Kumar', '123, 5th Cross, Koramangala', '9876543210', 1),
('Priya Sharma', '456, 80 Feet Road, Koramangala', '9876543211', 1),
('Amit Patel', '789, MG Road', '9876543212', 2),
('Sneha Reddy', '101, Brigade Road', '9876543213', 2),
('Vikram Singh', '202, ITPL Main Road', '9876543214', 3),
('Anita Desai', '303, 100 Feet Road, Jayanagar', '9876543215', 4),
('Suresh Iyer', '404, 11th Main, Jayanagar', '9876543216', 4),
('Deepa Nair', '505, 27th Main, HSR', '9876543217', 5),
('Karthik Rao', '606, 14th Cross, HSR', '9876543218', 5),
('Meena Agarwal', '707, Outer Ring Road, Whitefield', '9876543219', 3);

-- =====================================================
-- ASSETS (15 sample assets)
-- =====================================================

INSERT INTO ASSET (asset_type, capacity, installation_date, health_status, area_id) VALUES
('transformer', '500 KVA', '2020-01-15', 'good', 1),
('transformer', '1000 KVA', '2019-06-20', 'good', 2),
('transformer', '2000 KVA', '2018-03-10', 'fair', 3),
('transformer', '500 KVA', '2021-11-05', 'good', 4),
('transformer', '750 KVA', '2020-08-12', 'poor', 5),
('pole', 'Standard', '2020-01-20', 'good', 1),
('pole', 'Standard', '2020-01-20', 'good', 1),
('pole', 'Heavy Duty', '2019-07-15', 'good', 2),
('pole', 'Heavy Duty', '2019-07-15', 'fair', 2),
('pole', 'Industrial', '2018-04-01', 'good', 3),
('cable', '3-Phase', '2020-02-10', 'good', 1),
('cable', '3-Phase', '2019-08-20', 'good', 2),
('cable', '3-Phase Heavy', '2018-05-15', 'fair', 3),
('cable', '3-Phase', '2021-12-01', 'good', 4),
('cable', '3-Phase', '2020-09-10', 'poor', 5);

-- =====================================================
-- METERS (10 meters - one per consumer)
-- =====================================================

INSERT INTO METER (meter_number, installation_date, meter_status, consumer_id) VALUES
('MTR-2020-001', '2020-02-01', 'active', 1),
('MTR-2020-002', '2020-02-01', 'active', 2),
('MTR-2019-045', '2019-09-15', 'active', 3),
('MTR-2019-046', '2019-09-15', 'active', 4),
('MTR-2018-078', '2018-06-20', 'active', 5),
('MTR-2021-101', '2021-12-10', 'active', 6),
('MTR-2021-102', '2021-12-10', 'active', 7),
('MTR-2020-150', '2020-10-05', 'active', 8),
('MTR-2020-151', '2020-10-05', 'active', 9),
('MTR-2018-089', '2018-07-25', 'faulty', 10);

-- =====================================================
-- CONSUMPTION (Sample readings for last 3 months)
-- =====================================================

-- Consumer 1 (Rajesh Kumar) - Residential
INSERT INTO CONSUMPTION (reading_time, units_consumed, peak_period, meter_id) VALUES
('2024-01-15 10:00:00', 120.50, 0, 1),
('2024-02-15 10:00:00', 135.75, 0, 1);

-- Consumer 2 (Priya Sharma) - Residential
INSERT INTO CONSUMPTION (reading_time, units_consumed, peak_period, meter_id) VALUES
('2024-01-15 11:00:00', 95.25, 0, 2),
('2024-02-15 11:00:00', 105.50, 0, 2);

-- Consumer 3 (Amit Patel) - Commercial
INSERT INTO CONSUMPTION (reading_time, units_consumed, peak_period, meter_id) VALUES
('2024-01-15 09:00:00', 450.00, 1, 3),
('2024-02-15 09:00:00', 475.50, 1, 3);

-- Consumer 4 (Sneha Reddy) - Commercial
INSERT INTO CONSUMPTION (reading_time, units_consumed, peak_period, meter_id) VALUES
('2024-01-15 09:30:00', 380.75, 1, 4),
('2024-02-15 09:30:00', 395.25, 1, 4);

-- Consumer 5 (Vikram Singh) - Industrial
INSERT INTO CONSUMPTION (reading_time, units_consumed, peak_period, meter_id) VALUES
('2024-01-15 08:00:00', 1250.00, 1, 5),
('2024-02-15 08:00:00', 1300.50, 1, 5);

-- =====================================================
-- BILLS (Sample bills for January & February 2024)
-- =====================================================

-- Residential consumers (₹5.50 per unit)
INSERT INTO BILL (billing_month, total_units, total_amount, payment_status, due_date, consumer_id) VALUES
('January 2024', 120.50, 662.75, 'paid', '2024-01-30', 1),
('February 2024', 135.75, 746.63, 'pending', '2024-02-28', 1),
('January 2024', 95.25, 523.88, 'paid', '2024-01-30', 2),
('February 2024', 105.50, 580.25, 'pending', '2024-02-28', 2);

-- Commercial consumers (₹7.00 per unit)
INSERT INTO BILL (billing_month, total_units, total_amount, payment_status, due_date, consumer_id) VALUES
('January 2024', 450.00, 3150.00, 'paid', '2024-01-30', 3),
('February 2024', 475.50, 3328.50, 'pending', '2024-02-28', 3),
('January 2024', 380.75, 2665.25, 'overdue', '2024-01-30', 4),
('February 2024', 395.25, 2766.75, 'pending', '2024-02-28', 4);

-- Industrial consumers (₹6.50 per unit)
INSERT INTO BILL (billing_month, total_units, total_amount, payment_status, due_date, consumer_id) VALUES
('January 2024', 1250.00, 8125.00, 'paid', '2024-01-30', 5),
('February 2024', 1300.50, 8453.25, 'pending', '2024-02-28', 5);

-- =====================================================
-- FAULTS (Sample fault records)
-- =====================================================

INSERT INTO FAULT (fault_type, fault_date, description, resolution_status, resolution_date, asset_id) VALUES
('power_outage', '2024-01-20 14:30:00', 'Complete power failure in Koramangala Block 5', 'resolved', '2024-01-20 18:00:00', 1),
('voltage_fluctuation', '2024-02-05 09:15:00', 'Voltage drops during peak hours', 'resolved', '2024-02-05 16:00:00', 2),
('equipment_failure', '2024-02-10 11:00:00', 'Transformer overheating issue', 'in_progress', NULL, 5),
('power_outage', '2024-02-15 07:30:00', 'Cable damage due to construction work', 'pending', NULL, 13),
('other', '2024-02-18 16:45:00', 'Pole tilt noticed after heavy rain', 'pending', NULL, 9);