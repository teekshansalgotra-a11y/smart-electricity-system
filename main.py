"""
Smart Electricity Distribution & Management System
Main CLI Interface
"""

from src.modules.area_consumers import AreaConsumerManager
from src.modules.asset import AssetManager
from src.modules.meter_consumption import MeterConsumptionManager
from src.modules.billing import BillingManager
from src.modules.fault import FaultManager
from src.database import Database


def print_main_menu():
    """Display main menu"""
    print("\n" + "="*70)
    print("     SMART ELECTRICITY DISTRIBUTION & MANAGEMENT SYSTEM")
    print("="*70)
    print("1.  Area & Consumer Management")
    print("2.  Asset Management")
    print("3.  Meter & Consumption Management")
    print("4.  Billing Management")
    print("5.  Fault Management")
    print("6.  System Reports")
    print("7.  Exit")
    print("="*70)


# =====================================================
# MODULE 1: AREA & CONSUMER MANAGEMENT
# =====================================================

def area_consumer_menu():
    """Area and Consumer Management Menu"""
    acm = AreaConsumerManager()
    
    while True:
        print("\n" + "="*60)
        print("MODULE 1: AREA & CONSUMER MANAGEMENT")
        print("="*60)
        print("AREA OPERATIONS:")
        print("  1. Add New Area")
        print("  2. List All Areas")
        print("  3. View Area Details")
        print("  4. Update Area Priority")
        print("\nCONSUMER OPERATIONS:")
        print("  5. Add New Consumer")
        print("  6. View Consumer Details")
        print("  7. List All Consumers")
        print("  8. List Consumers by Area")
        print("  9. Search Consumer by Name")
        print(" 10. Update Consumer Details")
        print("\n 0. Back to Main Menu")
        print("="*60)
        
        choice = input("\nEnter your choice: ").strip()
        
        try:
            if choice == '1':
                print("\n--- ADD NEW AREA ---")
                name = input("Area Name: ").strip()
                area_type = input("Type (residential/commercial/industrial): ").strip()
                priority = input("Priority (high/medium/low) [default: medium]: ").strip() or 'medium'
                acm.add_area(name, area_type, priority)
            
            elif choice == '2':
                acm.list_all_areas()
            
            elif choice == '3':
                area_id = int(input("Enter Area ID: "))
                acm.view_area_details(area_id)
            
            elif choice == '4':
                area_id = int(input("Enter Area ID: "))
                new_priority = input("New Priority (high/medium/low): ").strip()
                acm.update_area_priority(area_id, new_priority)
            
            elif choice == '5':
                print("\n--- ADD NEW CONSUMER ---")
                name = input("Consumer Name: ").strip()
                address = input("Address: ").strip()
                phone = input("Phone: ").strip()
                area_id = int(input("Area ID: "))
                acm.add_consumer(name, address, phone, area_id)
            
            elif choice == '6':
                consumer_id = int(input("Enter Consumer ID: "))
                acm.view_consumer(consumer_id)
            
            elif choice == '7':
                acm.list_all_consumers()
            
            elif choice == '8':
                area_id = int(input("Enter Area ID: "))
                acm.list_consumers_by_area(area_id)
            
            elif choice == '9':
                search_term = input("Enter name to search: ").strip()
                acm.search_consumer_by_name(search_term)
            
            elif choice == '10':
                consumer_id = int(input("Enter Consumer ID: "))
                print("Leave blank to skip updating a field")
                name = input("New Name: ").strip()
                address = input("New Address: ").strip()
                phone = input("New Phone: ").strip()
                
                updates = {}
                if name: updates['name'] = name
                if address: updates['address'] = address
                if phone: updates['phone'] = phone
                
                if updates:
                    acm.update_consumer(consumer_id, **updates)
                else:
                    print("No fields to update.")
            
            elif choice == '0':
                break
            
            else:
                print("❌ Invalid choice! Please try again.")
        
        except ValueError:
            print("❌ Invalid input! Please enter a valid number.")
        except Exception as e:
            print(f"❌ An error occurred: {e}")
        
        input("\nPress Enter to continue...")


# =====================================================
# MODULE 2: ASSET MANAGEMENT
# =====================================================

