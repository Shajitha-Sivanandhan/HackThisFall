import streamlit as st
from web3 import Web3
from config import CONTRACT_ABI, CONTRACT_ADDRESS, OWNER_ADDRESS
import tender_creation
import bid_submission
import active_tenders
import tender_details
import sidebar  # Import sidebar navigation function
import logging

# Initialize Web3
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))  # Replace with your Ethereum node provider

# Check if Web3 is connected


# Connect to the contract
contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)

# Store the owner's wallet address in the OWNER variable
OWNER = OWNER_ADDRESS

# Set up logging to capture error details (optional)
logging.basicConfig(filename='app_error_log.txt', level=logging.ERROR)

def main():
    st.set_page_config(page_title="Bidding and Tendering Platform", layout="wide")

    # Retrieve wallet address from query parameters in the URL
    query_params = st.experimental_get_query_params()
    wallet_address = query_params.get("address", [None])[0]

    # Store wallet address in session state
    if wallet_address:
        st.session_state["wallet_address"] = wallet_address
    else:
        st.session_state["wallet_address"] = None

    # Check if the connected wallet is the owner's address
    is_owner = st.session_state["wallet_address"] == OWNER

    # Navigation bar (With wallet address)
    st.markdown(
        f"""
        <style>
        .navbar {{
            background-color: #333;
            padding: 10px;
            color: white;
            font-size: 18px;
            font-weight: bold;
            text-align: right;
        }}
        .wallet {{
            color: #4CAF50;
        }}
        </style>
        <div class="navbar">
            Connected Wallet: <span class="wallet">{st.session_state["wallet_address"] or "Not Connected"}</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Display role message (Owner or Regular User)
    if is_owner:
        st.markdown("### You are the **Owner** of this platform. You can create tenders.")
    else:
        st.markdown("### You are a **Regular User**. You can place bids on active tenders.")

    # Sidebar navigation
    selected_page = sidebar.sidebar_navigation()

    # Display content based on selected page
    if selected_page == "Create Tender" and is_owner:
        tender_creation.create_tender()
    elif selected_page == "Place Bid" and not is_owner:
        bid_submission.place_bid()
    elif selected_page == "Active Tenders":
        active_tenders.display_active_tenders()
    elif selected_page == "Tender Details":
        tender_details.show_tender_details()
    else:
        # If an invalid page is selected or a page is restricted, show an appropriate message
        if selected_page == "Create Tender":
            st.markdown("**As a regular user, you are not allowed to create tenders.**")
        elif selected_page == "Place Bid":
            st.markdown("**As the owner, you are not allowed to place bids.**")
        else:
            st.markdown("**Page not available.**")

    # Example: You can call contract functions here if needed
    try:
        # Check if bidding is open
        if contract.functions.isBiddingOpen().call():
            st.markdown("Bidding is open!")
        else:
            st.markdown("Bidding is closed.")
        
        # Example: Use Web3 to get details of the current winner or bidders
        winner_address = contract.functions.winner().call()
        winner_name, winner_amount = contract.functions.getBidderDetails(winner_address).call()
        st.markdown(f"### Winner: {winner_name} ({winner_address}) with a bid of {winner_amount} ETH")

    except Exception as e:
        # Log the error to a file (optional)
        logging.error(f"Error interacting with contract: {str(e)}")
        
        # Display a user-friendly message without showing the error details
        

if __name__ == "__main__":
    main()
