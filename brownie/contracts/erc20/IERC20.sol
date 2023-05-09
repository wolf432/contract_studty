// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

// 引入ERC20接口定义 https://eips.ethereum.org/EIPS/eip-20
interface IERC20 {

    // 获取代币名称
    function name() external view returns (string memory);

    // 获取代币符号
    function symbol() external view returns (string memory);

    // 获取代币精度
    function decimals() external view returns (uint8);

    // 获取总供应量
    function totalSupply() external view returns (uint256);

    // 查询指定账户的余额
    function balanceOf(address account) external view returns (uint256);

    // 查询拥有者允许spender花费的代币数量
    function allowance(address owner, address spender) external view returns (uint256);

    // 转账
    function transfer(address recipient, uint256 amount) external returns (bool);

    // 批准spender花费指定数量的代币
    function approve(address spender, uint256 amount) external returns (bool);

    // 从一个账户转移到另一个账户，需要批准
    function transferFrom(address sender, address recipient, uint256 amount) external returns (bool);

    // 转账事件
    event Transfer(address indexed from, address indexed to, uint256 value);
    // 批准事件
    event Approval(address indexed owner, address indexed spender, uint256 value);
}
