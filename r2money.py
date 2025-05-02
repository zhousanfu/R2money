'''
Author: sanford courageux_san@wechat.com
Date: 2025-05-02 13:22:36
LastEditors: sanford courageux_san@wechat.com
LastEditTime: 2025-05-02 17:22:34
FilePath: /web3_script/web3_drop_script/script_py/r2money2.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import json
import requests
from web3 import Web3
from decimal import Decimal
from eth_abi import encode



token_abi = json.loads('[{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"constant":true,"inputs":[],"name":"_decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"_name","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"_symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"burn","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"getOwner","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"mint","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"renounceOwnership","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"}]')


def load_private_keys(pk_path):
    private_keys = []

    with open(pk_path, 'r') as f:
        for line in f:
            private_keys.append(line.strip())

    return private_keys

def load_config_rpc(rpc_name: str):
    with open("config/rpc.json", 'r') as f:
        cof = json.load(f)
    try:
        return cof[rpc_name]
    except Exception as e:
        print(e)

def set_w3(conf: dict):
    w3 = Web3(Web3.HTTPProvider(conf['RPC_URL']))

    if w3.is_connected():
        print("✅ Web3 Connected")
        return w3
    else:
        print("❌ Error Connecting. Please Try Again...")
        exit()

def approve_tokens(ws: object, pk, token_addr, target_addr):
    account = w3.eth.account.from_key(pk)
    sender_addr = account.address

    token_addr = w3.to_checksum_address(token_addr)
    target_addr = w3.to_checksum_address(target_addr)
    token_contract = w3.eth.contract(address=token_addr, abi=token_abi)

    approve_token = token_contract.functions.allowance(sender_addr, target_addr).call()

    if approve_token == 0:
        approve_tx = token_contract.functions.approve(target_addr, 2**256 - 1).build_transaction({
                'chainId': w3.eth.chain_id,
                'from': sender_addr,
                'gasPrice': int(w3.eth.gas_price * Decimal(1.1)),
                'gas': token_contract.functions.approve(target_addr, 2**256 - 1).estimate_gas({
                    'from': sender_addr,
                    'gasPrice': int(w3.eth.gas_price * Decimal(1.1)),
                    'nonce': int(w3.eth.get_transaction_count(sender_addr))
                }),
                'nonce': int(w3.eth.get_transaction_count(sender_addr))
            })

        tx_hash = w3.eth.send_raw_transaction(w3.eth.account.sign_transaction(approve_tx, pk).raw_transaction)
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        if receipt.status == 1:
            print("✅ approve_tokens Transaction Successful")
        else:
            print("❌ approve_tokens Transaction Failed")

def get_balance(w3: object, sender_addr: str, token_addr: str):
    # balance = w3.eth.get_balance(address)

    erc20_abi = [
        {
            "constant": True,
            "inputs": [],
            "name": "name",
            "outputs": [{"name": "", "type": "string"}],
            "payable": False,
            "stateMutability": "view",
            "type": "function"
        },
        {
            "constant": True,
            "inputs": [{"name": "owner", "type": "address"}],
            "name": "balanceOf",
            "outputs": [{"name": "", "type": "uint256"}],
            "payable": False,
            "stateMutability": "view",
            "type": "function"
        }
    ]
    
    # 创建合约对象
    contract = w3.eth.contract(address=token_addr, abi=erc20_abi)
    token_name = contract.functions.name().call()
    balance = contract.functions.balanceOf(sender_addr).call()
    # 输出余额（通常是以最小单位表示，例如 wei）
    print(f"地址 {sender_addr[-4:]} 余额为: {balance/1000000} {token_name}")
    
    return balance

def transfer_tokens(w3: object, pk: str, target_addr: str, data):
    account = w3.eth.account.from_key(pk)
    sender_addr = account.address
    target_addr = w3.to_checksum_address(target_addr)

    gas_estimate = w3.eth.estimate_gas({'from': sender_addr, 'to': target_addr, 'data': data})
    gas_price = w3.eth.gas_price  # gas_price 是以 wei 为单位
    # 将 gas_price 从 wei 转换为 Gwei
    gas_price_gwei = gas_price / 10**9
    # 计算 gas 费用（以 ETH 为单位）
    gas_fee_eth = (gas_estimate * gas_price_gwei) * 10**-9
    print(f"Estimated gas fee in ETH: {gas_fee_eth}")

    if gas_fee_eth <= 0.006:
        tx = {
            'chainId': w3.eth.chain_id,
            'from': sender_addr,
            'to': target_addr,
            'data': data,
            'gasPrice': int(w3.eth.gas_price * Decimal(1.1)),
            'gas': w3.eth.estimate_gas({'from': sender_addr, 'to': target_addr, 'data': data}),
            'nonce': int(w3.eth.get_transaction_count(sender_addr))
        }
        tx_hash = w3.eth.send_raw_transaction(w3.eth.account.sign_transaction(tx, pk).raw_transaction)
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        if receipt.status == 1:
            print("✅ transfer_tokens Transaction Successful")
        else:
            print("❌ transfer_tokens Transaction Failed")
    else:
        print("❌ Gas Fee is high")
        exit()


def usdc_to_rusd(w3: object, pk):
    usdc = "0xef84994eF411c4981328fFcE5Fda41cD3803faE4"
    rusd = "0x20c54C5F742F123Abb49a982BFe0af47edb38756"

    account = w3.eth.account.from_key(pk)
    sender_addr = account.address

    # 授权
    approve_tokens(w3, pk, token_addr=usdc, target_addr=rusd)
    # 获取余额
    amount = get_balance(w3, sender_addr, token_addr=usdc)

    if amount > 0:
        funcbuy = bytes.fromhex('095e7a95')
        enc = encode(['address', 'uint256', 'uint256', 'uint256', 'uint256', 'uint256', 'uint256'], [sender_addr, amount, 0, 0, 0, 0, 0])
        data = w3.to_hex(funcbuy + enc)
        transfer_tokens(w3, pk, target_addr=rusd, data=data)

def rusd_to_srusd(w3: object, pk):
    print("rusd_to_srusd")
    rusd = "0x20c54C5F742F123Abb49a982BFe0af47edb38756"
    srusd = "0xBD6b25c4132F09369C354beE0f7be777D7d434fa"

    account = w3.eth.account.from_key(pk)
    sender_addr = account.address

    # 授权
    approve_tokens(w3, pk, token_addr=rusd, target_addr=srusd)
    # 获取余额
    amount = get_balance(w3, sender_addr, token_addr=rusd)

    if amount > 0:
        data = w3.to_hex(bytes.fromhex('1a5f0f00') + encode(['uint256'] * 10, [amount] + [0]*9))
        transfer_tokens(w3, pk, target_addr=srusd, data=data)

def rusd_liq_srusd(w3: object, pk):
    print("rusd_liq_srusd")
    rusd = "0x20c54C5F742F123Abb49a982BFe0af47edb38756"
    srusd = "0xBD6b25c4132F09369C354beE0f7be777D7d434fa"
    liquidity = "0xF64a77f6e57d9fEeFd2E8fEDbd0032798dAC21Fa"

    account = w3.eth.account.from_key(pk)
    sender_addr = account.address

    # 授权
    approve_tokens(w3, pk, token_addr=rusd, target_addr=liquidity)
    approve_tokens(w3, pk, token_addr=srusd, target_addr=liquidity)
    # 获取余额
    amount_rusd = get_balance(w3, sender_addr, token_addr=rusd)
    amount_srusd = get_balance(w3, sender_addr, token_addr=srusd)
    amount = min(amount_rusd, amount_srusd)

    if amount > 0:
        data = web3.to_hex(
            bytes.fromhex('2e1a7d4d') + encode(
                ['address', 'address', 'uint256', 'uint256', 'uint256', 'address', 'uint256'],
                [w3.to_checksum_address(rusd), w3.to_checksum_address(srusd), amount, 0, 0, sender, int(time.time()) + 1000]
            )
        )
        transfer_tokens(w3, pk, target_addr=srusd, data=data)



if __name__ == "__main__":
    conf = load_config_rpc(rpc_name="testnet_eth_sepolia")
    private_keys = load_private_keys(pk_path='data/private_keys/r2money.txt')

    w3 = set_w3(conf)

    for index, pk in enumerate(private_keys):
        print(f"账号 index: {index}")
        usdc_to_rusd(w3, pk)
        rusd_to_srusd(w3, pk)
        rusd_liq_srusd(w3, pk)


