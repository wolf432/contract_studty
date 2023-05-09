// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

import "./IERC20.sol";

contract MyToken20 is IERC20 {
    // 代币名称
    string private _name;
    // 代币符号
    string private _symbol;
    // 代币精度
    uint8 constant _decimals = 18;
    // 存储每个地址的余额
    mapping(address => uint256) balances;

    // 存储每个地址允许其他地址花费的代币数量，
    // 二维映射数组，跟踪委托代币余额，其主键是代币所有者的地址，映射到被委托地址和对应的委托代币余额：
    mapping(address => mapping(address => uint256)) allowed;

    // 总供应量
    uint256 totalSupply_;

    // 构造函数，初始化代币总供应量
    constructor(string memory name_, string memory symbol_, uint256 _totalSupply) {
        balances[msg.sender] = _totalSupply * 10 ** 18;
        totalSupply_ = _totalSupply * 10 ** 18;
        _name = name_;
        _symbol = symbol_;
    }

    // 返回代币的名字
    function name() public view returns (string memory) {
        return _name;
    }

    // 返回代币的符号
    function symbol() public view returns (string memory) {
        return _symbol;
    }

    function decimals() public view returns (uint8){
        return _decimals;
    }

    // 获取代币总供应量
    function totalSupply() public override view returns (uint256) {
        return totalSupply_;
    }

    // 查询指定地址的余额
    function balanceOf(address tokenOwner) public override view returns (uint256) {
        return balances[tokenOwner];
    }

    // 转账函数
    function transfer(address receiver, uint256 numTokens) public override returns (bool) {
        require(numTokens <= balances[msg.sender]);
        balances[msg.sender] = balances[msg.sender] - numTokens;
        balances[receiver] = balances[receiver] + numTokens;
        emit Transfer(msg.sender, receiver, numTokens);
        return true;
    }

    // 批准spender花费指定数量的代币
    function approve(address delegate, uint256 numTokens) public override returns (bool) {
        allowed[msg.sender][delegate] = numTokens;
        emit Approval(msg.sender, delegate, numTokens);
        return true;
    }

    // 查询拥有者允许spender花费的代币数量
    function allowance(address owner, address delegate) public override view returns (uint) {
        return allowed[owner][delegate];
    }

    // 转账指定数量的代币（需要先获得批准）
    function transferFrom(address owner, address buyer, uint256 numTokens) public override returns (bool) {
        // 检查余额是否足够
        require(numTokens <= balances[owner]);
        // 检查授权的代币数量是否足够
        require(numTokens <= allowed[owner][msg.sender]);

        // 更新余额和允许的代币数量
        balances[owner] = balances[owner] - numTokens;
        allowed[owner][msg.sender] = allowed[owner][msg.sender] - numTokens;
        balances[buyer] = balances[buyer] + numTokens;

        // 触发转账事件
        emit Transfer(owner, buyer, numTokens);
        return true;
    }
}