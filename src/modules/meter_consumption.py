"""
Module 3: Meter & Consumption Management
Handles all operations related to electricity meters and consumption tracking
"""

from src.database import Database
from datetime import date, datetime, timedelta


class MeterConsumptionManager:
    """Manages electricity meters and consumption records"""
    
    def __init__(self):
        self.db = Database()
    
    # =====================================================
    # METER OPERATIONS
    # =====================================================
    
    def add_meter(self, meter_number, consumer_id, installation_date=None, meter_status='active'):
        """
        Add a new meter for a consumer
        
        Args:
            meter_number (str): Unique meter identification number
            consumer_id (int): ID of the consumer
            installation_date (str/date): Installation date (defaults to today)
            meter_status (str): Status - 'active', 'inactive', or 'faulty'
        
        Returns:
            int: meter_id of newly created meter
        """
        # Validate meter status
        valid_statuses = ['active', 'inactive', 'faulty']
        if meter_status.lower() not in valid_statuses:
            print(f"❌ Invalid meter status! Must be one of: {', '.join(valid_statuses)}")
            return None
        
        # Set installation date to today if not provided
        if installation_date is None:
            installation_date = date.today()
        
        # Check if consumer exists
        consumer_check = self.db.execute_query(
            "SELECT consumer_id, name FROM CONSUMER WHERE consumer_id = ?",
            (consumer_id,)
        )
        
        if not consumer_check:
            print(f"❌ Consumer with ID {consumer_id} not found!")
            return None
        
        consumer_name = dict(consumer_check[0])['name']
        
        # Check if consumer already has a meter (1:1 relationship)
        existing_meter = self.db.execute_query(
            "SELECT meter_id, meter_number FROM METER WHERE consumer_id = ?",
            (consumer_id,)
        )
        
        if existing_meter:
            existing = dict(existing_meter[0])
            print(f"❌ Consumer already has a meter assigned!")
            print(f"Existing Meter: {existing['meter_number']} (ID: {existing['meter_id']})")
            return None
        
        # Check if meter number already exists
        meter_check = self.db.execute_query(
            "SELECT meter_id FROM METER WHERE meter_number = ?",
            (meter_number,)
        )
        
        if meter_check:
            print(f"❌ Meter number '{meter_number}' already exists!")
            return None
        
        query = """
            INSERT INTO METER (meter_number, installation_date, meter_status, consumer_id)
            VALUES (?, ?, ?, ?)
        """
        
        try:
            meter_id = self.db.execute_update(
                query,
                (meter_number, installation_date, meter_status.lower(), consumer_id)
            )
            
            print(f"\n✅ Meter added successfully!")
            print(f"Meter ID: {meter_id}")
            print(f"Meter Number: {meter_number}")
            print(f"Consumer: {consumer_name}")
            print(f"Installation Date: {installation_date}")
            print(f"Status: {meter_status.capitalize()}\n")
            
            return meter_id
        except Exception as e:
            print(f"❌ Error adding meter: {e}")
            return None
    
    def view_meter(self, meter_id):
        """
        View detailed information about a specific meter
        
        Args:
            meter_id (int): ID of the meter
        
        Returns:
            dict: Meter details or None if not found
        """
        query = """
            SELECT m.*, c.name as consumer_name, c.address, c.phone,
                   a.area_name, a.area_type
            FROM METER m
            JOIN CONSUMER c ON m.consumer_id = c.consumer_id
            JOIN AREA a ON c.area_id = a.area_id
            WHERE m.meter_id = ?
        """
        
        result = self.db.execute_query(query, (meter_id,))
        
        if result:
            meter = dict(result[0])
            
            # Get total consumption records
            count_query = "SELECT COUNT(*) as count FROM CONSUMPTION WHERE meter_id = ?"
            count_result = self.db.execute_query(count_query, (meter_id,))
            reading_count = dict(count_result[0])['count'] if count_result else 0
            
            print("\n" + "="*60)
            print("METER DETAILS")
            print("="*60)
            print(f"Meter ID:          {meter['meter_id']}")
            print(f"Meter Number:      {meter['meter_number']}")
            print(f"Status:            {meter['meter_status'].capitalize()}")
            print(f"Installation Date: {meter['installation_date']}")
            print(f"\nConsumer Details:")
            print(f"  Name:            {meter['consumer_name']}")
            print(f"  Phone:           {meter['phone']}")
            print(f"  Address:         {meter['address']}")
            print(f"  Area:            {meter['area_name']} ({meter['area_type']})")
            print(f"\nTotal Readings:    {reading_count}")
            print("="*60 + "\n")
            
            return meter
        else:
            print(f"\n❌ Meter with ID {meter_id} not found!\n")
            return None
    
    def list_all_meters(self):
        """
        Display all meters in the system
        
        Returns:
            list: All meter records
        """
        query = """
            SELECT m.meter_id, m.meter_number, m.meter_status, m.installation_date,
                   c.name as consumer_name, a.area_name
            FROM METER m
            JOIN CONSUMER c ON m.consumer_id = c.consumer_id
            JOIN AREA a ON c.area_id = a.area_id
            ORDER BY m.meter_id
        """
        
        results = self.db.execute_query(query)
        
        if results:
            print("\n" + "="*105)
            print("ALL METERS")
            print("="*105)
            print(f"{'ID':<6} {'Meter Number':<20} {'Status':<12} {'Installed':<12} {'Consumer':<30} {'Area':<25}")
            print("="*105)
            
            for row in results:
                meter = dict(row)
                consumer_name = meter['consumer_name'][:27] + "..." if len(meter['consumer_name']) > 30 else meter['consumer_name']
                area_name = meter['area_name'][:22] + "..." if len(meter['area_name']) > 25 else meter['area_name']
                
                print(f"{meter['meter_id']:<6} {meter['meter_number']:<20} "
                      f"{meter['meter_status']:<12} {meter['installation_date']:<12} "
                      f"{consumer_name:<30} {area_name:<25}")
            
            print("="*105 + "\n")
        else:
            print("\n⚠️  No meters found in the system.\n")
        
        return results
    
    def update_meter_status(self, meter_id, new_status):
        """
        Update the status of a meter
        
        Args:
            meter_id (int): ID of the meter
            new_status (str): New status ('active', 'inactive', 'faulty')
        
        Returns:
            bool: True if successful, False otherwise
        """
        # Validate status
        valid_statuses = ['active', 'inactive', 'faulty']
        if new_status.lower() not in valid_statuses:
            print(f"❌ Invalid status! Must be one of: {', '.join(valid_statuses)}")
            return False
        
        # Check if meter exists
        check_query = "SELECT meter_id, meter_number FROM METER WHERE meter_id = ?"
        result = self.db.execute_query(check_query, (meter_id,))
        
        if not result:
            print(f"❌ Meter with ID {meter_id} not found!")
            return False
        
        meter_number = dict(result[0])['meter_number']
        
        query = "UPDATE METER SET meter_status = ? WHERE meter_id = ?"
        
        try:
            self.db.execute_update(query, (new_status.lower(), meter_id))
            print(f"\n✅ Meter {meter_number} status updated to '{new_status}' successfully!\n")
            return True
        except Exception as e:
            print(f"❌ Error updating meter: {e}")
            return False
    
    def get_faulty_meters(self):
        """
        Get all meters with faulty status
        
        Returns:
            list: Faulty meter records
        """
        query = """
            SELECT m.meter_id, m.meter_number, m.installation_date,
                   c.name as consumer_name, c.phone, a.area_name
            FROM METER m
            JOIN CONSUMER c ON m.consumer_id = c.consumer_id
            JOIN AREA a ON c.area_id = a.area_id
            WHERE m.meter_status = 'faulty'
            ORDER BY m.meter_id
        """
        
        results = self.db.execute_query(query)
        
        if results:
            print("\n" + "="*100)
            print("⚠️  FAULTY METERS")
            print("="*100)
            print(f"{'ID':<6} {'Meter Number':<20} {'Consumer':<30} {'Phone':<15} {'Area':<29}")
            print("="*100)
            
            for row in results:
                meter = dict(row)
                consumer_name = meter['consumer_name'][:27] + "..." if len(meter['consumer_name']) > 30 else meter['consumer_name']
                area_name = meter['area_name'][:26] + "..." if len(meter['area_name']) > 29 else meter['area_name']
                
                print(f"{meter['meter_id']:<6} {meter['meter_number']:<20} "
                      f"{consumer_name:<30} {meter['phone']:<15} {area_name:<29}")
            
            print("="*100)
            print(f"Total faulty meters: {len(results)}")
            print("="*100 + "\n")
        else:
            print("\n✅ No faulty meters found! All meters are operational.\n")
        
        return results
    
    # =====================================================
    # CONSUMPTION OPERATIONS
    # =====================================================
    
    def record_consumption(self, meter_id, units_consumed, is_peak_period=False, reading_time=None):
        """
        Record electricity consumption for a meter
        
        Args:
            meter_id (int): ID of the meter
            units_consumed (float): Units of electricity consumed
            is_peak_period (bool): Whether consumption was during peak hours
            reading_time (datetime): Time of reading (defaults to now)
        
        Returns:
            int: consumption_id of newly created record
        """
        # Set reading time to now if not provided
        if reading_time is None:
            reading_time = datetime.now()
        
        # Verify meter exists and is active
        meter_check = self.db.execute_query(
            "SELECT meter_id, meter_number, meter_status FROM METER WHERE meter_id = ?",
            (meter_id,)
        )
        
        if not meter_check:
            print(f"❌ Meter with ID {meter_id} not found!")
            return None
        
        meter = dict(meter_check[0])
        
        if meter['meter_status'] != 'active':
            print(f"❌ Meter {meter['meter_number']} is not active! Status: {meter['meter_status']}")
            print("Please activate the meter before recording consumption.")
            return None
        
        # Validate units
        if units_consumed < 0:
            print("❌ Units consumed cannot be negative!")
            return None
        
        query = """
            INSERT INTO CONSUMPTION (reading_time, units_consumed, peak_period, meter_id)
            VALUES (?, ?, ?, ?)
        """
        
        try:
            consumption_id = self.db.execute_update(
                query,
                (reading_time, units_consumed, 1 if is_peak_period else 0, meter_id)
            )
            
            print(f"\n✅ Consumption recorded successfully!")
            print(f"Consumption ID: {consumption_id}")
            print(f"Meter: {meter['meter_number']}")
            print(f"Units Consumed: {units_consumed}")
            print(f"Peak Period: {'Yes' if is_peak_period else 'No'}")
            print(f"Reading Time: {reading_time}\n")
            
            return consumption_id
        except Exception as e:
            print(f"❌ Error recording consumption: {e}")
            return None
    
    def view_consumption(self, consumption_id):
        """
        View details of a specific consumption record
        
        Args:
            consumption_id (int): ID of the consumption record
        
        Returns:
            dict: Consumption details or None if not found
        """
        query = """
            SELECT co.*, m.meter_number, c.name as consumer_name
            FROM CONSUMPTION co
            JOIN METER m ON co.meter_id = m.meter_id
            JOIN CONSUMER c ON m.consumer_id = c.consumer_id
            WHERE co.consumption_id = ?
        """
        
        result = self.db.execute_query(query, (consumption_id,))
        
        if result:
            consumption = dict(result[0])
            
            print("\n" + "="*60)
            print("CONSUMPTION RECORD DETAILS")
            print("="*60)
            print(f"Consumption ID:    {consumption['consumption_id']}")
            print(f"Reading Time:      {consumption['reading_time']}")
            print(f"Units Consumed:    {consumption['units_consumed']}")
            print(f"Peak Period:       {'Yes' if consumption['peak_period'] else 'No'}")
            print(f"Meter Number:      {consumption['meter_number']}")
            print(f"Consumer:          {consumption['consumer_name']}")
            print("="*60 + "\n")
            
            return consumption
        else:
            print(f"\n❌ Consumption record with ID {consumption_id} not found!\n")
            return None
    
    def get_consumption_history(self, meter_id, limit=10):
        """
        Get recent consumption history for a meter
        
        Args:
            meter_id (int): ID of the meter
            limit (int): Number of recent records to retrieve
        
        Returns:
            list: Recent consumption records
        """
        # Verify meter exists
        meter_check = self.db.execute_query(
            "SELECT meter_number FROM METER WHERE meter_id = ?",
            (meter_id,)
        )
        
        if not meter_check:
            print(f"❌ Meter with ID {meter_id} not found!")
            return []
        
        meter_number = dict(meter_check[0])['meter_number']
        
        query = """
            SELECT consumption_id, reading_time, units_consumed, peak_period
            FROM CONSUMPTION
            WHERE meter_id = ?
            ORDER BY reading_time DESC
            LIMIT ?
        """
        
        results = self.db.execute_query(query, (meter_id, limit))
        
        if results:
            print("\n" + "="*85)
            print(f"CONSUMPTION HISTORY - Meter: {meter_number} (ID: {meter_id})")
            print("="*85)
            print(f"{'ID':<8} {'Reading Time':<22} {'Units':<12} {'Peak Period':<15} {'Days Ago':<28}")
            print("="*85)
            
            for row in results:
                consumption = dict(row)
                reading_time = datetime.fromisoformat(consumption['reading_time'])
                days_ago = (datetime.now() - reading_time).days
                
                print(f"{consumption['consumption_id']:<8} {consumption['reading_time']:<22} "
                      f"{consumption['units_consumed']:<12.2f} "
                      f"{'Yes' if consumption['peak_period'] else 'No':<15} "
                      f"{days_ago} days ago{' ' * 20}")
            
            print("="*85 + "\n")
        else:
            print(f"\n⚠️  No consumption records found for meter {meter_number}.\n")
        
        return results
    
    def get_monthly_consumption(self, meter_id, month_year):
        """
        Get total consumption for a specific month
        
        Args:
            meter_id (int): ID of the meter
            month_year (str): Month in format 'YYYY-MM' (e.g., '2024-02')
        
        Returns:
            dict: Monthly consumption summary
        """
        # Verify meter exists
        meter_check = self.db.execute_query(
            "SELECT meter_number, consumer_id FROM METER WHERE meter_id = ?",
            (meter_id,)
        )
        
        if not meter_check:
            print(f"❌ Meter with ID {meter_id} not found!")
            return None
        
        meter = dict(meter_check[0])
        
        # Get consumer name
        consumer_query = "SELECT name FROM CONSUMER WHERE consumer_id = ?"
        consumer_result = self.db.execute_query(consumer_query, (meter['consumer_id'],))
        consumer_name = dict(consumer_result[0])['name'] if consumer_result else "Unknown"
        
        query = """
            SELECT 
                SUM(units_consumed) as total_units,
                AVG(units_consumed) as avg_units,
                COUNT(*) as reading_count,
                SUM(CASE WHEN peak_period = 1 THEN units_consumed ELSE 0 END) as peak_units,
                SUM(CASE WHEN peak_period = 0 THEN units_consumed ELSE 0 END) as off_peak_units
            FROM CONSUMPTION
            WHERE meter_id = ?
              AND strftime('%Y-%m', reading_time) = ?
        """
        
        result = self.db.execute_query(query, (meter_id, month_year))
        
        if result:
            data = dict(result[0])
            
            if data['total_units'] is None:
                print(f"\n⚠️  No consumption data found for {month_year}.\n")
                return None
            
            # Handle None values properly
            peak_units = float(data['peak_units']) if data['peak_units'] is not None else 0.0
            off_peak_units = float(data['off_peak_units']) if data['off_peak_units'] is not None else 0.0
            
            print("\n" + "="*60)
            print(f"MONTHLY CONSUMPTION SUMMARY - {month_year}")
            print("="*60)
            print(f"Meter Number:      {meter['meter_number']}")
            print(f"Consumer:          {consumer_name}")
            print(f"\nConsumption:")
            print(f"  Total Units:     {data['total_units']:.2f}")
            print(f"  Peak Units:      {peak_units:.2f}")
            print(f"  Off-Peak Units:  {off_peak_units:.2f}")
            print(f"\nStatistics:")
            print(f"  Average per Reading: {data['avg_units']:.2f}")
            print(f"  Number of Readings:  {data['reading_count']}")
            print("="*60 + "\n")
            
            return data
        
        return None
    
    def get_consumption_statistics(self, days=30):
        """
        Get consumption statistics for the last N days
        
        Args:
            days (int): Number of days to analyze
        
        Returns:
            dict: Consumption statistics
        """
        cutoff_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        
        query = """
            SELECT 
                COUNT(DISTINCT meter_id) as active_meters,
                SUM(units_consumed) as total_consumption,
                AVG(units_consumed) as avg_consumption,
                MAX(units_consumed) as max_consumption,
                MIN(units_consumed) as min_consumption,
                SUM(CASE WHEN peak_period = 1 THEN units_consumed ELSE 0 END) as peak_consumption,
                SUM(CASE WHEN peak_period = 0 THEN units_consumed ELSE 0 END) as off_peak_consumption
            FROM CONSUMPTION
            WHERE DATE(reading_time) >= ?
        """
        
        result = self.db.execute_query(query, (cutoff_date,))
        
        if result:
            stats = dict(result[0])
            
            # Handle None values
            total_consumption = float(stats['total_consumption']) if stats['total_consumption'] is not None else 0.0
            avg_consumption = float(stats['avg_consumption']) if stats['avg_consumption'] is not None else 0.0
            max_consumption = float(stats['max_consumption']) if stats['max_consumption'] is not None else 0.0
            min_consumption = float(stats['min_consumption']) if stats['min_consumption'] is not None else 0.0
            peak_consumption = float(stats['peak_consumption']) if stats['peak_consumption'] is not None else 0.0
            off_peak_consumption = float(stats['off_peak_consumption']) if stats['off_peak_consumption'] is not None else 0.0
            
            print("\n" + "="*60)
            print(f"CONSUMPTION STATISTICS (Last {days} Days)")
            print("="*60)
            print(f"Active Meters:        {stats['active_meters']}")
            print(f"Total Consumption:    {total_consumption:.2f} units")
            print(f"Peak Consumption:     {peak_consumption:.2f} units")
            print(f"Off-Peak:             {off_peak_consumption:.2f} units")
            print(f"\nPer Reading:")
            print(f"  Average:            {avg_consumption:.2f} units")
            print(f"  Maximum:            {max_consumption:.2f} units")
            print(f"  Minimum:            {min_consumption:.2f} units")
            print("="*60 + "\n")
            
            return stats
        
        return None