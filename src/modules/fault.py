"""
Module 5: Fault Management
Handles all operations related to electrical infrastructure faults
"""

from src.database import Database
from datetime import datetime


class FaultManager:
    """Manages fault reporting and tracking for electrical assets"""
    
    def __init__(self):
        self.db = Database()
    
    # =====================================================
    # FAULT OPERATIONS
    # =====================================================
    
    def report_fault(self, asset_id, fault_type, description=""):
        """
        Report a new fault for an asset
        
        Args:
            asset_id (int): ID of the asset with the fault
            fault_type (str): Type - 'power_outage', 'voltage_fluctuation', 'equipment_failure', 'other'
            description (str): Detailed description of the fault
        
        Returns:
            int: fault_id of newly created fault record
        """
        # Validate fault type
        valid_types = ['power_outage', 'voltage_fluctuation', 'equipment_failure', 'other']
        if fault_type.lower() not in valid_types:
            print(f"❌ Invalid fault type! Must be one of: {', '.join(valid_types)}")
            return None
        
        # Verify asset exists
        asset_check = self.db.execute_query(
            "SELECT asset_id, asset_type, capacity FROM ASSET WHERE asset_id = ?",
            (asset_id,)
        )
        
        if not asset_check:
            print(f"❌ Asset with ID {asset_id} not found!")
            return None
        
        asset = dict(asset_check[0])
        fault_date = datetime.now()
        
        query = """
            INSERT INTO FAULT (fault_type, fault_date, description, resolution_status, asset_id)
            VALUES (?, ?, ?, 'pending', ?)
        """
        
        try:
            fault_id = self.db.execute_update(
                query,
                (fault_type.lower(), fault_date, description, asset_id)
            )
            
            print("\n" + "="*60)
            print("🚨 FAULT REPORTED")
            print("="*60)
            print(f"Fault ID:          {fault_id}")
            print(f"Asset:             {asset['asset_type'].capitalize()} (ID: {asset_id})")
            print(f"Capacity:          {asset['capacity']}")
            print(f"Fault Type:        {fault_type.replace('_', ' ').title()}")
            print(f"Reported:          {fault_date.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Status:            Pending")
            if description:
                print(f"Description:       {description}")
            print("="*60 + "\n")
            
            return fault_id
        except Exception as e:
            print(f"❌ Error reporting fault: {e}")
            return None
    
    def view_fault(self, fault_id):
        """
        View detailed information about a specific fault
        
        Args:
            fault_id (int): ID of the fault
        
        Returns:
            dict: Fault details or None if not found
        """
        query = """
            SELECT f.*, ast.asset_type, ast.capacity, a.area_name, a.priority_level
            FROM FAULT f
            JOIN ASSET ast ON f.asset_id = ast.asset_id
            JOIN AREA a ON ast.area_id = a.area_id
            WHERE f.fault_id = ?
        """
        
        result = self.db.execute_query(query, (fault_id,))
        
        if result:
            fault = dict(result[0])
            
            print("\n" + "="*60)
            print("FAULT DETAILS")
            print("="*60)
            print(f"Fault ID:          {fault['fault_id']}")
            print(f"Fault Type:        {fault['fault_type'].replace('_', ' ').title()}")
            print(f"Reported:          {fault['fault_date']}")
            print(f"Status:            {fault['resolution_status'].upper()}")
            
            if fault['resolution_date']:
                print(f"Resolved:          {fault['resolution_date']}")
            
            print(f"\nAsset Information:")
            print(f"  Asset ID:        {fault['asset_id']}")
            print(f"  Type:            {fault['asset_type'].capitalize()}")
            print(f"  Capacity:        {fault['capacity']}")
            print(f"  Area:            {fault['area_name']}")
            print(f"  Priority:        {fault['priority_level'].capitalize()}")
            
            if fault['description']:
                print(f"\nDescription:")
                print(f"  {fault['description']}")
            
            print("="*60 + "\n")
            
            return fault
        else:
            print(f"\n❌ Fault with ID {fault_id} not found!\n")
            return None
    
    def list_all_faults(self):
        """
        Display all faults in the system
        
        Returns:
            list: All fault records
        """
        query = """
            SELECT f.fault_id, f.fault_type, f.fault_date, f.resolution_status,
                   ast.asset_type, a.area_name
            FROM FAULT f
            JOIN ASSET ast ON f.asset_id = ast.asset_id
            JOIN AREA a ON ast.area_id = a.area_id
            ORDER BY f.fault_date DESC
        """
        
        results = self.db.execute_query(query)
        
        if results:
            print("\n" + "="*100)
            print("ALL FAULTS")
            print("="*100)
            print(f"{'ID':<6} {'Type':<25} {'Asset':<15} {'Area':<25} {'Date':<15} {'Status':<14}")
            print("="*100)
            
            for row in results:
                fault = dict(row)
                fault_type_display = fault['fault_type'].replace('_', ' ').title()[:22]
                area_name = fault['area_name'][:22] + "..." if len(fault['area_name']) > 25 else fault['area_name']
                
                # Status indicator
                status_icon = "✅" if fault['resolution_status'] == 'resolved' else "🔄" if fault['resolution_status'] == 'in_progress' else "🟡"
                
                fault_date = fault['fault_date'][:10]  # Just date, not time
                
                print(f"{fault['fault_id']:<6} {fault_type_display:<25} "
                      f"{fault['asset_type']:<15} {area_name:<25} "
                      f"{fault_date:<15} {status_icon} {fault['resolution_status']:<12}")
            
            print("="*100 + "\n")
        else:
            print("\n⚠️  No faults found in the system.\n")
        
        return results
    
    def update_fault_status(self, fault_id, new_status):
        """
        Update the resolution status of a fault
        
        Args:
            fault_id (int): ID of the fault
            new_status (str): New status - 'pending', 'in_progress', or 'resolved'
        
        Returns:
            bool: True if successful, False otherwise
        """
        # Validate status
        valid_statuses = ['pending', 'in_progress', 'resolved']
        if new_status.lower() not in valid_statuses:
            print(f"❌ Invalid status! Must be one of: {', '.join(valid_statuses)}")
            return False
        
        # Check if fault exists
        check_query = "SELECT fault_id, fault_type FROM FAULT WHERE fault_id = ?"
        result = self.db.execute_query(check_query, (fault_id,))
        
        if not result:
            print(f"❌ Fault with ID {fault_id} not found!")
            return False
        
        fault_type = dict(result[0])['fault_type']
        
        # Set resolution date if marking as resolved
        resolution_date = datetime.now() if new_status.lower() == 'resolved' else None
        
        if resolution_date:
            query = """
                UPDATE FAULT 
                SET resolution_status = ?, resolution_date = ?
                WHERE fault_id = ?
            """
            params = (new_status.lower(), resolution_date, fault_id)
        else:
            query = "UPDATE FAULT SET resolution_status = ? WHERE fault_id = ?"
            params = (new_status.lower(), fault_id)
        
        try:
            self.db.execute_update(query, params)
            
            status_msg = {
                'pending': '⏸️  Marked as Pending',
                'in_progress': '🔄 Marked as In Progress',
                'resolved': '✅ Marked as Resolved'
            }
            
            print(f"\n{status_msg[new_status.lower()]}")
            print(f"Fault ID: {fault_id}")
            print(f"Type: {fault_type.replace('_', ' ').title()}")
            if resolution_date:
                print(f"Resolved: {resolution_date.strftime('%Y-%m-%d %H:%M:%S')}")
            print()
            
            return True
        except Exception as e:
            print(f"❌ Error updating fault: {e}")
            return False
    
    def get_pending_faults(self):
        """
        Get all unresolved faults (pending or in progress)
        
        Returns:
            list: Unresolved fault records
        """
        query = """
            SELECT f.fault_id, f.fault_type, f.fault_date, f.resolution_status,
                   ast.asset_type, ast.capacity, a.area_name, a.priority_level
            FROM FAULT f
            JOIN ASSET ast ON f.asset_id = ast.asset_id
            JOIN AREA a ON ast.area_id = a.area_id
            WHERE f.resolution_status != 'resolved'
            ORDER BY 
                CASE a.priority_level
                    WHEN 'high' THEN 1
                    WHEN 'medium' THEN 2
                    WHEN 'low' THEN 3
                END,
                f.fault_date ASC
        """
        
        results = self.db.execute_query(query)
        
        if results:
            print("\n" + "="*105)
            print("🚨 PENDING FAULTS (Sorted by Area Priority & Age)")
            print("="*105)
            print(f"{'ID':<6} {'Type':<25} {'Asset':<15} {'Priority':<10} {'Area':<22} {'Days Open':<10} {'Status':<16}")
            print("="*105)
            
            for row in results:
                fault = dict(row)
                fault_type_display = fault['fault_type'].replace('_', ' ').title()[:22]
                area_name = fault['area_name'][:19] + "..." if len(fault['area_name']) > 22 else fault['area_name']
                
                # Calculate days open
                fault_date = datetime.fromisoformat(fault['fault_date'])
                days_open = (datetime.now() - fault_date).days
                
                # Status indicator
                status_icon = "🔄" if fault['resolution_status'] == 'in_progress' else "🟡"
                
                print(f"{fault['fault_id']:<6} {fault_type_display:<25} "
                      f"{fault['asset_type']:<15} {fault['priority_level']:<10} "
                      f"{area_name:<22} {days_open:<10} {status_icon} {fault['resolution_status']:<14}")
            
            print("="*105)
            print(f"Total pending faults: {len(results)}")
            print("="*105 + "\n")
        else:
            print("\n✅ No pending faults! All faults have been resolved.\n")
        
        return results
    
    def get_faults_by_area(self, area_id):
        """
        Get all faults in a specific area
        
        Args:
            area_id (int): ID of the area
        
        Returns:
            list: Fault records for the specified area
        """
        # Check if area exists
        area_check = self.db.execute_query("SELECT area_name FROM AREA WHERE area_id = ?", (area_id,))
        
        if not area_check:
            print(f"\n❌ Area with ID {area_id} not found!\n")
            return []
        
        area_name = dict(area_check[0])['area_name']
        
        query = """
            SELECT f.fault_id, f.fault_type, f.fault_date, f.resolution_status,
                   ast.asset_type, ast.capacity
            FROM FAULT f
            JOIN ASSET ast ON f.asset_id = ast.asset_id
            WHERE ast.area_id = ?
            ORDER BY f.fault_date DESC
        """
        
        results = self.db.execute_query(query, (area_id,))
        
        if results:
            print("\n" + "="*100)
            print(f"FAULTS IN: {area_name} (Area ID: {area_id})")
            print("="*100)
            print(f"{'ID':<6} {'Type':<25} {'Asset':<15} {'Capacity':<20} {'Date':<15} {'Status':<19}")
            print("="*100)
            
            for row in results:
                fault = dict(row)
                fault_type_display = fault['fault_type'].replace('_', ' ').title()[:22]
                fault_date = fault['fault_date'][:10]
                
                # Status indicator
                status_icon = "✅" if fault['resolution_status'] == 'resolved' else "🔄" if fault['resolution_status'] == 'in_progress' else "🟡"
                
                print(f"{fault['fault_id']:<6} {fault_type_display:<25} "
                      f"{fault['asset_type']:<15} {fault['capacity']:<20} "
                      f"{fault_date:<15} {status_icon} {fault['resolution_status']:<17}")
            
            print("="*100 + "\n")
        else:
            print(f"\n⚠️  No faults found in {area_name}.\n")
        
        return results
    
    def get_faults_by_type(self, fault_type):
        """
        Get all faults of a specific type
        
        Args:
            fault_type (str): Type of fault
        
        Returns:
            list: Fault records of the specified type
        """
        # Validate fault type
        valid_types = ['power_outage', 'voltage_fluctuation', 'equipment_failure', 'other']
        if fault_type.lower() not in valid_types:
            print(f"❌ Invalid fault type! Must be one of: {', '.join(valid_types)}")
            return []
        
        query = """
            SELECT f.fault_id, f.fault_date, f.resolution_status,
                   ast.asset_type, a.area_name
            FROM FAULT f
            JOIN ASSET ast ON f.asset_id = ast.asset_id
            JOIN AREA a ON ast.area_id = a.area_id
            WHERE f.fault_type = ?
            ORDER BY f.fault_date DESC
        """
        
        results = self.db.execute_query(query, (fault_type.lower(),))
        
        if results:
            print("\n" + "="*95)
            print(f"FAULTS: {fault_type.replace('_', ' ').upper()}")
            print("="*95)
            print(f"{'ID':<6} {'Asset':<15} {'Area':<30} {'Date':<20} {'Status':<24}")
            print("="*95)
            
            for row in results:
                fault = dict(row)
                area_name = fault['area_name'][:27] + "..." if len(fault['area_name']) > 30 else fault['area_name']
                fault_date = fault['fault_date'][:10]
                
                # Status indicator
                status_icon = "✅" if fault['resolution_status'] == 'resolved' else "🔄" if fault['resolution_status'] == 'in_progress' else "🟡"
                
                print(f"{fault['fault_id']:<6} {fault['asset_type']:<15} "
                      f"{area_name:<30} {fault_date:<20} {status_icon} {fault['resolution_status']:<22}")
            
            print("="*95 + "\n")
        else:
            print(f"\n⚠️  No {fault_type.replace('_', ' ')} faults found.\n")
        
        return results
    
    def get_fault_statistics(self):
        """
        Get overall fault statistics
        """
        print("\n" + "="*60)
        print("FAULT STATISTICS")
        print("="*60)
        
        # Total faults
        total_query = "SELECT COUNT(*) as count FROM FAULT"
        total = dict(self.db.execute_query(total_query)[0])['count']
        print(f"Total Faults:      {total}")
        
        # By resolution status
        status_query = """
            SELECT resolution_status, COUNT(*) as count
            FROM FAULT
            GROUP BY resolution_status
            ORDER BY 
                CASE resolution_status 
                    WHEN 'pending' THEN 1 
                    WHEN 'in_progress' THEN 2 
                    WHEN 'resolved' THEN 3 
                END
        """
        status_results = self.db.execute_query(status_query)
        
        print("\nBy Resolution Status:")
        for row in status_results:
            data = dict(row)
            percentage = (data['count'] / total * 100) if total > 0 else 0
            print(f"  - {data['resolution_status'].capitalize()}: {data['count']} ({percentage:.1f}%)")
        
        # By fault type
        type_query = """
            SELECT fault_type, COUNT(*) as count
            FROM FAULT
            GROUP BY fault_type
            ORDER BY count DESC
        """
        type_results = self.db.execute_query(type_query)
        
        print("\nBy Fault Type:")
        for row in type_results:
            data = dict(row)
            fault_type_display = data['fault_type'].replace('_', ' ').title()
            print(f"  - {fault_type_display}: {data['count']}")
        
        # Average resolution time for resolved faults
        resolution_query = """
            SELECT AVG(JULIANDAY(resolution_date) - JULIANDAY(fault_date)) as avg_days
            FROM FAULT
            WHERE resolution_status = 'resolved' AND resolution_date IS NOT NULL
        """
        resolution_result = self.db.execute_query(resolution_query)
        
        if resolution_result:
            avg_days = dict(resolution_result[0])['avg_days']
            if avg_days is not None:
                print(f"\nAverage Resolution Time: {avg_days:.1f} days")
        
        print("="*60 + "\n")
    
    def get_critical_faults(self):
        """
        Get critical faults (power outages in high priority areas)
        
        Returns:
            list: Critical fault records
        """
        query = """
            SELECT f.fault_id, f.fault_type, f.fault_date, f.resolution_status,
                   ast.asset_type, a.area_name, a.priority_level
            FROM FAULT f
            JOIN ASSET ast ON f.asset_id = ast.asset_id
            JOIN AREA a ON ast.area_id = a.area_id
            WHERE f.resolution_status != 'resolved'
              AND (f.fault_type = 'power_outage' OR a.priority_level = 'high')
            ORDER BY 
                CASE f.fault_type
                    WHEN 'power_outage' THEN 1
                    ELSE 2
                END,
                CASE a.priority_level
                    WHEN 'high' THEN 1
                    WHEN 'medium' THEN 2
                    WHEN 'low' THEN 3
                END,
                f.fault_date ASC
        """
        
        results = self.db.execute_query(query)
        
        if results:
            print("\n" + "="*100)
            print("🔴 CRITICAL FAULTS (Power Outages & High Priority Areas)")
            print("="*100)
            print(f"{'ID':<6} {'Type':<25} {'Asset':<15} {'Area':<25} {'Priority':<10} {'Days Open':<14}")
            print("="*100)
            
            for row in results:
                fault = dict(row)
                fault_type_display = fault['fault_type'].replace('_', ' ').title()[:22]
                area_name = fault['area_name'][:22] + "..." if len(fault['area_name']) > 25 else fault['area_name']
                
                # Calculate days open
                fault_date = datetime.fromisoformat(fault['fault_date'])
                days_open = (datetime.now() - fault_date).days
                
                print(f"{fault['fault_id']:<6} {fault_type_display:<25} "
                      f"{fault['asset_type']:<15} {area_name:<25} "
                      f"{fault['priority_level']:<10} {days_open}{' ' * 14}")
            
            print("="*100)
            print(f"🔴 Total critical faults: {len(results)}")
            print("="*100 + "\n")
        else:
            print("\n✅ No critical faults! System is stable.\n")
        
        return results