// SPDX-License-Identifier: MIT
pragma solidity >=0.8.1 <0.9.0;

import "../interfaces/ICuboDaoV1.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract ConeVaultV1 {
    address public owner;
    string public name;
    uint256 public totalDaiInvested;
    uint256 public totalCuboInvested;
    uint256 public daiTarget;
    uint256 public cuboTarget;
    uint8 public nodeType;
    address public cuboDaoAddress;
    address public cuboTokenAddress;
    address public daiTokenAddress;
    address[] public investorAddresses;

    uint256 public mgmtFeePercentage;
    address public mgmtWalletAddress;
    bool public isFull;
    uint256 public tokenDecimals;
    uint256 public minInvestableAmount;

    struct Investor {
        bool exists;
        uint256 investedDai;
        uint256 investedCubo;
        uint256 claimedCubo;
    }

    mapping(address => Investor) public investors;

    constructor(
        string memory _name,
        address _cuboDaoAddress,
        address _cuboAddress,
        address _daiAddress,
        uint8 _nodeType,
        uint256 _daiTarget,
        uint256 _cuboTarget,
        uint256 _mgmtFeePercentage,
        address _mgmtWallet
    ) {
        require(_nodeType >= 0 && _nodeType <= 4, "Invalid node type");
        owner = msg.sender;
        name = _name;
        totalCuboInvested = 0;
        totalDaiInvested = 0;
        cuboDaoAddress = _cuboDaoAddress;
        daiTokenAddress = _daiAddress;
        cuboTokenAddress = _cuboAddress;
        nodeType = _nodeType;
        daiTarget = _daiTarget;
        cuboTarget = _cuboTarget;
        mgmtFeePercentage = _mgmtFeePercentage;
        mgmtWalletAddress = _mgmtWallet;
        isFull = false;
        tokenDecimals = 10**18;
        minInvestableAmount = 1; //_cuboTarget / 300;
    }

    function getInvestedAmounts() public view returns (uint256, uint256) {
        if (investors[msg.sender].exists) {
            return (
                investors[msg.sender].investedCubo,
                investors[msg.sender].investedDai
            );
        }
        return (0, 0);
    }

    function getClaimedRewards(address investor) public view returns (uint256) {
        if (investors[investor].exists) {
            return investors[investor].claimedCubo;
        }
        return 0;
    }

    function getTotalInvested() public view returns (uint256, uint256) {
        return (totalCuboInvested, totalDaiInvested);
    }

    function getAmountTargets() public view returns (uint256, uint256) {
        return (cuboTarget, daiTarget);
    }

    function getInvestorShares(address investor) public view returns (uint256) {
        uint256 nInvestedCubo = (investors[investor].investedCubo * 100) /
            tokenDecimals;
        uint256 nCuboTarget = cuboTarget / tokenDecimals;
        return (nInvestedCubo / nCuboTarget);
    }

    function getNodes()
        public
        view
        returns (
            uint256,
            uint256,
            uint256,
            uint256,
            uint256,
            uint256
        )
    {
        return ICuboDaoV1(cuboDaoAddress).getAccount(address(this));
    }

    function deposit(uint256 cuboAmount, uint256 daiAmount) public {
        require(
            cuboAmount == daiAmount,
            "CUBO and DAI amounts should be the same"
        );
        require(
            cuboAmount > minInvestableAmount && daiAmount > minInvestableAmount,
            "You haven't reached the minimum investable amount"
        );

        require(!isFull, "This vault is already full and invested");

        if (!investors[msg.sender].exists) {
            Investor memory investor = Investor(true, 0, 0, 0);
            investors[msg.sender] = investor;
            investorAddresses.push(msg.sender);
        }

        // Safeguard from possible over spending
        if (totalCuboInvested + cuboAmount > cuboTarget) {
            uint256 diff = totalCuboInvested + cuboAmount - cuboTarget;
            cuboAmount = cuboAmount - diff;
        }

        if (totalDaiInvested + daiAmount > daiTarget) {
            uint256 diff = totalDaiInvested + daiAmount - daiTarget;
            daiAmount = daiAmount - diff;
        }

        IERC20 cuboToken = IERC20(cuboTokenAddress);
        IERC20 daiToken = IERC20(daiTokenAddress);

        cuboToken.transferFrom(msg.sender, address(this), cuboAmount);
        daiToken.transferFrom(msg.sender, address(this), daiAmount);

        investors[msg.sender].investedCubo += cuboAmount;
        investors[msg.sender].investedDai += daiAmount;

        totalCuboInvested += cuboAmount;
        totalDaiInvested += daiAmount;

        if (totalCuboInvested >= cuboTarget && totalDaiInvested >= daiTarget) {
            cuboToken.approve(cuboDaoAddress, cuboTarget);
            daiToken.approve(cuboDaoAddress, daiTarget);

            ICuboDaoV1(cuboDaoAddress).mintNode(
                address(this),
                cuboTarget,
                daiTarget,
                nodeType
            );

            isFull = true;
        }
    }

    function withdraw(uint256 cuboAmount, uint256 daiAmount) public {
        require(
            !isFull,
            "You can't withdraw from a vault that is already invested"
        );
        require(investors[msg.sender].exists, "You have not invested yet");
        require(
            cuboAmount == daiAmount,
            "CUBO and DAI amounts have to be the same"
        );

        Investor memory investor = investors[msg.sender];

        require(
            investor.investedCubo >= cuboAmount &&
                investor.investedDai >= daiAmount,
            "You are exceeding your withdraw limits"
        );

        IERC20 cuboToken = IERC20(cuboTokenAddress);
        IERC20 daiToken = IERC20(daiTokenAddress);

        uint256 cuboFee = (cuboAmount * mgmtFeePercentage) / 100;
        uint256 daiFee = (daiAmount * mgmtFeePercentage) / 100;

        cuboToken.transfer(mgmtWalletAddress, cuboFee);
        daiToken.transfer(mgmtWalletAddress, daiFee);

        cuboToken.transfer(msg.sender, cuboAmount - cuboFee);
        daiToken.transfer(msg.sender, daiAmount - daiFee);

        investors[msg.sender].investedCubo -= cuboAmount;
        investors[msg.sender].investedDai -= daiAmount;

        totalCuboInvested -= cuboAmount;
        totalDaiInvested -= daiAmount;
    }

    function claimInterests() public {
        ICuboDaoV1(cuboDaoAddress).widthrawInterest(address(this));

        IERC20 cuboToken = IERC20(cuboTokenAddress);
        uint256 rewardBalance = cuboToken.balanceOf(address(this));

        uint256 mgmtFee = (rewardBalance * mgmtFeePercentage) / 100;
        cuboToken.transfer(mgmtWalletAddress, mgmtFee);

        rewardBalance = rewardBalance - mgmtFee;

        for (uint256 i = 0; i < investorAddresses.length; i++) {
            uint256 shares = getInvestorShares(investorAddresses[i]);

            if (shares <= 0) continue;

            uint256 investorRewards = (rewardBalance * shares) / 100;

            cuboToken.transfer(investorAddresses[i], investorRewards);
            investors[investorAddresses[i]].claimedCubo = investorRewards;
        }
    }
}
