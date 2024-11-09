import streamlit as st
from web3 import Web3
import json
import requests
import os

# Function to load all bids for multiple tenders from a central file
def load_all_tender_bids():
    if os.path.exists("all_tenders_applications.json"):
        with open("all_tenders_applications.json", "r") as file:
            return json.load(file)
    else:
        return {}  # Return an empty dictionary if the file doesn't exist

# Function to save all bids for multiple tenders into the central file
def save_all_tender_bids(all_bids):
    with open("all_tenders_applications.json", "w") as file:
        json.dump(all_bids, file, indent=4)

# Function to fetch current ETH to INR conversion rate
def get_eth_to_inr():
    try:
        response = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=inr")
        data = response.json()
        return data["ethereum"]["inr"]
    except:
        return 2000  # Fallback rate if API fails

def place_bid():
    st.title("Place Your Bid")

    # Auto-populate tender ID from session state
    tender_id = st.session_state.get('tender_id', None)
    tender_name = st.session_state.get('tender_name', 'No tender selected')
    tender_min_bid = st.session_state.get('tender_min_bid', 0)

    if not tender_id:
        st.error("No tender selected. Please go back and select a tender.")
        return

    st.write(f"Tender ID: {tender_id}")
    st.write(f"Tender Name: {tender_name}")
    st.write(f"Minimum Bid: {tender_min_bid} ETH")

    # Input for bid amount in INR
    bid_in_inr = st.number_input("Bid Amount (in INR)", min_value=1, format="%.2f")

    if bid_in_inr < tender_min_bid * get_eth_to_inr():
        st.warning(f"Bid amount must be greater than the minimum bid of {tender_min_bid * get_eth_to_inr():.2f} INR!")
    else:
        eth_to_inr = get_eth_to_inr()
        bid_in_eth = bid_in_inr / eth_to_inr
        st.write(f"Equivalent ETH Value: {bid_in_eth:.6f} ETH")

    mobile_number = st.text_input("Your Mobile Number")
    address = st.text_input("Your Address")
    salary = st.number_input("Your Monthly Salary (in USD)", min_value=0)
    occupation = st.text_input("Your Occupation")
    previous_tenders_count = st.number_input("How many previous tenders have you participated in?", min_value=0)

    # Connect to Ethereum (using Ganache for local testing)
    ganache_url = "http://127.0.0.1:8545"  # Ganache default RPC URL
    w3 = Web3(Web3.HTTPProvider(ganache_url))

    if st.button("Place Bid"):
        if bid_in_inr > 0 and mobile_number and address and salary and occupation:
            bid_data = {
                'tender_id': tender_id,
                'tender_name': tender_name,
                'bid_in_inr': bid_in_inr,
                'bid_in_eth': bid_in_eth,
                'mobile_number': mobile_number,
                'address': address,
                'salary': salary,
                'occupation': occupation,
                'previous_tenders_count': previous_tenders_count,
                'status': 'Pending',
                'bidder_wallet': '0xe0B91993111a6C70f3E938438b82eAAe79206b4B'
            }

            # Load all existing bids from file
            all_bids = load_all_tender_bids()

            # If this tender_id is not in the dictionary, initialize it as an empty list
            if tender_id not in all_bids:
                all_bids[tender_id] = []

            # Append the current bid to the list of bids for this tender
            all_bids[tender_id].append({address: bid_in_eth})

            # Save the updated bids back to the file
            save_all_tender_bids(all_bids)

            st.success(f"Bid of {bid_in_inr} INR placed successfully! Your details have been saved.")
        else:
            st.error("Please fill in all required fields (bid amount, mobile number, address, salary, occupation).")
