// SPDX-License-Identifier: MIT
pragma solidity >=0.8.1 <0.9.0;

import "./ConeVault.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract ConeVaultFactory {
    address public owner;
    address public cuboDaoAddress;
    address public cuboAddress;
    address public daiAddress;

    address mgmtWalletAddress;
    address[] vaultAddresses;

    uint256 tokenDecimals = 10**18;

    struct Node {
        uint256 nodeType;
        uint256 daiTarget;
        uint256 cuboTarget;
        uint256 mgmtFee;
        uint256 minInvestableAmount;
    }

    constructor(
        address _mgmtWalletAddress,
        address _cuboDaoAddress,
        address _cuboAddress,
        address _daiAddress,
        uint256 _nodeType
    ) {
        owner = msg.sender;
        mgmtWalletAddress = _mgmtWalletAddress;
        cuboDaoAddress = _cuboDaoAddress;
        cuboAddress = _cuboAddress;
        daiAddress = _daiAddress;
    }

    function getManagementAddress() public view returns (address) {
        return mgmtWalletAddress;
    }

    function updateManagementAddress(address mgmtAddress) public {
        require(
            msg.sender != owner,
            "You are not allowed to perform this action"
        );
        mgmtWalletAddress = mgmtAddress;
    }

    function mintVault(string memory name, uint8 nodeType) public {
        Node memory node = getNodeDetails(nodeType);

        ConeVaultV1 vault = new ConeVaultV1(
            name,
            cuboDaoAddress,
            cuboAddress,
            daiAddress,
            nodeType,
            node.daiTarget,
            node.cuboTarget,
            node.mgmtFee,
            mgmtWalletAddress
        );

        vaultAddresses.push(address(vault));
    }

    function getVaults() public view returns (address[] memory vaults) {
        return vaultAddresses;
    }

    function getNodeDetails(uint256 nodeType)
        internal
        view
        returns (Node memory node)
    {
        if (nodeType == 0) {
            uint256 targetAmount = 100 * tokenDecimals;
            uint256 mgmtFee = 10;
            uint256 minInvestableAmount = targetAmount / 30;
            return
                Node(
                    nodeType,
                    targetAmount,
                    targetAmount,
                    mgmtFee,
                    minInvestableAmount
                );
        } else if (nodeType == 1) {
            uint256 targetAmount = 250 * tokenDecimals;
            uint256 mgmtFee = 7;
            uint256 minInvestableAmount = targetAmount / 30;
            return
                Node(
                    nodeType,
                    targetAmount,
                    targetAmount,
                    mgmtFee,
                    minInvestableAmount
                );
        } else if (nodeType == 2) {
            uint256 targetAmount = 500 * tokenDecimals;
            uint256 mgmtFee = 5;
            uint256 minInvestableAmount = targetAmount / 30;
            return
                Node(
                    nodeType,
                    targetAmount,
                    targetAmount,
                    mgmtFee,
                    minInvestableAmount
                );
        } else if (nodeType == 3) {
            uint256 targetAmount = 1000 * tokenDecimals;
            uint256 mgmtFee = 5;
            uint256 minInvestableAmount = targetAmount / 30;
            return
                Node(
                    nodeType,
                    targetAmount,
                    targetAmount,
                    mgmtFee,
                    minInvestableAmount
                );
        } else if (nodeType == 4) {
            uint256 targetAmount = 5000 * tokenDecimals;
            uint256 mgmtFee = 5;
            uint256 minInvestableAmount = targetAmount / 30;
            return
                Node(
                    nodeType,
                    targetAmount,
                    targetAmount,
                    mgmtFee,
                    minInvestableAmount
                );
        }
    }
}
