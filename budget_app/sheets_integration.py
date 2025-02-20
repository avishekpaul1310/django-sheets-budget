from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class GoogleSheetsManager:
    def __init__(self):
        self.SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        self.creds = None
        self.service = None
        self.spreadsheet_id = os.getenv('GOOGLE_SHEET_ID')

    def authenticate(self):
        creds_path = os.path.join(os.path.dirname(__file__), 'credentials.json')
        token_path = os.path.join(os.path.dirname(__file__), 'token.json')

        if os.path.exists(token_path):
            self.creds = Credentials.from_authorized_user_file(token_path, self.SCOPES)

        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(creds_path, self.SCOPES)
                self.creds = flow.run_local_server(port=0)

            with open(token_path, 'w') as token:
                token.write(self.creds.to_json())

        self.service = build('sheets', 'v4', credentials=self.creds)
        return True

    def initialize_sheets(self):
        """Initialize the spreadsheet with required sheets and headers"""
        try:
            # Define sheets and their headers
            sheets_structure = {
                'Budget Overview': [['Total Budget', 'Last Updated', 'Total Expenses', 'Remaining Budget']],
                'Expenses': [['Date', 'Category', 'Description', 'Amount', 'Running Total']],
                'Categories': [['Category', 'Total Spent', 'Budget Allocation']]
            }

            # Get existing sheets
            sheet_metadata = self.service.spreadsheets().get(spreadsheetId=self.spreadsheet_id).execute()
            existing_sheets = [sheet['properties']['title'] for sheet in sheet_metadata['sheets']]

            # Create new sheets if they don't exist
            requests = []
            for sheet_name in sheets_structure:
                if sheet_name not in existing_sheets:
                    requests.append({
                        'addSheet': {
                            'properties': {
                                'title': sheet_name
                            }
                        }
                    })

            if requests:
                body = {'requests': requests}
                self.service.spreadsheets().batchUpdate(
                    spreadsheetId=self.spreadsheet_id,
                    body=body
                ).execute()

            # Add headers to each sheet
            for sheet_name, headers in sheets_structure.items():
                self.service.spreadsheets().values().update(
                    spreadsheetId=self.spreadsheet_id,
                    range=f'{sheet_name}!A1',
                    valueInputOption='RAW',
                    body={'values': headers}
                ).execute()

            return True

        except Exception as e:
            print(f"Error initializing sheets: {str(e)}")
            return False

    def update_budget(self, amount):
        """Update the total budget in the Overview sheet"""
        try:
            values = [[
                amount,
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                '=SUM(Expenses!D:D)',
                f'={amount}-C2'
            ]]
            
            self.service.spreadsheets().values().update(
                spreadsheetId=self.spreadsheet_id,
                range='Budget Overview!A2:D2',
                valueInputOption='USER_ENTERED',
                body={'values': values}
            ).execute()
            return True
        except Exception as e:
            print(f"Error updating budget: {str(e)}")
            return False

    def add_expense(self, expense):
        """Add a new expense entry"""
        try:
            values = [[
                expense['date'],
                expense['category'],
                expense['description'],
                expense['amount'],
                '=SUM($D$2:D2)'  # Running total formula
            ]]
            
            self.service.spreadsheets().values().append(
                spreadsheetId=self.spreadsheet_id,
                range='Expenses!A2',
                valueInputOption='USER_ENTERED',
                insertDataOption='INSERT_ROWS',
                body={'values': values}
            ).execute()
            
            # Update category totals
            self.update_category_totals()
            return True
        except Exception as e:
            print(f"Error adding expense: {str(e)}")
            return False

    def update_category_totals(self):
        """Update the category totals using spreadsheet formulas"""
        try:
            categories = ['equipment', 'salaries', 'marketing', 'miscellaneous']
            values = []
            
            for category in categories:
                values.append([
                    category,
                    f'=SUMIF(Expenses!B:B,"{category}",Expenses!D:D)',
                    ''  # Budget allocation can be set manually
                ])
            
            self.service.spreadsheets().values().update(
                spreadsheetId=self.spreadsheet_id,
                range='Categories!A2',
                valueInputOption='USER_ENTERED',
                body={'values': values}
            ).execute()
            return True
        except Exception as e:
            print(f"Error updating category totals: {str(e)}")
            return False

    def get_all_data(self):
        """Retrieve all data from the sheets"""
        try:
            ranges = [
                'Budget Overview!A2:D2',
                'Expenses!A2:E',
                'Categories!A2:C'
            ]
            
            result = self.service.spreadsheets().values().batchGet(
                spreadsheetId=self.spreadsheet_id,
                ranges=ranges
            ).execute()
            
            return {
                'overview': result['valueRanges'][0].get('values', [[0, '', 0, 0]])[0],
                'expenses': result['valueRanges'][1].get('values', []),
                'analysis': result['valueRanges'][2].get('values', [])
            }
        except Exception as e:
            print(f"Error getting data: {str(e)}")
            return None