// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Tender {
    address public owner;
    bool public isBiddingOpen;
    address public winner;

    struct Bidder {
        address bidderAddress;
        string name;
        uint256 amount;
    }

    mapping(address => Bidder) public bidders;
    address[] public bidderList;

    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can call this function");
        _;
    }

    modifier biddingOpen() {
        require(isBiddingOpen, "Bidding is not open");
        _;
    }

    modifier biddingClosed() {
        require(!isBiddingOpen, "Bidding is still open");
        _;
    }

    constructor() {
        owner = msg.sender;
        isBiddingOpen = false;
    }

    // Function to start the bidding, only accessible by the owner
    function startBid() public onlyOwner {
        require(!isBiddingOpen, "Bidding is already open");
        isBiddingOpen = true;
    }

    // Function to close the bidding, only accessible by the owner
    function closeBid() public onlyOwner {
        require(isBiddingOpen, "Bidding is already closed");
        isBiddingOpen = false;
    }

    // Function for bidders to submit their bids
    function placeBid(string memory _name, uint256 _amount) public biddingOpen {
        require(bidders[msg.sender].bidderAddress == address(0), "Bidder already placed a bid");
        
        // Store the bidder details
        bidders[msg.sender] = Bidder({
            bidderAddress: msg.sender,
            name: _name,
            amount: _amount
        });
        
        bidderList.push(msg.sender);
    }

    // Function to declare a winner, only accessible by the owner after bidding is closed
    function declareWinner(address _winnerAddress) public onlyOwner biddingClosed {
        require(bidders[_winnerAddress].bidderAddress != address(0), "Winner must be a valid bidder");
        
        winner = _winnerAddress;
    }

    // Get the bid details of a specific address
    function getBidderDetails(address _bidderAddress) public view returns (string memory, uint256) {
        require(bidders[_bidderAddress].bidderAddress != address(0), "Bidder not found");
        
        Bidder memory bidder = bidders[_bidderAddress];
        return (bidder.name, bidder.amount);
    }

    // Get the list of all bidder addresses
    function getAllBidders() public view returns (address[] memory) {
        return bidderList;
    }

    // Get the winner details
    function getWinnerDetails() public view biddingClosed returns (string memory, uint256) {
        require(winner != address(0), "Winner has not been declared yet");
        
        Bidder memory winningBidder = bidders[winner];
        return (winningBidder.name, winningBidder.amount);
    }
}