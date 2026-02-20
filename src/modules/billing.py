"""
Module 4: Billing Management
Handles all operations related to bill generation and payment tracking
"""

from src.database import Database
from src.config import BILLING_RATES, BILL_DUE_DAYS
from datetime import date, timedelta, datetime


class BillingManager:
    """Manages billing and payment operations"""
    
    def __init__(self):
        self.db = Database()
        self.rates = BILLING_RATES
        self.due_days = BILL_DUE_DAYS
    
    # =====================================================
    # BILL GENERATION
    # =====================================================
    
    def generate_bill(self, consumer_id, billing_month, total_units):
        """
        Generate a bill for a consumer
        
        Args:
            consumer_id (int): ID of the consumer
            billing_month (str): Billing month (e.g., 'February 2024')
            total_units (float): Total units consumed
        
        Returns:
            int: bill_id of newly created bill
        """
        # Get consumer and area information
        query = """
            SELECT c.consumer_id, c.name, c.address, c.phone,
                   a.area_type, a.area_name
            FROM CONSUMER c
            JOIN AREA a ON c.area_id = a.area_id
            WHERE c.consumer_id = ?
        """
        
        result = self.db.execute_query(query, (consumer_id,))
        
        if not result:
            print(f"❌ Consumer with ID {consumer_id} not found!")
            return None
        
        consumer = dict(result[0])
        area_type = consumer['area_type']
        
        # Validate units
        if total_units < 0:
            print("❌ Total units cannot be negative!")
            return None
        
        # Calculate total amount based on area type
        rate = self.rates.get(area_type, 5.50)
        total_amount = round(total_units * rate, 2)
        
        # Set due date
        due_date = date.today() + timedelta(days=self.due_days)
        
        # Insert bill
        insert_query = """
            INSERT INTO BILL (billing_month, total_units, total_amount, payment_status, due_date, consumer_id)
            VALUES (?, ?, ?, 'pending', ?, ?)
        """
        
        try:
            bill_id = self.db.execute_update(
                insert_query,
                (billing_month, total_units, total_amount, due_date, consumer_id)
            )
            
            print("\n" + "="*60)
            print("✅ BILL GENERATED SUCCESSFULLY")
            print("="*60)
            print(f"Bill ID:           {bill_id}")
            print(f"Consumer:          {consumer['name']}")
            print(f"Address:           {consumer['address']}")
            print(f"Billing Month:     {billing_month}")
            print(f"Area Type:         {area_type.capitalize()}")
            print(f"\nCharges:")
            print(f"  Total Units:     {total_units}")
            print(f"  Rate per Unit:   ₹{rate}")
            print(f"  Total Amount:    ₹{total_amount:.2f}")
            print(f"\nPayment Details:")
            print(f"  Status:          Pending")
            print(f"  Due Date:        {due_date}")
            print("="*60 + "\n")
            
            return bill_id
        except Exception as e:
            print(f"❌ Error generating bill: {e}")
            return None
    
    def generate_bill_from_consumption(self, consumer_id, billing_month, month_year):
        """
        Generate bill automatically from consumption records
        
        Args:
            consumer_id (int): ID of the consumer
            billing_month (str): Display name for billing month (e.g., 'February 2024')
            month_year (str): Month in format 'YYYY-MM' for querying consumption
        
        Returns:
            int: bill_id of newly created bill
        """
        # Get meter for consumer
        meter_query = """
            SELECT meter_id FROM METER WHERE consumer_id = ?
        """
        meter_result = self.db.execute_query(meter_query, (consumer_id,))
        
        if not meter_result:
            print(f"❌ No meter found for consumer ID {consumer_id}!")
            print("Please add a meter first.")
            return None
        
        meter_id = dict(meter_result[0])['meter_id']
        
        # Get total consumption for the month
        consumption_query = """
            SELECT SUM(units_consumed) as total_units
            FROM CONSUMPTION
            WHERE meter_id = ?
              AND strftime('%Y-%m', reading_time) = ?
        """
        consumption_result = self.db.execute_query(consumption_query, (meter_id, month_year))
        
        if not consumption_result or dict(consumption_result[0])['total_units'] is None:
            print(f"❌ No consumption data found for {billing_month}!")
            print("Please record consumption first or use manual bill generation.")
            return None
        
        total_units = dict(consumption_result[0])['total_units']
        
        # Generate bill using the total units
        return self.generate_bill(consumer_id, billing_month, total_units)
    
    # =====================================================
    # BILL VIEWING
    # =====================================================
    
    def view_bill(self, bill_id):
        """
        View detailed bill information
        
        Args:
            bill_id (int): ID of the bill
        
        Returns:
            dict: Bill details or None if not found
        """
        query = """
            SELECT b.*, c.name, c.address, c.phone, a.area_type, a.area_name
            FROM BILL b
            JOIN CONSUMER c ON b.consumer_id = c.consumer_id
            JOIN AREA a ON c.area_id = a.area_id
            WHERE b.bill_id = ?
        """
        
        result = self.db.execute_query(query, (bill_id,))
        
        if result:
            bill = dict(result[0])
            
            # Calculate rate from total
            rate = bill['total_amount'] / bill['total_units'] if bill['total_units'] > 0 else 0
            
            print("\n" + "="*60)
            print("ELECTRICITY BILL")
            print("="*60)
            print(f"Bill ID:           {bill['bill_id']}")
            print(f"Billing Month:     {bill['billing_month']}")
            print(f"\nConsumer Details:")
            print(f"  Name:            {bill['name']}")
            print(f"  Address:         {bill['address']}")
            print(f"  Phone:           {bill['phone']}")
            print(f"  Area:            {bill['area_name']} ({bill['area_type']})")
            print(f"\nCharges:")
            print(f"  Total Units:     {bill['total_units']}")
            print(f"  Rate per Unit:   ₹{rate:.2f}")
            print(f"  Total Amount:    ₹{bill['total_amount']:.2f}")
            print(f"\nPayment Details:")
            print(f"  Status:          {bill['payment_status'].upper()}")
            print(f"  Due Date:        {bill['due_date']}")
            
            # Show overdue warning if applicable
            if bill['payment_status'] == 'pending':
                due_date_obj = datetime.strptime(bill['due_date'], '%Y-%m-%d').date()
                if due_date_obj < date.today():
                    days_overdue = (date.today() - due_date_obj).days
                    print(f"\n⚠️  OVERDUE by {days_overdue} days!")
            elif bill['payment_status'] == 'paid':
                print(f"\n✅ PAID")
            
            print("="*60 + "\n")
            
            return bill
        else:
            print(f"\n❌ Bill with ID {bill_id} not found!\n")
            return None
    
    def list_all_bills(self):
        """
        Display all bills in the system
        
        Returns:
            list: All bill records
        """
        query = """
            SELECT b.bill_id, c.name, b.billing_month, b.total_units, 
                   b.total_amount, b.payment_status, b.due_date
            FROM BILL b
            JOIN CONSUMER c ON b.consumer_id = c.consumer_id
            ORDER BY b.bill_id DESC
        """
        
        results = self.db.execute_query(query)
        
        if results:
            print("\n" + "="*110)
            print("ALL BILLS")
            print("="*110)
            print(f"{'ID':<8} {'Consumer':<25} {'Month':<18} {'Units':<10} {'Amount':<12} {'Status':<10} {'Due Date':<27}")
            print("="*110)
            
            for row in results:
                bill = dict(row)
                consumer_name = bill['name'][:22] + "..." if len(bill['name']) > 25 else bill['name']
                
                # Add status indicator
                status_icon = "✅" if bill['payment_status'] == 'paid' else "⚠️" if bill['payment_status'] == 'overdue' else "🟡"
                
                print(f"{bill['bill_id']:<8} {consumer_name:<25} "
                      f"{bill['billing_month']:<18} {bill['total_units']:<10.2f} "
                      f"₹{bill['total_amount']:<11.2f} {status_icon} {bill['payment_status']:<8} "
                      f"{bill['due_date']:<27}")
            
            print("="*110 + "\n")
        else:
            print("\n⚠️  No bills found in the system.\n")
        
        return results
    
    def get_pending_bills(self, consumer_id=None):
        """
        Get all pending bills (optionally for a specific consumer)
        
        Args:
            consumer_id (int): Optional consumer ID to filter
        
        Returns:
            list: Pending bill records
        """
        if consumer_id:
            # Verify consumer exists
            consumer_check = self.db.execute_query(
                "SELECT name FROM CONSUMER WHERE consumer_id = ?",
                (consumer_id,)
            )
            if not consumer_check:
                print(f"❌ Consumer with ID {consumer_id} not found!")
                return []
            
            consumer_name = dict(consumer_check[0])['name']
            
            query = """
                SELECT b.bill_id, b.billing_month, b.total_units, b.total_amount, b.due_date
                FROM BILL b
                WHERE b.payment_status = 'pending' AND b.consumer_id = ?
                ORDER BY b.due_date
            """
            results = self.db.execute_query(query, (consumer_id,))
            
            header = f"PENDING BILLS FOR: {consumer_name} (Consumer ID: {consumer_id})"
        else:
            query = """
                SELECT b.bill_id, c.name, b.billing_month, b.total_amount, b.due_date
                FROM BILL b
                JOIN CONSUMER c ON b.consumer_id = c.consumer_id
                WHERE b.payment_status = 'pending'
                ORDER BY b.due_date
            """
            results = self.db.execute_query(query)
            
            header = "ALL PENDING BILLS"
        
        if results:
            print("\n" + "="*95)
            print(header)
            print("="*95)
            
            if consumer_id:
                print(f"{'Bill ID':<10} {'Month':<20} {'Units':<10} {'Amount':<15} {'Due Date':<40}")
            else:
                print(f"{'Bill ID':<10} {'Consumer':<25} {'Month':<20} {'Amount':<15} {'Due Date':<25}")
            
            print("="*95)
            
            for row in results:
                bill = dict(row)
                
                # Check if overdue
                due_date_obj = datetime.strptime(bill['due_date'], '%Y-%m-%d').date()
                is_overdue = due_date_obj < date.today()
                overdue_flag = " ⚠️ OVERDUE" if is_overdue else ""
                
                if consumer_id:
                    print(f"{bill['bill_id']:<10} {bill['billing_month']:<20} "
                          f"{bill['total_units']:<10.2f} ₹{bill['total_amount']:<14.2f} "
                          f"{bill['due_date']}{overdue_flag:<40}")
                else:
                    consumer_name = bill['name'][:22] + "..." if len(bill['name']) > 25 else bill['name']
                    print(f"{bill['bill_id']:<10} {consumer_name:<25} {bill['billing_month']:<20} "
                          f"₹{bill['total_amount']:<14.2f} {bill['due_date']}{overdue_flag:<25}")
            
            print("="*95)
            print(f"Total pending bills: {len(results)}")
            print("="*95 + "\n")
        else:
            if consumer_id:
                print(f"\n✅ No pending bills for {consumer_name}.\n")
            else:
                print("\n✅ No pending bills in the system.\n")
        
        return results
    
    # =====================================================
    # PAYMENT OPERATIONS
    # =====================================================
    
    def record_payment(self, bill_id):
        """
        Record payment for a bill and mark it as paid
        
        Args:
            bill_id (int): ID of the bill
        
        Returns:
            bool: True if successful, False otherwise
        """
        # Check if bill exists
        bill_query = "SELECT bill_id, total_amount, payment_status, consumer_id FROM BILL WHERE bill_id = ?"
        result = self.db.execute_query(bill_query, (bill_id,))
        
        if not result:
            print(f"❌ Bill with ID {bill_id} not found!")
            return False
        
        bill = dict(result[0])
        
        if bill['payment_status'] == 'paid':
            print(f"❌ Bill ID {bill_id} is already paid!")
            return False
        
        # Get consumer name
        consumer_query = "SELECT name FROM CONSUMER WHERE consumer_id = ?"
        consumer_result = self.db.execute_query(consumer_query, (bill['consumer_id'],))
        consumer_name = dict(consumer_result[0])['name'] if consumer_result else "Unknown"
        
        # Update payment status
        update_query = "UPDATE BILL SET payment_status = 'paid' WHERE bill_id = ?"
        
        try:
            self.db.execute_update(update_query, (bill_id,))
            
            print("\n" + "="*60)
            print("✅ PAYMENT RECORDED SUCCESSFULLY")
            print("="*60)
            print(f"Bill ID:           {bill_id}")
            print(f"Consumer:          {consumer_name}")
            print(f"Amount Paid:       ₹{bill['total_amount']:.2f}")
            print(f"Payment Date:      {date.today()}")
            print(f"Status:            PAID")
            print("="*60 + "\n")
            
            return True
        except Exception as e:
            print(f"❌ Error recording payment: {e}")
            return False
    
    def get_payment_history(self, consumer_id):
        """
        View payment history for a consumer
        
        Args:
            consumer_id (int): ID of the consumer
        
        Returns:
            list: Paid bill records
        """
        # Verify consumer exists
        consumer_check = self.db.execute_query(
            "SELECT name FROM CONSUMER WHERE consumer_id = ?",
            (consumer_id,)
        )
        
        if not consumer_check:
            print(f"❌ Consumer with ID {consumer_id} not found!")
            return []
        
        consumer_name = dict(consumer_check[0])['name']
        
        query = """
            SELECT bill_id, billing_month, total_units, total_amount, due_date
            FROM BILL
            WHERE consumer_id = ? AND payment_status = 'paid'
            ORDER BY bill_id DESC
        """
        
        results = self.db.execute_query(query, (consumer_id,))
        
        if results:
            print("\n" + "="*95)
            print(f"PAYMENT HISTORY FOR: {consumer_name} (Consumer ID: {consumer_id})")
            print("="*95)
            print(f"{'Bill ID':<10} {'Month':<20} {'Units':<10} {'Amount':<15} {'Paid':<40}")
            print("="*95)
            
            total_paid = 0
            for row in results:
                bill = dict(row)
                total_paid += bill['total_amount']
                
                print(f"{bill['bill_id']:<10} {bill['billing_month']:<20} "
                      f"{bill['total_units']:<10.2f} ₹{bill['total_amount']:<14.2f} "
                      f"✅ Paid{' ' * 35}")
            
            print("="*95)
            print(f"Total amount paid: ₹{total_paid:.2f}")
            print("="*95 + "\n")
        else:
            print(f"\n⚠️  No payment history found for {consumer_name}.\n")
        
        return results
    
    # =====================================================
    # BILLING STATISTICS & REPORTS
    # =====================================================
    
    def get_billing_statistics(self):
        """
        Get overall billing statistics
        """
        print("\n" + "="*60)
        print("BILLING STATISTICS")
        print("="*60)
        
        # Total bills
        total_query = "SELECT COUNT(*) as count FROM BILL"
        total = dict(self.db.execute_query(total_query)[0])['count']
        print(f"Total Bills:       {total}")
        
        # By payment status
        status_query = """
            SELECT payment_status, COUNT(*) as count, SUM(total_amount) as amount
            FROM BILL
            GROUP BY payment_status
        """
        status_results = self.db.execute_query(status_query)
        
        print("\nBy Payment Status:")
        for row in status_results:
            data = dict(row)
            print(f"  - {data['payment_status'].capitalize()}: {data['count']} bills, ₹{data['amount']:.2f}")
        
        # Revenue summary
        revenue_query = """
            SELECT SUM(total_amount) as total_revenue
            FROM BILL
            WHERE payment_status = 'paid'
        """
        revenue_result = self.db.execute_query(revenue_query)
        total_revenue = dict(revenue_result[0])['total_revenue'] or 0
        
        pending_query = """
            SELECT SUM(total_amount) as pending_amount
            FROM BILL
            WHERE payment_status = 'pending'
        """
        pending_result = self.db.execute_query(pending_query)
        pending_amount = dict(pending_result[0])['pending_amount'] or 0
        
        print("\nRevenue Summary:")
        print(f"  - Total Revenue (Paid):    ₹{total_revenue:.2f}")
        print(f"  - Pending Collections:     ₹{pending_amount:.2f}")
        print(f"  - Total Billed Amount:     ₹{total_revenue + pending_amount:.2f}")
        
        print("="*60 + "\n")
    
    def get_revenue_by_area_type(self):
        """
        Get revenue breakdown by area type
        """
        query = """
            SELECT a.area_type, 
                   COUNT(b.bill_id) as bill_count,
                   SUM(b.total_units) as total_units,
                   SUM(b.total_amount) as total_revenue
            FROM BILL b
            JOIN CONSUMER c ON b.consumer_id = c.consumer_id
            JOIN AREA a ON c.area_id = a.area_id
            WHERE b.payment_status = 'paid'
            GROUP BY a.area_type
            ORDER BY total_revenue DESC
        """
        
        results = self.db.execute_query(query)
        
        if results:
            print("\n" + "="*80)
            print("REVENUE BY AREA TYPE")
            print("="*80)
            print(f"{'Area Type':<20} {'Bills':<10} {'Units':<15} {'Revenue':<35}")
            print("="*80)
            
            for row in results:
                data = dict(row)
                print(f"{data['area_type'].capitalize():<20} {data['bill_count']:<10} "
                      f"{data['total_units']:<15.2f} ₹{data['total_revenue']:<34.2f}")
            
            print("="*80 + "\n")
        else:
            print("\n⚠️  No revenue data available.\n")
        
        return results
    
    def update_overdue_bills(self):
        """
        Update status of pending bills that are past due date
        
        Returns:
            int: Number of bills marked as overdue
        """
        query = """
            UPDATE BILL 
            SET payment_status = 'overdue'
            WHERE payment_status = 'pending'
              AND DATE(due_date) < DATE('now')
        """
        
        try:
            # Get count before update
            count_query = """
                SELECT COUNT(*) as count FROM BILL
                WHERE payment_status = 'pending'
                  AND DATE(due_date) < DATE('now')
            """
            count_result = self.db.execute_query(count_query)
            count = dict(count_result[0])['count']
            
            if count > 0:
                self.db.execute_update(query)
                print(f"\n✅ Marked {count} bill(s) as overdue.\n")
            else:
                print("\n✅ No bills to mark as overdue.\n")
            
            return count
        except Exception as e:
            print(f"❌ Error updating overdue bills: {e}")
            return 0