def asset_menu():
    """Asset Management Menu"""
    am = AssetManager()
    
    while True:
        print("\n" + "="*60)
        print("MODULE 2: ASSET MANAGEMENT")
        print("="*60)
        print("1. Add New Asset")
        print("2. View Asset Details")
        print("3. List All Assets")
        print("4. List Assets by Area")
        print("5. List Assets by Type")
        print("6. Update Asset Health Status")
        print("7. View Assets Needing Maintenance")
        print("8. Asset Statistics")
        print("9. Search Assets by Capacity")
        print("\n0. Back to Main Menu")
        print("="*60)
        
        choice = input("\nEnter your choice: ").strip()
        
        try:
            if choice == '1':
                print("\n--- ADD NEW ASSET ---")
                asset_type = input("Type (transformer/pole/cable): ").strip()
                capacity = input("Capacity/Specification: ").strip()
                area_id = int(input("Area ID: "))
                health = input("Health Status (good/fair/poor) [default: good]: ").strip() or 'good'
                am.add_asset(asset_type, capacity, area_id, health_status=health)
            
            elif choice == '2':
                asset_id = int(input("Enter Asset ID: "))
                am.view_asset(asset_id)
            
            elif choice == '3':
                am.list_all_assets()
            
            elif choice == '4':
                area_id = int(input("Enter Area ID: "))
                am.list_assets_by_area(area_id)
            
            elif choice == '5':
                asset_type = input("Asset Type (transformer/pole/cable): ").strip()
                am.list_assets_by_type(asset_type)
            
            elif choice == '6':
                asset_id = int(input("Enter Asset ID: "))
                new_status = input("New Health Status (good/fair/poor): ").strip()
                am.update_asset_health(asset_id, new_status)
            
            elif choice == '7':
                am.get_assets_needing_maintenance()
            
            elif choice == '8':
                am.get_asset_statistics()
            
            elif choice == '9':
                search_term = input("Enter capacity to search: ").strip()
                am.search_assets_by_capacity(search_term)
            
            elif choice == '0':
                break
            
            else:
                print("❌ Invalid choice! Please try again.")
        
        except ValueError:
            print("❌ Invalid input! Please enter a valid number.")
        except Exception as e:
            print(f"❌ An error occurred: {e}")
        
        input("\nPress Enter to continue...")


# =====================================================
# MODULE 3: METER & CONSUMPTION MANAGEMENT
# =====================================================

def meter_consumption_menu():
    """Meter and Consumption Management Menu"""
    mcm = MeterConsumptionManager()
    
    while True:
        print("\n" + "="*60)
        print("MODULE 3: METER & CONSUMPTION MANAGEMENT")
        print("="*60)
        print("METER OPERATIONS:")
        print("  1. Add New Meter")
        print("  2. View Meter Details")
        print("  3. List All Meters")
        print("  4. Update Meter Status")
        print("  5. View Faulty Meters")
        print("\nCONSUMPTION OPERATIONS:")
        print("  6. Record Consumption")
        print("  7. View Consumption Details")
        print("  8. Get Consumption History")
        print("  9. Get Monthly Consumption")
        print(" 10. Consumption Statistics")
        print("\n 0. Back to Main Menu")
        print("="*60)
        
        choice = input("\nEnter your choice: ").strip()
        
        try:
            if choice == '1':
                print("\n--- ADD NEW METER ---")
                meter_number = input("Meter Number: ").strip()
                consumer_id = int(input("Consumer ID: "))
                status = input("Status (active/inactive/faulty) [default: active]: ").strip() or 'active'
                mcm.add_meter(meter_number, consumer_id, meter_status=status)
            
            elif choice == '2':
                meter_id = int(input("Enter Meter ID: "))
                mcm.view_meter(meter_id)
            
            elif choice == '3':
                mcm.list_all_meters()
            
            elif choice == '4':
                meter_id = int(input("Enter Meter ID: "))
                new_status = input("New Status (active/inactive/faulty): ").strip()
                mcm.update_meter_status(meter_id, new_status)
            
            elif choice == '5':
                mcm.get_faulty_meters()
            
            elif choice == '6':
                print("\n--- RECORD CONSUMPTION ---")
                meter_id = int(input("Meter ID: "))
                units = float(input("Units Consumed: "))
                peak = input("Peak Period? (yes/no) [default: no]: ").strip().lower() == 'yes'
                mcm.record_consumption(meter_id, units, peak)
            
            elif choice == '7':
                consumption_id = int(input("Enter Consumption ID: "))
                mcm.view_consumption(consumption_id)
            
            elif choice == '8':
                meter_id = int(input("Enter Meter ID: "))
                limit = input("Number of records [default: 10]: ").strip()
                limit = int(limit) if limit else 10
                mcm.get_consumption_history(meter_id, limit)
            
            elif choice == '9':
                meter_id = int(input("Enter Meter ID: "))
                month_year = input("Month (YYYY-MM, e.g., 2024-02): ").strip()
                mcm.get_monthly_consumption(meter_id, month_year)
            
            elif choice == '10':
                days = input("Last N days [default: 30]: ").strip()
                days = int(days) if days else 30
                mcm.get_consumption_statistics(days)
            
            elif choice == '0':
                break
            
            else:
                print("❌ Invalid choice! Please try again.")
        
        except ValueError:
            print("❌ Invalid input! Please enter a valid number.")
        except Exception as e:
            print(f"❌ An error occurred: {e}")
        
        input("\nPress Enter to continue...")


