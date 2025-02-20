from sheets_integration import GoogleSheetsManager
from datetime import datetime

def test_sheets_connection():
    # Create instance of GoogleSheetsManager
    sheets_manager = GoogleSheetsManager()
    
    try:
        # Authenticate
        print("Authenticating...")
        if sheets_manager.authenticate():
            print("Authentication successful!")
        else:
            print("Authentication failed!")
            return

        # Initialize sheets
        print("\nInitializing sheets...")
        if sheets_manager.initialize_sheets():
            print("Sheets initialized successfully!")
        else:
            print("Failed to initialize sheets!")
            return

        # Test updating budget
        print("\nTesting budget update...")
        if sheets_manager.update_budget(5000):
            print("Budget updated successfully!")
        else:
            print("Failed to update budget!")

        # Test adding an expense
        print("\nTesting expense addition...")
        test_expense = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'category': 'equipment',
            'description': 'Test Expense',
            'amount': 100
        }
        if sheets_manager.add_expense(test_expense):
            print("Expense added successfully!")
        else:
            print("Failed to add expense!")

        # Test data retrieval
        print("\nTesting data retrieval...")
        data = sheets_manager.get_all_data()
        if data:
            print("Data retrieved successfully!")
            print("\nCurrent budget overview:", data['overview'])
            print(f"Number of expenses: {len(data['expenses'])}")
        else:
            print("Failed to retrieve data!")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    test_sheets_connection()