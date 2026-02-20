"""
Module 1: Area & Consumer Management
Handles all operations related to areas and consumers
"""

from src.database import Database


class AreaConsumerManager:
    """Manages areas and consumers in the electricity distribution system"""
    
    def __init__(self):
        self.db = Database()
    
    # =====================================================
    # AREA OPERATIONS
    # =====================================================
    
    def add_area(self, area_name, area_type, priority_level='medium'):
        """
        Add a new distribution area
        
        Args:
            area_name (str): Name of the area
            area_type (str): Type - 'residential', 'commercial', or 'industrial'
            priority_level (str): Priority - 'high', 'medium', or 'low'
        
        Returns:
            int: area_id of newly created area
        """
        # Validate area_type
        valid_types = ['residential', 'commercial', 'industrial']
        if area_type.lower() not in valid_types:
            print(f"❌ Invalid area type! Must be one of: {', '.join(valid_types)}")
            return None
        
        # Validate priority_level
        valid_priorities = ['high', 'medium', 'low']
        if priority_level.lower() not in valid_priorities:
            print(f"❌ Invalid priority level! Must be one of: {', '.join(valid_priorities)}")
            return None
        
        query = """
            INSERT INTO AREA (area_name, area_type, priority_level)
            VALUES (?, ?, ?)
        """
        
        try:
            area_id = self.db.execute_update(query, (area_name, area_type.lower(), priority_level.lower()))
            print(f"\n✅ Area added successfully!")
            print(f"Area ID: {area_id}")
            print(f"Name: {area_name}")
            print(f"Type: {area_type}")
            print(f"Priority: {priority_level}\n")
            return area_id
        except Exception as e:
            print(f"❌ Error adding area: {e}")
            return None
    
    def list_all_areas(self):
        """
        Display all areas in the system
        
        Returns:
            list: All area records
        """
        query = "SELECT * FROM AREA ORDER BY area_id"
        results = self.db.execute_query(query)
        
        if results:
            print("\n" + "="*85)
            print("ALL AREAS")
            print("="*85)
            print(f"{'ID':<6} {'Area Name':<35} {'Type':<15} {'Priority':<10} {'Consumers':<10}")
            print("="*85)
            
            for row in results:
                area = dict(row)
                # Get consumer count for this area
                count_query = "SELECT COUNT(*) as count FROM CONSUMER WHERE area_id = ?"
                count_result = self.db.execute_query(count_query, (area['area_id'],))
                consumer_count = dict(count_result[0])['count'] if count_result else 0
                
                print(f"{area['area_id']:<6} {area['area_name']:<35} "
                      f"{area['area_type']:<15} {area['priority_level']:<10} {consumer_count:<10}")
            
            print("="*85 + "\n")
        else:
            print("\n  No areas found in the system.\n")
        
        return results
    
    def view_area_details(self, area_id):
        """
        View detailed information about a specific area
        
        Args:
            area_id (int): ID of the area to view
        
        Returns:
            dict: Area details or None if not found
        """
        query = """
            SELECT a.*, COUNT(c.consumer_id) as consumer_count
            FROM AREA a
            LEFT JOIN CONSUMER c ON a.area_id = c.area_id
            WHERE a.area_id = ?
            GROUP BY a.area_id
        """
        
        result = self.db.execute_query(query, (area_id,))
        
        if result:
            area = dict(result[0])
            
            print("\n" + "="*60)
            print("AREA DETAILS")
            print("="*60)
            print(f"Area ID:          {area['area_id']}")
            print(f"Name:             {area['area_name']}")
            print(f"Type:             {area['area_type'].capitalize()}")
            print(f"Priority Level:   {area['priority_level'].capitalize()}")
            print(f"Total Consumers:  {area['consumer_count']}")
            print("="*60 + "\n")
            
            return area
        else:
            print(f"\n Area with ID {area_id} not found!\n")
            return None
    
    def update_area_priority(self, area_id, new_priority):
        """
        Update priority level of an area
        
        Args:
            area_id (int): ID of the area
            new_priority (str): New priority level
        
        Returns:
            bool: True if successful, False otherwise
        """
        # Validate priority
        valid_priorities = ['high', 'medium', 'low']
        if new_priority.lower() not in valid_priorities:
            print(f"\n Invalid priority! Must be one of: {', '.join(valid_priorities)}")
            return False
        
        # Check if area exists
        check_query = "SELECT area_id FROM AREA WHERE area_id = ?"
        if not self.db.execute_query(check_query, (area_id,)):
            print(f"\n Area with ID {area_id} not found!")
            return False
        
        query = "UPDATE AREA SET priority_level = ? WHERE area_id = ?"
        
        try:
            self.db.execute_update(query, (new_priority.lower(), area_id))
            print(f"\n Area priority updated to '{new_priority}' successfully!\n")
            return True
        except Exception as e:
            print(f" Error updating area: {e}")
            return False
    
    # =====================================================
    # CONSUMER OPERATIONS
    # =====================================================
    
    def add_consumer(self, name, address, phone, area_id):
        """
        Add a new consumer to the system
        
        Args:
            name (str): Consumer name
            address (str): Consumer address
            phone (str): Phone number
            area_id (int): ID of the area where consumer is located
        
        Returns:
            int: consumer_id of newly created consumer
        """
        # Verify area exists
        area_check = self.db.execute_query("SELECT area_id, area_name FROM AREA WHERE area_id = ?", (area_id,))
        
        if not area_check:
            print(f"\n Area with ID {area_id} not found!")
            print("Please use a valid area ID or create a new area first.")
            return None
        
        area_name = dict(area_check[0])['area_name']
        
        query = """
            INSERT INTO CONSUMER (name, address, phone, area_id)
            VALUES (?, ?, ?, ?)
        """
        
        try:
            consumer_id = self.db.execute_update(query, (name, address, phone, area_id))
            print(f"\n Consumer added successfully!")
            print(f"Consumer ID: {consumer_id}")
            print(f"Name: {name}")
            print(f"Area: {area_name}")
            print(f"Phone: {phone}\n")
            return consumer_id
        except Exception as e:
            print(f" Error adding consumer: {e}")
            return None
    
    def view_consumer(self, consumer_id):
        """
        View detailed information about a specific consumer
        
        Args:
            consumer_id (int): ID of the consumer
        
        Returns:
            dict: Consumer details or None if not found
        """
        query = """
            SELECT c.*, a.area_name, a.area_type, a.priority_level
            FROM CONSUMER c
            JOIN AREA a ON c.area_id = a.area_id
            WHERE c.consumer_id = ?
        """
        
        result = self.db.execute_query(query, (consumer_id,))
        
        if result:
            consumer = dict(result[0])
            
            print("\n" + "="*60)
            print("CONSUMER DETAILS")
            print("="*60)
            print(f"Consumer ID:  {consumer['consumer_id']}")
            print(f"Name:         {consumer['name']}")
            print(f"Address:      {consumer['address']}")
            print(f"Phone:        {consumer['phone']}")
            print(f"Area:         {consumer['area_name']} ({consumer['area_type']})")
            print(f"Priority:     {consumer['priority_level'].capitalize()}")
            print("="*60 + "\n")
            
            return consumer
        else:
            print(f"\n Consumer with ID {consumer_id} not found!\n")
            return None
    
    def list_all_consumers(self):
        """
        Display all consumers in the system
        
        Returns:
            list: All consumer records
        """
        query = """
            SELECT c.consumer_id, c.name, c.phone, c.address, a.area_name
            FROM CONSUMER c
            JOIN AREA a ON c.area_id = a.area_id
            ORDER BY c.consumer_id
        """
        
        results = self.db.execute_query(query)
        
        if results:
            print("\n" + "="*100)
            print("ALL CONSUMERS")
            print("="*100)
            print(f"{'ID':<6} {'Name':<25} {'Phone':<15} {'Area':<30} {'Address':<24}")
            print("="*100)
            
            for row in results:
                consumer = dict(row)
                # Truncate address if too long
                address = consumer['address'][:21] + "..." if len(consumer['address']) > 24 else consumer['address']
                
                print(f"{consumer['consumer_id']:<6} {consumer['name']:<25} "
                      f"{consumer['phone']:<15} {consumer['area_name']:<30} {address:<24}")
            
            print("="*100 + "\n")
        else:
            print("\n  No consumers found in the system.\n")
        
        return results
    
    def list_consumers_by_area(self, area_id):
        """
        Display all consumers in a specific area
        
        Args:
            area_id (int): ID of the area
        
        Returns:
            list: Consumer records for the specified area
        """
        # Check if area exists
        area_check = self.db.execute_query("SELECT area_name FROM AREA WHERE area_id = ?", (area_id,))
        
        if not area_check:
            print(f"\n Area with ID {area_id} not found!\n")
            return []
        
        area_name = dict(area_check[0])['area_name']
        
        query = """
            SELECT consumer_id, name, phone, address
            FROM CONSUMER
            WHERE area_id = ?
            ORDER BY consumer_id
        """
        
        results = self.db.execute_query(query, (area_id,))
        
        if results:
            print("\n" + "="*90)
            print(f"CONSUMERS IN: {area_name} (Area ID: {area_id})")
            print("="*90)
            print(f"{'ID':<6} {'Name':<25} {'Phone':<15} {'Address':<44}")
            print("="*90)
            
            for row in results:
                consumer = dict(row)
                print(f"{consumer['consumer_id']:<6} {consumer['name']:<25} "
                      f"{consumer['phone']:<15} {consumer['address']:<44}")
            
            print("="*90 + "\n")
        else:
            print(f"\n  No consumers found in {area_name}.\n")
        
        return results
    
    def update_consumer(self, consumer_id, **kwargs):
        """
        Update consumer details
        
        Args:
            consumer_id (int): ID of the consumer
            **kwargs: Fields to update (name, address, phone)
        
        Returns:
            bool: True if successful, False otherwise
        """
        # Check if consumer exists
        check_query = "SELECT consumer_id FROM CONSUMER WHERE consumer_id = ?"
        if not self.db.execute_query(check_query, (consumer_id,)):
            print(f" Consumer with ID {consumer_id} not found!")
            return False
        
        allowed_fields = ['name', 'address', 'phone']
        updates = []
        params = []
        
        for key, value in kwargs.items():
            if key in allowed_fields and value:
                updates.append(f"{key} = ?")
                params.append(value)
        
        if not updates:
            print(" No valid fields to update!")
            return False
        
        params.append(consumer_id)
        query = f"UPDATE CONSUMER SET {', '.join(updates)} WHERE consumer_id = ?"
        
        try:
            self.db.execute_update(query, tuple(params))
            print(f"\n Consumer updated successfully!\n")
            return True
        except Exception as e:
            print(f" Error updating consumer: {e}")
            return False
    
    def search_consumer_by_name(self, search_term):
        """
        Search for consumers by name (partial match)
        
        Args:
            search_term (str): Name or partial name to search
        
        Returns:
            list: Matching consumer records
        """
        query = """
            SELECT c.consumer_id, c.name, c.phone, a.area_name
            FROM CONSUMER c
            JOIN AREA a ON c.area_id = a.area_id
            WHERE c.name LIKE ?
            ORDER BY c.name
        """
        
        results = self.db.execute_query(query, (f"%{search_term}%",))
        
        if results:
            print("\n" + "="*80)
            print(f"SEARCH RESULTS FOR: '{search_term}'")
            print("="*80)
            print(f"{'ID':<6} {'Name':<30} {'Phone':<15} {'Area':<29}")
            print("="*80)
            
            for row in results:
                consumer = dict(row)
                print(f"{consumer['consumer_id']:<6} {consumer['name']:<30} "
                      f"{consumer['phone']:<15} {consumer['area_name']:<29}")
            
            print("="*80 + "\n")
        else:
            print(f"\n  No consumers found matching '{search_term}'.\n")
        
        return results