# =====================================================
# MODULE 4: BILLING MANAGEMENT
# =====================================================

def billing_menu():
    """Billing Management Menu"""
    bm = BillingManager()
    
    while True:
        print("\n" + "="*60)
        print("MODULE 4: BILLING MANAGEMENT")
        print("="*60)
        print("1. Generate Bill (Manual)")
        print("2. Generate Bill from Consumption Data")
        print("3. View Bill Details")
        print("4. List All Bills")
        print("5. View Pending Bills (All)")
        print("6. View Pending Bills (By Consumer)")
        print("7. Record Payment")
        print("8. View Payment History")
        print("9. Update Overdue Bills")
        print("10. Billing Statistics")
        print("11. Revenue by Area Type")
        print("\n0. Back to Main Menu")
        print("="*60)
        
        choice = input("\nEnter your choice: ").strip()
        
        try:
            if choice == '1':
                print("\n--- GENERATE BILL (MANUAL) ---")
                consumer_id = int(input("Consumer ID: "))
                billing_month = input("Billing Month (e.g., February 2024): ").strip()
                total_units = float(input("Total Units: "))
                bm.generate_bill(consumer_id, billing_month, total_units)
            
            elif choice == '2':
                print("\n--- GENERATE BILL FROM CONSUMPTION ---")
                consumer_id = int(input("Consumer ID: "))
                billing_month = input("Billing Month Display (e.g., February 2024): ").strip()
                month_year = input("Month for Query (YYYY-MM, e.g., 2024-02): ").strip()
                bm.generate_bill_from_consumption(consumer_id, billing_month, month_year)
            
            elif choice == '3':
                bill_id = int(input("Enter Bill ID: "))
                bm.view_bill(bill_id)
            
            elif choice == '4':
                bm.list_all_bills()
            
            elif choice == '5':
                bm.get_pending_bills()
            
            elif choice == '6':
                consumer_id = int(input("Enter Consumer ID: "))
                bm.get_pending_bills(consumer_id)
            
            elif choice == '7':
                bill_id = int(input("Enter Bill ID to pay: "))
                bm.record_payment(bill_id)
            
            elif choice == '8':
                consumer_id = int(input("Enter Consumer ID: "))
                bm.get_payment_history(consumer_id)
            
            elif choice == '9':
                bm.update_overdue_bills()
            
            elif choice == '10':
                bm.get_billing_statistics()
            
            elif choice == '11':
                bm.get_revenue_by_area_type()
            
            elif choice == '0':
                break
            
            else:
                print("❌ Invalid choice! Please try again.")
        
        except ValueError:
            print("❌ Invalid input! Please enter a valid number.")
        except Exception as e:
            print(f"❌ An error occurred: {e}")
        
        input("\nPress Enter to continue...")


# =====================================================
# MODULE 5: FAULT MANAGEMENT
# =====================================================

