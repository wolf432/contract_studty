from brownie import accounts, SimpleSwap, Token, network, Wei, project

total_supply = 100000


def deploy_contract():
    """
    发布到本地测试网络
    :return:
    """
    # 获取一个账号
    account = accounts[0]
    # 进行合约部署
    ETH = Token.deploy("MYETH", "ETH", total_supply, {"from": account})
    print(f"ETH合约已部署到: {ETH.address}")  # 打印部署后的合约地址

    USDT = Token.deploy("MYUSDT", "USDT", total_supply, {"from": account})
    print(f"USDT合约已部署到: {USDT.address}")  # 打印部署后的合约地址

    contract = SimpleSwap.deploy(ETH.address, USDT.address, {"from": account})
    print(f"swap合约已部署到: {contract.address}")  # 打印部署后的合约地址


def deploy_contract_with_testnetwork():
    """
    发布到链上的测试网络，并且使用测试网络的私钥
    :return:
    """
    accounts = import_private_keys()

    if len(accounts) == 0:
        raise ValueError("No account imported")

    # 进行合约部署
    ETH = Token.deploy("MYETH", "ETH", total_supply, {"from": accounts[0]}, publish_source=True)
    print(f"ETH合约已部署到: {ETH.address}")  # 打印部署后的合约地址

    USDT = Token.deploy("MYUSDT", "USDT", total_supply, {"from": accounts[0]}, publish_source=True)
    print(f"USDT合约已部署到: {USDT.address}")  # 打印部署后的合约地址

    contract = SimpleSwap.deploy(ETH.address, USDT.address, {"from": accounts[0]}, publish_source=True)
    print(f"swap合约已部署到: {contract.address}")  # 打印部署后的合约地址

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

def main():
    if network.show_active() != 'development':
        deploy_contract_with_testnetwork()
    else:
        deploy_contract()
