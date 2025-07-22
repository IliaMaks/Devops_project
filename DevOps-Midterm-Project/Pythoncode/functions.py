"""
Functions module for the Bank Loan Management System.
Contains reusable logic for managing clients and loans.
"""
def add_client(clients):
    """Add a new client to the system."""
    try:
        client_id = len(clients) + 1
        name = input("Enter client name: ").strip()
        if not name:
            raise ValueError("Name cannot be empty.")
        email = input("Enter client email: ").strip()
        if "@" not in email or "." not in email:
            raise ValueError("Invalid email format.")
        phone = input("Enter client phone (e.g., 052-45-55-78): ").strip()
        if not phone:
            raise ValueError("Phone cannot be empty.")
        
        client = {
            "id": client_id,
            "name": name,
            "email": email,
            "phone": phone
        }
        clients.append(client)
        print(f"Client '{name}' added successfully!")
    except ValueError as e:
        print(f"Error: {e}")

def remove_client(clients, loans):
    """Remove a client and their associated loans by ID."""
    try:
        client_id = int(input("Enter client ID to remove: "))
        client = next((c for c in clients if c["id"] == client_id), None)
        if not client:
            print(f"Client ID {client_id} not found.")
            return
        # Remove associated loans
        loans[:] = [loan for loan in loans if loan["client_id"] != client_id]
        clients.remove(client)
        print(f"Client ID {client_id} and their loans removed successfully!")
    except ValueError:
        print("Error: Invalid ID. Please enter a number.")

def edit_client(clients):
    """Edit an existing client's details."""
    try:
        client_id = int(input("Enter client ID to edit: "))
        client = next((c for c in clients if c["id"] == client_id), None)
        if not client:
            print(f"Client ID {client_id} not found.")
            return
        print(f"Editing client: {client['name']}")
        client["name"] = input("Enter new name (or press Enter to keep current): ").strip() or client["name"]
        client["email"] = input("Enter new email (or press Enter to keep current): ").strip() or client["email"]
        client["phone"] = input("Enter new phone (or press Enter to keep current): ").strip() or client["phone"]
        if "@" not in client["email"] or "." not in client["email"]:
            raise ValueError("Invalid email format.")
        print(f"Client ID {client_id} updated successfully!")
    except ValueError as e:
        print(f"Error: {e}")

def display_clients(clients):
    """Display all clients in the system."""
    if not clients:
        print("No clients in the system.")
        return
    print("\nClients:")
    print("ID | Name | Email | Phone")
    print("-" * 50)
    for client in clients:
        print(f"{client['id']} | {client['name']} | {client['email']} | {client['phone']}")

def add_loan(loans, clients):
    """Add a new loan for a client."""
    try:
        client_id = int(input("Enter client ID for the loan: "))
        client = next((c for c in clients if c["id"] == client_id), None)
        if not client:
            print(f"Client ID {client_id} not found.")
            return
        loan_id = len(loans) + 1
        amount = float(input("Enter loan amount: "))
        interest_rate = float(input("Enter interest rate (%): "))
        term_months = int(input("Enter loan term (months): "))
        status = input("Enter loan status (active/paid): ").lower()
        
        if amount < 0 or interest_rate < 0 or term_months <= 0:
            raise ValueError("Amount and interest rate must be non-negative, term must be positive.")
        if status not in ["active", "paid"]:
            raise ValueError("Status must be 'active' or 'paid'.")
        
        loan = {
            "id": loan_id,
            "client_id": client_id,
            "amount": amount,
            "interest_rate": interest_rate,
            "term_months": term_months,
            "status": status
        }
        loans.append(loan)
        print(f"Loan ID {loan_id} added successfully for {client['name']}!")
    except ValueError as e:
        print(f"Error: {e}")

def remove_loan(loans):
    """Remove a loan by ID."""
    try:
        loan_id = int(input("Enter loan ID to remove: "))
        loan = next((l for l in loans if l["id"] == loan_id), None)
        if not loan:
            print(f"Loan ID {loan_id} not found.")
            return
        loans.remove(loan)
        print(f"Loan ID {loan_id} removed successfully!")
    except ValueError:
        print("Error: Invalid ID. Please enter a number.")

