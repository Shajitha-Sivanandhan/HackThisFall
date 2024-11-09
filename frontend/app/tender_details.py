import streamlit as st
import json
from datetime import datetime

# Function to load tender data from the JSON file
def load_tender_data():
    try:
        with open('tenders_data.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        st.error("Tender data file not found!")
        return []

# Function to load bids from the bids JSON file
def load_bids():
    try:
        with open('bids.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        st.error("Bids file not found!")
        return []

# Function to load all applications from the all_tenders_applications.json
def load_applications():
    try:
        with open('all_tenders_applications.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        st.error("Applications file not found!")
        return []

# Function to get tender details by tender_id
def get_tender_by_id(tender_id, tenders):
    return next((tender for tender in tenders if tender["id"] == str(tender_id)), None)

# Function to get bids for a specific tender_id
def get_bids_for_tender(tender_id, bids):
    return [bid for bid in bids if bid["tender_id"] == str(tender_id)]

# Function to check if the tender is finished (end time has passed)
def is_tender_finished(end_time_str):
    try:
        # Convert tender's end_time to a datetime object
        end_time = datetime.strptime(end_time_str, "%Y-%m-%d %H:%M:%S")  # Format depends on your data
        return datetime.now() > end_time
    except ValueError:
        st.error("Invalid date format in tender's end time.")
        return False

# Function to display tender details and select the winner
def show_tender_details():
    tenders = load_tender_data()  # Load all tenders from JSON file
    bids = load_bids()  # Load all bids
    applications = load_applications()  # Load applications (empty original data)

    if not tenders:
        st.error("No tenders available!")
        return

    # Categorize tenders into finished and not finished
    finished_tenders = [tender for tender in tenders if is_tender_finished(tender['end_time'])]
    not_completed_tenders = [tender for tender in tenders if not is_tender_finished(tender['end_time'])]

    # Display finished and not completed tenders separately
    st.subheader("Finished Tenders")
    for tender in finished_tenders:
        st.write(f"Tender ID: {tender['id']} - {tender['name']}")

    st.subheader("Not Completed Tenders")
    for tender in not_completed_tenders:
        st.write(f"Tender ID: {tender['id']} - {tender['name']}")

    # List tender IDs for selection (only for unfinished tenders)
    tender_ids = [tender["id"] for tender in not_completed_tenders]

    if not tender_ids:
        st.write("No tenders available for selection.")
        return

    tender_id = st.selectbox("Select Tender ID", tender_ids)

    # Get tender details for the selected tender ID
    tender = get_tender_by_id(tender_id, not_completed_tenders)

    if tender:
        st.title(f"Tender Details: {tender['name']}")
        st.write(tender['description'])
        st.write(f"Minimum Bid INR: {tender['min_bid_inr']} INR")
        st.write(f"Minimum Bid ETH: {tender['min_bid_eth']} ETH")
        st.write(f"End Time: {tender['end_time']}")
        st.write(f"Category: {tender['category']}")

        # Get bids for this specific tender
        tender_bids = get_bids_for_tender(tender_id, bids)

        if not tender_bids:
            st.write("No bids available for this tender.")
            return

        st.subheader("Bids")
        for bid in tender_bids:
            st.write(f"Bidder Wallet: {bid['bidder_wallet']}, Bid Amount: {bid['bid_in_inr']} INR")

        # Check if the tender is finished and show results
        if is_tender_finished(tender["end_time"]):
            # Determine winner based on tender's category (e.g., Lower bid wins or Higher bid wins)
            winner_type = tender["category"]  # Could be "Lower bid wins" or "Higher bid wins"

            if winner_type == "Lower bid wins":
                # Find the bid with the minimum amount for "Lower bid wins"
                winning_bid = min(tender_bids, key=lambda x: x["bid_in_inr"])
            else:
                # Find the bid with the maximum amount for "Higher bid wins"
                winning_bid = max(tender_bids, key=lambda x: x["bid_in_inr"])

            if winning_bid:
                # Show winner information from the winning bid
                st.subheader("Winner")
                st.write(f"Winner: {winning_bid['bidder_wallet']}")
                st.write(f"Amount: {winning_bid['bid_in_inr']} INR")

                # Fetch the winner's application details
                application = next((app for app in applications if app["bidder_wallet"] == winning_bid["bidder_wallet"]), None)

                if application:
                    st.subheader("Winner Application Details")
                    st.write(f"Mobile Number: {application['mobile_number']}")
                    st.write(f"Address: {application['address']}")
                    st.write(f"Salary: {application['salary']}")
                    st.write(f"Occupation: {application['occupation']}")
                    st.write(f"Previous Tenders Count: {application['previous_tenders_count']}")
                    st.write(f"Status: {application['status']}")
                else:
                    st.write("No application details available for the winner.")
            else:
                st.write("No valid bids available for this tender.")
        else:
            st.write("The tender has not yet ended. Results will be available after the tender ends.")
    else:
        st.error(f"Tender with ID {tender_id} not found.")

if __name__ == "__main__":
    show_tender_details()
