# Online Tendering DApp

## Overview

The **Online Contracting DApp** is a decentralized application built on blockchain technology to facilitate a transparent, secure, and efficient tendering and contracting process. This project uses smart contracts to create a tamper-proof system where tenders can be created, bids can be placed, and contracts can be awarded—all managed on the blockchain.

## Features

- **Decentralized Tender Management**: Tenders and bids are securely stored on the blockchain, eliminating data tampering.
- **Smart Contract Automation**: Bidding and awarding processes are handled by smart contracts, removing human intervention and ensuring fairness.
- **Secure User Authentication**: Access to tender and bidding features is role-based, protecting sensitive operations.
- **Frontend-Backend Integration**: Built with a React frontend and JavaScript blockchain interaction, providing a seamless user experience.
- **Responsive Design**: Optimized for a user-friendly interface with mobile compatibility.

## Project Structure

```
/Online-Contracting-DApp
│
├── /blockchain
│   ├── TenderPlatform.sol            # Solidity smart contract for tender management and bidding
│   ├── TenderPlatformABI.json        # ABI file for the smart contract (generated during deployment)
│   ├── blockchain.js                 # JavaScript file for connecting to the blockchain and interacting with the contract
│
├── /public
│   ├── index.html                    # The main HTML file, contains basic HTML structure and links to React app
│   └── /assets                       # Folder for images, logos, etc.
│
├── /src
│   ├── /components
│   │   ├── TenderCard.js             # React component for displaying tender cards
│   │   ├── CreateTender.js           # React component for creating and editing tenders
│   │   ├── BidOnTender.js            # React component for placing bids on tenders
│   │   └── Navbar.js                 # React component for navigation bar
│   │
│   ├── /pages
│   │   ├── Dashboard.js              # Page for listing all tenders
│   │   ├── CreateTenderPage.js       # Page for creating and editing tenders
│   │   └── BidTenderPage.js          # Page for placing bids on tenders
│   │
│   ├── App.js                        # Main React app file, where routing is set up
│   ├── index.js                      # Entry point for React app, renders the App component
│   └── /styles                       # Folder for custom CSS or Tailwind CSS configurations
│
├── package.json                      # Project dependencies and scripts
└── .env                              # Environment variables for API keys, network configurations
```

## Technologies Used

- **Blockchain**: Solidity, Ethereum
- **Frontend**: React.js
- **Backend/Blockchain Integration**: Web3.js
- **Smart Contracts**: Written in Solidity
- **IPFS** (optional): For decentralized storage of additional documents or assets

## Installation

### Prerequisites

- **Node.js** and **npm**
- **Truffle** or **Hardhat** (for smart contract development)
- **Ganache** for local blockchain testing
- **Metamask** browser extension

### Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/Online-Contracting-DApp.git
   cd Online-Contracting-DApp
   ```

2. **Install dependencies**:
   - For frontend:
     ```bash
     cd frontend
     npm install
     ```
   - For backend/smart contracts:
     ```bash
     cd ../blockchain
     npm install
     ```

3. **Compile and Deploy Smart Contracts**:
   - If using Truffle:
     ```bash
     truffle compile
     truffle migrate --network development
     ```
   - If using Hardhat, adapt commands accordingly.

4. **Set up environment variables**:
   - Create a `.env` file based on `.env.example` and add your blockchain configuration details, such as contract addresses and API keys.

5. **Run the application**:
   - Start the React frontend:
     ```bash
     cd ../frontend
     npm start
     ```

6. **Connect Metamask** to your local blockchain network and interact with the DApp on `http://localhost:3000`.

## Usage

1. **Open the DApp in your browser** and connect your wallet (Metamask).
2. **Register or Log In** based on your role (administrator, bidder, or evaluator).
3. **Create, Bid, and Award Contracts** through the intuitive interface.

## Smart Contract

The `TenderPlatform.sol` smart contract handles all tendering functions, including creating tenders, managing bids, and awarding contracts. The ABI file (`TenderPlatformABI.json`) enables the frontend to interact with this contract on the blockchain.

## Contributing

We welcome contributions! Please fork this repository, create a new branch for your features or fixes, and submit a pull request.

## License

This project is licensed under the MIT License. 
