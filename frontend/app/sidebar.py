import streamlit as st
import streamlit.components.v1 as components

# Function to display the sidebar and handle navigation
def sidebar_navigation():
    # Apply Glassmorphism styling using custom CSS
    st.sidebar.markdown("""
        <style>
            /* Glassmorphism effect */
            .css-1d391kg {
                background: rgba(255, 255, 255, 0.15);  /* Slightly more transparent white */
                backdrop-filter: blur(12px);  /* Increased blur for more glass-like effect */
                border-radius: 20px;  /* More rounded corners */
                padding: 25px;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15); /* Add a soft shadow for more depth */
            }

            /* Set the sidebar width */
            .css-1d391kg {
                width: 240px !important;  /* Slightly wider sidebar for better visibility */
            }

            /* Title styling */
            .css-15txf4l {
                font-family: 'Arial', sans-serif;
                font-size: 2em;  /* Increased font size for better visibility */
                font-weight: 700;
                color: #ffffff;
                text-align: center;
                margin-bottom: 20px;
            }

            /* Button styling */
            .stButton>button {
                background-color: #007bff;  /* Blue button color */
                color: white;
                border-radius: 15px;
                font-size: 1.8em;  /* Increased font size for text */
                font-weight: 600;
                padding: 20px 25px;  /* Adjusted padding for better spacing */
                width: 100%;  /* Full width button */
                border: 2px solid #007bff;  /* Border for button */
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                cursor: pointer;
                transition: all 0.3s ease;
                margin-bottom: 20px;  /* Space between buttons */
                text-align: center;  /* Align the text in the middle */
            }

            /* Hover effect for the button */
            .stButton>button:hover {
                background-color: white;  /* White background on hover */
                color: #007bff;  /* Change text color to blue */
                box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
                transform: translateY(-2px);
            }

            /* Add spacing between elements and increase hover effect */
            .st-radio div {
                margin-bottom: 20px;
                padding: 10px 15px;
                border: 2px solid #007bff;
                margin-bottom: 10px;
                border-radius: 10px; /* Rounded corners for radio buttons */
            }

            /* Hover effect for radio items */
            .st-radio div:hover {
                background-color: rgba(0, 123, 255, 0.1); /* Light blue background on hover */
                cursor: pointer;
                border: 2px solid #0056b3; /* Darker border on hover */
            }

            /* User Address Styling (MetaMask Address) */
            .wallet-address {
                background: rgba(255, 255, 255, 0.2);
                border-radius: 10px;
                padding: 10px;
                margin-bottom: 20px;
                text-align: center;
                color: #ffffff;
                font-size: 1.2em;
                font-weight: 600;
                word-wrap: break-word;
                overflow: hidden;
                text-overflow: ellipsis;
            }

        </style>
    """, unsafe_allow_html=True)

    # Display the MetaMask address (if available)
    if 'meta_mask_address' in st.session_state and st.session_state.meta_mask_address:
        st.sidebar.markdown(f"<div class='wallet-address'>Connected: {st.session_state.meta_mask_address}</div>", unsafe_allow_html=True)

    # Pages for navigation
    pages = ["Create Tender", "Place Bid", "Active Tenders", "Tender Details"]
    
    # Add icons or emojis for each page
    page_icons = {
        "Create Tender": "📝",
        "Place Bid": "💰",
        "Active Tenders": "📃",
        "Tender Details": "🔍"
    }

    # Initialize session state if not already present
    if 'selected_page' not in st.session_state:
        st.session_state.selected_page = pages[0]  # Default to the first page

    # Create a button for each page in the sidebar
    for p in pages:
        if st.sidebar.button(f"{page_icons[p]} {p}"):  # Use button for navigation
            st.session_state.selected_page = p  # Update the selected page in session state

    # Add page description or tooltip for each page
    if st.session_state.selected_page == "Create Tender":
        st.sidebar.markdown('<p class="sidebar-description">Create a new tender by filling in the required details.</p>', unsafe_allow_html=True)
    elif st.session_state.selected_page == "Place Bid":
        st.sidebar.markdown('<p class="sidebar-description">Place a bid on any of the active tenders.</p>', unsafe_allow_html=True)
    elif st.session_state.selected_page == "Active Tenders":
        st.sidebar.markdown('<p class="sidebar-description">View all the currently active tenders.</p>', unsafe_allow_html=True)
    elif st.session_state.selected_page == "Tender Details":
        st.sidebar.markdown('<p class="sidebar-description">View detailed information about any tender.</p>', unsafe_allow_html=True)

    return st.session_state.selected_page

# JavaScript integration for fetching the MetaMask address
def fetch_metamask_address():
    # Embed your HTML page containing MetaMask interaction here
    components.html(
        """
        <html>
            <body>
                <script src="https://cdn.jsdelivr.net/npm/ethers@5.7.2/dist/ethers.umd.min.js"></script>
                <script>
                    if (typeof window.ethereum !== 'undefined') {
                        const provider = new ethers.providers.Web3Provider(window.ethereum);
                        provider.send("eth_requestAccounts", [])
                            .then(accounts => {
                                const userAddress = accounts[0];
                                window.parent.postMessage({ type: 'SET_ADDRESS', address: userAddress }, '*');
                            })
                            .catch(error => {
                                console.error("MetaMask connection failed:", error);
                                alert("Please connect MetaMask.");
                            });
                    } else {
                        alert("MetaMask is not installed.");
                    }
                </script>
            </body>
        </html>
        """, height=0, width=0  # Invisible to the user
    )

# Initialize fetching MetaMask address when the Streamlit app loads
fetch_metamask_address()
