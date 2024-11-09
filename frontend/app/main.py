import streamlit as st
import time

# Import necessary functions (assuming they exist in your project)
import tender_creation
import bid_submission
import active_tenders
import tender_details
import sidebar  # Import sidebar navigation function

# Store the owner's wallet address in the OWNER variable
OWNER = "0xe0b91993111a6c70f3e38438b82eaae79206b4b"  # Replace with the actual owner's address

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

    # Remove the continuous current time display unless needed
    # time_display = st.empty()
    # while True:
    #     current_time = time.strftime("%H:%M:%S")  # Get the current time in HH:MM:SS format
    #     time_display.markdown(
    #         f"**Current Time:** {current_time}",
    #         unsafe_allow_html=True
    #     )
    #     time.sleep(1)  # Wait for 1 second before updating the time


if __name__ == "__main__":
    main()
