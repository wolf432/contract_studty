import pytest
from brownie import network, accounts

# 合约代币发型总量
TokenTotalSupply = 100000


@pytest.fixture
def token(Token):
    if network.show_active() != 'development':
        # 获取最新部署的MyToken20的合约地址
        deployed_count = len(Token)
        if deployed_count == 0:
            raise ValueError("No deployed MyToken20")
        latest_deployed_instance = Token[deployed_count - 1]
        latest_deployed_address = latest_deployed_instance.address

        # 加载已部署的MyToken20合约
        myToken = Token.at(latest_deployed_address)
        imported_accounts = import_private_keys()
    else:
        myToken = Token.deploy("METH", "METH", TokenTotalSupply, {"from": accounts[0]})
        imported_accounts = accounts

    return myToken, imported_accounts


def import_private_keys():
    """
    导入本地私钥的地址
    :return: accounts
    """
    with open("private_key.txt", "r") as f:
        private_keys = f.read().splitlines()

    for private_key in private_keys:
        accounts.add(private_key)

    # raise SystemExit("停止测试并退出")
    return accounts


def test_base_info(token):
    """
    测试合约部署的基础信息，发型币的数量
    :param token:
    :param a:
    :return:
    """
    myToken, a = token
    totalSupply = myToken.totalSupply()
    assert totalSupply == TokenTotalSupply * 10 ** myToken.decimals()

    assert myToken.name() == "METH"

    assert myToken.symbol() == "METH"


def test_transfer(token):
    """
    测试转账功能,a[0] 转给 a[1] 1个MTK代币
    :param token:
    :param a:
    :return:
    """
    myToken, a = token
    a0Balance = myToken.balanceOf(a[0])
    a1Balance = myToken.balanceOf(a[1])

    total = 1 * 10 ** myToken.decimals()

    tx = myToken.transfer(a[1], total, {"from": a[0]})
    assert tx.status == 1

    assert myToken.balanceOf(a[0]) == a0Balance - total

    assert myToken.balanceOf(a[1]) == a1Balance + total


def test_approve(token):
    """
    测试授权功能,a[0] 批准 a[1] 10个MTK代币
    :param token:
    :return:
    """
    myToken, a = token

    amount = 10

    approveRs = myToken.approve(a[1], amount, {"from": a[0]})
    assert approveRs.return_value == True

    # 通过approve中定义的事件来测试执行结果
    eventApproval = approveRs.events["Approval"]
    assert eventApproval["owner"] == a[0]
    assert eventApproval["spender"] == a[1]
    assert eventApproval["value"] == amount

    assert myToken.allowance(a[0], a[1]) == amount

    transferRs = myToken.transferFrom(a[0], a[1], amount, {"from": a[1]})
    # 通过transferFrom中定义的事件来测试执行结果
    eventTransfer = transferRs.events["Transfer"]
    assert eventTransfer["from"] == a[0]
    assert eventTransfer["to"] == a[1]
    assert eventTransfer["value"] == amount
