from brownie import accounts, MyToken20, network, Wei

total_supply = 100000

def deploy_contract():
    """
    发布到本地测试网络
    :return:
    """
    # 获取一个账号
    account = accounts[0]
    # 进行合约部署
    contract = MyToken20.deploy("METH","METH",total_supply, {"from": account})
    print(f"合约已部署到: {contract.address}")  # 打印部署后的合约地址


def deploy_contract_with_testnetwork():
    """
    发布到链上的测试网络，并且使用测试网络的私钥
    :return:
    """
    accounts = import_private_keys()

    network_name = network.show_active()

    gas_price_wei = Wei("176 gwei")
    # 部署合约
    contract = MyToken20.deploy("LiNan","LN",total_supply, {"from": accounts[0], "gasPrice": gas_price_wei}, publish_source=True)
    print(f"合约已部署到: {contract.address}")


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