def fault_menu():
    """Fault Management Menu"""
    fm = FaultManager()
    
    while True:
        print("\n" + "="*60)
        print("MODULE 5: FAULT MANAGEMENT")
        print("="*60)
        print("1. Report New Fault")
        print("2. View Fault Details")
        print("3. List All Faults")
        print("4. Update Fault Status")
        print("5. View Pending Faults")
        print("6. View Critical Faults")
        print("7. View Faults by Area")
        print("8. View Faults by Type")
        print("9. Fault Statistics")
        print("\n0. Back to Main Menu")
        print("="*60)
        
        choice = input("\nEnter your choice: ").strip()
        
        try:
            if choice == '1':
                print("\n--- REPORT NEW FAULT ---")
                asset_id = int(input("Asset ID: "))
                print("Fault Types: power_outage, voltage_fluctuation, equipment_failure, other")
                fault_type = input("Fault Type: ").strip()
                description = input("Description: ").strip()
                fm.report_fault(asset_id, fault_type, description)
            
            elif choice == '2':
                fault_id = int(input("Enter Fault ID: "))
                fm.view_fault(fault_id)
            
            elif choice == '3':
                fm.list_all_faults()
            
            elif choice == '4':
                fault_id = int(input("Enter Fault ID: "))
                print("Status Options: pending, in_progress, resolved")
                new_status = input("New Status: ").strip()
                fm.update_fault_status(fault_id, new_status)
            
            elif choice == '5':
                fm.get_pending_faults()
            
            elif choice == '6':
                fm.get_critical_faults()
            
            elif choice == '7':
                area_id = int(input("Enter Area ID: "))
                fm.get_faults_by_area(area_id)
            
            elif choice == '8':
                print("Fault Types: power_outage, voltage_fluctuation, equipment_failure, other")
                fault_type = input("Fault Type: ").strip()
                fm.get_faults_by_type(fault_type)
            
            elif choice == '9':
                fm.get_fault_statistics()
            
            elif choice == '0':
                break
            
            else:
                print("❌ Invalid choice! Please try again.")
        
        except ValueError:
            print("❌ Invalid input! Please enter a valid number.")
        except Exception as e:
            print(f"❌ An error occurred: {e}")
        
        input("\nPress Enter to continue...")


# =====================================================
# SYSTEM REPORTS
# =====================================================

def reports_menu():
    """System Reports Menu"""
    acm = AreaConsumerManager()
    am = AssetManager()
    mcm = MeterConsumptionManager()
    bm = BillingManager()
    fm = FaultManager()
    
    while True:
        print("\n" + "="*60)
        print("SYSTEM REPORTS")
        print("="*60)
        print("1. Asset Statistics")
        print("2. Assets Needing Maintenance")
        print("3. Consumption Statistics (Last 30 Days)")
        print("4. Billing Statistics")
        print("5. Revenue by Area Type")
        print("6. Fault Statistics")
        print("7. Pending Faults")
        print("8. Critical Faults")
        print("9. Faulty Meters")
        print("10. All Pending Bills")
        print("\n0. Back to Main Menu")
        print("="*60)
        
        choice = input("\nEnter your choice: ").strip()
        
        try:
            if choice == '1':
                am.get_asset_statistics()
            elif choice == '2':
                am.get_assets_needing_maintenance()
            elif choice == '3':
                mcm.get_consumption_statistics(30)
            elif choice == '4':
                bm.get_billing_statistics()
            elif choice == '5':
                bm.get_revenue_by_area_type()
            elif choice == '6':
                fm.get_fault_statistics()
            elif choice == '7':
                fm.get_pending_faults()
            elif choice == '8':
                fm.get_critical_faults()
            elif choice == '9':
                mcm.get_faulty_meters()
            elif choice == '10':
                bm.get_pending_bills()
            elif choice == '0':
                break
            else:
                print("❌ Invalid choice! Please try again.")
        
        except Exception as e:
            print(f"❌ An error occurred: {e}")
        
        input("\nPress Enter to continue...")


# =====================================================
# MAIN FUNCTION
# =====================================================

def main():
    """Main function"""
    # Initialize database check
    db = Database()
    
    print("\n" + "="*70)
    print("     SMART ELECTRICITY DISTRIBUTION & MANAGEMENT SYSTEM")
    print("="*70)
    print("\nInitializing system...")
    
    # Check if database exists and has data
    try:
        db.get_table_counts()
    except:
        print("\n⚠️  Database not initialized!")
        print("Please run: python test_database.py")
        return
    
    while True:
        try:
            print_main_menu()
            choice = input("\nEnter your choice: ").strip()
            
            if choice == '1':
                area_consumer_menu()
            elif choice == '2':
                asset_menu()
            elif choice == '3':
                meter_consumption_menu()
            elif choice == '4':
                billing_menu()
            elif choice == '5':
                fault_menu()
            elif choice == '6':
                reports_menu()
            elif choice == '7':
                print("\n" + "="*70)
                print("Thank you for using Smart Electricity Management System!")
                print("="*70 + "\n")
                break
            else:
                print("❌ Invalid choice! Please enter a number between 1 and 7.")
        
        except KeyboardInterrupt:
            print("\n\n⚠️  Program interrupted by user.")
            print("Exiting...")
            break
        except Exception as e:
            print(f"\n❌ An unexpected error occurred: {e}")
            print("Please try again.")


if __name__ == "__main__":
    main()