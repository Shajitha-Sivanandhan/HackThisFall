import streamlit as st
import streamlit.components.v1 as components

# HTML/JS code to connect with MetaMask using ethers.js
metamask_code = """
<!DOCTYPE html>
<html>
<head>
    <title>Connect MetaMask</title>
    <script src="https://cdn.jsdelivr.net/npm/ethers@5.7.2/dist/ethers.umd.min.js"></script>
</head>
<body>
    <button id="connectButton">Connect MetaMask</button>
    <p id="account"></p>

    <script>
        let provider;
        let signer;
        let userAddress;
        
        // Detect if MetaMask is installed
        if (typeof window.ethereum !== 'undefined') {
            provider = new ethers.providers.Web3Provider(window.ethereum, "any");
            signer = provider.getSigner();
            document.getElementById("connectButton").onclick = async () => {
                try {
                    // Request MetaMask connection
                    await provider.send("eth_requestAccounts", []);
                    userAddress = await signer.getAddress();
                    document.getElementById("account").innerText = "Connected address: " + userAddress;
                    window.parent.postMessage({ type: 'SET_ADDRESS', address: userAddress }, '*');
                } catch (error) {
                    console.log(error);
                }
            };
        } else {
            document.getElementById("account").innerText = "Please install MetaMask!";
        }
    </script>
</body>
</html>
"""

# Display the HTML/JS component
components.html(metamask_code, height=300)

# Wait for the user to connect
st.write("MetaMask login interface. Please connect your wallet.")

# You can use Streamlit's session state to save the connected address
if 'metamask_address' in st.session_state:
    st.write(f"Connected with address: {st.session_state.metamask_address}")
else:
    st.write("No wallet connected yet.")
