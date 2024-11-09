import streamlit as st
import json
import os
from datetime import datetime

# File to store tenders and applications
TENDER_FILE = 'tenders_data.json'
APPLICATIONS_FILE = 'applications_data.json'

# Function to load tenders from the JSON file
def load_tenders():
    if os.path.exists(TENDER_FILE):
        with open(TENDER_FILE, 'r') as f:
            return json.load(f)
    else:
        return []

# Function to load applications from the JSON file
def load_applications():
    if os.path.exists(APPLICATIONS_FILE):
        with open(APPLICATIONS_FILE, 'r') as f:
            return json.load(f)
    else:
        return []

# Function to save applications to the JSON file
def save_applications(applications):
    with open(APPLICATIONS_FILE, 'w') as f:
        json.dump(applications, f, indent=4)

# Function to save tenders to the JSON file
def save_tenders(tenders):
    with open(TENDER_FILE, 'w') as f:
        json.dump(tenders, f, indent=4)

# Function to display active tenders with sorting and category filter
def display_active_tenders():
    st.title("Active Tenders")

    # Load tenders from the JSON file
    tenders = load_tenders()

    # Search box for filtering tenders by ID
    search_id = st.text_input("Search Tender by ID")
    category_filter = st.selectbox("Filter by Category", ["All", "Construction", "Technology", "Healthcare"])

    # Check if the input box is focused and apply custom styling for resizing input fields
    st.markdown("""
        <style>
            .stTextInput>div>div>input {
                width: 100%;
                padding: 10px;
                font-size: 16px;
                border-radius: 8px;
            }
            .stButton>button {
                padding: 10px 20px;
                font-size: 16px;
                border-radius: 8px;
            }
            .stButton>button:hover {
                background-color: #007BFF;
                color: white;
            }
        </style>
    """, unsafe_allow_html=True)

    # Filter tenders based on search input and category
    if search_id:
        tenders = [tender for tender in tenders if search_id.lower() in tender['id'].lower()]
    if category_filter != "All":
        tenders = [tender for tender in tenders if tender['category'].lower() == category_filter.lower()]

    # Ensure that end_time is parsed correctly (handle both date and datetime formats)
    for tender in tenders:
        if len(tender['end_time'].strip()) == 10:  # Only a date (YYYY-MM-DD)
            tender['end_time'] += ' 00:00:00'  # Add default time (midnight)
        try:
            tender['end_time'] = datetime.strptime(tender['end_time'], '%Y-%m-%d %H:%M:%S')
        except ValueError:
            st.error(f"Error parsing end_time for Tender ID: {tender['id']}")

    # Sorting tenders by end date (ascending)
    tenders.sort(key=lambda tender: tender['end_time'])

    # Check if tenders exist and display them
    if len(tenders) > 0:
        st.markdown("""
            <style>
                .card {
                    background-color: rgba(255, 255, 255, 0.1);
                    backdrop-filter: blur(10px);
                    padding: 20px;
                    border-radius: 15px;
                    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
                    color: #fff;
                    transition: transform 0.3s, background-color 0.3s;
                }
                .card:hover {
                    background-color: rgba(0, 123, 255, 0.2);
                    transform: scale(1.02);
                }
                .card-title {
                    font-size: 18px;
                    font-weight: bold;
                    margin-bottom: 10px;
                }
                .card-content {
                    font-size: 14px;
                    color: #ddd;
                    margin-bottom: 5px;
                }
            </style>
        """, unsafe_allow_html=True)

        # Retrieve the connected wallet address (replace with actual method of obtaining wallet address)
        wallet_address = st.session_state.get('wallet_address', None)
        OWNER = "0xe0b91993111a6c70f3e38438b82eaae79206b4b"  # Replace with the owner's address
        
        # Display each tender in a card format, two per row
        for index in range(0, len(tenders), 2):
            col1, col2 = st.columns(2)

            # Display the first tender in the first column
            with col1:
                tender1 = tenders[index]
                st.markdown(f"""
                    <div class="card">
                        <div class="card-title">Tender ID: {tender1['id']}</div>
                        <div class="card-content"><strong>Name:</strong> {tender1['name']}</div>
                        <div class="card-content"><strong>Description:</strong> {tender1['description']}</div>
                        <div class="card-content"><strong>Min Bid (ETH):</strong> {tender1['min_bid_eth']}</div>
                        <div class="card-content"><strong>End Time:</strong> {tender1['end_time']}</div>
                        <div class="card-content"><strong>Category:</strong> {tender1['category']}</div>
                    </div>
                """, unsafe_allow_html=True)

                # Apply or Delete actions
                if wallet_address == OWNER:
                    if st.button(f"Delete Tender {tender1['id']}", key=f"delete_{tender1['id']}"):
                        tenders.remove(tender1)
                        save_tenders(tenders)  # Save updated tenders list
                        st.success(f"Tender {tender1['id']} has been deleted.")
                else:
                    if st.button(f"Apply to Tender {tender1['id']}", key=f"apply_{tender1['id']}"):
                        # Store tender details in session for later use
                        st.session_state.selected_tender = tender1
                        st.session_state.tender_id = tender1['id']
                        st.session_state.tender_name = tender1['name']
                        st.session_state.tender_description = tender1['description']
                        st.session_state.tender_min_bid = tender1['min_bid_eth']
                        st.session_state.tender_end_time = tender1['end_time']
                        st.session_state.tender_category = tender1['category']
                        
                        # Set flag for bid submission page
                        st.session_state.is_bid_submission = True

                        # Trigger rerun to navigate to the application form
                        st.rerun()

            if index + 1 < len(tenders):
                with col2:
                    tender2 = tenders[index + 1]
                    st.markdown(f"""
                        <div class="card">
                            <div class="card-title">Tender ID: {tender2['id']}</div>
                            <div class="card-content"><strong>Name:</strong> {tender2['name']}</div>
                            <div class="card-content"><strong>Description:</strong> {tender2['description']}</div>
                            <div class="card-content"><strong>Min Bid (ETH):</strong> {tender2['min_bid_eth']}</div>
                            <div class="card-content"><strong>End Time:</strong> {tender2['end_time']}</div>
                            <div class="card-content"><strong>Category:</strong> {tender2['category']}</div>
                        </div>
                    """, unsafe_allow_html=True)

                    if wallet_address == OWNER:
                        if st.button(f"Delete Tender {tender2['id']}", key=f"delete_{tender2['id']}"):
                            tenders.remove(tender2)
                            save_tenders(tenders)
                            st.success(f"Tender {tender2['id']} has been deleted.")
                    else:
                        if st.button(f"Apply to Tender {tender2['id']}", key=f"apply_{tender2['id']}"):
                            st.session_state.selected_tender = tender2
                            st.session_state.tender_id = tender2['id']
                            st.session_state.tender_name = tender2['name']
                            st.session_state.tender_description = tender2['description']
                            st.session_state.tender_min_bid = tender2['min_bid_eth']
                            st.session_state.tender_end_time = tender2['end_time']
                            st.session_state.tender_category = tender2['category']
                            st.session_state.is_bid_submission = True
                            st.rerun()

    else:
        st.write("No active tenders available.")

# If an application form is to be shown
if 'selected_tender' in st.session_state and st.session_state.is_bid_submission:
    tender = st.session_state.selected_tender
    st.title(f"Apply for Tender: {tender['name']}")
    wallet_address = st.session_state.get('wallet_address', None)

    if wallet_address:
        bid_amount = st.number_input("Enter your bid amount (ETH)", min_value=tender['min_bid_eth'], value=tender['min_bid_eth'])
        if st.button("Submit Bid"):
            applications = load_applications()
            applications.append({
                'tender_id': tender['id'],
                'bidder': wallet_address,
                'bid_amount': bid_amount,
                'status': 'Pending'
            })
            save_applications(applications)
            st.success("Your bid has been submitted!")
    else:
        st.warning("Please connect your wallet to submit a bid.")
