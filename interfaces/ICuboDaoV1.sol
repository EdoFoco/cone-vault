// SPDX-License-Identifier: MIT
pragma solidity >=0.8.1 <0.9.0;

interface ICuboDaoV1 {
    function mintNode(
        address _address,
        uint256 _cuboAmount,
        uint256 _daiAmount,
        uint256 _nodeType
    ) external;

    function widthrawInterest(address _to) external;

    function getAccount(address _address)
        external
        view
        returns (
            uint256,
            uint256,
            uint256,
            uint256,
            uint256,
            uint256
        );
}
