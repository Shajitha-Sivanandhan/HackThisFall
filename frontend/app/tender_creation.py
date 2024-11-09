import streamlit as st
import json
import os
import time

# File to store tenders
TENDER_FILE = 'tenders_data.json'

# Function to load tenders from the JSON file
def load_tenders():
    if os.path.exists(TENDER_FILE):
        with open(TENDER_FILE, 'r') as f:
            return json.load(f)
    else:
        return []

# Function to save tenders to the JSON file
def save_tenders(tenders):
    with open(TENDER_FILE, 'w') as f:
        json.dump(tenders, f)

# Function to convert INR to ETH (using the correct conversion rate)
def convert_inr_to_eth(inr_amount):
    conversion_rate = 256755  # 1 ETH = 2,56,755 INR
    return inr_amount / conversion_rate

# Main function for creating a tender
def create_tender():
    st.title("Create a New Tender")

    # Apply custom styling to the form
    st.markdown("""
        <style>
            .form-input {
                border: 2px solid #007bff;
                border-radius: 10px;
                padding: 10px;
                margin-bottom: 15px;
            }
            .stTextInput, .stTextArea, .stNumberInput {
                width: 100%;
                padding: 10px;
            }
            .stButton button {
                width: 100%;
                padding: 15px;
                background-color: #007bff;
                color: white;
                border-radius: 10px;
                font-size: 1.2em;
                border: none;
            }
            .stButton button:hover {
                background-color: #0056b3;
            }
        </style>
    """, unsafe_allow_html=True)

    # Form Inputs
    tender_name = st.text_input("Tender Name")
    tender_description = st.text_area("Tender Description")
    inr_bid = st.number_input("Minimum Bid Amount (in INR)", min_value=0.01, format="%.2f")
    
    # Convert INR to ETH
    min_bid_eth = convert_inr_to_eth(inr_bid)

    # Display equivalent ETH below the INR input
    if inr_bid > 0:
        st.write(f"**Equivalent ETH:** {round(min_bid_eth, 4)} ETH")

    # Additional fields for tender
    end_time = st.date_input("Tender End Time")
    category = st.radio("Bid Category", options=["Lower bid wins", "Higher bid wins"])

    # Generate unique tender ID (based on current timestamp)
    tender_id = str(int(time.time()))

    # Load tenders from the JSON file
    tenders = load_tenders()

    # Create Tender Button
    if st.button("Create Tender"):
        if tender_name and tender_description and inr_bid > 0:
            tender = {
                "id": tender_id,
                "name": tender_name,
                "description": tender_description,
                "min_bid_inr": inr_bid,
                "min_bid_eth": round(min_bid_eth, 4),  # Round to 4 decimal places
                "end_time": str(end_time),
                "category": category
            }
            tenders.append(tender)
            save_tenders(tenders)

            st.success(f"Tender '{tender_name}' created successfully!")
            st.write(f"**Tender ID**: {tender_id}")
            st.write(f"**Description**: {tender_description}")
            st.write(f"**Minimum Bid**: {inr_bid} INR / {round(min_bid_eth, 4)} ETH")
            st.write(f"**End Time**: {end_time}")
            st.write(f"**Category**: {category}")
        else:
            st.error("Please fill all fields and provide a valid bid amount.")
