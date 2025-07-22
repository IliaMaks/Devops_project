"""
Streamlit web interface for the Bank Loan Management System.
Provides a web-based UI for managing clients and loans.
"""
import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'python_app')))
import pandas as pd

# Initialize session state for clients and loans
if "clients" not in st.session_state:
    st.session_state.clients = []
    st.session_state.loans = []


st.markdown("""
    <style>
    div.stButton > button {
        width: 100%;
        text-align: left;
        padding: 0.5em 1em;
        margin-bottom: 5px;
        font-size: 1rem;
    }
    </style>
""", unsafe_allow_html=True)


# Welcome screen
st.title("Bank Loan Management System")
st.markdown("Welcome to the web interface for managing clients and loans!")

# Sidebar with uniform buttons using columns
with st.sidebar:
    st.markdown("### Menu")
    
    if st.button("View Clients", key="view_clients"):
        st.session_state.selected_action = "view_clients"
    if st.button("Add Client", key="add_client"):
        st.session_state.selected_action = "add_client"
    if st.button("Edit Client", key="edit_client"):
        st.session_state.selected_action = "edit_client"
    if st.button("Remove Client", key="remove_client"):
        st.session_state.selected_action = "remove_client"
    if st.button("View Loans", key="view_loans"):
        st.session_state.selected_action = "view_loans"
    if st.button("Add Loan", key="add_loan"):
        st.session_state.selected_action = "add_loan"
    if st.button("Edit Loan", key="edit_loan"):
        st.session_state.selected_action = "edit_loan"
    if st.button("Remove Loan", key="remove_loan"):
        st.session_state.selected_action = "remove_loan"
    if st.button("Calculate Total Loans", key="calculate_loans"):
        st.session_state.selected_action = "calculate_loans"
    if st.button("Generate Amortization Schedule", key="amortization"):
        st.session_state.selected_action = "amortization"

# Main area content based on selected action
if "selected_action" not in st.session_state:
    st.session_state.selected_action = None

if st.session_state.selected_action == "view_clients":
    st.subheader("All Clients")
    if st.session_state.clients:
        df = pd.DataFrame(st.session_state.clients)
        st.table(df)
    else:
        st.write("No clients in the system.")

elif st.session_state.selected_action == "add_client":
    st.subheader("Add a New Client")
    with st.form("add_client_form"):
        name = st.text_input("Client Name")
        email = st.text_input("Client Email")
        phone = st.text_input("Client Phone")
        submitted = st.form_submit_button("Add Client")
        if submitted:
            try:
                if not name:
                    raise ValueError("Name cannot be empty.")
                if "@" not in email or "." not in email:
                    raise ValueError("Invalid email format.")
                if not phone:
                    raise ValueError("Phone cannot be empty.")
                client = {
                    "id": len(st.session_state.clients) + 1,
                    "name": name,
                    "email": email,
                    "phone": phone
                }
                st.session_state.clients.append(client)
                st.success(f"Client '{name}' added successfully!")
                st.session_state.selected_action = None  # Reset after action
            except ValueError as e:
                st.error(f"Error: {e}")

elif st.session_state.selected_action == "edit_client":
    st.subheader("Edit a Client")
    client_id = st.number_input("Enter Client ID to edit", min_value=1, step=1)
    client = next((c for c in st.session_state.clients if c["id"] == client_id), None)
    if client:
        with st.form("edit_client_form"):
            name = st.text_input("Client Name", value=client["name"])
            email = st.text_input("Client Email", value=client["email"])
            phone = st.text_input("Client Phone", value=client["phone"])
            submitted = st.form_submit_button("Update Client")
            if submitted:
                try:
                    if "@" not in email or "." not in email:
                        raise ValueError("Invalid email format.")
                    client["name"] = name
                    client["email"] = email
                    client["phone"] = phone
                    st.success(f"Client ID {client_id} updated successfully!")
                    st.session_state.selected_action = None  # Reset after action
                except ValueError as e:
                    st.error(f"Error: {e}")
    else:
        st.error(f"Client ID {client_id} not found.")
        if st.button("Back"):
            st.session_state.selected_action = None

elif st.session_state.selected_action == "remove_client":
    st.subheader("Remove a Client")
    client_id = st.number_input("Enter Client ID to remove", min_value=1, step=1)
    if st.button("Confirm Client Removal"):
        client = next((c for c in st.session_state.clients if c["id"] == client_id), None)
        if client:
            st.session_state.loans[:] = [loan for loan in st.session_state.loans if loan["client_id"] != client_id]
            st.session_state.clients.remove(client)
            st.success(f"Client ID {client_id} and their loans removed successfully!")
            st.session_state.selected_action = None  # Reset after action
        else:
            st.error(f"Client ID {client_id} not found.")
    if st.button("Back"):
        st.session_state.selected_action = None

elif st.session_state.selected_action == "view_loans":
    st.subheader("All Loans")
    if st.session_state.loans:
        df = pd.DataFrame(st.session_state.loans)
        df["client_name"] = [next((c["name"] for c in st.session_state.clients if c["id"] == loan["client_id"]), "Unknown") for loan in st.session_state.loans]
        st.table(df)
    else:
        st.write("No loans in the system.")

