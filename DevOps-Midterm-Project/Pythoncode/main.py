"""
Main module for the Bank Loan Management System.
Handles the user interface and program flow.
"""

import functions 
#streamlit run app.py


def display_welcome():
    """Display the welcome screen."""
    print("Welcome to the Bank Loan Management System!")
    print("==========================================")

def display_menu():
    """Display the user menu."""
    print("\nMenu:")
    print("1. Add a client")
    print("2. Remove a client")
    print("3. Edit a client")
    print("4. Display all clients")
    print("5. Add a loan")
    print("6. Remove a loan")
    print("7. Edit a loan")
    print("8. Display all loans")
    print("9. Sort clients")
    print("10. Sort loans")
    print("11. Calculate total loan amounts")
    print("12. Generate amortization schedule")
    print("13. Exit")

def initialize_test_data(clients, loans):
    """Initialize test data for demonstration."""
    clients.extend([
        {"id": 1, "name": "אלי דרוד", "email": "elid@campus.technion.ac.il", "phone": "052-55-66-77"},
        {"id": 2, "name": "איליה מקס", "email": "iliama@campus.technion.ac.il", "phone": "052-55-55-55"}
    ])
    loans.extend([
        {"id": 1, "client_id": 1, "amount": 5000.00, "interest_rate": 5.0, "term_months": 36, "status": "active"},
        {"id": 2, "client_id": 1, "amount": 10000.00, "interest_rate": 4.5, "term_months": 24, "status": "paid"},
        {"id": 3, "client_id": 2, "amount": 7500.00, "interest_rate": 6.0, "term_months": 48, "status": "active"}
    ])
    print("Test data initialized for demonstration.")

def main():
    clients = []  # Initialize empty client list
    loans = []    # Initialize empty loan list
    display_welcome()
    initialize_test_data(clients, loans)  # Add test data for demo
    
    while True:
        display_menu()
        choice = input("Enter your choice (1-13): ")
        
        if choice == "1":
            functions.add_client(clients)
        elif choice == "2":
            functions.remove_client(clients, loans)
        elif choice == "3":
            functions.edit_client(clients)
        elif choice == "4":
            functions.display_clients(clients)
        elif choice == "5":
            functions.add_loan(loans, clients)
        elif choice == "6":
            functions.remove_loan(loans)
        elif choice == "7":
            functions.edit_loan(loans, clients)
        elif choice == "8":
            functions.display_loans(loans, clients)
        elif choice == "9":
            functions.sort_clients(clients)
        elif choice == "10":
            functions.sort_loans(loans)
        elif choice == "11":
            functions.calculate_total_loans(loans)
        elif choice == "12":
            functions.generate_amortization_schedule(loans, clients)
        elif choice == "13":
            print("Thank you for using the Bank Loan Management System!")
            break
        else:
            print("Invalid choice. Please try again!!!!")

if __name__ == "__main__":
    main()