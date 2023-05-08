// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

// 简单的ERC20代币合约，用于测试
contract Token is ERC20{
    constructor(string memory name, string memory symbol, uint256 amount) ERC20(name, symbol) {
        _mint(msg.sender, amount);
    }
}

//简单的模拟一个兑换代币的合约，可以存储两个ERC20的代币进入池子，然后用户可以从池子中用其中一个代币兑换另一个代币。
contract SimpleSwap {

    // Token合约地址
    address token0;
    address token1;


    // 记录两个代币的合约地址
    constructor(address _t0, address _t1){
        token0 = _t0;
        token1 = _t1;
    }

    // 添加代币到池子中, 需要先授权。为了代币的简单，这里两个代币存入的数量相同
    function add(uint amount) public  {
        //检查是否授权
        require(IERC20(token0).allowance(msg.sender, address(this)) >= amount, "token0 allowance is not enough");
        require(IERC20(token1).allowance(msg.sender, address(this)) >= amount, "token1 allowance is not enough");

        //转移代币到合约地址
        IERC20(token0).transferFrom(msg.sender, address(this), amount);
        IERC20(token1).transferFrom(msg.sender, address(this), amount);
    }

    // 用A代币兑换B代币,为了代码简单兑换比例1：1
    // @param amount 兑换数量
    // @param fromToken 兑换的代币A
    // @param toToken 兑换成的代币B
    function swap(uint amount, address fromToken, address toToken) public {
        //检查A授权的数量是否足够
        require(IERC20(token0).allowance(msg.sender, address(this)) >= amount, "token0 allowance is not enough");

        //将A代币从用户钱包转移到合约地址
        IERC20(token0).transferFrom(msg.sender, address(this), amount);

        //检查B代币在合约中是否足够
        require(IERC20(token1).balanceOf(address(this)) >= amount, "token1 balance is not enough");

        // 将B代币从合约中转移到用户钱包
        IERC20(token1).transfer(msg.sender, amount);
    }

}
