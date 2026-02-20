"""
Module 2: Asset Management
Handles all operations related to electrical assets (transformers, poles, cables)
"""

from src.database import Database
from datetime import date


class AssetManager:
    """Manages electrical infrastructure assets"""
    
    def __init__(self):
        self.db = Database()
    
    # =====================================================
    # ASSET OPERATIONS
    # =====================================================
    
    def add_asset(self, asset_type, capacity, area_id, installation_date=None, health_status='good'):
        """
        Add a new asset to the system
        
        Args:
            asset_type (str): Type - 'transformer', 'pole', or 'cable'
            capacity (str): Capacity/specification of the asset
            area_id (int): Area where asset is located
            installation_date (str/date): Installation date (defaults to today)
            health_status (str): Health status - 'good', 'fair', or 'poor'
        
        Returns:
            int: asset_id of newly created asset
        """
        # Validate asset type
        valid_types = ['transformer', 'pole', 'cable']
        if asset_type.lower() not in valid_types:
            print(f" Invalid asset type! Must be one of: {', '.join(valid_types)}")
            return None
        
        # Validate health status
        valid_statuses = ['good', 'fair', 'poor']
        if health_status.lower() not in valid_statuses:
            print(f" Invalid health status! Must be one of: {', '.join(valid_statuses)}")
            return None
        
        # Set installation date to today if not provided
        if installation_date is None:
            installation_date = date.today()
        
        # Verify area exists
        area_check = self.db.execute_query("SELECT area_id, area_name FROM AREA WHERE area_id = ?", (area_id,))
        
        if not area_check:
            print(f" Area with ID {area_id} not found!")
            return None
        
        area_name = dict(area_check[0])['area_name']
        
        query = """
            INSERT INTO ASSET (asset_type, capacity, installation_date, health_status, area_id)
            VALUES (?, ?, ?, ?, ?)
        """
        
        try:
            asset_id = self.db.execute_update(
                query,
                (asset_type.lower(), capacity, installation_date, health_status.lower(), area_id)
            )
            
            print(f"\n Asset added successfully!")
            print(f"Asset ID: {asset_id}")
            print(f"Type: {asset_type.capitalize()}")
            print(f"Capacity: {capacity}")
            print(f"Area: {area_name}")
            print(f"Installation Date: {installation_date}")
            print(f"Health Status: {health_status.capitalize()}\n")
            
            return asset_id
        except Exception as e:
            print(f" Error adding asset: {e}")
            return None
    
    def view_asset(self, asset_id):
        """
        View detailed information about a specific asset
        
        Args:
            asset_id (int): ID of the asset
        
        Returns:
            dict: Asset details or None if not found
        """
        query = """
            SELECT ast.*, a.area_name, a.area_type
            FROM ASSET ast
            JOIN AREA a ON ast.area_id = a.area_id
            WHERE ast.asset_id = ?
        """
        
        result = self.db.execute_query(query, (asset_id,))
        
        if result:
            asset = dict(result[0])
            
            print("\n" + "="*60)
            print("ASSET DETAILS")
            print("="*60)
            print(f"Asset ID:          {asset['asset_id']}")
            print(f"Type:              {asset['asset_type'].capitalize()}")
            print(f"Capacity:          {asset['capacity']}")
            print(f"Installation Date: {asset['installation_date']}")
            print(f"Health Status:     {asset['health_status'].capitalize()}")
            print(f"Area:              {asset['area_name']} ({asset['area_type']})")
            print("="*60 + "\n")
            
            return asset
        else:
            print(f"\n Asset with ID {asset_id} not found!\n")
            return None
    
    def list_all_assets(self):
        """
        Display all assets in the system
        
        Returns:
            list: All asset records
        """
        query = """
            SELECT ast.asset_id, ast.asset_type, ast.capacity, ast.health_status, 
                   ast.installation_date, a.area_name
            FROM ASSET ast
            JOIN AREA a ON ast.area_id = a.area_id
            ORDER BY ast.asset_id
        """
        
        results = self.db.execute_query(query)
        
        if results:
            print("\n" + "="*100)
            print("ALL ASSETS")
            print("="*100)
            print(f"{'ID':<6} {'Type':<15} {'Capacity':<20} {'Health':<10} {'Installed':<12} {'Area':<37}")
            print("="*100)
            
            for row in results:
                asset = dict(row)
                area_name = asset['area_name'][:34] + "..." if len(asset['area_name']) > 37 else asset['area_name']
                
                print(f"{asset['asset_id']:<6} {asset['asset_type']:<15} "
                      f"{asset['capacity']:<20} {asset['health_status']:<10} "
                      f"{asset['installation_date']:<12} {area_name:<37}")
            
            print("="*100 + "\n")
        else:
            print("\n  No assets found in the system.\n")
        
        return results
    
    def list_assets_by_area(self, area_id):
        """
        Display all assets in a specific area
        
        Args:
            area_id (int): ID of the area
        
        Returns:
            list: Asset records for the specified area
        """
        # Check if area exists
        area_check = self.db.execute_query("SELECT area_name FROM AREA WHERE area_id = ?", (area_id,))
        
        if not area_check:
            print(f"\n Area with ID {area_id} not found!\n")
            return []
        
        area_name = dict(area_check[0])['area_name']
        
        query = """
            SELECT asset_id, asset_type, capacity, health_status, installation_date
            FROM ASSET
            WHERE area_id = ?
            ORDER BY asset_type, asset_id
        """
        
        results = self.db.execute_query(query, (area_id,))
        
        if results:
            print("\n" + "="*90)
            print(f"ASSETS IN: {area_name} (Area ID: {area_id})")
            print("="*90)
            print(f"{'ID':<6} {'Type':<15} {'Capacity':<25} {'Health':<12} {'Installed':<32}")
            print("="*90)
            
            for row in results:
                asset = dict(row)
                print(f"{asset['asset_id']:<6} {asset['asset_type']:<15} "
                      f"{asset['capacity']:<25} {asset['health_status']:<12} "
                      f"{asset['installation_date']:<32}")
            
            print("="*90 + "\n")
        else:
            print(f"\n  No assets found in {area_name}.\n")
        
        return results
    
    def list_assets_by_type(self, asset_type):
        """
        Display all assets of a specific type
        
        Args:
            asset_type (str): Type of asset ('transformer', 'pole', 'cable')
        
        Returns:
            list: Asset records of the specified type
        """
        # Validate asset type
        valid_types = ['transformer', 'pole', 'cable']
        if asset_type.lower() not in valid_types:
            print(f" Invalid asset type! Must be one of: {', '.join(valid_types)}")
            return []
        
        query = """
            SELECT ast.asset_id, ast.capacity, ast.health_status, 
                   ast.installation_date, a.area_name
            FROM ASSET ast
            JOIN AREA a ON ast.area_id = a.area_id
            WHERE ast.asset_type = ?
            ORDER BY ast.asset_id
        """
        
        results = self.db.execute_query(query, (asset_type.lower(),))
        
        if results:
            print("\n" + "="*95)
            print(f"ALL {asset_type.upper()}S")
            print("="*95)
            print(f"{'ID':<6} {'Capacity':<25} {'Health':<12} {'Installed':<15} {'Area':<37}")
            print("="*95)
            
            for row in results:
                asset = dict(row)
                area_name = asset['area_name'][:34] + "..." if len(asset['area_name']) > 37 else asset['area_name']
                
                print(f"{asset['asset_id']:<6} {asset['capacity']:<25} "
                      f"{asset['health_status']:<12} {asset['installation_date']:<15} {area_name:<37}")
            
            print("="*95 + "\n")
        else:
            print(f"\n  No {asset_type}s found in the system.\n")
        
        return results
    
    def update_asset_health(self, asset_id, new_status):
        """
        Update the health status of an asset
        
        Args:
            asset_id (int): ID of the asset
            new_status (str): New health status ('good', 'fair', 'poor')
        
        Returns:
            bool: True if successful, False otherwise
        """
        # Validate health status
        valid_statuses = ['good', 'fair', 'poor']
        if new_status.lower() not in valid_statuses:
            print(f" Invalid health status! Must be one of: {', '.join(valid_statuses)}")
            return False
        
        # Check if asset exists
        check_query = "SELECT asset_id, asset_type FROM ASSET WHERE asset_id = ?"
        result = self.db.execute_query(check_query, (asset_id,))
        
        if not result:
            print(f" Asset with ID {asset_id} not found!")
            return False
        
        asset_type = dict(result[0])['asset_type']
        
        query = "UPDATE ASSET SET health_status = ? WHERE asset_id = ?"
        
        try:
            self.db.execute_update(query, (new_status.lower(), asset_id))
            print(f"\n {asset_type.capitalize()} health status updated to '{new_status}' successfully!\n")
            return True
        except Exception as e:
            print(f" Error updating asset: {e}")
            return False
    
    def get_assets_needing_maintenance(self):
        """
        Get all assets with poor or fair health status
        
        Returns:
            list: Assets that need maintenance
        """
        query = """
            SELECT ast.asset_id, ast.asset_type, ast.capacity, ast.health_status,
                   ast.installation_date, a.area_name, a.priority_level
            FROM ASSET ast
            JOIN AREA a ON ast.area_id = a.area_id
            WHERE ast.health_status IN ('fair', 'poor')
            ORDER BY 
                CASE ast.health_status 
                    WHEN 'poor' THEN 1 
                    WHEN 'fair' THEN 2 
                END,
                CASE a.priority_level
                    WHEN 'high' THEN 1
                    WHEN 'medium' THEN 2
                    WHEN 'low' THEN 3
                END
        """
        
        results = self.db.execute_query(query)
        
        if results:
            print("\n" + "="*100)
            print("  ASSETS NEEDING MAINTENANCE (Sorted by Priority)")
            print("="*100)
            print(f"{'ID':<6} {'Type':<15} {'Capacity':<20} {'Health':<10} {'Area Priority':<15} {'Area':<34}")
            print("="*100)
            
            for row in results:
                asset = dict(row)
                area_name = asset['area_name'][:31] + "..." if len(asset['area_name']) > 34 else asset['area_name']
                
                # Add visual indicator for poor health
                health_indicator = "🔴 " if asset['health_status'] == 'poor' else "🟡 "
                
                print(f"{asset['asset_id']:<6} {asset['asset_type']:<15} "
                      f"{asset['capacity']:<20} {health_indicator}{asset['health_status']:<8} "
                      f"{asset['priority_level']:<15} {area_name:<34}")
            
            print("="*100)
            print(f"Total assets needing maintenance: {len(results)}")
            print("="*100 + "\n")
        else:
            print("\n All assets are in good condition! No maintenance needed.\n")
        
        return results
    
    def get_asset_statistics(self):
        """
        Get statistics about assets in the system
        """
        print("\n" + "="*60)
        print("ASSET STATISTICS")
        print("="*60)
        
        # Total assets
        total_query = "SELECT COUNT(*) as count FROM ASSET"
        total = dict(self.db.execute_query(total_query)[0])['count']
        print(f"Total Assets: {total}")
        
        # By type
        type_query = """
            SELECT asset_type, COUNT(*) as count
            FROM ASSET
            GROUP BY asset_type
            ORDER BY count DESC
        """
        type_results = self.db.execute_query(type_query)
        
        print("\nBy Type:")
        for row in type_results:
            data = dict(row)
            print(f"  - {data['asset_type'].capitalize()}: {data['count']}")
        
        # By health status
        health_query = """
            SELECT health_status, COUNT(*) as count
            FROM ASSET
            GROUP BY health_status
            ORDER BY 
                CASE health_status 
                    WHEN 'good' THEN 1 
                    WHEN 'fair' THEN 2 
                    WHEN 'poor' THEN 3 
                END
        """
        health_results = self.db.execute_query(health_query)
        
        print("\nBy Health Status:")
        for row in health_results:
            data = dict(row)
            percentage = (data['count'] / total * 100) if total > 0 else 0
            print(f"  - {data['health_status'].capitalize()}: {data['count']} ({percentage:.1f}%)")
        
        print("="*60 + "\n")
    
    def search_assets_by_capacity(self, search_term):
        """
        Search for assets by capacity (partial match)
        
        Args:
            search_term (str): Capacity or partial capacity to search
        
        Returns:
            list: Matching asset records
        """
        query = """
            SELECT ast.asset_id, ast.asset_type, ast.capacity, ast.health_status, a.area_name
            FROM ASSET ast
            JOIN AREA a ON ast.area_id = a.area_id
            WHERE ast.capacity LIKE ?
            ORDER BY ast.asset_type, ast.asset_id
        """
        
        results = self.db.execute_query(query, (f"%{search_term}%",))
        
        if results:
            print("\n" + "="*95)
            print(f"SEARCH RESULTS FOR CAPACITY: '{search_term}'")
            print("="*95)
            print(f"{'ID':<6} {'Type':<15} {'Capacity':<25} {'Health':<12} {'Area':<37}")
            print("="*95)
            
            for row in results:
                asset = dict(row)
                area_name = asset['area_name'][:34] + "..." if len(asset['area_name']) > 37 else asset['area_name']
                
                print(f"{asset['asset_id']:<6} {asset['asset_type']:<15} "
                      f"{asset['capacity']:<25} {asset['health_status']:<12} {area_name:<37}")
            
            print("="*95 + "\n")
        else:
            print(f"\n  No assets found matching capacity '{search_term}'.\n")
        
        return results