elif st.session_state.selected_action == "add_loan":
    st.subheader("Add a New Loan")
    with st.form("add_loan_form"):
        client_id = st.number_input("Client ID", min_value=1, step=1)
        amount = st.number_input("Loan Amount", min_value=0.0, step=100.0)
        interest_rate = st.number_input("Interest Rate (%)", min_value=0.0, step=0.1)
        term_months = st.number_input("Term (Months)", min_value=1, step=1)
        status = st.selectbox("Status", ["active", "paid"])
        submitted = st.form_submit_button("Add Loan")
        if submitted:
            try:
                client = next((c for c in st.session_state.clients if c["id"] == client_id), None)
                if not client:
                    raise ValueError(f"Client ID {client_id} not found.")
                loan = {
                    "id": len(st.session_state.loans) + 1,
                    "client_id": client_id,
                    "amount": amount,
                    "interest_rate": interest_rate,
                    "term_months": term_months,
                    "status": status
                }
                st.session_state.loans.append(loan)
                st.success(f"Loan ID {loan['id']} added successfully for {client['name']}!")
                st.session_state.selected_action = None  # Reset after action
            except ValueError as e:
                st.error(f"Error: {e}")

elif st.session_state.selected_action == "edit_loan":
    st.subheader("Edit a Loan")
    loan_id = st.number_input("Enter Loan ID to edit", min_value=1, step=1)
    loan = next((l for l in st.session_state.loans if l["id"] == loan_id), None)
    if loan:
        with st.form("edit_loan_form"):
            amount = st.number_input("Loan Amount", value=loan["amount"], min_value=0.0, step=100.0)
            interest_rate = st.number_input("Interest Rate (%)", value=loan["interest_rate"], min_value=0.0, step=0.1)
            term_months = st.number_input("Term (Months)", value=loan["term_months"], min_value=1, step=1)
            status = st.selectbox("Status", ["active", "paid"], index=0 if loan["status"] == "active" else 1)
            submitted = st.form_submit_button("Update Loan")
            if submitted:
                try:
                    loan["amount"] = amount
                    loan["interest_rate"] = interest_rate
                    loan["term_months"] = term_months
                    loan["status"] = status
                    st.success(f"Loan ID {loan_id} updated successfully!")
                    st.session_state.selected_action = None  # Reset after action
                except ValueError as e:
                    st.error(f"Error: {e}")
    else:
        st.error(f"Loan ID {loan_id} not found.")
        if st.button("Back"):
            st.session_state.selected_action = None

elif st.session_state.selected_action == "remove_loan":
    st.subheader("Remove a Loan")
    loan_id = st.number_input("Enter Loan ID to remove", min_value=1, step=1)
    if st.button("Confirm Loan Removal"):
        loan = next((l for l in st.session_state.loans if l["id"] == loan_id), None)
        if loan:
            st.session_state.loans.remove(loan)
            st.success(f"Loan ID {loan_id} removed successfully!")
            st.session_state.selected_action = None  # Reset after action
        else:
            st.error(f"Loan ID {loan_id} not found.")
    if st.button("Back"):
        st.session_state.selected_action = None

elif st.session_state.selected_action == "calculate_loans":
    st.subheader("Calculate Total Loan Amounts")
    if st.button("Calculate"):
        total_amount = sum(loan["amount"] for loan in st.session_state.loans if loan["status"] == "active")
        total_interest = sum(loan["amount"] * (loan["interest_rate"] / 100) for loan in st.session_state.loans if loan["status"] == "active")
        st.write(f"Total active loan amount: ${total_amount:.2f}")
        st.write(f"Total interest on active loans: ${total_interest:.2f}")
        if st.button("Back"):
            st.session_state.selected_action = None

elif st.session_state.selected_action == "amortization":
    st.subheader("Generate Amortization Schedule")
    loan_id = st.number_input("Enter Loan ID", min_value=1, step=1)
    if st.button("Generate Schedule"):
        loan = next((l for l in st.session_state.loans if l["id"] == loan_id), None)
        if loan:
            client = next((c for c in st.session_state.clients if c["id"] == loan["client_id"]), None)
            client_name = client["name"] if client else "Unknown"
            principal = loan["amount"]
            annual_rate = loan["interest_rate"] / 100
            monthly_rate = annual_rate / 12
            term_months = loan["term_months"]
            
            # Calculate monthly payment
            monthly_payment = principal * (monthly_rate * (1 + monthly_rate) ** term_months) / ((1 + monthly_rate) ** term_months - 1)
            
            # Generate schedule
            schedule = []
            balance = principal
            for month in range(1, term_months + 1):
                interest = balance * monthly_rate
                principal_payment = monthly_payment - interest
                balance -= principal_payment
                schedule.append({
                    "Month": month,
                    "Payment": round(monthly_payment, 2),
                    "Principal": round(principal_payment, 2),
                    "Interest": round(interest, 2),
                    "Balance": round(balance, 2) if balance > 0 else 0
                })
            
            st.write(f"Amortization Schedule for Loan ID {loan_id} ({client_name})")
            st.write(f"Loan Amount: ${principal:.2f}, Interest Rate: {loan['interest_rate']}%, Term: {term_months} months")
            df = pd.DataFrame(schedule)
            st.table(df)
            st.write(f"Total Payment: ${monthly_payment * term_months:.2f}")
        else:
            st.error(f"Loan ID {loan_id} not found.")
        if st.button("Back"):
            st.session_state.selected_action = None

if st.session_state.selected_action is None:
    st.write("Select an action from the sidebar to begin.")

if __name__ == "__main__":
    pass  # Streamlit runs via `streamlit run app.py`