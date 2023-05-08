import pytest
from brownie import network, accounts

# 合约代币发型总量
TokenTotalSupply = 100000


@pytest.fixture
def token(Token, SimpleSwap):
    ETH = Token.deploy("MYETH", "ETH", TokenTotalSupply, {"from": accounts[0]})
    USDT = Token.deploy("MUSDT", "USDT", TokenTotalSupply, {"from": accounts[0]})
    SWAP = SimpleSwap.deploy(ETH, USDT, {"from": accounts[0]})

    return ETH, USDT, SWAP, accounts


@pytest.fixture
def test_add(token):
    """
    测试添加2中代币到合约中
    :param token:
    :param a:
    :return:
    """
    ETH, USDT, SWAP, a = token

    # ETH授权给SWAP合约可以使用用户代币的数量
    ETH.approve(SWAP, 1000, {"from": a[0]})
    # 验证授权数量是否位1000
    assert ETH.allowance(a[0], SWAP) == 1000

    # USDT授权给SWAP合约可以使用用户代币的数量
    USDT.approve(SWAP, 1000, {"from": a[0]})
    # 验证授权数量是否位1000
    assert USDT.allowance(a[0], SWAP) == 1000

    # 添加代币到合约中
    SWAP.add(10, {"from": a[0]})

    # 验证合约中的代币数量是否为10
    assert ETH.balanceOf(SWAP.address) == 10
    assert USDT.balanceOf(SWAP.address) == 10
    return ETH, USDT, SWAP, accounts


def test_swap(test_add):
    """
    测试代币兑换
    :param token:
    :return:
    """
    ETH, USDT, SWAP, a = test_add

    # 用户ETH代币数量
    ETH_balance = ETH.balanceOf(a[0])
    # 用户USDT代币数量
    USDT_balance = USDT.balanceOf(a[0])

    # 用ETH兑换USDT
    SWAP.swap(1, ETH.address, USDT.address, {"from": a[0]})

    assert (ETH.balanceOf(a[0]) == ETH_balance - 1)
    assert (USDT.balanceOf(a[0]) == USDT_balance + 1)