def edit_loan(loans, clients):
    """Edit an existing loan's details."""
    try:
        loan_id = int(input("Enter loan ID to edit: "))
        loan = next((l for l in loans if l["id"] == loan_id), None)
        if not loan:
            print(f"Loan ID {loan_id} not found.")
            return
        client = next((c for c in clients if c["id"] == loan["client_id"]), None)
        print(f"Editing loan ID {loan_id} for {client['name']}")
        loan["amount"] = float(input("Enter new amount (or press Enter to keep current): ") or loan["amount"])
        loan["interest_rate"] = float(input("Enter new interest rate (or press Enter to keep current): ") or loan["interest_rate"])
        loan["term_months"] = int(input("Enter new term in months (or press Enter to keep current): ") or loan["term_months"])
        loan["status"] = input("Enter new status (active/paid, or press Enter to keep current): ").lower() or loan["status"]
        if loan["amount"] < 0 or loan["interest_rate"] < 0 or loan["term_months"] <= 0:
            raise ValueError("Amount and interest rate must be non-negative, term must be positive.")
        if loan["status"] not in ["active", "paid"]:
            raise ValueError("Status must be 'active' or 'paid'.")
        print(f"Loan ID {loan_id} updated successfully!")
    except ValueError as e:
        print(f"Error: {e}")

def display_loans(loans, clients):
    """Display all loans with client information."""
    if not loans:
        print("No loans in the system.")
        return
    print("\nLoans:")
    print("ID | Client | Amount | Interest Rate | Term (Months) | Status")
    print("-" * 70)
    for loan in loans:
        client = next((c for c in clients if c["id"] == loan["client_id"]), None)
        client_name = client["name"] if client else "Unknown"
        print(f"{loan['id']} | {client_name} | ${loan['amount']:.2f} | {loan['interest_rate']}% | {loan['term_months']} | {loan['status']}")

def sort_clients(clients):
    """Sort clients by name."""
    if not clients:
        print("No clients to sort.")
        return
    sort_key = input("Sort by (name): ").lower()
    if sort_key != "name":
        print("Invalid sort key. Only 'name' is supported.")
        return
    clients.sort(key=lambda x: x["name"].lower())
    print("Clients sorted by name.")
    display_clients(clients)

def sort_loans(loans):
    """Sort loans by a chosen key (amount, interest_rate, term_months)."""
    if not loans:
        print("No loans to sort.")
        return
    sort_key = input("Sort by (amount/interest_rate/term_months): ").lower()
    valid_keys = ["amount", "interest_rate", "term_months"]
    if sort_key not in valid_keys:
        print("Invalid sort key. Choose from: amount, interest_rate, term_months")
        return
    loans.sort(key=lambda x: x[sort_key])
    print(f"Loans sorted by {sort_key}.")
    display_loans(loans, [])

def calculate_total_loans(loans):
    """Calculate the total amount and interest of all active loans."""
    if not loans:
        print("No loans in the system.")
        return
    total_amount = sum(loan["amount"] for loan in loans if loan["status"] == "active")
    total_interest = sum(loan["amount"] * (loan["interest_rate"] / 100) for loan in loans if loan["status"] == "active")
    print(f"Total active loan amount: ${total_amount:.2f}")
    print(f"Total interest on active loans: ${total_interest:.2f}")

def generate_amortization_schedule(loans, clients):
    """Generate an amortization schedule for a selected loan."""
    try:
        loan_id = int(input("Enter loan ID to generate amortization schedule: "))
        loan = next((l for l in loans if l["id"] == loan_id), None)
        if not loan:
            print(f"Loan ID {loan_id} not found.")
            return
        client = next((c for c in clients if c["id"] == loan["client_id"]), None)
        client_name = client["name"] if client else "Unknown"
        
        principal = loan["amount"]
        annual_rate = loan["interest_rate"] / 100
        monthly_rate = annual_rate / 12
        term_months = loan["term_months"]
        
        # Calculate monthly payment using annuity formula
        monthly_payment = principal * (monthly_rate * (1 + monthly_rate) ** term_months) / ((1 + monthly_rate) ** term_months - 1)
        
        print(f"\nAmortization Schedule for Loan ID {loan_id} ({client_name})")
        print(f"Loan Amount: ${principal:.2f}, Interest Rate: {loan['interest_rate']}%, Term: {term_months} months")
        print("Month | Payment | Principal | Interest | Balance")
        print("-" * 50)
        
        balance = principal
        for month in range(1, term_months + 1):
            interest = balance * monthly_rate
            principal_payment = monthly_payment - interest
            balance -= principal_payment
            print(f"{month:2} | ${monthly_payment:.2f} | ${principal_payment:.2f} | ${interest:.2f} | ${balance:.2f}")
            if balance < 0:
                balance = 0  # Prevent negative balance due to rounding
        
        print(f"Total Payment: ${monthly_payment * term_months:.2f}")
    except ValueError:
        print("Error: Invalid ID or calculation error.")